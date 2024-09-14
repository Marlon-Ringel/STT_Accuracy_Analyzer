class TestData():
    # Initializes TestData Object. Saves given IDs into the class attributes.
    # 
    # Class attributes: 
    # ids: List containing the database table IDs for the test dataset. 
    # originalSentences: List containing the original sentences (Labels) from the test data set. 
    # audioFileNames: List containing names of the audio files of the test dataset. 
    def __init__(self, ids, originalSentences, audioFileNames):
        self.ids = ids
        self.originalSentences = originalSentences
        self.audioFileNames = audioFileNames

    # Returns the ID for a given index from the ids class attribute.
    # 
    # Input:
    # index: Integer for identifing the desired entry. 
    # 
    # Return: 
    # The ID from the ids class attribute corressponding index number.  
    def getId(self, index):
        return self.ids[index]

    # Returns the audio file name for a given index from the audioFileNames class attribute.
    # 
    # Input:
    # index: Integer for identifying the desired entry. 
    # 
    # Return: 
    # The audio file name from the audioFileNames class attribute corresponding index number. 
    def getAudioFileName(self, index):
        return self.audioFileNames[index]

    # Returns the original sentence for a given index from the originalSentences class attribute.
    # 
    # Input:
    # index: Integer for identifying the desired entry. 
    # 
    # Return: 
    # The original sentence from the originalSentences class attribute corresponding index number. 
    def getOriginalSentence(self, index):
        return self.originalSentences[index]

    # Returns the number of entries from the dataset stored in the class attributes.
    # 
    # Return:
    # Number of entries from the dataset stored in the class attributes as integer. 
    def len(self):
        return len(self.audioFileNames)
