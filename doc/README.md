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
Here is the simplified architectural overview of the PySSPFM application's source code (path and file management, data extraction and storage, settings, and polarization signal management are not included in the diagram). Nevertheless, it provides a fairly accurate representation of the overall interaction between the various components of the code. <br>
&#8226 The functions within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> are quite generic and not specific to SSPFM. They exhibit relative independence from the rest of the code and serve as fundamental building blocks for the execution of all other functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/seg_to_loop">seg_to_loop</a></code> module facilitates the conversion of measurements into nanoloops. It relies on the use of both <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> module enables the creation and processing of nanoloops. It relies on the utilization of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/hyst_to_map">hyst_to_map</a></code> module is responsible for extracting material properties from nanoloops. It relies on the utilization of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">map</a></code> module formats material properties into a map. It depends on the use of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>. <br>
&#8226 The The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/seg_to_loop_s1.py">seg_to_loop_s1</a></code> executable file performs the initial stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/seg_to_loop">seg_to_loop</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/hyst_to_map_s2.py">hyst_to_map_s2</a></code> executable file accomplishes the second stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/hyst_to_map">hyst_to_map</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code> contains a set of executable tools that enable in-depth analysis of processed measurements and call various functions contained within <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing">data_processing</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils">utils.</a></code> <br>
&#8226 The graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">gui</a></code> facilitates the execution of all executables, which include the code within <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing">data_processing</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code>. <br>
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
All measurement files and the measurement sheet must be placed within the same directory. The data contained in these file types are then extracted using the file <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/raw_extraction.py">utils/raw_extraction</a></code>. For files with the <code>.spm</code> extension (Bruker), the extraction script relies on a second file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_reader.py">utils/datacube_reader</a></code>, which employs the <code>DataExtraction</code> object with the <a href="https://pypi.org/project/nanoscope/">nanoscope</a> library. However, the nanoscope library alone is insufficient for data extraction, as it requires the use of DLL files installed with the Nanoscope Analysis software (Bruker). In the event that the DLL files are not present, the <code>NanoscopeError</code> object has been created to handle the error.
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
                <li>A text file: <code>saving_parameters.txt</code>, that saves all the measurement parameters initially present in the measurement form, along with parameters and information about the first measurement processing step. It is generated by the script: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/file.py">utils/seg_to_loop/file</a></code>.</li>
                <li>A directory <code>figs</code> directory containing all the figures generated during the first step, including various graphical representations of the raw data managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/plot.py">utils/seg_to_loop/plot</a></code> script, phase histograms used for calibration managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase</a></code> script, and phase, amplitude, and piezoresponse nanoloops managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot</a></code> scripts.</li>
            </ul>
        <li>The <code>txt_loops</code> directory contains the processed data following the first step of processing in the form of amplitude and phase nanoloops as a function of polarization voltage, both in Off and On Field modes, for each measurement file. This directory is generated using the script located in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file</a></code>.</li>
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
                <li>The text file <code>saving_parameters.txt</code> enriched with parameters and information pertaining to the second stage of measurement processing. This stage is conducted by the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/file.py">utils/hyst_to_map/file</a></code>.</li>
                <li>The <code>figs</code> directory houses the visual representations generated during the second stage of processing, encompassing off and on-field hysteresis with fitting and parameter extraction, along with the extraction of the artifact-related component through multiple protocols. This stage is executed by the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/plot.py">utils/hyst_to_map/plot</a></code>.</li>
            </ul>
        <li>A new <code>txt_ferro_meas</code> folder contains all material properties measured for each measurement file, both in on-field and off-field conditions, as well as in differential (or coupled) measurements. These properties are extracted during the hysteresis fitting stage and artifact analysis, accomplished by the scripts <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/analysis.py">utils/hyst_to_map/analysis</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/electrostatic.py">utils/hyst_to_map/electrostatic</a></code>, respectively.</li>
        <li>A <code>txt_best_loops</code> directory that contains the singular hysteresis for each mode (on-field and off-field) per measurement file.</li>
     </ul>
</p>

#### Toolbox

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Path_Management_Toolbox.PNG> <br>
</p>

