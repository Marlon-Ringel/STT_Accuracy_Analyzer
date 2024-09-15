import os
import pathlib
import subprocess

# Class that implements functionality to verify and manage the configuration data. Also used to store the 
# configuration data at runtime.  
class ConfigurationService:

    # Initialize the ConfigurationService Object. Store the received configuration data in the 
    # class attributes. Initialize the configuration error codes.
    # 
    # Class attributes: 
    # subprocessCommandString: String containing the Linux-terminal command to start the transcription subprocess.  
    # audioFilesPath: String containing the path to the directory with the audio files of the test dataset. 
    # tsvFilePath: String containing the path to the TSV file containing the labels of the test dataset.    
    # configurationError: List containing the error codes for the configuration validation.
    # 
    # Input:
    # subprocessCommandString: String containing the Linux-terminal command to start the transcription subprocess.  
    # audioFilesPath: String containing the path to the directory with the audio files of the test dataset. 
    # tsvFilePath: String containing the path to the TSV file containing the labels of the test dataset.  
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

    # Validate the configuration data. Check if the subprocess command was given and can be used to start the 
    # transcription subprocess. Checks if paths for a custom test dataset were given. If this is the case: Check that
    # the given paths are valid. Store error codes for every failed check in configurationError class attribute. 
    # If at least one check failed, return false. Else return true. 
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

    # Check if the given path does not exist in the file system.
    # 
    # Input:
    # pathToTest: String containing a path to be tested. 
    #  
    # Return: 
    # Boolean, indicating if the given path does not exist.  
    def isNotPath(self, pathToTest):
        if os.path.exists(pathToTest):
            return False
        return True

    # Check if the given string is empty.
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

    # Validate the subprocess command string. Check if that the given string is not empty. Use the 
    # subprocess command string to run the subprocess to verify that the string can be used to start the 
    # subprocess and check if the subprocess runs without errors.
    # 
    # Return: 
    # Error code corresponding to result of verification as an integer.  
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

    # Return the subprocess command string.
    # 
    # Return: 
    # String containing the command to start the transcription subprocess.  
    def getSubprocessCommandString(self):
        return self.subprocessCommandString

    # Return the path to the directory containing the audio files of the test dataset.
    # 
    # Return: 
    # String containing the path to the directory containing the audio files of the test dataset. 
    def getAudioFilesPath(self):
        return self.audioFilesPath

    # Return the path to the TSV file containing the labels of the test dataset.
    # 
    # Return: 
    # String containing the path to the TSV file containing the labels of the test dataset.
    def getTsvFilePath(self):
        return self.tsvFilePath

    # Return the configuration error codes.
    # 
    # Return:
    # List containing the configuration error codes.  
    def getConfigurationError(self):
        return self.configurationError
    
    # Format the configuration data as SQLite-insert-query and return it.
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
