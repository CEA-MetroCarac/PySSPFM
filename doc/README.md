# PySSPFM Documentation

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/logoPySSPFM_white.PNG> <br>
</p>

## Overview

### Workflow

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20worflow.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

<p align="justify" width="100%">
Following the SSPFM measurement, one or more SSPFM files are generated. A measurement form should be completed by the user (template for: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a>, <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>). 
The PySSPFM application then proceeds with two stages of measurement processing. In the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/seg_to_loop_s1.py">first step</a> of data analysis, amplitude and phase measurements are extracted and calibrated for each segment and nanoloops are determined. The <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/hyst_to_map_s2.py">second step</a> creates the piezoresponse hysteresis loop, and extracts piezoelectric and ferroelectric properties using an algorithm based on the <a href="https://pypi.org/project/lmfit/">lmfit</a> library. Various artifact decorrelation protocols improve measurement accuracy. Then, <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">SSPFM mapping</a> can be performed. A <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a> is provided including:
</p>

* [`Machine learning (K-Means)`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py)
* [`Phase separation`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_loop.py)
* [`Mapping cross-correlation`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py)
* [`SPM file converter`](https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py)
* `Viewers`
* `...`

### Code architecture

<p align="center" width="100%">
    <img align="center" width=50%" src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20architecture.PNG"> <br>
    <em>Simplified code architecture diagram</em>
</p>

<p align="justify" width="100%">
Here is the simplified architectural overview of the PySSPFM application's source code (path management, data extraction and storage, settings, and polarization signal management are not included in the diagram). Nevertheless, it provides a fairly accurate representation of the overall interaction between the various components of the code. <br>
&#8226 The functions within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> are quite generic and not specific to SSPFM. They exhibit relative independence from the rest of the code and serve as fundamental building blocks for the execution of all other functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/seg_to_loop">seg_to_loop</a></code> module facilitates the conversion of measurements into nanoloops. It relies on the use of both <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> module enables the creation and processing of nanoloops. It relies on the utilization of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/hyst_to_map">hyst_to_map</a></code> module is responsible for extracting material properties from nanoloops. It relies on the utilization of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The "map" module formats material properties into a map. It depends on the use of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>. <br>
&#8226 The The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/seg_to_loop_s1.py">seg_to_loop_s1</a></code> executable file performs the initial stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/seg_to_loop">seg_to_loop</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/hyst_to_map_s2.py">hyst_to_map_s2</a></code> executable file accomplishes the second stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/hyst_to_map">hyst_to_map</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code> contains a set of executable tools that enable in-depth analysis of processed measurements and call various functions contained within "data_processing" and "utils." <br>
&#8226 The graphical user interface facilitates the execution of all executables, which include the code within "data_processing" and code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code>. <br>
</p>

## GUI

<p align="justify" width="100%"> 
The graphical user interface <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">codes</a> have been crafted using the <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a> library. The <a href="https://pypi.org/project/Pillow">PIL library</a> is employed to open and display the application's logo and icon on the graphical interfaces.
</p>

### Main window

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20main%20GUI.PNG> <br>
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

<p align="justify" width="100%">
All measurement files and the measurement sheet must be placed within the same directory. The data contained in these file types are then extracted using the file <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/raw_extraction.py">utils/raw_extraction</a>. For files with the <code>.spm</code> extension (Bruker), the extraction script relies on a second file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_reader.py">utils/datacube_reader</a>, which employs the <code>DataExtraction</code> object with the <a href="https://pypi.org/project/nanoscope/">nanoscope</a> library. However, the nanoscope library alone is insufficient for data extraction, as it requires the use of DLL files installed with the Nanoscope Analysis software (Bruker). In the event that the DLL files are not present, the <code>NanoscopeError</code> object has been created to handle the error.
</p>

### Output files

<p align="justify" width="100%">
A default data processing path management is provided, but the user has the option to select their own path management.
</p>