<p align="justify" width="100%">
For each tool in the toolbox, it is possible to save the analysis conducted. A <code>toolbox</code> folder is then created within the processing directory. This folder comprises a set of subdirectories, one for each toolbox treatment, following the nomenclature: <code>'tool_used'_'yyyy-mm-dd-HHh-MMm'</code>. Each of these directories contains the figures generated during the analysis performed by the respective tool, along with a text file <code>user_params.txt</code> that maintains a record of the parameters employed for the analysis.
</p>

<p align="justify" width="100%">
Two tools deviate from this path management: <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">raw_file_reader</a></code>: It creates a folder with the nomenclature: <code>'initial_file_name'_toolbox</code> at the same root as the input folder. This folder contains a sub-folder <code>raw_file_reader'_yyyy-mm-dd-HHh-MMm'</code>. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">spm_converter</a></code>: It creates a folder with the nomenclature: <code>'initial_file_name'_datacube'_extension'</code> at the same root as the input folder, containing all the converted datacube files.
</p>

## First step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/GUI_first_step.PNG> <br>
</p>

<p align="justify" width="100%">
The initial step of the process may be initiated either through the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/seg_to_loop_s1.py">executable source code</a> or via the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/seg_to_loop_s1.py">graphical user interface</a>. At the outset, an SSPFM datacube measurement file is selected as input. Subsequently, the data is extracted, including the information contained within the measurement record. The file is then processed based on specified parameters, and a set of graphical representations is presented. Following this, each measurement file within the input directory is processed automatically, without graphical output. The data is transformed into nanoloops and stored in text files.
</p>

<p align="justify" width="100%">
For a deeper understanding of the file management in this phase, please refer to the relevant section in the documentation:<br>
&#8226 Input: File Management/Input Files.<br>
&#8226 Output: File Management/Output Files/First Step of Data Analysis.
</p>

### Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Parameters_first_step.PNG> <br>
</p>

### Polarization voltage

<p align="justify" width="100%">
In cases where the acquisition of polarization voltage is not conducted, it can be reconstructed from a property dictionary containing the following information for both write (On Field) and read (Off Field) segments: their duration, the number of samples per segment, the number of segments, their direction of variation, and their voltage limits. These parameters are specified in the measurement sheet and are subsequently employed during the processing step. The script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/signal_bias.py">utils/signal_bias</a></code> is responsible for generating the polarization signal based on these parameters and vice versa.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Polarization%20bias.PNG> <br>
    <em>Polarization voltage</em>
</p>

<p align="justify" width="100%">
This polarization signal is generated with these parameters: 
</p>

```
    sspfm_pars = {
        'Min volt (R) [V]': 0,
        'Max volt (R) [V]': 0,
        'Nb volt (R)': 10,
        'Mode (R)': 'Low to High',
        'Seg durat (R) [ms]': 500,
        'Seg sample (R)': 100,
        'Min volt (W) [V]': -10,
        'Max volt (W) [V]': 10,
        'Nb volt (W)': 9,
        'Mode (W)': 'Zero, up',
        'Seg durat (W) [ms]': 500,
        'Seg sample (W)': 100
    }
```

<p align="justify" width="100%">
The code also includes other polarization voltage form that can be utilized for the development of various modes:
</p>

<p align="center" width="100%">
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Increasing%20polarization%20bias.PNG>
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/dynamic%20switching%20bias.PNG> <br>
</p>
<p align="center" width="100%">*
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/ckpfm_bias_1.PNG>
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/ckpfm_bias_2.PNG> <br>
</p>
<p align="center" width="100%">
    <em>1 - Increasing polarization voltage</em> <br>
    <em>2 - Dynamic switching spectroscopy voltage</em> <br>
    <em>3 - cKPFM voltage n°1</em> <br>
    <em>4 - cKPFM voltage n°2</em> <br>
</p>

### Pre-measurement calibration

<p align="justify" width="100%">
Calibration is indispensable for obtaining quantitative measurements. In the measurement data sheet, values can be provided to quantify the measured amplitude, including tip sensitivity (nm/V) and spring constant (N/m), which can be obtained from the manufacturer or through pre-measurement calibration. Additionally, a pre-measurement calibration can be used to determine the phase offset. All amplitude and phase values are calibrated with the result in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/analysis.py">seg_to_loop/analysis</a></code>.
</p>

### Segment

