import subprocess
from databaseService import DatabaseService
from transcriptionResults import TranscriptionResults

# Class that implements functionality to generate transcripts based on the test dataset.
class TranscriptionService:

    # Initialize the TranscriptionService Object. Request the configuration data from the database and store it in the 
    # class attributes alongside the TestProgressPage Object (guiConnection). Send a Progress update to the GUI that 
    # process of reading the test dataset into the database has started. Invoke process of reading the test dataset into the database. 
    # Request test dataset from database and store it in the class attributes. Initialize TranscriptionResults Object. 
    # Send a progress update to the GUI that the test dataset was successfully read into the database.
    #
    # Class attributes: 
    # configuration: ConfigurationService Object containing the configuration data. 
    # guiConnection: TestProgressPage Object used to update GUI. 
    # testData: TestData Object containing the test dataset. 
    # transcriptionResults: TranscriptionResults Object for storage of the transcription results. 
    #  
    # Input:
    # guiConnection: TestProgressPage Object used to update GUI. 
    def __init__(self, guiConnection):
        self.configuration = DatabaseService.loadConfiguration()
        self.guiConnection = guiConnection
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Einlesen der Testdaten.")
        DatabaseService.readTestDataFileIntoDatabase(self.configuration.getTsvFilePath())
        self.testData = DatabaseService.loadTestData()
        self.transcriptionResults = TranscriptionResults()
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Ausstehend.")

    # Calculate the number of transcription steps. For every step, send a progress update to GUI, generate a transcript
    # and store it in the transcriptionResults class attribute. When all steps are completed. Store the transcription results
    # in the database and send progress update to GUI that transcription process is finished. 
    def generateTranscriptions(self):
        totalTranscriptionSteps = self.testData.len()

        for counter in range(0, totalTranscriptionSteps):
            self.sendTranscriptionProgressUpdateToGuiBar(counter, totalTranscriptionSteps)
            transcript = self.generateTranscriptionViaSubprocess(self.configuration.getSubprocessCommandString(), f"{self.configuration.getAudioFilesPath()}/{self.testData.getAudioFileName(counter)}")
            self.transcriptionResults.addTranscriptionResult(self.testData.getId(counter), transcript)
            
        DatabaseService.saveTranscriptionResults(self.transcriptionResults)
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Abgeschlossen.")

    # Start the transcription subprocess using the command string and pass the path of the audio file that should be transcribed 
    # to it. Take the generated transcription from the transcription subprocess and return it.
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
    
    # Update the text above the transcription progress bar on the test-progress-page.
    # 
    # Input: 
    # String containing the text that should be displayed above the transcription progress bar.    
    def sendTranscriptionProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateTranscriptionProgressLbl(progressUpdate)
        
    # Update the text above the transcription progress bar on the test-progress-page. Calculate the percentage of the progress
    # of the transcription process and use it to update the transcription progress bar.
    # 
    # Input: 
    # currentStep: The number of the current transcription step as integer.
    # totalSteps: The total number of required transcription steps as integer.      
    def sendTranscriptionProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendTranscriptionProgressUpdateToGuiLbl(f"Transkriptionsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setTranscriptionProgressStatus(int((currentStep+1)/totalSteps*100))
    