class TranscriptionResults:
    def __init__(self, ids=[], originalSentences=[], originalSentanceIds=[], transcripts=[]):
        self.ids = ids
        self.originalSentences = originalSentences
        self.originalSentanceIds = originalSentanceIds
        self.transcripts = transcripts

    def addTranscriptionResult(self, newOriginalSentanceId, newTranscript):
        self.originalSentanceIds.append(newOriginalSentanceId)
        self.transcripts.append(newTranscript)

    def getId(self, index):
        return self.ids[index]

    def getOriginalSentence(self, index):
        return self.originalSentences[index]

    def getTranscript(self, index):
        return self.transcripts[index]

    def getTranscriptionResultDataAsSqliteQuery(self):
        sqlQuery = "INSERT INTO TranscriptionResults (originalSentaceId, transcript) VALUES"
        for index in range(0, self.len()):
            sqlQuery += f"({self.originalSentanceIds[index]}, '{self.transcripts[index]}'),"
        return sqlQuery[:-1] + ";"

    def len(self):
        return len(self.transcripts)