<p align="justify" width="100%">
The SSPFM measurement is divided into segments, one for each polarization voltage signal switch. A hold segment is present at the beginning and end of the measurement. For the Bruker constructor mode, their duration is equal to the ratio between the ramp size (in nanometers) and the tip velocity (in nanometers per second). Depending on the polarization signal parameters, the total number of segments in the measurement can be determined: <br>
</p>
    
```
sspfm_pars = (sspfm_pars['Nb volt (W)'] - 1) * 4 * sspfm_pars['Nb volt (R)']
```

<p align="justify" width="100%">
To obtain the total duration (or total sample count) of the measurement, it suffices to multiply the total number of segments by the average of <code>sspfm_pars['Seg durat (W) [ms]']</code> and <code>sspfm_pars['Seg durat (R) [ms]']</code> (or <code>sspfm_pars['Seg sample (W)']</code> and <code>sspfm_pars['Seg sample (R)']</code>). 
One can then compare the theoretical and actual duration of the measurement: the two values should align. This verification can be performed if the <code>detect_bug_segments</code> parameter is enabled.
</p>

<p align="justify" width="100%">
Once the segmentation process is completed, each segment is generated. When the <code>Segment</code> object is initialized in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/seg_to_loop/analysis.py">seg_to_loop/analysis</a></code>, it generates some of its attributes, including arrays of PFM amplitude and phase measurements, as well as frequency (used in sweep mode in resonance) and time bounded by the start and end indices of the segment. These arrays are optionally trimmed at the beginning and end based on the <code>cut_seg</code> parameter. Noise in the amplitude and phase measurements is potentially reduced by a mean filter, which can be enabled (<code>filter</code>) and is defined by its order (<code>filter_ord</code>). The segment is then processed according to the <code>mode</code> chosen by the user:
</p>

<p align="justify" width="100%">
&#8226 <code>max</code> (usable for resonance sweep): the maximum value from the amplitude array is extracted. The corresponding index is used to extract the resonance frequency value along with the phase value. The bandwidth of the peak is determined using a function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/peak.py">utils/core/peak</a></code>, allowing for the calculation of the quality factor. This method is advantageous due to its speed and robustness.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/max_resonance_segment.PNG> <br>
    <em>Segment treatment in max mode</em>
</p>

<p align="justify" width="100%">
&#8226 <code>fit</code> (usable for a resonance sweep): The amplitude resonance peak with frequency $R(f)$ is fitted using the SHO (simple harmonic oscillator) model:
</p>

$$ R(f) = A * {f_0^2 \over \sqrt{f_0^2 - f^2)^2 + (f * f_0 / Q)^2}} $$

<p align="justify" width="100%">
Parameters such as amplitude $A$, quality factor $Q$, and the center of the peak (corresponding to the resonance frequency $f_0$) can be extracted. Background by adding a constant in the fit and therefore can be removed from the measurement to improve accuracy.
</p>

<p align="justify" width="100%">
The phase $\phi$ can be extracted simply at the index of the resonance frequency $f0$ or by performing a fit in the narrow vicinity of the resonance peak using the <code>fit_pha</code> parameter with an arctangent function model, with or without a switch:
</p>

$$ \phi(f) = arctan({f * f_0 \over Q * (f_0^2 - f^2)}) $$

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/resonance_peak_segment.png> <br>
    <em>Segment treatment in fit mode</em>
</p>

<p align="justify" width="100%">
This entire process enhances the precision of the measured values. The robustness of the treatment can be increased with a peak detection algorithm (activated with <code>detect_peak</code> and with order of <code>filter_ord</code>), allowing a choice regarding whether to perform the fit. All fits are conducted using the <a href="https://pypi.org/project/lmfit/">lmfit</a> library, and methods like <code>least_sq</code>, <code>least_square</code> (prioritizing speed), or <code>nelder</code> (prioritizing convergence) can be selected.
</p>

<p align="justify" width="100%">
&#8226 <code>dfrt</code> : The average of the arrays of measurements in amplitude and phase maintained at resonance through the use of dfrt, defines the unique values of the segment in amplitude and phase, respectively. The uncertainty in these two quantities can be determined based on their variance within the segment. This process is swift, robust, and highly precise.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/dfrt_segment.PNG> <br>
    <em>Segment treatment in dfrt mode</em>
</p>

<p align="justify" width="100%">
All segments (in the Off Field mode) can be visualized on this map:
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/segment_map.PNG> <br>
    <em>Segment map (Off Field)</em>
