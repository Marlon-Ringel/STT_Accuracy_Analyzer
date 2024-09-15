import numpy as np

# Class for stroage of the results from the analysis service at runtime. 
class AnalysisResults:

    # Take the analysis results as a list of lists and store them in the individual class attributes. Calculate the
    # average for the analysis metrics if the calculateAverage variable is set to true. 
    #
    # class attributes:
    # wer: List containing the results from the calculation of the Word Error Rate metric. 
    # cer: List containing the results from the calculation of the Character Error Rate metric. 
    # mer: List containing the results from the calculation of the Match Error Rate metric. 
    # wil: List containing the results from the calculation of the Word Information Lost metric. 
    # jwd: List containing the results from the calculation of the Jaro Winkler Distance metric. 
    # idTranscriptionResult: List containing the database IDs of the transcription results 
    #                        for which the analysis metrics were calculated. 
    # averageOfMetrics: List containing the calculated averages for all analysis metrics. 
    # 
    # Input:  
    # analysisResults: The analysis results as a list of lists. Default value = Empty list of lists. 
    # calculateAverage: Boolean indicating if the averages of the analysis results should be calculated. Default Value = false. 
    def __init__(self, analysisResults=[[], [], [], [], [], []], calculateAverage=False):
        self.wer = analysisResults[0]
        self.cer = analysisResults[1]
        self.mer = analysisResults[2]
        self.wil = analysisResults[3]
        self.jwd = analysisResults[4]
        self.idTranscriptionResult = analysisResults[5]
        self.averageOfMetrics = []
        if calculateAverage:
            self.calculateAverageOfAnalysisMetrics()

    # Calculate the averages of the analysis metrics and return them as a list.
    # 
    # Return:
    # List containing the averages of the analysis results.  
    def calculateAverageOfAnalysisMetrics(self):
        self.averageOfMetrics = [np.average(self.wer), 
                                 np.average(self.cer), 
                                 np.average(self.mer), 
                                 np.average(self.wil),  
                                 np.average(self.jwd)]

    # Add a new analysis result to the class attributes by appending the result data to the 
    # corresponding class attributes. 
    # 
    # Input: 
    # newResult: A new analysis results set in form of a list containing the analysis metrics 
    #            and the database ID from the corresponding transcription result.    
    def addAnalysisResult(self, newResult):
        self.wer.append(newResult[0])
        self.cer.append(newResult[1])
        self.mer.append(newResult[2])
        self.wil.append(newResult[3])
        self.jwd.append(newResult[4])
        self.idTranscriptionResult.append(newResult[5])

    # Return the average of the analysis metrics.
    # 
    # Return: 
    # List containing the average of all analysis metrics.  
    def getAverageOfResults(self):
        return self.averageOfMetrics

    # Format the analysis result data as SQLite-insert-query and return it.
    # 
    # Return:
    # Analysis result data formated as SQLite-insert-query-string.  
    def getAnalysisResultsAsSqliteQuery(self):
        sqlQuery = "INSERT INTO AnalysisResults(wer, cer, mer, wil, jwd, idTranscriptionResult) VALUES"
        for index in range(0, len(self.wer)):
            sqlQuery += f"({self.wer[index]}, {self.cer[index]}, {self.mer[index]}, {self.wil[index]}, {self.jwd[index]}, {self.idTranscriptionResult[index]}),"
        return sqlQuery[:-1] + ";"
