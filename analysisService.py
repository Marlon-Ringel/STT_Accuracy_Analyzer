import jiwer
import jaro as jwd
from databaseService import DatabaseService
from analysisResults import AnalysisResults

class AnalysisService:
    # Initialize Object. Requests Transcription results from Database and store it in class attributes. Initialize AnalysisResults
    # and store it in class attributes for later use as storage for analysis results. 
    # 
    # Class attributes: 
    # guiConnection: Connection used to update GUI. 
    # transcriptionResults: TranscriptionResults Object holding the results from last Transkription Process execution. 
    # analysisResults: AnalysisResults Objekct for storage of the analysis results. 
    #
    # Input: 
    # guiConnection: Connection used to update GUI.  
    def __init__(self, guiConnection):
        self.guiConnection = guiConnection
        self.transcriptionResults = DatabaseService.loadTranscriptionResults()
        self.analysisResults = AnalysisResults()

    # Calculates the number of analysis steps. For every step, sends a progress update to GUI, calculate the ananlysis metrics
    # and stores them in the analysisResults class attribute. When all steps are done, stores the analysis results
    # in the database and send progress update to GUI that the analysis process is finished. 
    def performAnalysis(self):
        totalAnalysisSteps = self.transcriptionResults.len()

        for step in range(0, totalAnalysisSteps):
            self.sendAnalysisProgressUpdateToGuiBar(step, totalAnalysisSteps)        
            calculationResults = self.calculateAnalysisMetrics(self.transcriptionResults.getOriginalSentence(step), self.transcriptionResults.getTranscript(step))
            calculationResults.append(self.transcriptionResults.getId(step))
            self.analysisResults.addAnalysisResult(calculationResults)

        DatabaseService.saveAnalysisResults(self.analysisResults)
        self.sendAnalysisProgressUpdateToGuiLbl("Auswertung: Abgeschlossen")

    # Claclulates the five analysis metrics Word Error Rate (WER), Character Error Rate (CER), Match Error Rate (MER), 
    # Word Information Lost (WIL) and Jaro Winkler Distance (JWD). Then returns them as a list.
    # 
    # Input: 
    # originalText: A string containing a Text. 
    # transcript: A string containing a transcript. 
    # Return:
    # List containing the calculated analysis metrics.        
    def calculateAnalysisMetrics(self, originalText, transcript):
        return [jiwer.wer(originalText, transcript),
                jiwer.cer(originalText, transcript),
                jiwer.mer(originalText, transcript),
                jiwer.wil(originalText, transcript),
                1-jwd.jaro_winkler_metric(originalText, transcript)]
    
    # Updates the text above the analysis porgress bar of the GUI.
    # 
    # Input: 
    # String containing the current step and the number of all steps.
    def sendAnalysisProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateAnalysisProgressLbl(progressUpdate)

    # Updates the text above the analysis progress bar and the progress bar itself.
    # 
    # Input: 
    # currentStep: The number of the current step as integer.
    # totalSteps: The total number of required steps.    
    def sendAnalysisProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendAnalysisProgressUpdateToGuiLbl(f"Auswertungsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setAnalysisProgressStatus(int((currentStep+1)/totalSteps*100))
