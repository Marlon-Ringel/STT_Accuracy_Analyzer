# STT Accuracy Analyzer
STT Accuracy Analyzer ist eine Anwendung zur automatischen Bestimmung der Genauigkeit von Sprache-zu-Text-Systemen. 
Dazu kann STT Accuracy Analyzer der Startbefehl eines beliebigen Sprache-zu-Text-Systems übergeben werden. 
Diesen nutzt STT Accuracy Analyzer, um unter Verwendung eines Testdatensatzes Transkripte zu generieren. 
Basierend auf diesen Transkripten und den Labels des Testdatensatzes berechnet STT Accuracy Analyzer Metriken zur Bewertung der Genauigkeit des Sprache-zu-Text-Systems.

## Voraussetzungen
Bevor STT Accuracy Analyzer ausgeführt werden kann, müssen die folgenden Voraussetzungen erfüllt sein: 

Linux basiertes Betriebssystem (Getestet unter [Ubuntu](https://wiki.ubuntu.com/Releases) 22.04.5 LTS)

[Python](https://www.python.org/) Interpreter (Getestet mit Python Version 3.10.12)

### Python Libraries
Weiter werden folgende Python Libraries benötigt:
#### [NumPy](https://numpy.org/) 
```bash
pip install numpy
```

#### [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) 
```bash
pip install openpyxl
```

#### [Jaro-Winkler](https://pypi.org/project/jaro-winkler/) 
```bash
pip install jaro-winkler
```

#### [jiwer](https://github.com/jitsi/jiwer/tree/master) 
```bash
pip install jiwer
```


### Vorbereitung des zu testenden Sprache-zu-Text-Systems
Das zu testende Sprache-zu-Text-Systeme  wird innerhalb von STT Accuracy Analyzer als Subprozess ausgeführt. STT Accuracy Analyzer übergibt dem Subprozess den Pfad einer Audiodatei über stdin, wartet, bis die Ausführung des Subprozess abgeschlossen ist und liest danach stdout. Dies ermöglicht es, Sprache-zu-Text-Systeme unabhängig von der Programmiersprache, in der diese implementiert wurden, zu testen. Dieses Vorgehen erfordert die Vorbereitung des zu testenden Sprache-zu-Text-Systems durch den Nutzer. Es muss ein Wrapper-Programm für das zu testende Sprache-zu-Text-System implementiert werden, das die folgenden Schritte ausführt:
1. Lesen des Dateipfades der zu transkribierenden Audiodatei von stdin.
2. Generieren eines Transkripts mit dem zu testenden Sprache-zu-Text-System unter Nutzung des erhaltenen Dateipfades.
3. Schreiben des generierten Transkripts nach stdout. 

Um die Implementierung des Wrapper-Programms zu vereinfachen, 
stehen im Verzeichnis „Subprocecss_Templates“ Templates für die Implementierung dieses Wrapper-Programms 
in den Programmiersprachen C++, Java, R und Python zur Verfügung.  

## Benutzung von STT Accuracy Analyzer
Sind alle Voraussetzungen erfüllt, kann STT Accuracy Analyzer wie folgt über das Terminal ausgeführt werden:
```bash
“python3 <Pfad zum Anwendungsverzeichnis>main.py”
```

### Eingabe des Startbefehls
Nachdem STT Accuracy Analyzer gestartet wurde, muss zunächst der Startbefehl für das zu testende Sprache-zu-Text-System über die grafische Benutzeroberfläche eingegeben werden. Der Startbefehl ist der Terminal-Befehl, mit dem das vorher erstellte Wrapper-Programm gestartet wird. Eine Besonderheit hierbei ist, dass dieser Befehl durch Kommas separiert werden muss, sofern er aus mehreren durch Leerzeichen getrennten Bestandteilen besteht. 

Beispielhaft könnte der Startbefehl für eine kompilierte Java-Datei mit Namen „wrapper.class“ wie folgt aussehen: 
```bash
java -cp <Pfad zur wrapper.class Datei> wrapper.class
```


Dieser Befehl müsste, um von STT Accuracy Analyzer korrekt verarbeitet zu werden, wie folgt angepasst werden. An allen Stellen, an denen Bestandteile des Befehls durch Leerzeichen getrennt wurden muss ein Komma platziert werden (dies gilt nicht für Leerzeichen innerhalb von Pfaden!!!). Der angepasste Startbefehl sähe anschließend wie folgt aus:  
```bash
java, -cp, <Pfad zur wrapper.class Datei>, wrapper.class
```

Wurde der Startbefehl eingegeben, kann der Testprozess über den „Testprozess starten“ Button ausgeführt werden.

### Einlesen eines benutzerdefinierten Testdatensatzes
STT Accuracy Analyzer bringt einen Datensatz ([Common Voice](https://commonvoice.mozilla.org/de)) zum Testen von Sprache-zu-Text-Systemen mit. 
Es besteht aber optional die Möglichkeit, einen benutzerdefinierten Testdatensatz einzulesen, der anstelle des Standardtestdatensatzes verwendet wird. 
Dazu müssen vor dem Start des Testprozesses über die grafische Benutzeroberfläche zwei Pfade angegeben werden. 
Der erste Pfad muss zu einem Verzeichnis führen, das die Audiodateien des benutzerdefinierten Testdatensatzes enthält. 
Der zweite Pfad muss zu einer TSV-Datei führen, die die Labels (korrekte Transkripte) für diese Audiodateien enthält. 
Diese TSV-Datei muss wie folgt organisiert sein: 
- Die erste Zeile enthält eine Überschrift oder ist leer. 
- Alle weiteren Zeilen enthalten jeweils den vollständigen Dateinamen einer Audiodatei (mit Dateiendung) sowie das zugehörige korrekte Transkript. 
- Der Dateiname und das Transkript sind durch einen Tabulator separiert. 
- Der Dateiname ist der erste Eintrag einer Zeile, das Transkript der zweite. 
- Jede Zeile enthält genau einen Dateinamen und genau ein Transkript. 

Als Orientierung kann sich die Datei „dataSet.tsv“, die im Anwendungsverzeichnis unter „Data/TestData/CommonVoice“ zu finden ist, angesehen werden.
Wurden die Pfade zu diesen Dateien über die grafische Benutzeroberfläche eingegeben,
wird der benutzerdefinierte Testdatensatz während des Testprozesses anstelle des Standardtestdatensatzes verwendet.

### Anzeigen und Exportieren der Testergebnisse
Nach dem Abschluss des Testprozesses können die Ergebnisse über den „Ergebnisse anzeigen“ Button angezeigt werden. 
Die Anzeige umfasst dabei die Mittelwerte der Auswertungsmetriken. 
Die detaillierten Testergebnisse wurden an diesem Punkt bereits automatisiert als Excel-Tabelle in das Anwendungsverzeichnis exportiert. 
Es besteht die Möglichkeit, die Ergebnisse über den „Ergebnisse exportieren“ Button in ein gewünschtes Verzeichnis exportieren zu lassen. 















