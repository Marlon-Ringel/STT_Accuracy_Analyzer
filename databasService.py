import pathlib
import sqlite3
import os

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

