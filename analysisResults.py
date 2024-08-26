import numpy as np

class AnalysisResults:
    def __init__(self, analysisResults=[[], [], [], [], [], []], calculateAverage=False):
        self.wer = analysisResults[0]
        self.cer = analysisResults[1]
        self.mer = analysisResults[2]
        self.wil = analysisResults[3]
        self.jwd = analysisResults[4]
        self.idTestResult = analysisResults[5]
        self.averageOfMetrics = []
        if calculateAverage:
            self.calculateAverageOfAnalysisMetrics()

    def calculateAverageOfAnalysisMetrics(self):
        self.averageOfMetrics = [np.average(self.wer), 
                                 np.average(self.cer), 
                                 np.average(self.mer), 
                                 np.average(self.wil),  
                                 np.average(self.jwd)]
        
    def addAnalysisResult(self, newResult):
        self.wer.append(newResult[0])
        self.cer.append(newResult[1])
        self.mer.append(newResult[2])
        self.wil.append(newResult[3])
        self.jwd.append(newResult[4])
        self.idTestResult.append(newResult[5])

    def getAverageOfResults(self):
        return self.averageOfMetrics

    def getAnalysisResultsAsSqliteQuery(self):
        sqlQuery = "INSERT INTO AnalysisResults(wer, cer, mer, wil, jwd, idTestResult) VALUES"
        for index in range(0, len(self.wer)):
            sqlQuery += f"({self.wer[index]}, {self.cer[index]}, {self.mer[index]}, {self.wil[index]}, {self.jwd[index]}, {self.idTestResult[index]}),"
        return sqlQuery[:-1] + ";"
