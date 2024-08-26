import pathlib
import sqlite3
import os
from configurationService import ConfigurationService
from testData import TestData
from transcriptionResults import TranscriptionResults
from analysisResults import AnalysisResults

class DatabaseService:
    
    dataBasePath = f"{pathlib.Path(__file__).parent.resolve()}/Data/InternalData/database.db" 

    @staticmethod
    def getDataBaseConnection():
        return sqlite3.connect(DatabaseService.dataBasePath)

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
             idTestResult INTEGER NOT NULL,
             CONSTRAINT fk_TestResults
                FOREIGN KEY (idTestResult)
                REFERENCES TestResults(id));''')
        conn.commit()
        conn.close()

    @staticmethod
    def insertDataIntoDataBase(insertQuery):
        conn = DatabaseService.getDataBaseConnection()
        conn.execute(insertQuery)
        conn.commit()
        conn.close()
    
    @staticmethod
    def resetDataBase():
        if os.path.exists(DatabaseService.dataBasePath):
            os.remove(DatabaseService.dataBasePath)

    @staticmethod
    def saveConfiguration(configuration : ConfigurationService):
        DatabaseService.insertDataIntoDataBase(configuration.getConfigurationAsSqliteQuery())

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

    @staticmethod
    def saveTranscriptionResults(transcriptionResults : TranscriptionResults):
        DatabaseService.insertDataIntoDataBase(transcriptionResults.getTranscriptionResultDataAsSqliteQuery())
    
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

    @staticmethod
    def saveAnalysisResults(analysisResults : AnalysisResults):
        DatabaseService.insertDataIntoDataBase(analysisResults.getAnalysisResultsAsSqliteQuery())

    @staticmethod
    def loadAnalysisResults():
        conn = DatabaseService.getDataBaseConnection()
        dataBaseTable = conn.execute("SELECT wer, cer, mer, wil, jwd, idTestResult FROM AnalysisResults")
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

 