#### First step of data analysis

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_First_Step.PNG> <br>
</p>

<p align="justify" width="100%">
Following the first processing step, by default, a new directory is created at the same root as the input data folder, with the nomenclature: <code>'initial_file_name'_'yyyy-mm-dd-HHh-MMm'_out_'processing_type'</code>. This directory itself contains two subdirectories, <code>results</code> and <code>txt_loops</code>.
    <ul>
        <li>The first one contains:</li>
            <ul>
                <li>A text file: <code>saving_parameters.txt</code>, that saves all the measurement parameters initially present in the measurement form, along with parameters and information about the first measurement processing step. It is generated by the script: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/file.py">utils/seg_to_loop/file</a>.</li>
                <li>A directory <code>figs</code> directory containing all the figures generated during the first step, including various graphical representations of the raw data managed by the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/plot.py">utils/seg_to_loop/plot</a> script, phase histograms used for calibration managed by the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase</a> script, and phase, amplitude, and piezoresponse nanoloops managed by the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot</a> scripts.</li>
            </ul>
        <li>The <code>txt_loops</code> directory contains the processed data following the first step of processing in the form of amplitude and phase nanoloops as a function of polarization voltage, both in Off and On Field modes, for each measurement file. This directory is generated using the script located in <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file</a>.</li>
    </ul>
</p>

#### Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_Second_Step.PNG> <br>
</p>

<p align="justify" width="100%">
Following the second stage of processing, the processing folder is augmented as follows:
    <ul>
        <li>The <code>results</code> folder now includes:</li>
            <ul>
                <li>The text file <code>saving_parameters.txt</code> enriched with parameters and information pertaining to the second stage of measurement processing. This stage is conducted by the script <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/file.py">utils/hyst_to_map/file</a>.</li>
                <li>The <code>figs</code> directory houses the visual representations generated during the second stage of processing, encompassing off and on-field hysteresis with fitting and parameter extraction, along with the extraction of the artifact-related component through multiple protocols. This stage is executed by the script <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/plot.py">utils/hyst_to_map/plot</a>.</li>
            </ul>
        <li>A new <code>txt_ferro_meas</code> folder contains all material properties measured for each measurement file, both in on-field and off-field conditions, as well as in differential (or coupled) measurements. These properties are extracted during the hysteresis fitting stage and artifact analysis, accomplished by the scripts <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/analysis.py">utils/hyst_to_map/analysis</a> and <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/electrostatic.py">utils/hyst_to_map/electrostatic</a>, respectively.</li>
        <li>A <code>txt_best_loops</code> directory that contains the singular hysteresis for each mode (on-field and off-field) per measurement file.</li>
     </ul>
</p>

#### Toolbox

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_Toolbox.PNG> <br>
</p>

<p align="justify" width="100%">
For each tool in the toolbox, it is possible to save the analysis conducted. A <code>toolbox</code> folder is then created within the processing directory. This folder comprises a set of subdirectories, one for each toolbox treatment, following the nomenclature: <code>'tool_used'_'yyyy-mm-dd-HHh-MMm'</code>. Each of these directories contains the figures generated during the analysis performed by the respective tool, along with a text file <code>user_params.txt</code> that maintains a record of the parameters employed for the analysis.

Two tools deviate from this path management:
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">raw_file_reader</a>: It creates a folder with the nomenclature: <code>'initial_file_name'_toolbox</code> at the same root as the input folder. This folder contains a sub-folder <code>raw_file_reader'_yyyy-mm-dd-HHh-MMm'</code>.
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">spm_converter</a>: It creates a folder with the nomenclature: <code>'initial_file_name'_datacube'_extension'</code> at the same root as the input folder, containing all the converted datacube files.
</p>

## First step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/GUI_first_step.PNG> <br>
</p>

