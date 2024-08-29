import subprocess
from databaseService import DatabaseService
from transcriptionResults import TranscriptionResults

class TranscriptionService:
    def __init__(self, guiConnection):
        self.configuration = DatabaseService.loadConfiguration()
        self.guiConnection = guiConnection
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Einlesen der Testdaten.")
        DatabaseService.readTestDataFileIntoDatabase(self.configuration.getTsvFilePath())
        self.testData = DatabaseService.loadTestData()
        self.TranscriptionResults = TranscriptionResults()
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Ausstehend.")

    def generateTranscriptions(self):
        totalTranscriptionSteps = self.testData.len()

        for counter in range(0, totalTranscriptionSteps):
            self.sendTranscriptionProgressUpdateToGuiBar(counter, totalTranscriptionSteps)
            transcript = self.generateTranscriptionViaSubprocess(self.configuration.getSubprocessCommandString(), f"{self.configuration.getAudioFilesPath()}/{self.testData.getAudioFileName(counter)}")
            self.TranscriptionResults.addTranscriptionResult(self.testData.getId(counter), transcript)
            
        DatabaseService.saveTranscriptionResults(self.TranscriptionResults)
        self.sendTranscriptionProgressUpdateToGuiLbl("Transkription: Abgeschlossen.")

    def generateTranscriptionViaSubprocess(self, commandString, audioFilePath):
        subprocessResult = subprocess.run(commandString.split(", "), capture_output=True, text=True, input=audioFilePath)
        if subprocessResult.returncode != 0:
            print(f"Error in transcription Subprocess\nSubprocess returncode = {subprocessResult.returncode}\nSubprocess stderr = {subprocessResult.stderr}")
            raise RuntimeError(f"Error in transcription Subprocess\nSubprocess returncode = {subprocessResult.returncode}\nSubprocess stderr = {subprocessResult.stderr}")
        return subprocessResult.stdout.replace("\'", "")
    
    def sendTranscriptionProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateTranscriptionProgressLbl(progressUpdate)

    def sendTranscriptionProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendTranscriptionProgressUpdateToGuiLbl(f"Transkriptionsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setTranscriptionProgressStatus(int((currentStep+1)/totalSteps*100))
    