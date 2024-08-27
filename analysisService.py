import jiwer
import jaro as jwd
from databaseService import DatabaseService
from analysisResults import AnalysisResults

class AnalysisService:
    def __init__(self, guiConnection):
        self.guiConnection = guiConnection
        self.transcriptionResults = DatabaseService.loadTranscriptionResults()
        self.analysisResults = AnalysisResults()

    def performAnalysis(self):
        totalAnalysisSteps = self.transcriptionResults.len()

        for step in range(0, totalAnalysisSteps):
            self.sendAnalysisProgressUpdateToGuiBar(step, totalAnalysisSteps)        
            calculationResults = self.calculateAnalysisMetrics(self.transcriptionResults.getOriginalSentence(step), self.transcriptionResults.getTranscript(step))
            calculationResults.append(self.transcriptionResults.getId(step))
            self.analysisResults.addAnalysisResult(calculationResults)

        DatabaseService.saveAnalysisResults(self.analysisResults)
        self.sendAnalysisProgressUpdateToGuiLbl("Auswertung: Abgeschlossen")
        
    def calculateAnalysisMetrics(self, originalText, transcript):
        return [jiwer.wer(originalText, transcript),
                jiwer.cer(originalText, transcript),
                jiwer.mer(originalText, transcript),
                jiwer.wil(originalText, transcript),
                jwd.jaro_winkler_metric(originalText, transcript)]
    
    def sendAnalysisProgressUpdateToGuiLbl(self, progressUpdate):
        self.guiConnection.updateAnalysisProgressLbl(progressUpdate)

    def sendAnalysisProgressUpdateToGuiBar(self, currentStep, totalSteps):
        self.sendAnalysisProgressUpdateToGuiLbl(f"Auswertungsschritt: {currentStep+1} / {totalSteps}")
        self.guiConnection.setAnalysisProgressStatus(int((currentStep+1)/totalSteps*100))