</p>

## Nanoloop

<p align="justify" width="100%">
Once all the measurements are extracted per segment, phase and amplitude nanoloops as a function of polarization voltage can be created and saved. All the nanoloop script are located in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">utils/nanoloop</a></code> scripts. The script <code><a href="https://github.com/CEA MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop/theory">utils/nanoloop/theory</a></code> is designed to generate nanoloops in amplitude, phase, and piezoresponse based on the physical equations related to piezoelectric, ferroelectric, and electrostatic phenomena.
</p>

### Post-measurement phase calibration

<p align="justify" width="100%">
Post-measurement phase calibration is performed with <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase</a></code> script.
An angular histogram is constructed from the complete set of phase values within the file. In the case of Vertical PFM measurements, it's common to observe two peaks separated by approximately 180°. These two peaks can either be fitted using a <code>Gaussian</code> model for improved precision or their maxima can be directly extracted for enhanced robustness and efficiency. The setting <code>histo_phase_method</code> allows for the selection of either of these methods. In the event of a fitting failure, the maximum method is applied. The phase difference and the positions of these two peaks are then extracted. During PFM measurements, a phase offset is typically present, and phase inversion can occur. Therefore, it's imperative to identify both peaks within the histogram and assign them target phase values.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_histogram.png> <br>
</p>

<p align="justify" width="100%">
To accomplish this, taking inspiration from the publications of Neumayer et al. (INSERER LA SOURCE), a post-measurement calibration protocol has been devised. The underlying physical principles of this protocol are elaborated upon in the publication (INSERER LA SOURCE). We have tailored this protocol for integration into the PySSPFM application, considering the specific user-specific experimental conditions.
</p>

<p align="justify" width="100%">
The direction of vertical polarization (a purely ferroelectric effect) induced in the material is contingent on the applied voltage between the tip and the material's bottom electrode. Voltages greater in magnitude than the low and high coercive voltages of the hysteresis are referred to as low and high voltages, respectively. Two scenarios are then distinguished: one for the grounded tip case and the other for the grounded bottom case. The diagram below summarizes the direction of polarization concerning the applied voltage for both cases:
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_calibration_1.PNG> <br>
</p>

<p align="justify" width="100%">
One can then discern the rotational direction of the hysteresis (clockwise or counterclockwise), influenced by piezoelectric and ferroelectric effects. The correspondence between voltage and phase values (forward or reverse, meaning they induce a multiplicative coefficient of 1 or -1 in the piezoresponse calculation with amplitude) allows for the determination of the hysteresis's rotational direction. Two scenarios are also distinguished here: one for a material with a positive piezoelectric coefficient and one for a material with a negative coefficient.
</p>

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_calibration_2.PNG> <br>
</p>

<p align="justify" width="100%">
From these two initial tables, one can ascertain the subsequent table depicting the direction of hysteresis rotation, solely contingent on the experimental conditions:
</p>

<p align="center" width="100%">
    <img align="center" width="45%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_calibration_3.PNG> <br>
</p>

<p align="justify" width="100%">
Here are the various hysteresis configurations in the Off-Field mode, depending on the experimental parameters:
</p>

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/calibration_hysteresis_off_field.PNG> <br>
</p>

<p align="justify" width="100%">
In the specific scenario of On Field measurements with a predominant electrostatic component (where the electrostatic component determines the direction of hysteresis rotation), the sign of the electrostatic component's slope is contingent on the direction of the applied voltage, as established in the following table:
</p>

<p align="center" width="100%">
    <img align="center" width="35%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_calibration_4.PNG> <br>
</p>

<p align="justify" width="100%">
The voltage value can then be directly correlated with the phase according to the following table, without any alteration in the hysteresis rotation direction:
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_calibration_5.PNG> <br>
</p>

<p align="justify" width="100%">
Here are the various hysteresis configurations in the On-Field mode, depending on the experimental parameters:
</p>

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/calibration_hysteresis_on_field.PNG.PNG> <br>
</p>

<p align="justify" width="100%">
It is worth noting that in some cases of On-Field measurements, where the electrostatic and ferroelectric components are closely related, multiple phase transitions may occur during the cycle.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/problematic_case_on_field_nanoloop.PNG> <br>
    <em>Problematic case of nanoloop: same order of magnitude for both ferroelectric and electrostatic component (On Field, grounded tip, positive d33)</em>
