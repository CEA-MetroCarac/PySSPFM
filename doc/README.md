# PySSPFM Documentation

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/logoPySSPFM_white.PNG> <br>
</p>

## Introduction

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20worflow.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

<p align="justify" width="100%">
Following the SSPFM measurement, one or more SSPFM files are generated. A measurement form should be completed by the user (template for: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a>, <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>). 
The PySSPFM application then proceeds with two stages of measurement processing. In the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/seg_to_loop_s1.py">first step</a> of data analysis, amplitude and phase measurements are extracted and calibrated for each segment and nanoloops are determined. The <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/hyst_to_map_s2.py">second step</a> creates the piezoresponse hysteresis loop, and extracts piezoelectric and ferroelectric properties using an algorithm based on the <a href="https://pypi.org/project/lmfit/">lmfit</a> library. Various artifact decorrelation protocols improve measurement accuracy. Then, SSPFM mapping can be performed. A <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a> is provided including:
</p>

* [`Machine learning (K-Means)`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py)
* [`Phase separation`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_loop.py)
* [`Mapping cross-correlation`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py)
* [`SPM file converter`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py)
* `Viewers`
* `...`


## GUI

<p align="justify" width="100%"> 
The graphical user interface <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">codes</a> have been crafted using the <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a> library. The <a href="https://pypi.org/project/Pillow">PIL library</a> is employed to open and display the application's logo and icon on the graphical interfaces.
</p>

### Main window

<p align="center" width="100%">
    <img align="center" width="15%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20main%20GUI.PNG> <br>
</p>

<p align="justify" width="100%">
The graphical user interface of the main window constitutes the menu of the PySSPFM application. It can be launched directly from the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/main.py">interface code</a> or from the PySSPFM.exe file. It encompasses an array of buttons, each corresponding to an executable script. A secondary window is subsequently opened for the selected script. The interface can be closed either using the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Exit%20Button.PNG" width="60"> button in the bottom or the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Close%20Button.PNG" width="20"> button in the upper right corner.
</p>

### Secondary window

<p align="justify" width="100%">
The graphical user interface of the secondary window is specific to each of the respective executable Python scripts, constituting their dedicated menu. It can be initiated directly from the code of the respective interface or from the main menu. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/File%20Management%20Section.PNG> <br>
</p>

<p align="justify" width="100%">
In most instances, they encompass a primary file management section to select the input and output file paths, with a <code>Browse</code> or <code>Select</code> button to interactively choose the path in the file explorer. In the majority of cases, once the input path is selected, the other paths are automatically populated based on the default path management. However, all the paths can be modified.
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/User%20Parameters%20Section.PNG> <br>
</p>

<p align="justify" width="100%">
Following this, sections are allocated to parameters relevant to the processing step. Depending on the variable type, the parameter can be entered in a field, via a check button, a gauge, etc. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Tooltip.png> <br>
</p>

<p align="justify" width="100%">
Users are guided through tooltips when hovering the mouse over the button. The parameter name, a brief and overall description, along with its possible values and activation conditions, are provided.
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Plot%20and%20save%20section.PNG> <br>
</p>

<p align="justify" width="100%">
Lastly, in most cases, a final section allows the user to choose whether to display the processing results in the console: <code>verbose</code>, show the figures on the screen: <code>show plots</code>, or save them: <code>save analysis</code>. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Start%20and%20Exit%20section.PNG> <br>
</p>

<p align="justify" width="100%">
The processing can be executed with the <code>Start</code> button, and the interface also features an <code>Exit</code> button
</p>

## File management

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20File%20Management.PNG> <br>
    <em>PySSPFM file management</em>
</p>

### Input files

#### SSPFM measurement files

<p align="justify" width="100%">
The input processed SSPFM datacube files can be in the form of spreadsheets (columns of value lists for each measurement) with following extensions:
</p>

* `.txt`
* `.csv`
* `.xlsx`

<p align="justify" width="100%">
Or directly in the format of a Bruker SSPFM file with the extension:
</p>

* `.spm` (Bruker)

<p align="justify" width="100%">
SSPFM files from other manufacturers are not supported. It is advisable to extract the measurements from them and place them into a spreadsheet. The header dimensions, the column separator in the spreadsheet files to be extracted, and the measurements to be extracted are customizable. In the current version, deflection, polarization voltage, PFM amplitude and phase are plotted and treated, but the code can be adapted to further parameters measured. A converter from spm files to spreadsheets is also available.
</p>

#### Measurement sheet

