import tkinter as tk 
from tkinter import filedialog
from tkinter import ttk
from databasService import DatabaseService


class GuiService(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("STT Ai Analyzer")
        pageContainer = tk.Frame(self)
        pageContainer.pack(side = "top", fill = "both", expand = True)

        self.pages = {}

        for Page in (InputPage, TestProgressPage, ResultPage):
            newPage = Page(pageContainer, self)
            self.pages[Page] = newPage 
            newPage.grid(row = 0, column = 0, sticky ="nsew")

        self.showPage(InputPage)

    def showPage(self, pageName):
        page = self.pages[pageName]
        page.initializePage()
        page.tkraise()

class InputPage(tk.Frame):
    def __init__(self, pageContainer, guiService): 
        tk.Frame.__init__(self, pageContainer)
        
        # Subprocess Command String Input
        subprocessCommandStringInputLbl = tk.Label(self, text="Bitte den Terminal Befehl zum Starten des KI-Modell-Subprozesses als durch Kommata separierten Text eingeben (Benötigt).")
        subprocessCommandStringInputLbl.grid(row=0, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(15,0))

        self.subprocessCommandStringInputEtr = tk.Entry(self, width=100)
        self.subprocessCommandStringInputEtr.grid(row=1, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.subprocessCommandStringInputErrorLbl = tk.Label(self, text="", fg="red")
        self.subprocessCommandStringInputErrorLbl.grid(row=2, column=0, sticky="w", padx=(10,0), pady=(0,10))

        # Custom Test Data Audio Files Path Selection
        customTestDataAudioFilesPathSelectionLbl = tk.Label(self, text="Bitte ein Verzeichnis mit MP3-Testdaten auswählen (Optional).")
        customTestDataAudioFilesPathSelectionLbl.grid(row=3, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataAudioFilesPathSelectionEtr = tk.Entry(self, width=100)
        self.customTestDataAudioFilesPathSelectionEtr.grid(row=4, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataAudioFilesPathSelectionErrorLbl = tk.Label(self, text="", fg="red")
        self.customTestDataAudioFilesPathSelectionErrorLbl.grid(row=5, column=0, sticky="w", padx=(10,0), pady=(0,10))

        customTestDataAudioFilesPathSelectionBtn = tk.Button(self, text="Verzeichnis auswählen", command=lambda : self.selectCustomTestDataAudioFilesPath())
        customTestDataAudioFilesPathSelectionBtn.grid(row=4, column=52, sticky="w", padx=(15,10), pady=(0,0))

        # Tsv File Path input
        customTestDataTsvFilePathSelectionLbl = tk.Label(self, text="Bitte eine TSV-Datei auswählen (Optional).")
        customTestDataTsvFilePathSelectionLbl.grid(row=6, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataTsvFilePathSelectionEtr = tk.Entry(self, width=100)
        self.customTestDataTsvFilePathSelectionEtr.grid(row=7, column=0, columnspan=51, sticky="w", padx=(10,0), pady=(0,0))

        self.customTestDataTsvFilePathSelectionErrorLbl = tk.Label(self, text="", fg="red")
        self.customTestDataTsvFilePathSelectionErrorLbl.grid(row=8, column=0, sticky="w", padx=(10,0), pady=(0,0))

        customTestDataTsvFilePathSelectionBtn = tk.Button(self, text="TSV-Datei auswählen", command=lambda : self.selectCustomTestDataTsvFilePath())
        customTestDataTsvFilePathSelectionBtn.grid(row=7, column=52, sticky="ew", padx=(15,10), pady=(0,0))

        # Start Test Process Button
        startTestProcessBtn = tk.Button(self, text="Testprozess Starten", command=lambda : self.guiService.showPage(TestProgressPage))
        startTestProcessBtn.grid_propagate(0)
        startTestProcessBtn.grid(row=10, column=0, columnspan=10, sticky="w", padx=(10,0), pady=(0,10))

        self.guiService = guiService
    
    def initializePage(self):
        DatabaseService.resetDataBase()
        DatabaseService.initializeDataBase()

    def removeErrorMessages(self):
        self.subprocessCommandStringInputErrorLbl["text"] = ""
        self.customTestDataAudioFilesPathSelectionErrorLbl["text"] = ""
        self.customTestDataTsvFilePathSelectionErrorLbl["text"] = ""

    def updateSubprocessCommandStringInputError(self, errorText):
        self.subprocessCommandStringInputErrorLbl["text"] = errorText

    def updateCustomTestDataAudioFilesPathSelectionError(self, errorText):
        self.customTestDataAudioFilesPathSelectionErrorLbl["text"] = errorText

    def updateCustomTestDataTsvFilePathSelectionError(self, errorText):
        self.customTestDataTsvFilePathSelectionErrorLbl["text"] = errorText

    def selectCustomTestDataAudioFilesPath(self):
        folderPath = filedialog.askdirectory()
        self.customTestDataAudioFilesPathSelectionEtr.delete(0, tk.END)
        if folderPath: 
            self.customTestDataAudioFilesPathSelectionEtr.insert(0, folderPath)

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

class TestProgressPage(tk.Frame):
    def __init__(self, pageContainer, guiService):
        tk.Frame.__init__(self, pageContainer)

        self.transcriptionProgressLbl = tk.Label(self, text="Transkription: Ausstehend")
        self.transcriptionProgressLbl.grid(row = 2, column = 0, sticky="w", padx=(10,0), pady=(70,0))

        self.transcriptionProgressBarStatus = tk.IntVar()
        self.transcriptionProgressBar = ttk.Progressbar(self, length=1100, variable=self.transcriptionProgressBarStatus)
        self.transcriptionProgressBar.grid(row=3, column=0, columnspan=3, sticky="w", padx=(10,0), pady=(0,30))

        self.analysisProgressLbl = tk.Label(self, text="Auswertung: Ausstehend")
        self.analysisProgressLbl.grid(row = 4, column = 0, sticky="w", padx=(10,0), pady=(0,0))

        self.analysisProgressBarStatus = tk.IntVar()
        self.analysisProgressBar = ttk.Progressbar(self, length=1100, variable=self.analysisProgressBarStatus)
        self.analysisProgressBar.grid(row=5, column=0, columnspan=3, sticky="w", padx=(10,0), pady=(0,80))

        self.controlBtn = tk.Button(self, text="Abbrechen", command=lambda : self.guiService.showPage(ResultPage))
        self.controlBtn.grid(row=6, column=0, sticky="w", padx=(10,0), pady=(0,10))

        self.guiService = guiService 

    def initializePage(self):
        pass

    def updateTranscriptionProgressLbl(self, progressUpdate):
        self.transcriptionProgressLbl["text"] = progressUpdate

    def setTranscriptionProgressStatus(self, progressUpdate):
        self.transcriptionProgressBarStatus.set(progressUpdate)

    def updateAnalysisProgressLbl(self, progressUpdate):
        self.analysisProgressLbl["text"] = progressUpdate
    
    def setAnalysisProgressStatus(self, progressUpdate):
        self.analysisProgressBarStatus.set(progressUpdate)

class ResultPage(tk.Frame):
    def __init__(self, pageContainer, guiService):
        tk.Frame.__init__(self, pageContainer)

        resultsTitleLbl = tk.Label(self, text="Ergebnisse Mittelwerte:")
        resultsTitleLbl.grid(row=0, column=0, sticky="w", padx=(10,0), pady=(80,0))

        self.werResultFrm = tk.Frame(self, width=360, height=30)
        self.werResultFrm.grid_propagate(0)
        self.werResultFrm.grid(row=1, column=0, sticky="w", padx=(10,0), pady=(20,0))

        self.werResultLbl = tk.Label(self.werResultFrm, text="WER: -1")
        self.werResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))


        self.cerResultFrm = tk.Frame(self, width=360, height=30)
        self.cerResultFrm.grid_propagate(0)
        self.cerResultFrm.grid(row=1, column=1, sticky="w", padx=(0,0), pady=(20,0))

        self.cerResultLbl = tk.Label(self.cerResultFrm, text="CER: -1")
        self.cerResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))


        self.merResultFrm = tk.Frame(self, width=360, height=30)
        self.merResultFrm.grid_propagate(0)
        self.merResultFrm.grid(row=1, column=2, sticky="w", padx=(0,0), pady=(20,0))

        self.merResultLbl = tk.Label(self.merResultFrm, text="MER: -1")
        self.merResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))


        self.wilResultFrm = tk.Frame(self, width=360, height=30)
        self.wilResultFrm.grid_propagate(0)
        self.wilResultFrm.grid(row=2, column=0, sticky="w", padx=(10,0), pady=(20,0))

        self.wilResultLbl = tk.Label(self.wilResultFrm, text="WIL: -1")
        self.wilResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))


        self.jwdResultFrm = tk.Frame(self, width=360, height=30)
        self.jwdResultFrm.grid_propagate(0)
        self.jwdResultFrm.grid(row=2, column=1, sticky="w", padx=(0,0), pady=(20,0))

        self.jwdResultLbl = tk.Label(self.jwdResultFrm, text="JWD: -1")
        self.jwdResultLbl.grid(row=0, column=0, sticky="w", padx=(0,0), pady=(4,0))


        exportResultAsExcelBtn = tk.Button(self, text="Ergebnisse Exportieren", command=lambda : print("Export"))
        exportResultAsExcelBtn.grid(row=2, column=2, sticky="w", padx=(0,0), pady=(15,0))

        closeAppBtn = tk.Button(self, text="Fertigstellen", command=lambda : self.closeApplication())
        closeAppBtn.grid(row=3, column=0, sticky="w", padx=(10,0), pady=(60,0))
    
        self.guiService = guiService

    def initializePage(self):
        pass
    
    def setResultsDefaultVaules(self):
        self.werResultLbl["text"] = f"WER: -1"
        self.cerResultLbl["text"] = f"CER: -1"
        self.merResultLbl["text"] = f"MER: -1"
        self.wilResultLbl["text"] = f"WIL: -1"
        self.jwdResultLbl["text"] = f"Jaro: -1"

    def displayResults(self):
        pass

    def closeApplication(self):
        self.guiService.destroy()