La première étape du traitement peut être lancée via le code source excécutable, ou par le code de l'interface graphique. En entrée, un fichier de mesure SSPFM datacube est choisi. Les données sont alors extraites, tout comme les données contenues dans la fiche de mesure. Le fichier va être traité en fonction des paramètres, et un ensemble de figures va être affiché. Ensuite, chaque fichier de mesure du dossier d'entrée va être traité automatiquement, sans affichage des figures. Les données sont converties sous forme de nanoloops et enregistrées dans des fichiers textes.

Pour en savoir plus sur le path management de cette étape, lire la section de la documentation en question (File management/Output files/First step of data analysis).

### Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_first_step.PNG> <br>
</p>

### Polarization voltage

INSERER UNE IMAGE

Dans le cas ou l'acquisition de la tension de polarisation n'est pas effectuée, cette dernière peut être reconstruite à partir d'un dictionnaire de propriétés contenant respectivement pour les segments d'écriture (On Field) et de lecture (Off Field) : leur durée, leur nombre d'échantillon par segment, le nombre de segment, leur sens de variation, leur tension limite. Ces paramètres sont renseignés dans la fiche de mesure et sont ensuite utilisés lors de l'étape de traitement. Le script <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/signal_bias.py">utils/signal_bias</a> permet de générer le signal de polarization à partir de ces paramètres et vice versa. Il contient également d'autres signaux de polarisation qui peuvent être utilisés pour le développement d'autres modes.

FAIRE LE LISTING

INSERER LES DIFFERENTES IMAGES

### Segment

La mesure SSPFM est découpée en segment : un pour chaque commutation du signal de la tension de polarisation. Un segment de hold est présent en début et en fin de mesure: leur temps est INSIQUER LA FORMULE. En fonction des paramètres de signal de polarisation, le nombre de segment et la durée totale de la mesure peut être déterminée: INIDQUER LA FORMULE. On peut alors la comparer à la durée total mesuré : les deux valeurs doivent correspondre. Cette vérification peut être effectué si le pramaètre detect_bug_segments est activé.

Une fois le découpage effectué, chaque segment sont générés. L'objet segment, lorsqu'il est initialisé, génère certains de ses attribus tels que les tableaux de mesures en amplitude et phase PFM, ainsi que la fréquence (utilisé en mode sweep) et le temps délimités en fonction des index de début et de fin du segment. Puis ces tableaux sont éventuellement rognés au début et à la fin en fonction du paramètre cut_seg. Les bruit des mesures en amplitude et en phase est éventuellement réduit par un filtre de moyenne. Le segment est alors traités en fonction du mode choisi par l'utilisateur :

INSERER LES FIGURES DE CHACUN DES TROIS TRAITEMENTS

- max (utilisable pour un sweep à la résonance) : le maximum du tableau d'amplitude est extrait. L'indice correspondant permet d'extraire la valeur de la fréquence de résoancne, avec la valeur de phase. La bande passante du pic est extraite grâce à un script de , afin de déterminer le facetur de qualité. Ce traitement à l'avantage d'être rapide et robuste.
- fit (utilisable pour un sweep à la résonance) : le pic de résonance en amplitude est fité par le modèle SHO : INSERER EQUATION. Les paramètres tels que l'amplitude, le facteur de qualité et le centre du pic (correspondant à la fréquence de réosnance) peuvent être extraits. Le bruit peut être déduit de la mesure. La phase peut être extraite simplement à l'indice du centre du pic, ou bien en effetcuant un fit au voisinage restreint du pic de résoancne grâce au paramètre fit_pha selon un modèle de fonction arctengente avec ou sans switch: INSERTER EQUATION. L'ensemble de ce traitement permet de gagner en précision sur les valeurs mesurées. La robustesse du traitement peut être augmentée grâce à un algorithme de détection de pic, permettant de choisir quant à la réalisation du fit. EN DIRE PLUS. L'ensemble des fits sont réalisés avec la librairie lmfit, et des méthodes least_sq, least_square (rapidité priviégiée) ou Nelder (convergence privilégéie) peuvent être choisis.
- dfrt : la moyenne des tableaux de mesures en amplitude et en phase définisse respectivement les uniques valeurs du segment en amplitude en phase. L'incertitude sur ces deux grandeurs peut être déterminées en fonction de leur variance au sein du segment. Ce traitement est rapide, robuste et très précis.

