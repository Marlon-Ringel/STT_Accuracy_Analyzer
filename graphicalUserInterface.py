import tkinter as tk 
from tkinter import filedialog
from tkinter import ttk
import threading as th
from databaseService import DatabaseService
from configurationService import ConfigurationService
from transcriptionService import TranscriptionService
from analysisService import AnalysisService

# Class that implements funktionality to generate and manage the page objects for the GUI pages.
class GuiService(tk.Tk):

    # Initialize the GUI and the pages of the GUI. Display start-page. Set handler function for the close window event. 
    def __init__(self):
        tk.Tk.__init__(self)

        # Title text of the application. 
        self.title("Speech to Text Accuracy Analyzer")

        # Container frame in which the individual pages are placed. 
        pageContainer = tk.Frame(self)
        pageContainer.pack(side = "top", fill = "both", expand = True)

        # Dictionary for storage of the GUI page objects. 
        self.pages = {}

        # Create and initialize the page objects of the GUI. 
        for Page in (InputPage, TestProgressPage, ResultPage):
            newPage = Page(pageContainer, self)
            self.pages[Page] = newPage 
            newPage.grid(row = 0, column = 0, sticky ="nsew")

        # Display input-page (acts as start-page of application).
        self.showPage(InputPage)

        # Set handler function for close window event. 
        self.protocol("WM_DELETE_WINDOW", self.closeApplication)  

    # Display a specified page in the application window.
    # 
    # Input: 
    # pageName: A String containing the name of the page that should be displayed.  
    def showPage(self, pageName):
        page = self.pages[pageName]
        page.initializePage()
        page.tkraise()

    # Handler function for the close window event. Reset the database and close the application.  
    def closeApplication(self):
        DatabaseService.resetDataBase()
        self.destroy()

