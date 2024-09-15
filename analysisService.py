import jiwer
import jaro as jwd
from databaseService import DatabaseService
from analysisResults import AnalysisResults

# Class that implements functionality to calculate the analysis metrics based on the transcription results. 
class AnalysisService:

    # Initialize AnalysisService Object. Request transcription results from database and store it in class attributes 
    # to use later as basis of the analysis metrics calculations. Initialize AnalysisResults Object and store it in 
    # class attributes for later use as storage for the analysis results. 
    # 
    # Class attributes: 
    # guiConnection: TestProgressPage Object used to update GUI. 
    # transcriptionResults: TranscriptionResults Object holding the results from last transcription process execution. 
    # analysisResults: AnalysisResults Objekct for storage of the analysis results. 
    #
    # Input: 
    # guiConnection: TestProgressPage Object used to update GUI.  
    def __init__(self, guiConnection):
        self.guiConnection = guiConnection
        self.transcriptionResults = DatabaseService.loadTranscriptionResults()
        self.analysisResults = AnalysisResults()

    # Calculate the number of analysis steps. For every step, send a progress update to GUI (current analysis step), 
    # calculate the analysis metrics and store them in the analysisResults class attribute. When all steps are completed, 
    # store the analysis results in the database and send progress update to GUI (analysis process complete). 
    def performAnalysis(self):
        totalAnalysisSteps = self.transcriptionResults.len()

        for step in range(0, totalAnalysisSteps):
            self.sendAnalysisProgressUpdateToGuiBar(step, totalAnalysisSteps)        
            calculationResults = self.calculateAnalysisMetrics(self.transcriptionResults.getOriginalSentence(step), self.transcriptionResults.getTranscript(step))
            calculationResults.append(self.transcriptionResults.getId(step))
            self.analysisResults.addAnalysisResult(calculationResults)

        DatabaseService.saveAnalysisResults(self.analysisResults)
        self.sendAnalysisProgressUpdateToGuiLbl("Auswertung: Abgeschlossen")

    # Calculate the five analysis metrics Word Error Rate (WER), Character Error Rate (CER), Match Error Rate (MER), 
    # Word Information Lost (WIL) and Jaro Winkler Distance (JWD). Then returns them as a list.
    # 
    # Input: 
    # originalText: String containing the original sentence (Label of test dataset). 
    # transcript: String containing a transcript.
    #  
    # Return:
    # List containing the calculated analysis metrics.        
    def calculateAnalysisMetrics(self, originalText, transcript):
        return [jiwer.wer(originalText, transcript),
                jiwer.cer(originalText, transcript),
                jiwer.mer(originalText, transcript),
                jiwer.wil(originalText, transcript),
                1-jwd.jaro_winkler_metric(originalText, transcript)]
    
    # Update the text above the analysis progress bar on the test-progress-page.
    # 
    # Input: 
    # String containing the text that should be displayed above the analysis progress bar. 
    def sendAnalysisProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateAnalysisProgressLbl(progressUpdate)

    # Update the text above the analysis progress bar on the test-progress-page. Calculate the percentage of the progress
    # of the analysis process and use it to update the analysis progress bar.
    # 
    # Input: 
    # currentStep: The number of the current analysis step as integer.
    # totalSteps: The total number of required analysis steps as integer.    
    def sendAnalysisProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendAnalysisProgressUpdateToGuiLbl(f"Auswertungsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setAnalysisProgressStatus(int((currentStep+1)/totalSteps*100))