### Calibration

### Nanoloop

## Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/GUI_second_step.PNG> <br>
</p>

### Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_second_step_1.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_second_step_2.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_second_step_3.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_second_step_4.PNG> <br>
</p>

### Hysteresis

### Artifact decoupling

### File management

## SSPFM mapping

## Toolbox

### Viewers

#### Raw file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">toolbox
/raw_file_reader</a> or through the graphical user interface: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/raw_file_reader.py">gui
/raw_file_reader</a>.
</p>

#### Loop file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/loop_file_reader.py">toolbox
/loop_file_reader</a> or through the graphical user interface: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/loop_file_reader.py">gui
/loop_file_reader</a>.
</p>

#### List map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/list_map_reader.py">toolbox
/list_map_reader</a> or through the graphical user interface: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/list_map_reader.py">gui
/list_map_reader</a>.
</p>

#### Global map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/global_map_reader.py">toolbox
/global_map_reader</a> or through the graphical user interface: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/global_map_reader.py">gui
/global_map_reader</a>.
</p>

#### Parameters

### Hysteresis clustering (K-Means)

<p align="justify" width="100%">
The script can be executed directly using the executable file: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py">toolbox
/hysteresis_clustering</a> or through the graphical user interface: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/hysteresis_clustering.py">gui
/hysteresis_clustering</a>.
</p>

#### Parameters

<p align="justify" width="100%">
&#8226 File Management: In the initial phase, the algorithm ingests the <code>txt_best_loops</code> directory along with the <code>txt_ferro_meas</code> directory. <br>
&#8226 Clusters: For each measurement (On Field, Off Field, and coupled), the user specifies the number of clusters. <br>
&#8226 Save and Plot Parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

#### Extraction 

<p align="justify" width="100%">
The entirety of data stemming from the best hysteresis loops, both in the On Field and Off Field modes, is extracted from the files residing within the <code>txt_best_loops</code> directory. <br>
Vertical offset measurements in the Off Field mode and the dimensions of the mappings are drawn from the files within the <code>txt_ferro_meas</code> directory. <br>
The coupled measurements are subsequently generated through the process of differential analysis of On Field and Off Field measurements, with the flexibility to incorporate the vertical offset in the Off Field mode, a component influenced by the sample's surface contact potential.
</p>

#### Treatment

<p align="justify" width="100%">
For each of the modes (On Field, Off Field, and coupled), and for each of the hysteresis associated with each data point, a cluster is assigned using the K-Means methodology. To accomplish this, we import the <a href="https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html">KMeans</a> function from <a href="https://scikit-learn.org/stable/modules/clustering.html#clustering">sklearn.cluster</a>. A reference cluster is established, identified as the one encompassing the maximum number of data points. The index assigned to the other clusters is then computed as the distance between their centroid and that of the reference cluster, respectively. Subsequently, an average hysteresis for each cluster is computed.
</p>

#### Figures

<p align="center" width="100%">
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_all_hyst.PNG>
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_mean_hyst.PNG>
    <img align="center" width="19%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_carto.PNG>
</p>

<p align="justify" width="100%">
For each mode (On Field, Off Field, and coupled), three figures are generated, each containing: <br>
&#8226 The complete array of hysteresis loops from all datasets, distinguished by colors assigned based on their cluster index. <br>
&#8226 The average hysteresis loops for each cluster, distinguished by colors assigned according to their cluster index. <br>
&#8226 A spatial cartography displaying the assigned clusters. <br>
</p>

### Mean loop

#### Parameters

### 2D cross correlation

#### Parameters

### Pixel extremum

#### Parameters

### SPM converter

#### Parameters

## Overall settings

### Default settings & management