</p>

<p align="justify" width="100%">
In the PySSPFM application, users can concretely assign the desired phase values for both forward and reverse directions using the <code>pha_fwd</code> and <code>pha_rev</code> parameters. It is essential for the user to identify whether they are dealing with a predominant electrostatic component in the On-Field mode through the <code>main_electrostatic</code> parameter. Additionally, they can opt to specify the sign for the electrostatic component's slope. The user should also provide information about the piezoelectric coefficient sign of the material in the measurement record with the parameter <code>locked_elec_slope</code>. With these provided parameters and the calibration protocol, phase values can be attributed to the two peaks in the histogram.
</p>

<p align="justify" width="100%">
A potential phase inversion can be detected by examining the variation in the mean phase concerning the polarization voltage. If the theoretical and measured variations are opposite, a phase inversion has occurred, and it is subsequently corrected.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_variation_with_voltage.png> <br>
    <em>Detection of phase inversion with phase variation with voltage</em>
</p>

<p align="justify" width="100%">
Following the calibration process and the identification of the positions of the two peaks on the histogram, as well as the phase difference, phase correction can be achieved through four distinct protocols:<br>
&#8226 <code>raw_phase</code>: The raw phase is retained, and no processing is applied (suitable for use in pre-measurement phase calibration).<br>
&#8226 <code>offset</code>: A phase offset is determined through calibration, and the phase difference between the two peaks remains unchanged (a treatment method that aims to preserve the initial measurement as faithfully as possible).<br>
&#8226 <code>affine</code>: An affine relationship is applied to all phase values, adjusting the phase difference to 180°.<br>
&#8226 <code>up and down</code>: A threshold is established between the two peaks, and each phase value is assigned the target value, <code>pha_fwd</code> or <code>pha_rev</code>, based on its position relative to the threshold and the calibration process.
</p>

### MultiLoop

<p align="justify" width="100%">
For each measurement file, the acquisition of multiple nanoloop curves is possible, enabling the study of measurement repeatability and the reduction of measurement noise (by averaging all nanoloops within the file). This process involves the creation of a <code>MultiLoop</code> object with the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis</a></code> script, initialized with arrays of sub-arrays (the number of sub-arrays corresponding to the number of loops). These sub-arrays contain measurements such as polarization voltage, extracted amplitude, and phase values. Additionally, a voltage reading array is provided (with values corresponding to each nanoloop), a dictionary of phase calibration results, and the measurement mode (On or Off Field).
</p>

<p align="justify" width="100%">
To facilitate a more comprehensive data visualization:<br>
&#8226 Markers (at the beginning and end of the measurement, as well as at the extremities of the polarization voltages) are automatically determined based on the polarization voltage signal.<br>
&#8226 The branches of each nanoloop are divided into two categories: those on the right (in red) and those on the left (in blue).<br>
Phase values are then adjusted according to the phase calibration dictionary.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_amplitude.PNG> <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_phase.PNG> <br>
</p>

<p align="justify" width="100%">
Subsequently, based on the amplitude and phase loops, piezoresponse loops are generated. The user selects the function for calculating the piezoresponse with the parameter <code>pha_func</code>: $PR=R*func_{pha}(\phi)$. For phase values such as <code>pha_rev</code>=-90° and <code>pha_fwd</code>=90°, the chosen function should be <code>np.sin()</code>, whereas for phase values like <code>pha_rev</code>=180° and <code>pha_fwd</code>=0°, the selected function should be <code>np.cos()</code>.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_piezoresponse.PNG> <br>
</p>

### MeanLoop

<p align="justify" width="100%">
The <code>MeanLoop</code> is defined within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis</a></code> script. It is initialized with a <code>MultiLoop</code> object, and optionally, a phase calibration dictionary. This object facilitates the averaging of all loops within the <code>MultiLoop</code>, encompassing both amplitude, phase, and piezoresponse, except for the initial loop, which differs due to the sample's pre-polarized state at the beginning of the measurement. If a phase calibration dictionary is provided, the phase component of the MeanLoop is processed accordingly.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_amplitude.PNG> <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_phase.PNG> <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_piezoresponse.PNG> <br>
</p>

## Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/GUI_second_step.PNG> <br>
</p>

