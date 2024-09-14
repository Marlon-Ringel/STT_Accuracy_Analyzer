import numpy as np

class AnalysisResults:
    #Takes the analysis results as a list of lists and stores them in the individual class attributes. Calculates the
    # average for the analysis metrics if the calculateAverage variable is set to true. 
    #
    # class attributes:
    # wer: List containing the results from the calculation of the Word Error Rate metric. 
    # cer: List containing the results from the calculation of the Character Error Rate metric. 
    # mer: List containing the results from the calculation of the Match Error Rate metric. 
    # wil: List containing the results from the calculation of the Word Information Lost metric. 
    # jwd: List containing the results from the calculation of the Jaro Winkler Distance metric. 
    # idTestResult: List containing the IDs of the metrics from the database. 
    # averageOfMetrics: List containing the calculated averages of all metrics. 
    # 
    # Input:  
    # analysisResults: The analysis result in a list of list. Default value = Empty list of lists. 
    # calculateAverage: Boolean indicating if the averages of the analysis results should be calculated. Default Value = false. 
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

    # Calculates the averages of the five analysis metrics and returns them as a list.
    # 
    # Return:
    # List containing the averages of the analysis results.  
    def calculateAverageOfAnalysisMetrics(self):
        self.averageOfMetrics = [np.average(self.wer), 
                                 np.average(self.cer), 
                                 np.average(self.mer), 
                                 np.average(self.wil),  
                                 np.average(self.jwd)]

    # Adds a new analysis result to the class attributes by apending the results data to the 
    # corressponding class variables. 
    # 
    # Input: 
    # newResult: A new analysis results set in form of a list.     
    def addAnalysisResult(self, newResult):
        self.wer.append(newResult[0])
        self.cer.append(newResult[1])
        self.mer.append(newResult[2])
        self.wil.append(newResult[3])
        self.jwd.append(newResult[4])
        self.idTestResult.append(newResult[5])

    # Returns the average of metrics.
    # 
    # Return: 
    # List containing the average of all analysis metrics.  
    def getAverageOfResults(self):
        return self.averageOfMetrics

    # Formats the analysis result data as SQLite-insert-query and returns it.
    # 
    # Return:
    # Analysis result data formated as SQLite-insert-query-string.  
    def getAnalysisResultsAsSqliteQuery(self):
        sqlQuery = "INSERT INTO AnalysisResults(wer, cer, mer, wil, jwd, idTestResult) VALUES"
        for index in range(0, len(self.wer)):
            sqlQuery += f"({self.wer[index]}, {self.cer[index]}, {self.mer[index]}, {self.wil[index]}, {self.jwd[index]}, {self.idTestResult[index]}),"
        return sqlQuery[:-1] + ";"
