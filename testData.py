# Class for storage of the test dataset data at runtime. 
class TestData():
    # Initialize TestData Object. Saves given test data into the class attributes.
    # 
    # Class attributes: 
    # ids: List containing the database IDs for the test dataset. 
    # originalSentences: List containing the original sentences (Labels) from the test dataset. 
    # audioFileNames: List containing names of the audio files of the test dataset.
    # 
    # Input:
    # ids: List containing the database IDs for the test dataset. 
    # originalSentences: List containing the original sentences (Labels) from the test dataset. 
    # audioFileNames: List containing names of the audio files of the test dataset. 
    def __init__(self, ids, originalSentences, audioFileNames):
        self.ids = ids
        self.originalSentences = originalSentences
        self.audioFileNames = audioFileNames

    # Return the ID for a given index from the ids class attribute.
    # 
    # Input:
    # index: Integer for identifying the desired entry. 
    # 
    # Return: 
    # Integer containing the ID from the ids class attribute corresponding to the index number.  
    def getId(self, index):
        return self.ids[index]

    # Return the audio file name for a given index from the audioFileNames class attribute.
    # 
    # Input:
    # index: Integer for identifying the desired entry. 
    # 
    # Return: 
    # String containing the audio file name from the audioFileNames class attribute corresponding to the index number.  
    def getAudioFileName(self, index):
        return self.audioFileNames[index]

    # Return the original sentence (test dataset Label) for a given index from the originalSentences class attribute.
    # 
    # Input:
    # index: Integer for identifying the desired entry. 
    # 
    # Return: 
    # String containing the original sentence from the originalSentences class attribute corresponding to the index number. 
    def getOriginalSentence(self, index):
        return self.originalSentences[index]

    # Return the number of entries in the test dataset stored in the class attributes.
    # 
    # Return:
    # Integer, containing the Number of entries in the test dataset stored in the class attributes. 
    def len(self):
        return len(self.audioFileNames)