<p align="justify" width="100%">
The second step of the process may be initiated either through the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/hyst_to_map_s2.py">executable source code</a> or via the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/hyst_to_map_s2.py">graphical user interface</a>. 
</p>

<p align="justify" width="100%">
As an initial step, the <code>txt_loops</code> folder obtained is selected. The entirety of the files within it is arranged using the <code>generate_file_paths</code> function found in the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/file.py">utils/hyst_to_map/file</a></code> script. Subsequently, data extraction is carried out for each file, employing the <code>extract_loop</code> function from the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file">utils/nanoloop/file</a></code>. The measurement and processing parameters from the <code>result/parameters.txt</code> file are also read and extracted using the <code>read_plot_parameters</code> function within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/file.py">utils/hyst_to_map/file</a></code>.
</p>

<p align="justify" width="100%">
Figures resulting from the processing of the first file are generated. Subsequently, each of the files is automatically analyzed without displaying the figures. For each mode (On Field, Off Field, and coupled), a hysteresis loop is selected and associated with each pixel, and a set of ferroelectric piezo properties is extracted. Other properties are obtained through the analysis of measurement artifacts. The entirety of these properties contributes to the creation of SSPFM mappings.
</p>

<p align="justify" width="100%">
For a deeper understanding of the file management in this phase, please refer to the relevant section in the documentation:<br>
&#8226 File Management/Output Files/Second Step of Data Analysis.
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

### Best loop

<p align="justify" width="100%">
The nanoloops data is extracted from the files within the corresponding <code>txt_loops</code> directory, and a <code>MultiLoop</code> object is instantiated for each file. Subsequently, the amplitude and phase data are divided by the quality factor, calibrated ex-situ, and the amplitude and phase values at the first measurement point are extracted. These form two of the mapped piezo-ferroelectric properties, corresponding to the electrical polarization of the pristine state of the film.
</p>

<p align="justify" width="100%">
There are three distinct measurement processing modes, each involving the extraction of a 'best loop' using the <code>find_best_loop</code> function from the <code><a href=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/hyst_to_map/analysis.py">utils/hyst_to_map/analysis</a></code> script: <br>
&#8226 <code>'multi_loop'</code>: Measurements are conducted in Off Field, and various reading voltage values are applied. This mode corresponds to the cKPFM mode introduced by N. Balke and his colleagues (INSERT REFERENCE). All loops are fitted using the <code>Hysteresis</code> object, and the best loop is the one that minimizes the vertical offset associated with the electrostatic component in Off Field. <br>
&#8226 <code>'mean_loop'</code>: Measurements are conducted in Off Field with a single reading voltage value, often set at 0 volts. The best loop is the average of all the loops, determined through the creation of the <code>MeanLoop</code> object. <br>
&#8226 <code>'on_field'</code>: Measurements are conducted in On Field. The best loop, in this case, is the average of all the loops, determined through the creation of the <code>MeanLoop</code> object.
</p>

### Hysteresis and properties

<p align="justify" width="100%">
The script <code><a href=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/curve_hysteresis.py>utils/core/curve_hysteresis</a></code> introduces and processes a new object, the <code>Hysteresis</code>. This object is initialized with the variable <code>model</code>, which defines the algebraic function for each of its two branches: <br>
&#8226 <code>'sigmoid'</code>: $y(x) = a * ({1 \over 1. + exp(-coef * (x - x_0))} - 0.5)$ <br>
&#8226 <code>'arctan'</code>: $y(x) = a * arctan(coef * (x - x_0)$ <br>
A boolean variable <code>asymmetric</code> determines whether to assign different dilation coefficients to the two branches. An affine component is added to this model.
</p>

