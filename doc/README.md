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

La première étape du traitement peut être lancée via le code source excécutable, ou par le code de l'interface graphique. En entrée, un fichier de mesure SSPFM datacube est choisi. Les données sont alors extraites, tout comme les données contenues dans la fiche de mesure. Le fichier va être traité en fonction des paramètres, et l'ensemble des figures va être affiché. Ensuite, chaque fichier de mesure du dossier d'entrée va être traité automatiquement, sans affichage des figures. Les données sont converties sous forme de nanoloops et enregistrées.

Pour en savoir plus sur le path management de cette étape, lire la section de la documentation en question (File management/Output files/First step of data analysis).

### Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_first_step.PNG> <br>
</p>

### Segment

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

#### Parameters

### Hysteresis clustering (K-Means)

#### Parameters

<p align="justify" width="100%">
Two tools deviate from this path management:
&#8226 File Management: In the initial phase, the algorithm ingests the 'txt_best_loops' directory along with the 'txt_ferro_meas' directory.
&#8226 Clusters: For each measurement (On Field, Off Field, and coupled), the user specifies the number of clusters.
&#8226 Save and Plot Parameters: Pertaining to the management of display and the preservation of outcomes.
</p>

#### Extraction 

<p align="justify" width="100%">
The entirety of data stemming from the finest hysteresis loops, both in the 'On Field' and 'Off Field' modes, is meticulously extracted from the files residing within the 'txt_best_loops' directory.
Vertical offset measurements in the 'Off Field' mode and the dimensions of the mappings are scrupulously drawn from the files within the 'txt_ferro_meas' directory.
The coupled measurements are subsequently generated through the process of differential analysis of 'On Field' and 'Off Field' measurements, with the flexibility to incorporate the vertical offset in the 'Off Field' mode, a component influenced by the sample's surface contact potential.
</p>

#### Treatment

<p align="justify" width="100%">
For each of the modes (On Field, Off Field, and coupled), and for each of the hysteresis associated with each data point, a cluster is diligently assigned using the K-Means methodology. To accomplish this, we import the KMeans function from sklearn.cluster. A reference cluster is established, identified as the one encompassing the maximum number of data points. The index assigned to the other clusters is then computed as the distance between their centroid and that of the reference cluster, respectively. Subsequently, an average hysteresis for each cluster is computed.
</p>

#### Figures

<p align="center" width="100%">
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_all_hyst.PNG>
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_mean_hyst.PNG>
    <img align="center" width="19%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_clustering_carto.PNG>
</p>

<p align="justify" width="100%">
For each mode (On Field, Off Field, and coupled), three figures are meticulously generated, each containing:
&#8226 The complete array of hysteresis loops from all datasets, distinguished by colors assigned based on their cluster index.
&#8226 The average hysteresis loops for each cluster, distinguished by colors assigned according to their cluster index.
&#8226 A spatial cartography displaying the assigned clusters.
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