# Class that represents the input-page of the GUI. 
class InputPage(tk.Frame):

    # Initialize the elements of the GUI for the Iinput-page.
    # 
    # Input: 
    # pageContainer: The tkinter frame Object in which the page is contained.  
    # guiService: The GUIService Object used to request the next GUI page.  
    def __init__(self, pageContainer, guiService): 
        tk.Frame.__init__(self, pageContainer)
        
        # Subprocess command string input GUI elements. 
        subprocessCommandStringInputLbl = tk.Label(self, text="Bitte den Terminal Befehl zum Starten der zu testenden STT-Anwendung als durch Kommas separierten Text eingeben (Benötigt).")
        subprocessCommandStringInputLbl.grid(row=0, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(15,0))

        self.subprocessCommandStringInputEtr = tk.Entry(self, width=100)
        self.subprocessCommandStringInputEtr.grid(row=1, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.subprocessCommandStringInputErrorLbl = tk.Label(self, text="", fg="red")
        self.subprocessCommandStringInputErrorLbl.grid(row=2, column=0, sticky="w", padx=(10,0), pady=(0,10))

        # Custom test dataset audio files path input GUI elements.
        customTestDataAudioFilesPathSelectionLbl = tk.Label(self, text="Bitte ein Verzeichnis mit MP3-Testdaten auswählen (Optional).")
        customTestDataAudioFilesPathSelectionLbl.grid(row=3, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataAudioFilesPathSelectionEtr = tk.Entry(self, width=100)
        self.customTestDataAudioFilesPathSelectionEtr.grid(row=4, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataAudioFilesPathSelectionErrorLbl = tk.Label(self, text="", fg="red")
        self.customTestDataAudioFilesPathSelectionErrorLbl.grid(row=5, column=0, sticky="w", padx=(10,0), pady=(0,10))

        customTestDataAudioFilesPathSelectionBtn = tk.Button(self, text="Verzeichnis auswählen", command=lambda : self.selectCustomTestDataAudioFilesPath())
        customTestDataAudioFilesPathSelectionBtn.grid(row=4, column=52, sticky="w", padx=(15,10), pady=(0,0))

        # Custom test dataset TSV file path input GUI elements.
        customTestDataTsvFilePathSelectionLbl = tk.Label(self, text="Bitte eine TSV-Datei auswählen (Optional).")
        customTestDataTsvFilePathSelectionLbl.grid(row=6, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataTsvFilePathSelectionEtr = tk.Entry(self, width=100)
        self.customTestDataTsvFilePathSelectionEtr.grid(row=7, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataTsvFilePathSelectionErrorLbl = tk.Label(self, text="", fg="red")
        self.customTestDataTsvFilePathSelectionErrorLbl.grid(row=8, column=0, sticky="w", padx=(10,0), pady=(0,0))

        customTestDataTsvFilePathSelectionBtn = tk.Button(self, text="TSV-Datei auswählen", command=lambda : self.selectCustomTestDataTsvFilePath())
        customTestDataTsvFilePathSelectionBtn.grid(row=7, column=52, sticky="ew", padx=(15,10), pady=(0,0))

        # Start test process button
        self.startTestProcessBtn = tk.Button(self, text="Testprozess Starten", command=lambda : self.validateInput())
        self.startTestProcessBtn.grid_propagate(0)
        self.startTestProcessBtn.grid(row=10, column=0, columnspan=10, sticky="w", padx=(10,0), pady=(0,10))

        # Label for verification text display. 
        self.inputValidationLbl = tk.Label(self, text="")
        self.inputValidationLbl.grid(row=10, column=11, columnspan=20, sticky="w", padx=(0,0), pady=(0,0))

        # The GUIService Object used to request the next GUI page. 
        self.guiService = guiService
    
    # Prepare the display of the input-page. Delete the database and recreate it to ensure no data from previous executions of the 
    # application remains in the database. 
    def initializePage(self):
        DatabaseService.resetDataBase()
        DatabaseService.initializeDataBase()

    # Invoke the input validation process. Deactivate the "Testprozess Starten" Button and display a message to inform the 
    # user that he has to wait until the validation is complete. Start the validation Process in a new thread.  
    def validateInput(self):
        self.toggleStartTestProcessBtnAndMessage()
        th.Thread(target=self.performValidation, daemon=True).start()

    # Remove all error messages if present. Initialize a ConfigurationService Objecct and pass it the configuration data from the GUI. 
    # Use the ConfigurationService Object to conduct the validation. 
    # If the validation failed: Requests the configuration error from ConfigurationService Objekt and display corresponding error 
    # messages. Also reactivate the "Testprozess Starten" Button. 
    # If the validation was successful: Save the configuration data in the Database and display the test-progress-page.  
    def performValidation(self):
        self.removeErrorMessages()
        config = ConfigurationService(self.subprocessCommandStringInputEtr.get(),
                                        self.customTestDataAudioFilesPathSelectionEtr.get(),
                                        self.customTestDataTsvFilePathSelectionEtr.get())
        if not config.validateConfiguration():
            self.displayErrorMessages(config.getConfigurationError())
            self.toggleStartTestProcessBtnAndMessage()
        else:
            DatabaseService.saveConfiguration(config)
            self.guiService.showPage(TestProgressPage)

    # Check the state of the "Testprozess Starten" button. 
    # If the button is disabled: Set the state to normal (enabled) and remove the input validation message. 
    # If the button is not disabled: Set the state to disabled and display the input validation message. 
    def toggleStartTestProcessBtnAndMessage(self):
        if self.startTestProcessBtn["state"] == "disabled":
            self.startTestProcessBtn.configure(state="normal")
            self.inputValidationLbl["text"] = ""
        else:
            self.startTestProcessBtn.configure(state="disabled")
            self.inputValidationLbl["text"] = "Überprüfung der eingegebenen Daten. Bitte Warten …"

    # Remove all error messages on the input-page. 
    def removeErrorMessages(self):
        self.subprocessCommandStringInputErrorLbl["text"] = ""
        self.customTestDataAudioFilesPathSelectionErrorLbl["text"] = ""
        self.customTestDataTsvFilePathSelectionErrorLbl["text"] = ""

    # Use the error codes in the errorList parameter to display specific error messages on the input-page.
    # 
    # Input: 
    # errorList: List containing the configuration error codes.  
    def displayErrorMessages(self, errorList):
        if errorList[0] == 1:
            self.updateSubprocessCommandStringInputError("Fehler: Kein Terminal Befehl zum Starten des KI-Modell-Subprozesses eingegeben.")

        if errorList[0] == 2: 
            self.updateSubprocessCommandStringInputError("Fehler: Der Terminal Befehl zum Starten des KI-Modell-Subprozesses ist fehlerhaft.")

        if errorList[0] == 3:
            self.updateSubprocessCommandStringInputError("Fehler: Der KI-Modell-Subprozesses ist fehlerhaft.")

        if errorList[1] == 1:
            self.updateCustomTestDataAudioFilesPathSelectionError("Fehler: Kein Verzeichnis mit MP3-Testdaten ausgewählt.")

        if errorList[1] == 2:
            self.updateCustomTestDataTsvFilePathSelectionError("Fehler: Keine TSV-Datei ausgewählt")

        if errorList[2] == 1:
            self.updateCustomTestDataAudioFilesPathSelectionError("Fehler: Der ausgewählte Pfad existiert nicht.")

        if errorList[3] == 1:
            self.updateCustomTestDataTsvFilePathSelectionError("Fehler: Der ausgewählte Pfad existiert nicht.")  

    # Display a given error message below the command string entry field.
    # 
    # Input:
    # errorText: String containing the error description. 
    def updateSubprocessCommandStringInputError(self, errorText):
        self.subprocessCommandStringInputErrorLbl["text"] = errorText

    # Display a given error message below the audio files path entry field.
    # 
    # Input:
    # errorText: String containing the error description. 
    def updateCustomTestDataAudioFilesPathSelectionError(self, errorText):
        self.customTestDataAudioFilesPathSelectionErrorLbl["text"] = errorText

    # Display a given error message below the tsv file path entry field.
    # 
    # Input:
    # errorText: String containing the error description. 
    def updateCustomTestDataTsvFilePathSelectionError(self, errorText):
        self.customTestDataTsvFilePathSelectionErrorLbl["text"] = errorText

    # Open a system dialog where the user can choose a folder. 
    # Display the selected path to the folder in the audio files path entry field. 
    def selectCustomTestDataAudioFilesPath(self):
        folderPath = filedialog.askdirectory()
        self.customTestDataAudioFilesPathSelectionEtr.delete(0, tk.END)
        if folderPath: 
            self.customTestDataAudioFilesPathSelectionEtr.insert(0, folderPath)

    # Open a system dialog where the user can choose a TSV file. 
    # Display the selected path to the folder in the TSV file path entry field. 
    def selectCustomTestDataTsvFilePath(self):
        filePath = filedialog.askopenfile(
            filetypes=(
                ("TSV Files", "*.tsv"),
                ("All Files", "*.*")
            )
        )
        self.customTestDataTsvFilePathSelectionEtr.delete(0, tk.END)
        if filePath: 
            self.customTestDataTsvFilePathSelectionEtr.insert(0, filePath.name)

# Class that represents the test-progress-page of the GUI. 
class TestProgressPage(tk.Frame):

    # Initialize the elements of the GUI for the test-progress-page.
    # 
    # Input: 
    # pageContainer: The tkinter Frame Object in which the page is contained.  
    # guiService: The GUIService Object used to request the next GUI page. 
    def __init__(self, pageContainer, guiService):
        tk.Frame.__init__(self, pageContainer)

        # Transcription progress bar and text display GUI elements. 
        self.transcriptionProgressLbl = tk.Label(self, text="Transkription: Ausstehend")
        self.transcriptionProgressLbl.grid(row = 2, column = 0, sticky="w", padx=(10,0), pady=(70,0))

        self.transcriptionProgressBarStatus = tk.IntVar()
        self.transcriptionProgressBar = ttk.Progressbar(self, length=1100, variable=self.transcriptionProgressBarStatus)
        self.transcriptionProgressBar.grid(row=3, column=0, columnspan=3, sticky="w", padx=(10,0), pady=(0,30))

        # Analysis progress bar and text display GUI elements. 
        self.analysisProgressLbl = tk.Label(self, text="Auswertung: Ausstehend")
        self.analysisProgressLbl.grid(row = 4, column = 0, sticky="w", padx=(10,0), pady=(0,0))

        self.analysisProgressBarStatus = tk.IntVar()
        self.analysisProgressBar = ttk.Progressbar(self, length=1100, variable=self.analysisProgressBarStatus)
        self.analysisProgressBar.grid(row=5, column=0, columnspan=3, sticky="w", padx=(10,0), pady=(0,80))

        # Button to cancel application execution and displaying test results depending on context.  
        self.controlBtn = tk.Button(self, text="Abbrechen", command=lambda : self.guiService.closeApplication())
        self.controlBtn.grid(row=6, column=0, sticky="w", padx=(10,0), pady=(0,10))

        # The GUIService Object used to request the next GUI page.
        self.guiService = guiService 
    
    # Prepare the display of the test-progress-page. Start the test process in a separate thread. 
    def initializePage(self):
        th.Thread(target=self.startTranscriptionAndAnalysisProcess, daemon=True).start()

    # Initialize the TranscriptionService Object and start the transcription progress. Initialize the AnalysisService and 
    # start the analysis process. Afterwards export the test process results as Excel table to the application directory 
    # and display the result-page. 
    def startTranscriptionAndAnalysisProcess(self):  
        try:
            transcriptionService = TranscriptionService(guiConnection=self)
        except IndexError:
            self.updateTranscriptionProgressLbl("Transkription: Fehler. Lesen der Testdaten nicht möglich.") 
            self.controlBtn.configure(text="Beenden", fg="red")
            return
        try:
            transcriptionService.generateTranscriptions()
        except RuntimeError:
            self.updateTranscriptionProgressLbl("Transkription: Fehler. KI-Subprozess fehlerhaft.")
            self.controlBtn.configure(text="Beenden", fg="red")
            return
        analysisService = AnalysisService(guiConnection=self)
        analysisService.performAnalysis()
        DatabaseService.saveResultsAsExcel()
        self.controlBtn.configure(text="Ergebnisse Anzeigen", command=lambda : self.guiService.showPage(ResultPage))

    # Display a given status update above the transcription progress bar.
    # 
    # Input:
    # progressUpdate: String containing the status update to be displayed above the transcription progress bar.      
    def updateTranscriptionProgressLbl(self, progressUpdate):
        self.transcriptionProgressLbl["text"] = progressUpdate

    # Update the transcription progress bar according to the progressUpdate parameter.
    # 
    # Input:
    # progressUpdate: Integer containing the percentage of the progress of the transcription process.  
    def setTranscriptionProgressStatus(self, progressUpdate):
        self.transcriptionProgressBarStatus.set(progressUpdate)
    
    # Display a given status update above the analysis progress bar.
    # 
    # Input:
    # progressUpdate: String containing the status update to be displayed above the analysis progress bar.  
    def updateAnalysisProgressLbl(self, progressUpdate):
        self.analysisProgressLbl["text"] = progressUpdate
    
    # Update the analysis progress bar according to the progressUpdate parameter.
    # 
    # Input:
    # progressUpdate: Integer containing the percentage of the progress of the analysis process.  
    def setAnalysisProgressStatus(self, progressUpdate):
        self.analysisProgressBarStatus.set(progressUpdate)

# Class that represents the result-page of the GUI. 
class ResultPage(tk.Frame):

    # Initialize the elements of the GUI for the result-page.
    # 
    # Input: 
    # pageContainer: The tkinter Frame Object in which the page is contained.  
    # guiService: The GUIService Object used to close the application.
    def __init__(self, pageContainer, guiService):
        tk.Frame.__init__(self, pageContainer)

        # Page title text display GUI element. 
        resultsTitleLbl = tk.Label(self, text="Mittelwerte der Ergebnisse:")
        resultsTitleLbl.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(80,0))

        # GUI elements to display word error rate metric result. 
        self.werResultFrm = tk.Frame(self, width=360, height=30)
        self.werResultFrm.grid_propagate(0)
        self.werResultFrm.grid(row=1, column=0, sticky="w", padx=(10,0), pady=(20,0))

        self.werResultLbl = tk.Label(self.werResultFrm, text="WER: -1")
        self.werResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))

        # GUI elements to display character error rate metric result. 
        self.cerResultFrm = tk.Frame(self, width=360, height=30)
        self.cerResultFrm.grid_propagate(0)
        self.cerResultFrm.grid(row=1, column=1, sticky="w", padx=(0,0), pady=(20,0))

        self.cerResultLbl = tk.Label(self.cerResultFrm, text="CER: -1")
        self.cerResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))

        # GUI elements to display match error rate metric result. 
        self.merResultFrm = tk.Frame(self, width=360, height=30)
        self.merResultFrm.grid_propagate(0)
        self.merResultFrm.grid(row=1, column=2, sticky="w", padx=(0,0), pady=(20,0))

        self.merResultLbl = tk.Label(self.merResultFrm, text="MER: -1")
        self.merResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))

        # GUI elements to display word information lost metric result. 
        self.wilResultFrm = tk.Frame(self, width=360, height=30)
        self.wilResultFrm.grid_propagate(0)
        self.wilResultFrm.grid(row=2, column=0, sticky="w", padx=(10,0), pady=(20,0))

        self.wilResultLbl = tk.Label(self.wilResultFrm, text="WIL: -1")
        self.wilResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))

        # GUI elements to display jaro winkler distance metric result. 
        self.jwdResultFrm = tk.Frame(self, width=360, height=30)
        self.jwdResultFrm.grid_propagate(0)
        self.jwdResultFrm.grid(row=2, column=1, sticky="w", padx=(0,0), pady=(20,0))

        self.jwdResultLbl = tk.Label(self.jwdResultFrm, text="JWD: -1")
        self.jwdResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))

        # Button to export the detailed results as Excel table. 
        exportResultAsExcelBtn = tk.Button(self, text="Ergebnisse Exportieren", command=lambda : self.exportResultExcel())
        exportResultAsExcelBtn.grid(row=3, column=0, sticky="w", padx=(10,0), pady=(60,0))

        # Button to close the application. 
        closeAppBtn = tk.Button(self, text="Fertigstellen", command=lambda : self.guiService.closeApplication())
        closeAppBtn.grid(row=3, column=0, sticky="w", padx=(200,0), pady=(60,0))
    
        # guiService: The GUIService Object used to close the application.
        self.guiService = guiService
    
    # Prepare the display of the result-page. Set the default values for the result display in case the results do not contain any values. 
    # Display the actual result values. 
    def initializePage(self):
        self.setResultsDefaultVaules()
        self.displayResults()
    
    # Display the default values (all "-1") for the result display. 
    def setResultsDefaultVaules(self):
        self.werResultLbl["text"] = f"WER: -1"
        self.cerResultLbl["text"] = f"CER: -1"
        self.merResultLbl["text"] = f"MER: -1"
        self.wilResultLbl["text"] = f"WIL: -1"
        self.jwdResultLbl["text"] = f"Jaro: -1"

    # Request the average results from DatabaseService. Display the results on the result-page.
    def displayResults(self):
        data = DatabaseService.loadAnalysisResults().getAverageOfResults()
 
        self.werResultLbl["text"] = f"WER: {data[0]}"
        self.cerResultLbl["text"] = f"CER: {data[1]}"
        self.merResultLbl["text"] = f"MER: {data[2]}"
        self.wilResultLbl["text"] = f"WIL: {data[3]}"
        self.jwdResultLbl["text"] = f"JWD: {data[4]}"

    # Display a system dialog where the user can choose a directory to export the results. Exports the results to 
    # the path the user choose.
    def exportResultExcel(self):
        filePath = filedialog.asksaveasfile(initialfile="Results.xlsx", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if filePath: 
            DatabaseService.exportTestResultsAsExcel(filePath.name)
