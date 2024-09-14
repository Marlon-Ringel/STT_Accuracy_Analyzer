import subprocess
from databaseService import DatabaseService
from transcriptionResults import TranscriptionResults

class TranscriptionService:
    # Initializes the TranscriptionService Object. Requests the configuration data from the database and stores it in a 
    # class attribute alongside the guiConnection. Updates GUI that test dataset will be read into the database. Invokes
    # reading of test dataset into database. Requests test dataset from database and stores it in class attribute. 
    # Initializes TranscriptionResults Object. Updates GUI that was read successful.
    #
    # Class attributes: 
    # configuration: ConfigurationService Object containing the configuration data. 
    # guiConnection: Connection used to update GUI. 
    # testData: TestData Object containing the test dataset. 
    # transcriptionResults: TranscriptionResults Object for storage of transcription results. 
    #  
    # Input:
    # guiConnection: Connection used to update GUI.
    def __init__(self, guiConnection):
        self.configuration = DatabaseService.loadConfiguration()
        self.guiConnection = guiConnection
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Einlesen der Testdaten.")
        DatabaseService.readTestDataFileIntoDatabase(self.configuration.getTsvFilePath())
        self.testData = DatabaseService.loadTestData()
        self.transcriptionResults = TranscriptionResults()
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Ausstehend.")

    # Calculates the number of transcription steps. For every step, sends a progress update to GUI, generates a transcript
    # and stores it in the transcriptionResults class attribute. When all steps are done. Stores the transcription results
    # in the database and send progress update to GUI that transcription process is finished. 
    def generateTranscriptions(self):
        totalTranscriptionSteps = self.testData.len()

        for counter in range(0, totalTranscriptionSteps):
            self.sendTranscriptionProgressUpdateToGuiBar(counter, totalTranscriptionSteps)
            transcript = self.generateTranscriptionViaSubprocess(self.configuration.getSubprocessCommandString(), f"{self.configuration.getAudioFilesPath()}/{self.testData.getAudioFileName(counter)}")
            self.transcriptionResults.addTranscriptionResult(self.testData.getId(counter), transcript)
            
        DatabaseService.saveTranscriptionResults(self.transcriptionResults)
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Abgeschlossen.")

    # Starts the subprocess using the command string and passing the audioFilePath to it. Takes the generated transcription 
    # from the subprocess and returns it.
    # 
    # Input: 
    # commandString: String containing the command to start the transcription subprocess. 
    # audioFilePath: String containing the path to the audio file that should be transcribed.  
    # 
    # Return:
    # String containing the generated transcript. 
    def generateTranscriptionViaSubprocess(self, commandString, audioFilePath):
        subprocessResult = subprocess.run(commandString.split(", "), capture_output=True, text=True, input=audioFilePath)
        if subprocessResult.returncode != 0:
            print(f"Error in transcription Subprocess\nSubprocess returncode = {subprocessResult.returncode}\nSubprocess stderr = {subprocessResult.stderr}")
            raise RuntimeError(f"Error in transcription Subprocess\nSubprocess returncode = {subprocessResult.returncode}\nSubprocess stderr = {subprocessResult.stderr}")
        return subprocessResult.stdout.replace("\'", "")
    
    # Updates the text above the transcription porgress bar of the GUI.
    # 
    # Input: 
    # progressUpdate: String containing the current step and the number of all steps.   
    def sendTranscriptionProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateTranscriptionProgressLbl(progressUpdate)
    
    # Updates the text above the transcription progress bar and the progress bar itself.
    # 
    # Input: 
    # currentStep: The number of the current step as integer.
    # totalSteps: The total number of required steps.     
    def sendTranscriptionProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendTranscriptionProgressUpdateToGuiLbl(f"Transkriptionsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setTranscriptionProgressStatus(int((currentStep+1)/totalSteps*100))
    