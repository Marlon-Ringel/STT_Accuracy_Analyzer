import os
import pathlib
import subprocess

class ConfigurationService:

    def __init__(self, subprocessCommandString, audioFilesPath, tsvFilePath):
        self.subprocessCommandString = subprocessCommandString
        self.audioFilesPath = audioFilesPath
        self.tsvFilePath = tsvFilePath
        
        self.configurationError = [0, 0, 0, 0] 
        '''
        #For All:   0 = No Error. 
        #[0]: 1 = not command string given, 2 = commandstring error, 3 = subprocess Error
        #[1]: 1 = Audio path missing. 2 = Tsv Path missing 
        #[2]: 1 = audio path does not exist
        #[3]: 1 = tsv path does not exist
        '''
    
    def validateConfiguration(self):
        self.configurationError[0] = self.validateSubprocessCommandString ()
        
        if self.isEmptyString(self.audioFilesPath) and (not self.isEmptyString(self.tsvFilePath)):
            self.configurationError[1] = 1 
        
        if (not self.isEmptyString(self.audioFilesPath)) and self.isEmptyString(self.tsvFilePath):
            self.configurationError[1] = 2 

        if (not self.isEmptyString(self.audioFilesPath)) and (not self.isEmptyString(self.tsvFilePath)):
            if self.isNotPath(self.audioFilesPath):
                self.configurationError[2] = 1 
            if self.isNotPath(self.tsvFilePath):
                self.configurationError[3] = 1 

        if self.configurationError == [0, 0, 0, 0]:
            return True
        return False

    def isNotPath(self, pathToTest):
        if os.path.exists(pathToTest):
            return False
        return True

    def isEmptyString(self, stringToTest):
        if stringToTest == "":
            return True
        return False

    def validateSubprocessCommandString (self):
        if self.isEmptyString(self.subprocessCommandString):
            return 1
        audioValidationTestFilePath = f"{pathlib.Path(__file__).parent.resolve()}/Data/InternalData/Test.mp3"
        try:
            validationResult = subprocess.run(self.subprocessCommandString.split(", "), capture_output=True, text=True, input=audioValidationTestFilePath)
        except FileNotFoundError:
            return 2
        if validationResult.returncode == 2: 
            return 2
        if validationResult.returncode == 1:
            print(f"Subprocess Error:\n{validationResult.stderr}")
            return 3
        return 0 

    def getSubprocessCommandString(self):
        return self.subprocessCommandString
        
    def getAudioFilesPath(self):
        return self.audioFilesPath

    def getTsvFilePath(self):
        return self.tsvFilePath

    def getConfigurationError(self):
        return self.configurationError
    
    def getConfigurationAsSqliteQuery(self):
        sqlQuery = f"INSERT INTO Configuration(commandString, audioFilePath, tsvFilePath) VALUES"

        if self.audioFilesPath == "" and self.tsvFilePath == "": 
            defaultAudioFilesPath = f"{pathlib.Path(__file__).parent.resolve()}/Data/SampleTestData/CommonVoice_TestDataSet/AudioFiles"
            defaultTsvFilePath = f"{pathlib.Path(__file__).parent.resolve()}/Data/SampleTestData/CommonVoice_TestDataSet/dataSet.tsv"
            sqlQuery += f"('{self.subprocessCommandString}', '{defaultAudioFilesPath}', '{defaultTsvFilePath}');"
            return sqlQuery
        sqlQuery += f"('{self.subprocessCommandString}', '{self.audioFilesPath}', '{self.tsvFilePath}');"
        return sqlQuery



    