import os
import pathlib
import subprocess

class ConfigurationService:
    # Initializes the ConfigurationService Object. Stores the received configuration data in the 
    # class attributes. Initializes the configuration Error codes.
    # 
    # Class attributes: 
    # subprocessCommandString: The terminal command to start the transcription subprocess.  
    # audioFilesPath: The path to the directory with the audio files of the test dataset. 
    # tsvFilePath: The path to the TSV file containing the labels of the test dataset.    
    # configurationError: List containing the error codes for the configuration validation.
    # 
    # Input:
    # subprocessCommandString: The terminal command to start the transcription subprocess.  
    # audioFilesPath: The path to the directory with the audio files of the test dataset. 
    # tsvFilePath: The path to the TSV file containing the labels of the test dataset.     
    def __init__(self, subprocessCommandString, audioFilesPath, tsvFilePath):
        self.subprocessCommandString = subprocessCommandString
        self.audioFilesPath = audioFilesPath
        self.tsvFilePath = tsvFilePath
        self.configurationError = [0, 0, 0, 0] 
        #Description of error codes in configurationError:  
        #For All:   0 = No Error. 
        #[0]: 1 = not command string given, 2 = commandstring error, 3 = subprocess Error
        #[1]: 1 = Audio path missing. 2 = Tsv Path missing 
        #[2]: 1 = audio path does not exist
        #[3]: 1 = tsv path does not exist

    # Validates the configuration data. Checks if the subprocess command was given and can be used to start the 
    # transcription subprocess. Checks if paths for a custom test dataset where given. If this is the case: Checks 
    # the given paths are valid. Stores error codes for every failed check in configurationError. If at least one 
    # check failed returns false. Else returns true. 
    # 
    # Return: 
    # Boolean indication if the configuration data is valid.  
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

    # Checks if the given path exists in the filesystem.
    # 
    # Input:
    # pathToTest: The path that sould be tested. 
    #  
    # Return: 
    # Boolean, indicating if the given path exists.  
    def isNotPath(self, pathToTest):
        if os.path.exists(pathToTest):
            return False
        return True

    # Checks if the given string is empty.
    # 
    # Input:
    # stringToTest: The string that should be tested.
    #  
    # Return:
    # Boolean, indicating whether the given string is empty or not.  
    def isEmptyString(self, stringToTest):
        if stringToTest == "":
            return True
        return False

    # Validates the subprocess command string. Checks if that the given string is not empty. Uses the 
    # subprocess command string to run the subprocess to verify that the string can be used to start the 
    # subprocess and check if the subprocess runs without errors.
    # 
    # Return: 
    # Error code corresponding to result of verification as integer.  
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

    # Returns the subprocess command string.
    # 
    # Return: 
    # String containing the command to start the transcription subprocess.  
    def getSubprocessCommandString(self):
        return self.subprocessCommandString

    # Returns the path to the directory containing the audio files of the test dataset.
    # 
    # Return: 
    # The path to the directory containing the audio files of the test dataset. 
    def getAudioFilesPath(self):
        return self.audioFilesPath

    # Returns the path to the TSV file containing the labels of the test dataset.
    # 
    # Return: 
    # The path to the TSV file containing the labels of the test dataset.
    def getTsvFilePath(self):
        return self.tsvFilePath

    # Returns the configurationError.
    # 
    # Return:
    # The list containing the configuration error codes.  
    def getConfigurationError(self):
        return self.configurationError
    
    # Formats the configuration data as SQLite-insert-query and returns it.
    # 
    # Return:
    # Configuration data formated as SQLite-insert-query-string.  
    def getConfigurationAsSqliteQuery(self):
        sqlQuery = f"INSERT INTO Configuration(commandString, audioFilePath, tsvFilePath) VALUES"

        if self.audioFilesPath == "" and self.tsvFilePath == "": 
            defaultAudioFilesPath = f"{pathlib.Path(__file__).parent.resolve()}/Data/TestData/CommonVoice/AudioFiles"
            defaultTsvFilePath = f"{pathlib.Path(__file__).parent.resolve()}/Data/TestData/CommonVoice/dataSet.tsv"
            sqlQuery += f"('{self.subprocessCommandString}', '{defaultAudioFilesPath}', '{defaultTsvFilePath}');"
            return sqlQuery
        sqlQuery += f"('{self.subprocessCommandString}', '{self.audioFilesPath}', '{self.tsvFilePath}');"
        return sqlQuery
