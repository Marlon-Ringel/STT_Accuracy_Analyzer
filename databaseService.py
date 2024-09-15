import os
import pathlib
import sqlite3
import openpyxl
from datetime import datetime
from configurationService import ConfigurationService
from testData import TestData
from transcriptionResults import TranscriptionResults
from analysisResults import AnalysisResults

# Class that implements functionality to store and retrieve data from the database and also manage the database. 
class DatabaseService:
    # String containing the path to the database file. 
    dataBasePath = f"{pathlib.Path(__file__).parent.resolve()}/Data/InternalData/database.db" 

    # Establishe a connection to the database and return it.
    # 
    # Return:
    # Connection to database as sqlite3.Connection Object.
    @staticmethod
    def getDataBaseConnection():
        return sqlite3.connect(DatabaseService.dataBasePath)

    # Create the required database tables inside the database. 
    @staticmethod
    def initializeDataBase():
        conn = DatabaseService.getDataBaseConnection()
        conn.executescript('''CREATE TABLE Configuration
             (id INTEGER PRIMARY KEY,
             commandString TEXT NOT NULL,
             audioFilePath TEXT NOT NULL,
             tsvFilePath TEXT NOT NULL);
                   
             CREATE TABLE TestData
             (id INTEGER PRIMARY KEY,
             originalSentance TEXT NOT NULL, 
             audioFileName TEXT NOT NULL);
                   
             CREATE TABLE TranscriptionResults 
             (id INTEGER PRIMARY KEY, 
             originalSentaceId INTEGER NOT NULL, 
             transcript TEXT NOT NULL,
             CONSTRAINT fk_TestData
                FOREIGN KEY (originalSentaceId)
                REFERENCES TestData(id));
                   
             CREATE TABLE AnalysisResults
             (id INTEGER PRIMARY KEY,
             wer REAL NOT NULL, 
             cer REAL NOT NULL, 
             mer REAL NOT NULL, 
             wil REAL NOT NULL, 
             jwd REAL NOT NULL,
             idTranscriptionResult INTEGER NOT NULL,
             CONSTRAINT fk_transcriptionResults
                FOREIGN KEY (idTranscriptionResult)
                REFERENCES TranscriptionResults(id));''')
        conn.commit()
        conn.close()

    # Take a SQLite-Query-String containing an insert query and execute it on the database.
    # 
    # Input:
    # insertQuery: SQLite-Query-String containing an insert query.  
    @staticmethod
    def insertDataIntoDataBase(insertQuery):
        conn = DatabaseService.getDataBaseConnection()
        conn.execute(insertQuery)
        conn.commit()
        conn.close()
    
    # Checks if a database file exists and in this case, delete it. 
    @staticmethod
    def resetDataBase():
        if os.path.exists(DatabaseService.dataBasePath):
            os.remove(DatabaseService.dataBasePath)

    # Take the configuration data and save it in the database.
    # 
    # Input: 
    # configuration: ConfigurationService Object containing the configuration data. 
    @staticmethod
    def saveConfiguration(configuration : ConfigurationService):
        DatabaseService.insertDataIntoDataBase(configuration.getConfigurationAsSqliteQuery())

    # Load the configuration data from the database and return it.
    # 
    # Return:
    # Configuration Data as ConfigurationService Object. 
    @staticmethod
    def loadConfiguration():
        conn = DatabaseService.getDataBaseConnection()
        databaseTable = conn.execute("SELECT commandString, audioFilePath, tsvFilePath FROM Configuration")
        for configurationData in databaseTable:
            configuration = ConfigurationService(
                configurationData[0],
                configurationData[1],
                configurationData[2]
            )
            conn.close()
            return configuration

    # Use the provided TSV file to read and format the test dataset as an SQLite query. 
    # Afterwards execute the query on the database storing the test dataset in it.
    # 
    # Input:
    # tsvFilePath: String containing the path to the TSV file with the labels of the test dataset.   
    @staticmethod
    def readTestDataFileIntoDatabase(tsvFilePath):
        sqlQuery = "INSERT INTO TestData(originalSentance, audioFileName) VALUES"
        with open(tsvFilePath) as tsvFile: 
            tsvFile.readline()
            currentLine = tsvFile.readline()
            while currentLine != "":
                currentLineSegments = currentLine.replace("\n", "").replace("\'", "").split("\t")
                sqlQuery += f"('{currentLineSegments[1]}','{currentLineSegments[0]}'),"
                currentLine = tsvFile.readline()
        sqlQuery = sqlQuery[:-1] + ";"
        DatabaseService.insertDataIntoDataBase(sqlQuery)
   
    # Load the test dataset from the database and returns it.
    # 
    # Return:
    # Test dataset as testData Object. 
    @staticmethod
    def loadTestData():
        ids, originalSentances, audioFileNames = [], [], []
        conn = DatabaseService.getDataBaseConnection()
        databaseTable = conn.execute("SELECT id, originalSentance, audioFileName FROM TestData")
        for testData in databaseTable: 
            ids.append(testData[0])
            originalSentances.append(testData[1])
            audioFileNames.append(testData[2])
        conn.close()
        return TestData(ids, originalSentances, audioFileNames)

    # Save the given transcription results in the database.
    # 
    # Input: 
    # Transcription Results as TranscriptionResults Object.  
    @staticmethod
    def saveTranscriptionResults(transcriptionResults : TranscriptionResults):
        DatabaseService.insertDataIntoDataBase(transcriptionResults.getTranscriptionResultDataAsSqliteQuery())
    
    # Load the transcription results from the database and return it.
    # 
    # Return:
    # Transcription results as TranscriptionResults Object. 
    @staticmethod
    def loadTranscriptionResults():
        conn = DatabaseService.getDataBaseConnection()
        databaseTable = conn.execute('''SELECT 
                                            TranscriptionResults.id AS id,
                                            TestData.originalSentance AS originalSentance,
                                            TranscriptionResults.transcript AS transcript
                                        FROM 
                                            TestData
                                        INNER JOIN 
                                            TranscriptionResults ON TranscriptionResults.originalSentaceId = TestData.id;''')
        ids, originalSentance, transcript = [], [], []
        for transcriptionResult in databaseTable:
            ids.append(transcriptionResult[0])
            originalSentance.append(transcriptionResult[1])
            transcript.append(transcriptionResult[2])
        conn.close()
        return TranscriptionResults(ids=ids, originalSentences=originalSentance, transcripts=transcript)

    # Save the given analysis results in the database.
    # 
    # Input: 
    # Transcription Results as AnalysisResults Object.
    @staticmethod
    def saveAnalysisResults(analysisResults : AnalysisResults):
        DatabaseService.insertDataIntoDataBase(analysisResults.getAnalysisResultsAsSqliteQuery())

    # Load the analysis results from the database and return it.
    # 
    # Return:
    # Analysis results as AnalysisResults Object.
    @staticmethod
    def loadAnalysisResults():
        conn = DatabaseService.getDataBaseConnection()
        dataBaseTable = conn.execute("SELECT wer, cer, mer, wil, jwd, idTranscriptionResult FROM AnalysisResults")
        analysisResults = [[], [], [], [], [], [], []]
        for analysisResult in dataBaseTable:
            analysisResults[0].append(analysisResult[0])
            analysisResults[1].append(analysisResult[1])
            analysisResults[2].append(analysisResult[2])
            analysisResults[3].append(analysisResult[3])
            analysisResults[4].append(analysisResult[4])
            analysisResults[5].append(analysisResult[5])
        conn.close()
        return AnalysisResults(analysisResults, True)

    # Save the test results as Excel file in the default results directory. 
    @staticmethod
    def saveResultsAsExcel():
        resultsPath = f"{pathlib.Path(__file__).parent.resolve()}/Results/"
        if not os.path.exists(resultsPath):
            os.mkdir(resultsPath)
        DatabaseService.saveTestResultsAsExcel(f"{resultsPath}Results_{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}.xlsx")

    # Load the test results from the database and format it as an Excel table. Store the Excel table at the
    # location specified in targetPath.
    # 
    # Input: 
    # targetPath: String containing the path to the directory where the results should be stored.  
    @staticmethod
    def saveTestResultsAsExcel(targetPath):
        conn = DatabaseService.getDataBaseConnection()
        dataBaseTable = conn.execute('''SELECT
                                            TestData.originalSentance AS originalSentance,
                                            TranscriptionResults.transcript AS transcript,
                                            AnalysisResults.wer AS wer, 
                                            AnalysisResults.cer AS cer, 
                                            AnalysisResults.mer AS mer, 
                                            AnalysisResults.wil AS wil,  
                                            AnalysisResults.jwd AS jwd
                                        FROM
                                            TestData
                                        INNER JOIN 
                                            TranscriptionResults ON TranscriptionResults.originalSentaceId = TestData.id
                                        INNER JOIN 
                                            AnalysisResults ON AnalysisResults.idTranscriptionResult = TranscriptionResults.id;''') 

        excelSheet = openpyxl.Workbook()
        table = excelSheet.active

        table.append(["Original Sentance", "Transcript", "Wer", "Cer", "Mer", "Wil", "jwd"])
        
        for row in dataBaseTable:
            table.append(row)
        conn.close()

        averageResults = DatabaseService.loadAnalysisResults().getAverageOfResults()

        table.append(["Average Results:", "", averageResults[0], averageResults[1], averageResults[2], averageResults[3], averageResults[4]])
        excelSheet.save(targetPath)

    # Delete the file created by the GUI file dialog at the given target path. 
    # Save the test results as an Excel table at the given target path.
    # 
    # Input: 
    # targetPath: String containing the path to the directory where the test results should be stored.
    @staticmethod
    def exportTestResultsAsExcel(targetPath):
        os.remove(targetPath)
        DatabaseService.saveTestResultsAsExcel(targetPath) 
        