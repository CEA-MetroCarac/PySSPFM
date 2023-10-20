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
For a deeper understanding of the path management in this phase, please refer to the relevant section in the documentation (File Management/Output Files/First Step of Data Analysis).
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
Calibration is indispensable for obtaining quantitative measurements. In the measurement data sheet, values can be provided to quantify the measured amplitude, including tip sensitivity (nm/V) and spring constant (N/m), which can be obtained from the manufacturer or through pre-measurement calibration. Additionally, a pre-measurement calibration can be used to determine the phase offset. All amplitude and phase values are calibrated with the result in the script.  
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
Once the segmentation process is completed, each segment is generated. When the <code>Segment</code> object is initialized, it generates some of its attributes, including arrays of PFM amplitude and phase measurements, as well as frequency (used in sweep mode in resonance) and time bounded by the start and end indices of the segment. These arrays are optionally trimmed at the beginning and end based on the <code>cut_seg</code> parameter. Noise in the amplitude and phase measurements is potentially reduced by a mean filter, which can be enabled (<code>filter</code>) and is defined by its order (<code>filter_ord</code>). The segment is then processed according to the <code>mode</code> chosen by the user:
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
Parameters such as amplitude $A$, quality factor $Q$, and the center of the peak (corresponding to the resonance frequency $f0$) can be extracted. Background by adding a constant in the fit and therefore can be removed from the measurement to improve accuracy.
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

<p align="justify" width="100%">
Once all the measurements are extracted per segment, phase and amplitude nanoloops as a function of polarization voltage can be created and saved.
</p>

## Nanoloop

### Post-measurement phase calibration

<p align="justify" width="100%">
An angular histogram is constructed from the complete set of phase values within the file. In the case of Vertical PFM measurements, it's common to observe two peaks separated by approximately 180°. These two peaks can either be fitted using a <code>Gaussian</code> model for improved precision or their maxima can be directly extracted for enhanced robustness and efficiency. The setting </code>histo_phase_method</code> allows for the selection of either of these methods. In the event of a fitting failure, the maximum method is applied. The phase difference and the positions of these two peaks are then extracted. During PFM measurements, a phase offset is typically present, and phase inversion can occur. Therefore, it's imperative to identify both peaks within the histogram and assign them target phase values.
</p>

INSERER LA FIGURE

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

INSERER QUATRES HYSTERESIS OFF FIELD

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

INSERER QUATRES HYSTERESIS ON FIELD

<p align="justify" width="100%">
It is worth noting that in some cases of On-Field measurements, where the electrostatic and ferroelectric components are closely related, multiple phase transitions may occur during the cycle.
</p>

INSERER HYSTERESIS CAS PARTICULIER

Concrètement, dans l'application PySSPFM, l'utilisateur peut attriibuer la valeur de phase forward et reverse qu'il souhaite à partir des paramètres pha_fwd et pha_rev. Il doit identifier s'il se trouve dans le cas d'une composante électrostatique majoritaire ou non en On Field à travers le paramètre main_electrostatic. Il peut choisir ou non d'attribuer le signe qu'il souhaite à la pente de la composante électrstatqiue. Il renseigne dans la fiche de mesure le signe du coefficient piézoélectrique du matériau. Grâce aux paramètres renseignés et au protocole de calibration, une valeur de phase peut être attribuée aux deux pics de l'histogramme. 

Une inversion de phase éventuelle peut être détectée grâce à l'étude de la variation de la phase moyenne en fonction de la tension de polarisation. Si la variation théorique et mesurée sont inversée, une inversion de phase a eu lieu, et cette dernière est corrigée.
INSERER LA FIGURE

A la suite de la calibration et de l'identification de la position des deux pics sur l'histogramme et de la différence de phase, la phase peut être corrigée avec 4 différents protocoles :
- raw_phase : la phase brute est conservée et aucun traitement n'est appliqué (peut être utilisée dans le cas d'une calibration de phase pré mesure)
- offset : un offset de phase est déterminé par la calibration, la différence de phase reste entre les deux pics reste inchangé (traitement permettant le rester le plus fidèle à la mesure initiale).
- affine : une relation affine est appliquée à l'ensemble des valeurs de phase de telle sorte à ajuster la différence de phase à 180°.
- up and down : un threshold est déterminé (entre les deux pics) et chaque valeur de phase se voit attribuer la valeur cible pha_fwd ou pha_rev en fonction de sa position par rapport au threshold et de la calibration

### MultiLoop

<p align="justify" width="100%">
Pour chaque fichier de mesure, il est possible d'acquérir plusieurs courbe nanoloop, de telle sorte à étudier la répétabilité des mesures et à réduire le bruit des mesures (en effectuant la moyenne de l'ensemble des nanoloops du fichier). Un objet MultiLoop est alors créé. Ce dernier est initialisé avec des tableaux de sous tableaux (nombre de sous tableaux correspondant au nombre de loop) de mesures correspondantes : tension de polarisation, valeur d'amplitude et de phase extraites. Sont également rensignés un tableau de tension de lecture (dont les valeurs correspondent à chacune des nanoloop), un dictionnaire des réslultats de la calibration de phase. et le mode de mesure (On ou Off Field).
</p>

<p align="justify" width="100%">
Afin de permettre une meilleure visualition des données :
- Des marqueurs (au début et à la fin de la mesure, ainsi qu'aux extremums des tensions de polarisation) sont déterminés automatioquement en fonction du signal en tension de polarisation.
- Les branches de chaque nanoloop sont divisées en deux : celles de droite (en rouge) et celle de gauche (en bleu).
Les valeurs de phase sont alors modifiées en fonction du dictionnaire de calibration de phase.
</p>

INSERER LES MULTILOOPS EN AMPLITUDE ET EN PHASE

<p align="justify" width="100%">
Enfin, en fonction des loop en amplitude et en phase, les loop en piezoreponse sont crées.
</p>

INSERER LES MULTILOOPS PIEZORESPONSE

### MeanLoop

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