<p align="justify" width="100%">
Prior to conducting the SSPFM measurement, the user must complete a measurement form. Templates are available for both the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a> and <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>) modes. This measurement form serves to guide the user in carrying out the SSPFM measurements and to maintain a record of critical measurement parameters. It also automatically generates certain measurement information based on the provided parameters, such as total measurement time, tip-induced pressure, lock-in amplifier settings, quality factor, and resonance settling time. Furthermore, completing the form is a mandatory prerequisite for the subsequent measurement processing. The parameters to be employed for measurement processing include grid dimensions, calibration coefficients, sign of piezoelectric coeffcient, sinusoidal voltage magnitude, voltage application direction, and SSPFM polarization signal parameters.
</p>

#### Extraction

L'ensemble des fichiers de mesure ainsi que la feuille de mesure doivent être placés dans le même dossier. Les données contenues dans ces deux types de fichiers sont alors extraites grace au fichier <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/raw_extraction.py">utils/raw_extraction</a>. Pour des fichiers d'extension spm (Bruker), le script d'extraction se base sur un deuxième fichier: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_reader.py">utils/datacube_reader</a> qui utilise l'objet DataExtraction avec la librairie nanoscope. Cependant, la librairie nanoscope ne suffit pas à elle seule à extraire les données contenues dans le fichier: cette dernière demande l'utilisation de fichiers DLL installés avec le logiciel Nanoscope Analysis (Bruker). Dans le cas ou les fichiers DLL ne sont pas présent, l'objet NanoscopeError a été créé pour géré l'erreur.

### Output files

#### First step of data analysis

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_First_Step.PNG> <br>
</p>

A la suite de la première étape de traitement, par défaut, un nouveau dossier est créé à la même racine que le dossier des données d'entrée, avec la nomenclature :
'nom_du_fichier_initial'_'aaaa-mm-dd-HHh-MMm'_out_'type_de_traitement'. Ce dernier contient lui même deux sous dossiers results et txt_loops.

* Le premier contient:
** Un fichier texte (par défaut saving_parameters.txt) de sauvegarde de l'ensemble des paramètres de mesures initialement contenues dans la fiche de mesure, ainsi que les paramètres et des informations sur la première étape du traitement de mesure réalisé. Il est génégé par le script: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/file.py">utils/seg_to_loop/file</a>.
** Un dossier figs contenant l'ensemble des figures générées lors de la première étape: à savoir différentes représentations graphiques des données bruts gérées par les scripts <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/plot.py">utils/seg_to_loop/plot</a>, les histogramme de phase permettant à la calibration gérées par les scripts <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase</a> et les nanoloops en phase, amplitude et piezoresponse gérées par les scripts <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot</a>.

* Le dossier txt_loops contient les données traitées à la suite de la première étape de traitement sous forme de nanoloop en amplitude et en phase en fonction de la tension de polarization, aussi bien en Off et On Field, et ce pour chaque fichier de mesure. Ce dernier est généré grâce au script contenus dans <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file</a>

#### Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_Second_Step.PNG> <br>
</p>

A la suite de la deuxième étape du traitement, le dossier de traitement est complété:
* Le dossier results contient désormais:
** Un fichier texte (par défaut saving_parameters.txt) complété par les paramètres et des informations sur la deuxième étape du traitement de mesure réalisée. Cette étape est réalisé par le script <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/file.py">utils/hyst_to_map/file</a>.
** Le dossier figs avec les figures générées lors de la deuxième étape de traitement : à savoir les hystérésis off et on field avec le fit et l'extraction des paramètres correspondant ainsi que l'extraction par plusieurs protocoles de la composante liées aux artefacts de mesure. Cette étape est réalisé par le script <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/plot.py">utils/hyst_to_map/plot</a>.
* Un dossier txt_ferro_meas contient l'ensemble des propriétés du matériau mesurée pour chacun des fichiers de mesure, aussi bien en On et Off Field qu'en mesurées différentielles (ou couplées) extraites lors de l'étape du fit des hystérésis et de l'analyse des artefacts, respectivement par les scripts <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/analysis.py">utils/hyst_to_map/analysis</a> et <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/electrostatic.py">utils/hyst_to_map/electrostatic</a>
* Un dossier txt_best_loops qui contient l'unique hystérésis par mode (en On et Off Field ainsi qu'en mesures couplées) par fichier de mesure.

#### Toolbox

## First step of data analysis

### Input file

### Parameters

### Segment

### Calibration

### Nanoloop

### File management

## Second step of data analysis

### Input file

### Parameters

### Hysteresis

### Artifact decoupling

### File management

## SSPFM mapping

## Toolbox

### Viewers

### Hysteresis clustering (K-Means)

### Mean loop

### 2D cross correlation

### Pixel extremum

### SPM converter

## Overall settings

