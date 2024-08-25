class TestData():
    def __init__(self, ids, originalSentences, audioFileNames):
        self.ids = ids
        self.originalSentences = originalSentences
        self.audioFileNames = audioFileNames

    def getId(self, index):
        return self.ids[index]

    def getAudioFileName(self, index):
        return self.audioFileNames[index]

    def getOriginalSentence(self, index):
        return self.originalSentences[index]

    def len(self):
        return len(self.audioFileNames)