<p align="justify" width="100%">
Une initialisation des paramètres du fit est alors effectuée:
    <ul>
        <li>Intervale de définition:</li>
            <ul>
                <li>Les coefficients de diollatiuon des branches sont positifs.</li>
                <li>Le signe de l'amplitude de l'hystérésis est défini positivement pour une boucle <code>counterclockwise</code> et positivement pour une boucle <code>clockwise</code>.</li>
                <li>Les tensions coercitives des deux branches sont bornées dans l'intervalle de mesure de tension de polarisation.</li>
                <li>L'offset de la composante affine est bornée dans l'intervalle de mesure de piezoresponse.</li>
                <li>La pente:</li>
                    <ul>
                        <li>Pour <code>analysis_mode == 'on_f_loop'</code>: Dans le cas ou <code>locked_elec_slope = 'positive'</code>, la pente est définie positivement, et vice versa, si <code>locked_elec_slope = 'negative'</code>, la pente est définie négativement. Si <code>locked_elec_slope is None</code>, la pente est définie selon le sens d'application de la tension : <code>grounded_tip is True</code> -> <code>'negative'</code>, <code>grounded_tip is False</code> -> <code>'positive'</code>.</li>
                        <li>Sinon la pente est fixée à 0.</li>
                    </ul>
            </ul>
        <li>Le différentiel des deux branches, <code>diff_hyst</code>, est calculé puis filtré (par la fonction <code>filter_mean</code> du script INSERER), formant en quelque sorte un dome. Ce dernier permet d'initialiser les valeurs de paramètres de fit. Cette procédure est basée sur le stravaux de INSERER LA SOURCE.</li>
        <li>Valeur initiale:</li>
            <ul>
                <li>Les coefficients de diollatiuon des branches sont positifs.</li>
                <li>La valeur de l'amplitude de l'hystérésis est déterminé à partir du maximum de <code>diff_hyst</code>.</li>             
                <li>Les tensions coercitives des deux branches sont définies comme les absicices correpondant aux pentes minimum et maximum de <code>diff_hyst</code>.</li>
                <li>Pour <code>analysis_mode == 'on_f_loop'</code>, la pente est initialisée comme le rapport : ${max(PR)-min(PR)/overmax(tension)-min(tension)}$.</li>   
            </ul>
    </ul>
</p>

<p align="justify" width="100%">
L'hystérésis est alors fitée avec la méthode <code>fit</code>, en fonction des coordonnes des points de la best loop, et en choisissant la <code>method</code> voulue. Cette méthode repose sur la librairie lmfit et permet d'extraire les paramètres du modèle de l'hystérésis qui converge le plus vers les données expérimentales.
</p>

<p align="justify" width="100%">
Une fois le fit effectué, la méthode properties permet d'extraire les propriétés piézo-ferroélectriques de l'ghystérésis. 
L'ensemble des prorpriétés est calculé avec et sans la composante électrostatique: <br>
&#8226 L'imprint, <code>x_shift</code> est définit comme la moyenne entre les deux tensions coercitives des deux branches, tandis que la fenêtre en tension, <code>x0_wid</code> comme la différence entre ces deux valeurs. L'aire de l'hystérésis, <code>area</code>, est simplement définie comme le produit de la fenêtre en tension par l'amplitude de l'hystérésis. <br>
&#8226 Les points d'intersection des axes des des abscisses (<code>x_inters_l</code>, <code>x_inters_r</code>) et des ordonnées (<code>y_inters_l</code>, <code>y_inters_r</code>) définissent respectivement les tensions coercitives et de les piezoersponse rémanente. <br>
&#8226 Les tensions points d'inflection située par défaut à 10 et 90% de l'amplitude des branches définissent respectivement les tensions de nucléations (<code>x_infl_l</code>, <code>x_infl_r</code>) et de saturations (<code>x_sat_l</code>, <code>x_sat_r</code>). <br>
&#8226 La différence relative entre les coefficients de dilatation des branches de droite et de gauche, <code>diff_coef</code>, permet de traduire avec un scalaire le degré d'assymétrie de l'hystérésis. <br>
</p>

### Artifact decoupling

### File management

## SSPFM mapping

## Toolbox

### Viewers

#### Raw file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">toolbox/raw_file_reader</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/raw_file_reader.py">gui/raw_file_reader</a></code>.
</p>

#### Loop file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/loop_file_reader.py">toolbox/loop_file_reader</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/loop_file_reader.py">gui/loop_file_reader</a></code>.
</p>

#### List map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/list_map_reader.py">toolbox/list_map_reader</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/list_map_reader.py">gui/list_map_reader</a></code>.
</p>

#### Global map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/global_map_reader.py">toolbox/global_map_reader</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/global_map_reader.py">gui/global_map_reader</a></code>.
</p>

#### Parameters

### Hysteresis clustering (K-Means)

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py">toolbox/hysteresis_clustering</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/hysteresis_clustering.py">gui/hysteresis_clustering</a></code>.
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

