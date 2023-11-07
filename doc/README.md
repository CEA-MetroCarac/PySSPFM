# PySSPFM Documentation

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/pysspfm_white_logo.PNG> <br>
</p>

<div id="table-of-contents" style="text-align: justify;">
    <h2>Table of Contents</h2>
    <ul>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#i---overview">I) - Overview</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#i1---workflow">I.1) - Workflow</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#i2---code-architecture">I.2) - Code architecture</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#i3---examples--tests">I.3) - Examples & Tests</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#ii---gui">II) - GUI</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#ii1---main-window">II.1) - Main window</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#ii2---secondary-window">II.2) - Secondary window</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii---file-management">III) - File management</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii1---input-files">III.1) - Input files</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii1a---sspfm-measurement-files">III.1.a) - SSPFM measurement files</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii1b---measurement-sheet">III.1.b) - Measurement sheet</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii1c---extraction">III.1.c) - Extraction</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii1d---examples--tests">III.1.d) - Examples & Tests</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2---output-files">III.2) - Output files</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2a---first-step-of-data-analysis">III.2.a) - First step of data analysis</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2b---second-step-of-data-analysis">III.2.b) - Second step of data analysis</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2d---examples--tests">III.2.d) - Examples & Tests</a></li>
                    </ul>
                </li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv1---parameters">IV.1) - Parameters</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv2---polarization-voltage">IV.2) - Polarization voltage</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv3---pre-measurement-calibration">IV.3) - Pre-measurement calibration</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv4---segment">IV.4) - Segment</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v---nanoloop">V) - Nanoloop</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v1---post-measurement-phase-calibration">V.1) - Post-measurement phase calibration</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v2---multiloop">V.2) - MultiLoop</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v3---meanloop">V.3) - MeanLoop</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi1---parameters">VI.1) - Parameters</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi2---best-loop">VI.2) - Best loop</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi3---hysteresis-and-properties">VI.3) - Hysteresis and properties</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4---artifact-decoupling">VI.4) - Artifact decoupling</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4a---analysis-of-on-field-amplitude-nanoloop">VI.4.a) - Analysis of on field amplitude nanoloop</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4b---analysis-of-saturation-domain-of-on-field-piezoresponse-nanoloop">VI.4.b) - Analysis of saturation domain of on field piezoresponse nanoloop</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4c---multi-read-voltages-of-off-field-hysteresis">VI.4.c) - Multi read voltages of off field hysteresis</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4d---differential-analysis-of-on-and-off-field-hysteresis">VI.4.d) - Differential analysis of on and off field hysteresis</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4e---fit-of-both-on-and-off-field-hysteresis">VI.4.e) - Fit of both on and off field hysteresis</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi5---ckpfm">VI.5) - cKPFM</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vii---sspfm-mapping">VII) - SSPFM mapping</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vii1---mask">VII.1) - Mask</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vii2---interpolation-2d">VII.2) - Interpolation 2D</a></li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vii3---figures">VII.3) - Figures</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii-toolbox">VIII) - Toolbox</a>
            <ul>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1-viewers">VIII.1) Viewers</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1a-raw-file">VIII.1.a) Raw file</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1b-loop-file">VIII.1.b) Loop file</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1c-global-map-reader">VIII.1.c) Global map reader</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1d-list-map-reader">VIII.1.d) List map reader</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii2-hysteresis-clustering-k-means">VIII.2) Hysteresis clustering (K-Means)</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii2a-parameters">VIII.2.a) Parameters</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii2b-extraction">VIII.2.b) Extraction</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii2c-treatment">VIII.2.c) Treatment</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii2d-figures">VIII.2.d) Figures</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3-mean-hysteresis">VIII.3) Mean hysteresis</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3a-parameters">VIII.3.a) Parameters</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3b-extraction">VIII.3.b) Extraction</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3c-find-best-loop">VIII.3.c) Find best loop</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3d-mean-analysis">VIII.3.d) Mean analysis</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3e-figures">VIII.3.e) Figures</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii4-2d-cross-correlation">VIII.4) 2D cross correlation</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii4a-parameters">VIII.4.a) Parameters</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii4b-correlation-matrix">VIII.4.b) Correlation matrix</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii4c-workflow">VIII.4.c) Workflow</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii4d-figures">VIII.4.d) Figures</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii5-pixel-extremum">VIII.5) Pixel extremum</a>
                    <ul>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii5a-parameters">VIII.5.a) Parameters</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii5b-workflow">VIII.5.b) Workflow</a></li>
                        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii5c-figures">VIII.5.c) Figures</a></li>
                    </ul>
                </li>
                <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii6-spm-converter">VIII.6) SPM converter</a></li>
            </ul>
        </li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#ix-overall-settings">IX) Overall settings</a></li>
        <li><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#x-core-scripts">X) Core scripts</a></li>
    </ul>
</div>

## I) - Overview

### I.1) - Workflow

<p align="center" width="100%">
    <img align="center" width=100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/scheme_workflow_pysspfm.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

<p align="justify" width="100%">
Following the SSPFM (Switching Spectroscopy Piezoresponse Force Microscopy) <a href="#ref1">[1]</a> measurement, one or more SSPFM datacube files are generated. A measurement form should be completed by the user (template for: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a>, <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a>). 
The PySSPFM application then proceeds with two stages of measurement processing. In the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/datacube_to_nanoloop_s1.py">first step</a> of data analysis, amplitude and phase measurements are extracted and calibrated for each segment and nanoloops are determined. The <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/nanoloop_to_hyst_s2.py">second step</a> creates the piezoresponse hysteresis loop, and extracts piezoelectric and ferroelectric properties using an algorithm based on the <a href="https://pypi.org/project/lmfit/">lmfit</a> library. Various artifact decorrelation protocols improve measurement accuracy. Then, <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">SSPFM mapping</a> can be performed. A <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a> is provided including:
</p>

<p align="justify" width="100%">
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py">Machine learning (K-Means)</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_hyst.py">Phase separation</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">Mapping cross-correlation</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">SPM file converter</a> <br>
&#8226 ...
</p>

### I.2) - Code architecture

<p align="center" width="100%">
    <img align="center" width=50%" src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_pysspfm.PNG"> <br>
    <em>Simplified PySSPFM architecture diagram</em>
</p>

<p align="justify" width="100%">
Here is the simplified architectural overview of the PySSPFM application's source code (path and file management, data extraction and storage, settings, and polarization signal management are not included in the diagram). Nevertheless, it provides a fairly accurate representation of the overall interaction between the various components of the code. <br>
&#8226 The functions within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> are quite generic and not specific to SSPFM. They exhibit relative independence from the rest of the code and serve as fundamental building blocks for the execution of all other functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/datacube_to_nanoloop">datacube_to_nanoloop</a></code> module facilitates the conversion of raw datacube measurements into nanoloops. It relies on the use of both <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code> module enables the creation and processing of nanoloops. It relies on the utilization of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> functions. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop_to_hyst">nanoloop_to_hyst</a></code> module is responsible for extracting material properties from nanoloops. It relies on the utilization of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">map</a></code> module formats material properties into a map. It depends on the use of functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/datacube_to_nanoloop_s1.py">datacube_to_nanoloop_s1.py</a></code> executable file performs the initial stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/datacube_to_nanoloop">datacube_to_nanoloop</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/nanoloop_to_hyst_s2.py">nanoloop_to_hyst_s2.py</a></code> executable file accomplishes the second stage of SSPFM measurements processing. It assembles and relies upon functions from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop_to_hyst">nanoloop_to_hyst</a></code>, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">nanoloop</a></code>. <br>
&#8226 The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code> contains a set of executable tools that enable in-depth analysis of processed measurements and call various functions contained within <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing">data_processing</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils">utils</a></code>. <br>
&#8226 The graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">gui</a></code> facilitates the execution of all executables, which include the code within <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing">data_processing</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">toolbox</a></code>. <br>
</p>

### I.3) - Examples & Tests

<p align="justify" width="100%">
<code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples">Examples</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests">tests</a></code> are readily available for nearly all functions within the PySSPFM application. They adhere to the same structural framework as the primary scripts. The examples serve to afford the user a tangible perspective on the practical application of the associated function through its invocation. Furthermore, the examples provide a precise insight into the operations executed by the function, often manifested in the form of graphical representations. As for the tests, they also adhere to the same framework and directly invoke the corresponding examples. They extract their results through quantified variables, which are compared against target values with <a href="https://pypi.org/project/pytest/">pytest</a> library to ensure the proper functioning of the entirety of the scripts. They also serve to identify the sections of code affected during modifications or maintenance. The entirety of the examples and tests are grounded in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in">actual SSPFM data</a></code> or data simulated through purpose-built application scripts.
</p>

## II) - GUI

<p align="justify" width="100%"> 
The <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">graphical user interface (gui) codes</a> have been crafted using the <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a> library. The <a href="https://pypi.org/project/Pillow">PIL</a> library is employed to open and display the application's logo and icon on the graphical interfaces.
</p>

### II.1) - Main window

<p align="center" width="100%">
    <img align="center" width="20%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_main.PNG> <br>
    <em>GUI: Main window</em>
</p>

<p align="justify" width="100%">
The graphical user interface of the main window constitutes the menu of the PySSPFM application. It can be launched directly from the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/main.py">gui code</a> or from the PySSPFM.exe file. It encompasses an array of buttons, each corresponding to an executable script. A secondary window is subsequently opened for the selected script. The interface can be closed either using the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_exit_button.PNG" width="60"> button in the bottom or the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_close_button.PNG" width="20"> button in the upper right corner.
</p>

### II.2) - Secondary window

<p align="justify" width="100%">
The graphical user interface of the secondary window is specific to each of the respective executable Python scripts, constituting their dedicated menu. It can be initiated directly from the code of the respective interface or from the main menu. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_file_management_section.PNG> <br>
    <em>GUI: File management section</em>
</p>

<p align="justify" width="100%">
In most instances, they encompass a primary file management section to select the input and output file paths, with a <code>Browse</code> or <code>Select</code> button to interactively choose the path in the file explorer. In the majority of cases, once the input path is selected, the other paths are automatically populated based on the default path management. However, all the paths can be modified.
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_user_parameters_section.PNG> <br>
    <em>GUI: Treatment parameter section</em>
</p>

<p align="justify" width="100%">
Following this, sections are allocated to parameters relevant to the processing step. Depending on the variable type, the parameter can be entered in a field, via a check button, a gauge, etc. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_tooltip.PNG> <br>
    <em>GUI: Tooltip</em>
</p>

<p align="justify" width="100%">
Users are guided through tooltips when hovering the mouse over the button. The parameter name, a brief and overall description, along with its possible values and activation conditions, are provided.
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_plot_save_section.PNG> <br>
    <em>GUI: Plot and save section</em>
</p>

<p align="justify" width="100%">
Lastly, in most cases, a final section allows the user to choose whether to display the processing results in the console: <code>verbose</code>, show the figures on the screen: <code>show plots</code>, or save them: <code>save analysis</code>. 
</p>

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_start_exit_section.PNG> <br>
    <em>GUI: Start and Exit buttons</em>
</p>

<p align="justify" width="100%">
The processing can be executed with the <code>Start</code> button, and the interface also features an <code>Exit</code> button.
</p>

## III) - File management

<p align="center" width="100%">
    <img align="center" width=100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/file_management_pysspfm.PNG> <br>
    <em>PySSPFM file management</em>
</p>

### III.1) - Input files

#### III.1.a) - SSPFM measurement files

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
SSPFM files from other manufacturers are not supported in this application. It is advisable to extract the measurements from them and place them into a spreadsheet. The header dimensions, the column separator in the spreadsheet files to be extracted, and the measurements to be extracted are customizable. In the current version, deflection, polarization voltage, PFM amplitude and phase are plotted and treated, but the code can be adapted to further parameters measured. A <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">converter</a> from spm files to spreadsheets is also available.
</p>

#### III.1.b) - Measurement sheet

<p align="justify" width="100%">
Prior to conducting the SSPFM measurement, the user must complete a measurement form. Templates are available for both the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20Bruker.csv">standard SSPFM</a> and <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM%20ZI%20DFRT.csv">SSPFM-DFRT</a> modes. This measurement form serves to guide the user in carrying out the SSPFM measurements and to maintain a record of critical measurement parameters. It also automatically generates certain measurement information based on the provided parameters, such as: <br>
&#8226 total measurement time <br>
&#8226 tip-induced pressure <br>
&#8226 lock-in amplifier settings <br>
&#8226 quality factor <br>
&#8226 resonance settling time <br> <br>
Furthermore, completing the form is a mandatory prerequisite for the subsequent measurement processing. The parameters to be employed for measurement processing include: <br>
&#8226 grid dimensions <br>
&#8226 calibration coefficients <br>
&#8226 sign of piezoelectric coeffcient <br>
&#8226 sinusoidal voltage magnitude <br>
&#8226 voltage application direction <br>
&#8226 SSPFM polarization signal parameters <br>
</p>

#### III.1.c) - Extraction

<p align="justify" width="100%">
All measurement files and the measurement sheet must be placed within the same directory. The data contained in these file types are then extracted using the file <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/raw_extraction.py">utils/raw_extraction.py</a></code>. The functions <a href="https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html">genfromtxt</a> (from NumPy), <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html">read_csv</a> (from pandas), and <a href="https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html">read_excel</a> (from pandas) are employed, respectively, to extract data from files with extensions txt, csv, and xlsx. For files with the spm extension (Bruker), the extraction script relies on a second file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_reader.py">utils/datacube_reader.py</a></code>, which employs the <code>DataExtraction</code> object with the <a href="https://pypi.org/project/nanoscope/">nanoscope</a> library. However, the nanoscope library alone is insufficient for data extraction, as it requires the use of DLL (Dynamic Link Library) files installed with the Nanoscope Analysis software (Bruker). In the event that the DLL files are not present, the <code>NanoscopeError</code> object has been created to handle the error.
</p>

#### III.1.d) - Examples & Tests

<p align="justify" width="100%">
The <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples">examples</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests">tests</a></code> inherently rely upon input data, which may assume one of two distinct forms:

1. Authentic data stemming from SSPFM measurements conducted on a KNN (potassium sodium niobate) sample, which are located within the directory: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in">examples/data/PySSPFM_example_in</a></code>. This repository encompasses several subdirectories, specifically:
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n">KNN500n</a></code>: housing an assemblage of SSPFM datacube measurement files, bearing the spm extension (Bruker), alongside their corresponding measurement records. This serves the following purpose:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/datacube_to_nanoloop/ex_file.py">examples/utils/datacube_to_nanoloop/ex_file.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_2023-10-05-17h21m_out_dfrt">KNN500n_2023-10-05-17h21m_out_dfrt</a></code>: signifying the measurement output subsequent to the initial processing phase. This facilitates the following:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_loop_file_reader.py">examples/toolbox/ex_loop_file_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop_to_hyst/ex_file.py">examples/utils/nanoloop_to_hyst/ex_file.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_2023-10-05-17h23m_out_dfrt">KNN500n_2023-10-05-17h23m_out_dfrt</a></code>: embodying the measurement outcomes post the second phase of processing. This underpins the following endeavors:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_global_map_reader.py">examples/toolbox/ex_global_map_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_hysteresis_clustering.py">examples/toolbox/ex_hysteresis_clustering.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_list_map_reader.py">examples/toolbox/ex_list_map_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_map_correlation.py">examples/toolbox/ex_map_correlation.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_mean_hyst.py">examples/toolbox/ex_mean_hyst.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_sort_plot_pixel.py">examples/toolbox/ex_sort_plot_pixel.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_reduced">KNN500n_reduced</a></code>: constituting a diminished compilation of the SSPFM measurement, involving three Bruker spm datacube measurement files, along with their respective measurement records. This supports the following endeavors:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_raw_file_reader.py">examples/toolbox/ex_raw_file_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_spm_converter.py">examples/toolbox/ex_spm_converter.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/ex_raw_extraction.py">examples/utils/ex_raw_extraction.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_reduced_datacube_csv">KNN500n_reduced_datacube_csv</a></code>: denoting a reduced representation of the SSPFM measurement, incorporating three csv datacube SSPFM measurement files, as well as their associated measurement records. This is integral to the following:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_raw_file_reader.py">examples/toolbox/ex_raw_file_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/ex_raw_extraction.py">examples/utils/ex_raw_extraction.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_reduced_datacube_txt">KNN500n_reduced_datacube_txt</a></code>: signifying a streamlined interpretation of the SSPFM measurement, encompassing three txt datacube SSPFM measurement files, together with their pertinent measurement records. This lends support to the following:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_raw_file_reader.py">examples/toolbox/ex_raw_file_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/ex_raw_extraction.py">examples/utils/ex_raw_extraction.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data/PySSPFM_example_in/KNN500n_reduced_datacube_xlsx">KNN500n_reduced_datacube_xlsx</a></code>: representing a refined version of the SSPFM measurement, encapsulating three xlsx datacube SSPFM measurement files, in conjunction with their corresponding measurement records. This underpins the following:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/toolbox/ex_raw_file_reader.py">examples/toolbox/ex_raw_file_reader.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/ex_raw_extraction.py">examples/utils/ex_raw_extraction.py</a></code>.

2. Data crafted by dedicated scripts for this purpose:
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/gen_data.py">utils/datacube_to_nanoloop/gen_data.py</a></code> serves the function of generating an SSPFM datacube measurement, either in sweep resonance mode or dfrt mode. The ensuing examples derive their foundations from this source:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/data_processing/ex_datacube_to_nanoloop_s1.py">examples/data_processing/ex_datacube_to_nanoloop_s1.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/datacube_to_nanoloop/ex_analysis.py">examples/utils/datacube_to_nanoloop/ex_analysis.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/datacube_to_nanoloop/ex_gen_data.py">examples/utils/datacube_to_nanoloop/ex_gen_data.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/datacube_to_nanoloop/ex_plot.py">examples/utils/datacube_to_nanoloop/ex_plot.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/gen_data.py">utils/nanoloop/gen_data.py</a></code> enables the generation of nanoloops. The following examples are predicated on this foundation:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop_to_hyst/ex_electrostatic.py">examples/utils/nanoloop_to_hyst/ex_electrostatic.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop/ex_analysis.py">examples/utils/nanoloop/ex_analysis.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop/ex_file.py">examples/utils/nanoloop/ex_file.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop/ex_gen_data.py">examples/utils/nanoloop/ex_gen_data.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop/ex_phase.py">examples/utils/nanoloop/ex_phase.py</a></code>.
    - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/gen_data.py">utils/nanoloop_to_hyst/gen_data.py</a></code> is responsible for generating a nanoloop file. The ensuing examples are rooted in this source:
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/data_processing/ex_nanoloop_to_hyst_s2.py">examples/data_processing/ex_nanoloop_to_hyst_s2.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop_to_hyst/ex_analysis.py">examples/utils/nanoloop_to_hyst/ex_analysis.py</a></code>.
        - <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/examples/utils/nanoloop_to_hyst/ex_gen_data.py">examples/utils/nanoloop_to_hyst/ex_gen_data.py</a></code>.
</p>
                    
### III.2) - Output files

<p align="justify" width="100%">
A default data processing path management is provided, but the user has the option to select their own path management.
</p>

#### III.2.a) - First step of data analysis

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/file_management_first_step.PNG> <br>
    <em>File management after first step of data analysis</em>
</p>

<p align="justify" width="100%">
Following the first processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a> of the documentation), by default, a new directory is created at the same root as the input data folder, with the nomenclature: <code>'initial_file_name'_'yyyy-mm-dd-HHh-MMm'_out_'processing_type'</code>. This directory itself contains two subdirectories, <code>figs</code> and <code>nanoloops</code>, and a text file, <code>parameters.txt</code>.
    <ul>
        <li>The <code>parameters.txt</code> text file saves all the measurement parameters initially present in the measurement form, along with parameters and information about the first measurement processing step. It is generated by the function <code>save_parameters</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/file.py">utils/datacube_to_nanoloop/file.py</a></code>.</li>
        <li>The <code>figs</code> directory contains all the figures generated during the first step, including various graphical representations of the raw data and segments managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script, phase histograms used for calibration managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase.py</a></code> script, and phase, amplitude, and piezoresponse nanoloops managed by the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> scripts.</li>
        <li>The <code>nanoloops</code> directory contains the processed data following the first step of processing in the form of amplitude and phase nanoloops as a function of polarization voltage, both in off and on field modes, for each measurement file. This directory is generated using the functions <code>sort_nanoloop_data</code> and <code>save_nanoloop_file</code> of the script located in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file.py</a></code>.</li>
    </ul>
</p>

#### III.2.b) - Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/file_management_second_step.PNG> <br>
    <em>File management after second step of data analysis</em>
</p>

<p align="justify" width="100%">
Following the second stage of processing (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation), the processing folder is augmented as follows:
    <ul>
        <li>The text file <code>parameters.txt</code> enriched with parameters and information pertaining to the second stage of measurement processing. This stage is conducted by the function <code>complete_parameters</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>.</li>
        <li>The <code>figs</code> directory houses the visual representations generated during the second stage of processing, encompassing off and on field hysteresis with fitting and parameter extraction, along with the extraction of the artifact-related component through multiple protocols. This stage is executed by the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code>.</li>
        <li>A new <code>properties</code> folder contains all material properties measured for each measurement file, both in on field and off field conditions, as well as in differential (or coupled) measurements. The data is recorded using the function <code>save_properties</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>. These properties are extracted during the hysteresis fitting stage and artifact analysis, accomplished by the scripts <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code>, respectively.</li>
        <li>A <code>best_nanoloops</code> directory that contains the singular nanoloop for each mode (on field and off field) per measurement file. The data is recorded using the function <code>save_best_nanoloops</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>.</li>
     </ul>
</p>

#### III.2.c) - Toolbox

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/file_management_toolbox.PNG> <br>
    <em>File management for toolbox scripts</em>
</p>

<p align="justify" width="100%">
For each script in the toolbox, it is possible to save the analysis conducted. Using function <code>save_path_management</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/path_for_runable.py">PySSPFM/utils/path_for_runable.py</a></code>, a <code>toolbox</code> folder is then created within the processing directory. This folder comprises a set of subdirectories, one for each toolbox treatment, following the nomenclature: <code>'tool_used'_'yyyy-mm-dd-HHh-MMm'</code>. Each of these directories contains the figures generated during the analysis performed by the respective tool, along with a text file <code>user_params.txt</code> generated by the function <code>save_user_pars</code> of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/path_for_runable.py">PySSPFM/utils/path_for_runable.py</a></code> that maintains a record of the parameters employed for the analysis.
</p>

<p align="justify" width="100%">
Two tools deviate from this path management: <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">raw_file_reader.py</a></code>: It creates a folder with the nomenclature: <code>'initial_file_name'_toolbox</code> at the same root as the input folder. This folder contains a sub-folder <code>raw_file_reader'_yyyy-mm-dd-HHh-MMm'</code>. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">spm_converter.py</a></code>: It creates a folder with the nomenclature: <code>'initial_file_name'_datacube'_extension'</code> at the same root as the input folder, containing all the converted datacube files.
</p>

#### III.2.d) - Examples & Tests

<p align="justify" width="100%">
The management of paths for both the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples">examples</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests">tests</a></code> is overseen through the utilization of the <code>save_path_example</code> function within the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/path_for_runable.py">utils/path_for_runable.py</a></code>.
The majority of outcomes from the examples consist of visual representations, which are, by default, stored in the <code>PySSPFM_example_out</code> directory, located within <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples/data">examples/data</a></code>.
The results of the tests are not automatically stored, except for a few assessments where minimal or no comparisons are made with experimental results (<code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/tests/data_processing/test_datacube_to_nanoloop_s1.py">tests/data_processing/test_datacube_to_nanoloop_s1.py</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/tests/utils/nanoloop/test_theory.py">tests/utils/nanoloop/test_theory.py</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/tests/utils/map/test_map.py">tests/utils/map/test_map.py</a></code>, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/tests/data_processing/test_nanoloop_to_hyst_s2.py">tests/data_processing/test_nanoloop_to_hyst_s2.py</a></code>), as well as for <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/tests/toolbox/test_spm_converter.py">tests/toolbox/test_spm_converter.py</a></code>. These are, by default, stored in the <code>PySSPFM_data_out</code> directory, situated at the root of PySSPFM.
The <code>save_test_example</code> settings provide the option to determine whether the outcomes of examples and tests are automatically saved.
</p>

## IV) - First step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_first_step.PNG> <br>
    <em>GUI: First step of data analysis</em>
</p>

<p align="center" width="100%">
    <img align="center" width="50%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_first_step.PNG>
    <img align="center" width="35%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_first_step_single_script.PNG> <br>
    <em>Workflow: First step of data analysis (left: global, right: single script)</em>
</p>

<p align="justify" width="100%">
The initial step of the process may be initiated either through the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/datacube_to_nanoloop_s1.py">executable source code</a> or via the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/datacube_to_nanoloop_s1.py">graphical user interface</a>. At the outset, a raw SSPFM datacube measurement file is selected as input. Subsequently, the data is extracted, including the information contained within the measurement record. The file is then processed based on specified parameters, and a set of graphical representations is presented. Following this, each measurement file within the input directory is processed automatically, without graphical output. The data is transformed into nanoloops and stored in text files.
</p>

<p align="justify" width="100%">
For a deeper understanding of the file management in this phase, please refer to the relevant section in the documentation:<br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii1---input-files">III.1) - Input files</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2a---first-step-of-data-analysis">III.2.a) - First step of data analysis</a>
</p>

### IV.1) - Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/parameters_first_step.PNG> <br>
</p>

### IV.2) - Polarization voltage

<p align="justify" width="100%">
In cases where the acquisition of polarization voltage is not conducted, it can be reconstructed from a property dictionary containing the following information for both write (on field) and read (off field) segments: their duration, the number of samples per segment, the number of segments, their direction of variation, and their voltage limits. These parameters are specified in the measurement sheet and are subsequently employed during the processing step. The script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/signal_bias.py">utils/signal_bias.py</a></code> is responsible for generating the polarization signal based on these parameters and vice versa.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/bias_sspfm_polarization.PNG> <br>
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
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/bias_increasing_polarization.PNG>
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/bias_dynamic_switching.PNG> <br>
</p>
<p align="center" width="100%">*
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/bias_ckpfm_1.PNG>
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/bias_ckpfm_2.PNG> <br>
</p>
<p align="center" width="100%">
    <em>1 - Increasing polarization voltage</em> <br>
    <em>2 - Dynamic switching spectroscopy voltage</em> <br>
    <em>3 - cKPFM voltage n°1</em> <br>
    <em>4 - cKPFM voltage n°2</em> <br>
</p>

### IV.3) - Pre-measurement calibration

<p align="justify" width="100%">
Calibration is indispensable for obtaining quantitative measurements. In the measurement data sheet, values can be provided to quantify the measured amplitude, including tip sensitivity (nm/V) and spring constant (N/m), which can be obtained from the manufacturer or through pre-measurement calibration. Additionally, a pre-measurement calibration can be used to determine the phase offset. All amplitude and phase values are calibrated with the result in the scripts <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/datacube_to_nanoloop_s1.py">data_processing/datacube_to_nanoloop_s1.py</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/analysis.py">datacube_to_nanoloop/analysis.py</a></code> with the function <code>zi_calib</code>.
</p>

### IV.4) - Segment

<p align="justify" width="100%">
The SSPFM measurement is divided into segments, one for each polarization voltage signal switch. A hold segment is present at the beginning and end of the measurement. For the Bruker constructor mode, their duration is equal to the ratio between the ramp size (in nanometers) and the tip velocity (in nanometers per second). Depending on the polarization signal parameters, the total number of segments in the measurement can be determined: <br>
</p>
    
```
sspfm_pars = (sspfm_pars['Nb volt (W)'] - 1) * 4 * sspfm_pars['Nb volt (R)']
```

<p align="justify" width="100%">
To obtain the total duration (or total sample count) of the measurement, it suffices to multiply the total number of segments by the average of <code>sspfm_pars['Seg durat (W) [ms]']</code> and <code>sspfm_pars['Seg durat (R) [ms]']</code> (or <code>sspfm_pars['Seg sample (W)']</code> and <code>sspfm_pars['Seg sample (R)']</code>). 
One can then compare the theoretical and actual duration of the measurement: the two values should align. This verification can be performed if the <code>detect_bug_segments</code> setting is enabled.
</p>

<p align="justify" width="100%">
The segmentation process is performed with <code>cut_function</code> in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/analysis.py">datacube_to_nanoloop/analysis.py</a></code>, and each segment is generated. When the <code>Segment</code> object is initialized in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/analysis.py">datacube_to_nanoloop/analysis.py</a></code>, it generates some of its attributes, including arrays of PFM amplitude and phase measurements, as well as frequency (used in sweep mode in resonance) and time bounded by the start and end indices of the segment. These arrays are optionally trimmed at the beginning and end based on the <code>cut_seg</code> parameter. Noise in the amplitude and phase measurements is potentially reduced by a mean filter, which can be enabled (<code>filter</code>) and is defined by its order (<code>filter_ord</code>). The segment is then processed according to the <code>mode</code> chosen by the user:
</p>

<p align="justify" width="100%">
&#8226 <code>max</code> (usable for resonance sweep): the maximum value from the amplitude array is extracted. The corresponding index is used to extract the resonance frequency value along with the phase value. The bandwidth of the peak is determined with method <code>q_fact_max</code> using the function <code>width_peak</code> in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/peak.py">utils/core/peak.py</a></code>, allowing for the calculation of the quality factor. This method is advantageous due to its speed and robustness.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/segment_max_peak.PNG> <br>
    <em>Segment treatment in max mode (figure generated with <code>plt_seg_max</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
&#8226 <code>fit</code> (usable for a resonance sweep): The amplitude resonance peak with frequency $R(f)$ is fitted using the SHO (simple harmonic oscillator) model (<code>sho</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">utils/core/basic_func.py</a></code> script) <a href="#ref2">[2]</a>:
</p>

$$ R(f) = A * {f_0^2 \over \sqrt{f_0^2 - f^2)^2 + (f * f_0 / Q)^2}} + bckgnd $$

<p align="justify" width="100%">
Parameters such as amplitude $A$, quality factor $Q$, and the center of the peak (corresponding to the resonance frequency $f_0$) can be extracted. The background $bckgnd$ in the fit can be removed from the measurement to improve accuracy. All the peak fit process is performed in <code>peak_fit</code> method.
</p>

<p align="justify" width="100%">
The phase $\phi$ can be extracted simply at the index of the resonance frequency $f_0$ or by performing a fit (the process is performed in <code>phase_fit</code> method) in the narrow vicinity of the resonance peak using the <code>fit_pha</code> parameter with an arctangent function model (in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">utils/core/basic_func.py</a></code> script) with (<code>sho_phase_switch</code> function) or without (<code>sho_phase</code> function) a switch (detected with <code>phase_fit_analysis</code> method) <a href="#ref2">[2]</a>:
</p>

$$ \phi(f) = arctan({f * f_0 \over Q * (f_0^2 - f^2)}) + \phi_0 $$

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/segment_fit_peak.PNG> <br>
    <em>Segment treatment in fit mode (figure generated with <code>plt_seg_fit</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
This entire process enhances the precision of the measured values. The robustness of the treatment can be increased with <code>treatment_fit</code> method in which a peak detection algorithm is used (activated with <code>detect_peak</code> and with order of <code>filter_ord</code>), allowing a choice regarding whether to perform the fit.
</p>

<p align="justify" width="100%">
&#8226 <code>dfrt</code> : The average of the arrays of measurements in amplitude and phase maintained at resonance through the use of DFRT (Dual Frequency Resonance Tracking) <a href="#ref3">[3]</a>, defines the unique values of the segment in amplitude and phase, respectively. The uncertainty in these two quantities can be determined based on their variance (with <a href="https://numpy.org/doc/stable/reference/generated/numpy.var.html">var</a> function of NumPy library) within the segment. This process is swift, robust, and highly precise.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/segment_dfrt.PNG> <br>
    <em>Segment treatment in dfrt mode (figure generated with <code>plt_seg_dfrt</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
Note that SSPFM can also allow to investigate nanomechanical properties as a function of applied voltage, by analyzing the resonance frequency and quality factor of the contact resonance peak. Thus, we can gain insights into phase transitions or multi-ferroic material properties <a href="#ref4">[4]</a>.
</p>

<p align="justify" width="100%">
All segments (in the off field mode) can be visualized on this map:
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/amp_pha_segment_map.PNG> <br>
    <em>Segment map (off field) (figure generated with <code>amp_pha_map</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script)</em>
</p>

## V) - Nanoloop

<p align="justify" width="100%">
Once all the measurements are extracted per segment, phase and amplitude nanoloops as a function of polarization voltage can be created and saved. All the nanoloop script are located in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop">utils/nanoloop</a></code> scripts. The script <code><a href="https://github.com/CEA MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop/theory.py">utils/nanoloop/theory.py</a></code> is designed to generate nanoloops in amplitude, phase, and piezoresponse based on the physical equations related to piezoelectric, ferroelectric, and electrostatic phenomena.
</p>

### V.1) - Post-measurement phase calibration

<p align="justify" width="100%">
Post-measurement phase calibration is performed with <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase.py</a></code> script.
To accomplish the calibration, taking inspiration from the publications of Neumayer et al. [<a href="#ref5">5</a>, <a href="#ref6">6</a>], a post-measurement calibration protocol has been devised. We have tailored this protocol for integration into the PySSPFM application, considering the specific user-specific experimental conditions.
</p>

<p align="justify" width="100%">
The direction of vertical polarization (let's approximate that it's a purely ferroelectric effect) induced in the material is contingent on the applied voltage between the tip and the material's bottom electrode. Voltages greater in magnitude than the low and high coercive voltages of the hysteresis are referred to as low and high voltages, respectively. Two scenarios are then distinguished: one for the grounded tip case and the other for the grounded bottom case. The diagram below summarizes the direction of polarization concerning the applied voltage for both cases:
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
Here are the various hysteresis configurations in the off field mode, depending on the experimental parameters:
</p>

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/calibration_hysteresis_off_field.PNG> <br>
    <em>Hysteresis (off field) configuration depending on sign of d33 and direction of voltage</em>
</p>

<p align="justify" width="100%">
In the specific scenario of on field measurements with a predominant electrostatic component (where the electrostatic component determines the phase value with voltage), the sign of the electrostatic component's slope is contingent on the direction of the applied voltage, as established in the following table:
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
Here are the various hysteresis configurations in the on field mode, depending on the experimental parameters:
</p>

<p align="center" width="100%">
    <img align="center" width="60%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/calibration_hysteresis_on_field.PNG> <br>
    <em>Hysteresis (on field) configuration depending on sign of d33 and direction of voltage</em>
</p>

<p align="justify" width="100%">
The entirety of these steps, including the determination of the direction of hysteresis rotation, as well as the correlation between the various levels of bias, polarization, and phase, is ascertained within the first part of the <code>phase_calibration</code> function.
</p>

<p align="justify" width="100%">
It is worth noting that in some cases of on field measurements, where the electrostatic and ferroelectric components intensities are quite similar, multiple phase switching may occur during the cycle. In this case the calibration procedure is no longer valid.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/problematic_case_on_field_nanoloop.PNG> <br>
    <em>Problematic case of nanoloop: same order of magnitude for both ferroelectric and electrostatic component (on field, grounded tip, positive d33) (figure generated with <code><a href="https://github.com/CEA MetroCarac/PySSPFM/tree/main/PySSPFM/utils/nanoloop/theory.py">utils/nanoloop/theory.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
For the second part of the <code>phase_calibration</code> function, an in-depth analysis of the phase signal is conducted. An angular histogram is constructed from the complete set of phase values within the file, with <code>histo_init</code> function. In the case of Vertical PFM measurements, it's common to observe two peaks separated by approximately 180° [<a href="#ref5">5</a>, <a href="#ref7">7</a>]. These two peaks can either be fitted (with <code>fit_peak_hist</code> function) using a <code>Gaussian</code> model (function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">utils/core/basic_func.py</a></code> script) for improved precision or their maxima can be directly extracted for enhanced robustness and efficiency. The setting <code>histo_phase_method</code> allows for the selection of either of these methods. In the event of a fitting failure, the <code>maximum</code> method is applied. The phase difference and the positions of these two peaks are then extracted. During PFM measurements, a phase offset is typically present, and phase inversion can occur <a href="#ref6">[6]</a>. Therefore, it's imperative to identify both peaks within the histogram and assign them target phase values.
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_histogram.PNG> <br>
    <em>Phase histogram of SSPFM measurement (figure generated with <code>histo_init</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
In the PySSPFM application, users can concretely assign the desired phase values for both forward and reverse directions using the <code>pha_fwd</code> and <code>pha_rev</code> parameters. It is essential for the user to identify whether they are dealing with a predominant electrostatic component in the on field mode through the <code>main_electrostatic</code> parameter. Additionally, they can opt to specify the sign for the electrostatic component's slope with the parameter <code>locked_elec_slope</code>. The user should also provide information about the piezoelectric coefficient sign of the material in the measurement record. With these provided parameters and the calibration protocol, phase values can be attributed to the two peaks in the histogram.
</p>

<p align="justify" width="100%">
A potential phase inversion can be detected by examining the variation in the mean phase concerning the polarization voltage, using the <code>phase_analysis</code> function. If the theoretical and measured variations are opposite, a phase inversion has occurred, and it is subsequently corrected.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/phase_variation_with_voltage.PNG> <br>
    <em>Detection of phase inversion with phase variation with voltage (figure generated with <code>phase_analysis</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/phase.py">utils/nanoloop/phase.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
Following the calibration process and the identification of the positions of the two peaks on the histogram, as well as the phase difference, phase correction performed by <code>correct_phase_val</code> function can be achieved through four distinct protocols, chosen with <code>pha_corr</code> parameter:<br>
&#8226 <code>raw_phase</code>: The raw phase is retained, and no processing is applied (suitable for use in pre-measurement phase calibration).<br>
&#8226 <code>offset</code>: A phase offset is determined through calibration, and the phase difference between the two peaks remains unchanged (a treatment method that aims to preserve the initial measurement as faithfully as possible).<br>
&#8226 <code>affine</code>: An affine relationship is applied to all phase values, adjusting the phase difference to 180°.<br>
&#8226 <code>up and down</code>: A threshold is established between the two peaks, and each phase value is assigned the target value, <code>pha_fwd</code> or <code>pha_rev</code>, based on its position relative to the threshold and the calibration process.
</p>

### V.2) - MultiLoop

<p align="justify" width="100%">
For each measurement file, the acquisition of multiple nanoloop curves is possible, enabling the study of measurement repeatability and the reduction of measurement noise (by averaging all nanoloops within the file). This process involves the creation of a <code>MultiLoop</code> object with the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis.py</a></code> script, initialized with arrays of sub-arrays (the number of sub-arrays corresponding to the number of loops). These sub-arrays contain measurements such as polarization voltage, extracted amplitude, and phase values. Additionally, a voltage reading array is provided (with values corresponding to each nanoloop), a dictionary of phase calibration results (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v1---post-measurement-phase-calibration">V.1) - Post-measurement phase calibration</a> of the documentation), and the measurement mode (on or off field).
</p>

<p align="justify" width="100%">
To facilitate a more comprehensive data visualization:<br>
&#8226 Markers (at the beginning and end of the measurement, as well as at the extremities of the polarization voltages) are automatically determined based on the polarization voltage signal.<br>
&#8226 The branches of each nanoloop are divided into two categories: those on the right (in red) and those on the left (in blue). <br> <br>
Phase values are then adjusted according to the phase calibration dictionary.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_amplitude.PNG> <br>
    <em><code>MultiLoop</code> of amplitude (figure generated with <code>plot_all_loop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em> <br>
     <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_phase.PNG> <br>
    <em><code>MultiLoop</code> of phase (figure generated with <code>plot_all_loop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
Subsequently, based on the amplitude ($R$) and phase ($\phi$) loops, piezoresponse ($PR$) loops are generated. The user selects the function ($func_{pha}$) for calculating the piezoresponse with the parameter <code>pha_func</code>: $PR=R*func_{pha}(\phi)$. For phase values such as <code>pha_rev</code>=-90° and <code>pha_fwd</code>=90°, the chosen function should be <code>np.sin()</code>, whereas for phase values like <code>pha_rev</code>=180° and <code>pha_fwd</code>=0°, the selected function should be <code>np.cos()</code>.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/multiloop_piezoresponse.PNG> <br>
    <em><code>MultiLoop</code> of piezoresponse (figure generated with <code>plot_all_loop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em>
</p>

### V.3) - MeanLoop

<p align="justify" width="100%">
The <code>MeanLoop</code> object is defined within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis.py</a></code> script. It is initialized with a <code>MultiLoop</code> object (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v2---multiloop">V.2) - MultiLoop</a> of the documentation), and optionally, a phase calibration dictionary (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v1---post-measurement-phase-calibration">V.1) - Post-measurement phase calibration</a> of the documentation). This object facilitates the averaging of all loops within the <code>MultiLoop</code>, encompassing both amplitude, phase, and piezoresponse, except for the initial loop (if <code>del_first_loop is True</code>), which differs due to the sample's pre-polarized state at the beginning of the measurement. If a phase calibration dictionary is provided, the phase component of the <code>MeanLoop</code> is processed accordingly.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_amplitude.PNG> <br>
    <em><code>MeanLoop</code> of amplitude (figure generated with <code>plot_meanloop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em> <br>
     <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_phase.PNG> <br>
    <em><code>MeanLoop</code> of phase (figure generated with <code>plot_meanloop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em> <br>
     <br>
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/meanloop_piezoresponse.PNG> <br>
    <em><code>MeanLoop</code> of piezoresponse (figure generated with <code>plot_meanloop</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em>
</p>

## VI) - Second step of data analysis

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_second_step.PNG> <br>
    <em>GUI: Second step of data analysis</em>
</p>

<p align="center" width="100%">
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_second_step.PNG>
    <img align="center" width="49%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_second_step_single_script.PNG> <br>
    <em>Workflow: Second step of data analysis (left: global, right: single script)</em>
</p>

<p align="justify" width="100%">
The second step of the process may be initiated either through the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/nanoloop_to_hyst_s2.py">executable source code</a> or via the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/nanoloop_to_hyst_s2.py">graphical user interface</a>. 
</p>

<p align="justify" width="100%">
As an initial step, the <code>nanoloops</code> folder obtained is selected. The entirety of the files within it is arranged using the <code>generate_file_nanoloop_paths</code> function found in the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code> script. Subsequently, data extraction is carried out for each file, employing the <code>extract_nanoloop_data</code> function from the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file.py</a></code>. The measurement and processing parameters from the <code>parameters.txt</code> file are also read and extracted using the <code>print_parameters</code> function within the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>.
</p>

<p align="justify" width="100%">
Figures resulting from the processing of the first file are generated with <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code> scripts. Subsequently, each of the files is automatically analyzed without displaying the figures. For each mode (on field, off field, and coupled), a hysteresis loop is selected and associated with each pixel, and a set of ferroelectric properties is extracted. Additional properties are obtained through the analysis of measurement artifacts. The entirety of these properties contributes to the creation of SSPFM mappings.
</p>

<p align="justify" width="100%">
For a deeper understanding of the file management in this phase, please refer to the relevant section in the documentation:<br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2b---second-step-of-data-analysis">III.2.b) Second Step of Data Analysis</a>
</p>

### VI.1) - Parameters

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/parameters_second_step_1.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/parameters_second_step_2.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/parameters_second_step_3.PNG> <br>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/parameters_second_step_4.PNG> <br>
</p>

### VI.2) - Best loop

<p align="justify" width="100%">
The nanoloops data is extracted from the files within the corresponding <code>nanoloops</code> directory, and a <code>MultiLoop</code> object is instantiated for each file (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v2---multiloop">V.2) - MultiLoop</a> of the documentation). Subsequently, with the <code>nanoloop_treatment</code> function of the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis.py</a></code> script the amplitude and phase data are divided by the quality factor, calibrated ex-situ (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v1---post-measurement-phase-calibration">V.1) - Post-measurement phase calibration</a> of the documentation), and the amplitude and phase values at the first measurement point are extracted. These form two of the mapped ferroelectric properties, corresponding to the electrical polarization of the pristine state of the film.
</p>

<p align="justify" width="100%">
There are three distinct measurement processing modes, each involving the extraction of a <code>best_loop</code> using the <code>find_best_nanoloop</code> function from the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code> script: <br>
&#8226 <code>'multi_loop'</code>: Measurements are conducted in off field, and various reading voltage values are applied. This mode corresponds to the cKPFM (contact Kelvin Probe Force Microscopy) mode introduced by N. Balke and his colleagues <a href="#ref8">[8]</a>. All loops are fitted using the <code>Hysteresis</code> object (refer to Section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vi3---hysteresis-and-properties">IV.3) - Hysteresis and properties</a> in the documentation), and the best loop is the one that minimizes the vertical offset associated with the electrostatic component in off field. <br>
&#8226 <code>'mean_loop'</code>: Measurements are conducted in off field with a single reading voltage value, often set at 0 volts. The best loop is the average of all the loops (sometimes the first loop is not considered do to its pre-polarized state), determined through the creation of the <code>MeanLoop</code> object (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#v3---meanloop">V.3) - MeanLoop</a> of the documentation). <br>
&#8226 <code>'on_field'</code>: Measurements are conducted in on field. The best loop, in this case, is the average of all the loops, determined through the creation of the <code>MeanLoop</code> object.
</p>

### VI.3) - Hysteresis and properties

<p align="justify" width="100%">
The process of fitting hysteresis curves is a crucial step in determining the ferroelectric properties of a material. However, it is also a delicate part of the data processing that can greatly influence quality of the results. In many cases, the shape of the PFM hysteresis nanoloop can be deformed compared to macroscopic polarization hysteresis P(E).
</p>

<p align="justify" width="100%">
The script <code><a href=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/curve_hysteresis.py>utils/core/curve_hysteresis</a></code> introduces and processes a novel entity known as the <code>Hysteresis</code> object. This object is initialized through the variable <code>model</code>, encapsulating the mathematical formulations for both of its branches: <br>
&#8226 <code>'sigmoid'</code> (function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">utils/core/basic_func.py</a></code> script) <a href="#ref9">[9]</a>: $PR(V) = G * ({1 \over 1. + exp(-c^i * (V - V_0^i))} - 0.5) + a*V + b$ <br>
&#8226 <code>'arctan'</code> (function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">utils/core/basic_func.py</a></code> script): $PR(V) = G * arctan(c^i * (V - V_0^i)) + a*V + b$ <br>
$i$ serves as the index designating the branch: $i=L$ for the left branch, and $i=R$ for the right branch. <br>
The boolean variable, <code>asymmetric</code>, holds the responsibility of deciding whether to apportion distinct dilation coefficients to these bifurcated branches. 
If <code>asymmetric is False</code>, then $c^L = c^R$, while if <code>asymmetric is True</code>, $c^L \ne c^R$.
Artangent or sigmoid terms representing the influence of ferroelectric component, while the affine component representing the influence of the quadratic terms of artifacts is added to the the model <a href="#ref9">[9]</a>.
</p>

<p align="center" width="100%">
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_model.PNG> <br>
    <em>Hysteresis model used for the fit</em>
</p>

<p align="justify" width="100%">
The <code>hyst_analysis</code> function within the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code> facilitates the comprehensive analysis of hysteresis.
</p>

<p align="justify" width="100%">
An initialization of the fitting parameters is conducted with the function <code>init_hysteresis_params</code> of the <code><a href=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code> script:
    <ul>
        <li>Definition Interval:</li>
            <ul>
                <li>$c^i \in \left[0, +\infty\right[$ </li>
                <li>$G \in \left[0, +\infty\right[$ for a "counterclockwise" loop and $G \in \left]-\infty, 0\right]$ for a "clockwise" loop.</li>
                <li>$V_0^i \in \left[min(V), max(V)\right]$ </li>
                <li>$b \in \left[min(PR), max(PR)\right]$ </li>
                <li>$a$:</li>
                    <ul>
                        <li>For <code>analysis_mode == 'on_f_loop'</code>: In cases where:
                                <ul>
                                    <li><code>locked_elec_slope = 'positive'</code>, $a \in \left[0, +\infty\right[$</li>
                                    <li><code>locked_elec_slope = 'negative'</code>, $a \in \left]-\infty, 0\right]$</li>
                                    <li><code>locked_elec_slope is None</code>, $a$ is determined based on the direction of voltage application:</li>
                                        <ul>
                                            <li><code>grounded_tip is True</code> -> $a \in \left]-\infty, 0\right]$</li>
                                            <li><code>grounded_tip is False</code> -> $a \in \left[0, +\infty\right[$</li>
                                        </ul>
                                </ul>
                        <li>Otherwise, $a=0$ </li>
                    </ul>
            </ul>
        <li>The differential of the two branches, <code>diff_hyst</code>, is calculated and subsequently filtered (via the <code>filter_mean</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/noise.py">utils/core/noise.py</a></code>), effectively forming a dome. This process facilitates the initialization of fit parameter values and is derived from the work of Jesse et al. <a href="#ref9">[9]</a>. <br>
            <p align="center" width="100%">
                <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/diff_hysteresis.PNG> <br>
                <em>Differential hysteresis model (dome)</em>
            </p>
        </li>
        <li>Initial Value:</li>
            <ul>
                <li>$G$ is ascertained from the maximum of <code>diff_hyst</code>.</li>             
                <li>$V_0^i$ are defined as the abscissas corresponding to the minimum and maximum slopes of <code>diff_hyst</code>.</li>
                <li>For <code>analysis_mode == 'on_f_loop'</code>, $a$ is initialized as the ratio: ${max(PR)-min(PR) \over max(voltage)-min(voltage)}$.</li>   
            </ul>
    </ul>
</p>

<p align="justify" width="100%">
The hysteresis is subsequently fitted using the fit <code>method</code>, considering the coordinates of the best loop's points and selecting the desired method. This approach leverages the <a href="https://pypi.org/project/lmfit/">lmfit</a> library, enabling the extraction of parameters from the hysteresis model that best converges with the experimental data.
</p>

<p align="justify" width="100%">
It should be noted that the fitting process (based on minimization of mean square deviation between analytical model and experimental data) is performed on the entirety of the hysteresis curve and not on each individual branch separately. Some parameters are global to the hysteresis such as affine component and hysteresis amplitude while some can vary for each branch such as the position and the dilatation coefficient. 
</p>

<p align="justify" width="100%">
Following the completion of the fitting process, the <code>properties</code> method facilitates the extraction of the ferroelectric properties of the hysteresis <a href="#ref9">[9]</a>. All properties are calculated both with and without the electrostatic component: <br>
&#8226 The imprint, denoted by <code>x_shift</code>, is defined as the mean of the two coercive voltages of the hysteresis branches. The voltage window, <code>x0_wid</code>, is the difference between these two values. The hysteresis area, <code>area</code>, is simply the product of the voltage window and the hysteresis amplitude. <br>
&#8226 The intersection points on the abscissa axes (<code>x_inters_l</code>, <code>x_inters_r</code>) and the ordinate axes (<code>y_inters_l</code>, <code>y_inters_r</code>) respectively define the coercive voltages and the remanent piezoresponse voltages. <br>
&#8226 The inflection points, by default located at 10% and 90% of the branch amplitudes, determine the nucleation voltages (<code>x_infl_l</code>, <code>x_infl_r</code>) and saturation voltages (<code>x_sat_l</code>, <code>x_sat_r</code>). <br>
&#8226 The relative difference between the expansion coefficients of the right and left branches, denoted as <code>diff_coef</code>, quantifies the level of hysteresis asymmetry. <br>
&#8226 The quadratic error between the experimental data and the model. <br>

</p>

<p align="justify" width="100%">
The quality of the fit is expressed as the R-squared value, determined by the fit achieved using the <code>r_square</code> method. It represents the mean square deviation between the fit and measurements. During the analysis of ferroelectric properties, it is important to always consider the R-squared value. This is because variations in these properties can arise from both physical nanoscale effects and poor quality fitting. For hysteresis curves with abnormally low R-squared values, it is recommended to inspect each property individually to identify potential issues with the data. 
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/hysteresis_asymmetric_fit_and_properties.PNG> <br>
    <em>Asymmetric hysteresis fit and properties (figure generated with <code>plot</code> and <code>plot_properties</code> functions of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/curve_hysteresis.py">utils/core/curve_hysteresis.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
In the figure above, we can observe the fitting of an asymmetric hysteresis. The model is determined both with and without the affine component representing the electrostatic part. Here, the properties of the hysteresis are displayed on the model without the electrostatic component.
</p>

### VI.4) - Artifact decoupling

<p align="center" width="100%">
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_electrostatics.PNG> <br>
    <em>Electrostatic artifacts</em>
</p>

<p align="justify" width="100%">
Artifacts, primarily of electrostatic nature,  but more generally stemming from quadratic terms (electrostatics (both capacitive <a href="#ref10">[10]</a> and local <a href="#ref11">[11]</a>, electrostrictive, Joule's effect [<a href="#ref12">12</a>, <a href="#ref13">13</a>, <a href="#ref14">14</a>]), become non-negligible here due to the application of a continuous voltage, V_DC, which can influence the measurement in the following ways: <br>
&#8226 By introducing a vertical offset in off field measurements (artifacts mainly of electrostatic origin). <br>
&#8226 By introducing an affine component in on field measurements (influenced by quadratic terms) <a href="#ref15">[15]</a>. <br>
&#8226 Non-linearly, when the effect becomes active after a certain threshold voltage is reached in the on field scenario <a href="#ref15">[15]</a>.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_influence_on_hysteresis.PNG> <br>
    <em>Artifact influence on hysteresis</em>
</p>

<p align="justify" width="100%">
Within the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code>, protocols for artifact decorrelation have been developed.
</p>

### VI.4.a) - Analysis of on field amplitude nanoloop

<p align="justify" width="100%">
The function <code>btfly_analysis</code> enables the execution of the procedure. The first method used to isolate the influence of artifacts on the ferroelectric component involves analyzing the on field amplitude nanoloop. The method is simple, as the coercive voltages correspond to the points where the amplitude of the curve are the lower. The two points are then determined, and their average corresponds to a measurement of the CPD (Contact Potential Difference).
</p>

<p align="justify" width="100%">
The study of the CPD is useful and can provide further information on the sample. We can find CPD value with the work function of the material <a href="#ref16">[16]</a>: $CPD = {\phi_{Probe} - \phi_{Sample} \over |e|}$. CPD is sensitive to the nature of the sample but also to the surface charge density of the sample <a href="#ref17">[17]</a>.
</p>

<p align="justify" width="100%">
However, this method has some drawbacks. It cannot determine the slope of the electrostatic component, and it is only valid when the affine component predominates over the hysteresis component. Moreover, imprint effect can interfere with the measurement accuracy, which is already limited since the signal-to-noise ratio is low at the points of interest <a href="#ref6">[6]</a>. Additionally, the measurement of amplitude vanishing points is rare in practice because of the influence of noise on measurements [<a href="#ref18">18</a>, <a href="#ref19">19</a>].
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_btfly_analysis.PNG> <br>
    <em>Result of <code>btfly_analysis</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code> script (figure generated with <code>plot_btfly_analysis</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code> script)</em>
</p>

### VI.4.b) - Analysis of saturation domain of on field piezoresponse nanoloop

<p align="justify" width="100%">
This procedure has been inspired by the following publication <a href="#ref20">[20]</a>. The function <code>sat_analysis</code> enables the execution of the procedure. This method involves isolating the two saturation domains of the on field hysteresis, performing a linear regression of these domains, and measuring the line passing through them, which constitutes the affine component. The saturation domain can be determined in two modes. If the parameter <code>sat_mode = 'set'</code> is selected, it is defined by the user through the values <code>'min'</code> and <code>'max'</code> within the <code>sat_domain</code> dictionary. On the other hand, if <code>sat_mode = 'auto'</code> is chosen, it is automatically determined following the fitting process (voltages at which 90% (default value of <code>sat_thresh</code>) of the switch is achieved for both branches, respectively). This method is easy to implement and provides the entire affine component due to the artifacts. However, it requires reaching the saturation domain of the hysteresis, which is not always the case, especially for thick samples or those with high coercive voltages requiring high pulses voltages. Additionally, the influence of artifacts can be more significant in the saturation domains, especially for on field measurement, and other phenomena can play a significant role, such as charge injection <a href="#ref15">[15]</a>, leakage current <a href="#ref21">[21]</a>, joules heating <a href="#ref15">[15]</a>, surface or tip degradation <a href="#ref22">[22]</a>, etc [<a href="#ref15">15</a>, <a href="#ref22">22</a>, <a href="#ref23">23</a>]. The analysis domain is limited, resulting in less precise measurements.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_sat_analysis.PNG> <br>
    <em>Result of <code>sat_analysis</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code> script (figure generated with <code>plot_sat_analysis</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code> script)</em>
</p>

### VI.4.c) - Multi read voltages of off field hysteresis

<p align="justify" width="100%">
The function <code>offset_analysis</code> enables the execution of the procedure. This method involves measuring multiple off field hysteresis curves at different read voltages (equivalent of c-KPFM method introduced by N.Balke et al. <a href="#ref8">[8]</a>). Bruker recommends this technique <a href="#ref24">[24]</a>. For each curve, a vertical offset is extracted by fitting off field hysteresis. Then vertical offset is determined as a function of the read voltage, which constitutes the affine component. A linear regression is conducted using the <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html#scipy.stats.linregress">linregress</a> function of the scipy.stats library, enabling the deduction of the affine component. This approach is robust and precise as it is based solely on the off field fits, with a broad range of validity. Moreover, it allows obtaining the whole affine component. However, the implementation of this method necessitates measuring several off field hysteresis curves at various voltages, which is time-consuming and can disrupt the analysis of the hysteresis reproducibility.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_offset_analysis.PNG> <br>
    <em>Result of <code>offset_analysis</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code> script (figure generated with <code>plot_offset_analysis</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code> script)</em>
</p>

### VI.4.d) - Differential analysis of on and off field hysteresis

<p align="justify" width="100%">
This procedure has been inspired by the following publication [<a href="#ref15">15</a>, <a href="#ref25">25</a>]. The function <code>differential_analysis</code> enables the execution of the procedure. This method involves subtracting on and off field hysteresis curves, then a line passing through zero is obtained. At times, the differential component is no longer linear beyond certain threshold voltages where phenomena manifest. Thus, a voltage range must be defined within which the differential component remains linear. If the <code>diff_mode</code> parameter is set to <code>'set'</code>, the user defines this range using the <code>'min'</code> and <code>'max'</code> values within the <code>diff_domain</code> dictionary. However, if the <code>diff_mode</code> parameter is set to <code>'auto'</code>, half of the voltage range is considered, centered around 0. Then, a linear regression is performed to determine the slope, which is then used to divide the vertical offset of the off field hysteresis curve to obtain the CPD. This method enables the determination of the entire affine component. It is both robust and precise since it primarily relies on off field fits, and it is also easy to implement. Additionally, the differential analysis allows for choosing the voltage domain to perform the linear regression. Indeed, in some cases, it is better to do it in low voltage domain since non linear effects could appear at high voltage as previously mentioned. It can be usefull to study these phenomenons (charge injection, leakage current, joule effect …).
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/artifacts_diff_analysis.PNG> <br>
    <em>Workflow of <code>differential_analysis</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code> script</em>
</p>

### VI.4.e) - Fit of both on and off field hysteresis

<p align="justify" width="100%">
The last approach was already developed in (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi3---hysteresis-and-properties">VI.3) - Hysteresis and properties</a> of the documentation). It consists to fit both hysteresis on and off field, which involves extracting the affine component. One advantage of this method is that it is easy to implement since the hysteresis fit is necessarily done during data processing to extract ferroelectric sample properties. Additionally, this method enables to determine the entire affine component. However, the measurement requires robust on field hysteresis fitting, which can be challenging for predominant electrostatic effects.
</p>

### VI.5) - cKPFM

<p align="justify" width="100%">
The <code>'multi_loop'</code> analysis mode is equivalent to the cKPFM mode <a href="#ref8">[8]</a>: different read voltage values are employed for each hysteresis. Consequently, we can investigate the evolution of piezoresponse not with respect to the writing voltage, but with the reading voltage. To accomplish this, the <code>gen_ckpfm_meas</code> function from the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/analysis.py">utils/nanoloop/analysis.py</a></code> script is utilized to transform data initially in the form of nanoloops into cKPFM measurements. This mode allows for a more profound exploration of measurement artifacts, distinguishing between ferroelectric phenomena, electrostatic effects, charge injection, and more.
</p>

<p align="justify" width="100%">
For more information about the <code>'multi_loop'</code> analysis mode, see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi2---best-loop">VI.2) - Best loop</a> of the documentation.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/ckpfm_analysis.PNG> <br>
    <em>cKPFM analysis result (figure generated with <code>plot_ckpfm</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/plot.py">utils/nanoloop/plot.py</a></code> script)</em>
</p>

## VII) - SSPFM mapping

<p align="justify" width="100%">
The creation and processing of SSPFM maps are overseen by the set of scripts contained within: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">utils/map</a></code>. SSPFM maps represent the primary outcomes of measurement analysis. They can only be determined once both processing stages are completed, as the properties of hysteresis and electrostatic artifacts must first be ascertained before they are mapped.
</p>

<p align="justify" width="100%">
The script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code> orchestrates and manages the entire process of creating and processing SSPFM maps. It relies significantly on scripts such as <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/plot.py">utils/map/plot.py</a></code> for plotting maps, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/interpolate.py">utils/map/interpolate.py</a></code> for 2D interpolation, and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/matrix_processing.py">utils/map/matrix_processing.py</a></code> for formatting material properties into map representations.
</p>

<p align="justify" width="100%">
The maps are generated using the executable codes <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/global_map_reader.py">toolbox/global_map_reader.py</a></code> and <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/list_map_reader.py">toolbox/list_map_reader.py</a></code> (see sections <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1c-global-map-reader">VIII.1.c) Global map reader</a> and <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1d-list-map-reader">VIII.1.d) List map reader</a> of the documentation).
</p>

### VII.1) - Mask

<p align="justify" width="100%">
For cartographies, it is possible to establish a mask in order to: <br>
&#8226 Mitigate the influence of problematic or defective pixels in the map.<br>
&#8226 Isolate specific ferroelectric phases or areas on the sample's surface.
</p>

<p align="justify" width="100%">
The mask can be ascertained: <br>
&#8226 Manually, through the <code>man_mask</code> parameter, which contains a list of pixels provided by the user. <br>
&#8226 Using a reference property, in case <code>man_mask is None</code>, with parameters specified in the <code>ref</code> dictionary. The latter is chosen through the <code>'mode'</code> (<code>'off'</code>, <code>'on'</code>, or <code>'coupled'</code>) and <code>'meas'</code>, which contains the name of the reference property. The user then selects a measurement range using the <code>'min value'</code> and <code>'max value'</code> parameters. If either of the two values is <code>None</code>, the corresponding boundary is not considered. The <code>'interactive'</code> parameter allows interactive selection of the reference measurement boundaries, with an iterative display of the masked map and user keyboard input. This interactive procedure is provided by the <code>select_pixel</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code>. The entire procedure is executed by the <code>mask_ref</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code>. <br>
&#8226 The mask can be reverted by assigning the value <code>True</code> to the user parameter <code>revert_mask</code>.
</p>

### VII.2) - Interpolation 2D

<p align="justify" width="100%">
All the functions responsible for conducting 2D interpolations can be found in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/interpolate.py">utils/map/interpolate.py</a></code>. <br>
The <code>grid_interp</code> function performs a 2D interpolation on a map using the  <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html">griddata</a> function from scipy.interpolate. The <code>interp_func</code> parameter allows you to choose the interpolation function (<code>'linear'</code> or <code>'cubic'</code>). <br>
The <code>interp_2d_treated</code> function oversees the entire calibration procedure. Initially, by calling the <code>grid_interp</code> function, the map is interpolated with an interpolation coefficient of 1 to correct any defective or masked values (<code>nan</code>). Next, the dimensions of this map are expanded based on the <code>interp_fact</code> parameter with new <code>nan</code> values. Then, a new 2D interpolation is performed by invoking the <code>grid_interp</code> function once more.
</p>

### VII.3) - Figures

<p align="justify" width="100%">
The SSPFM matrices are determined using the main function <code>formatting_measure</code> in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/matrix_processing.py">utils/map/matrix_processing.py</a></code>. The data is initially in the form of a 1D array. Initially, it needs to be transformed into a matrix based on the probe's path. This process is partially handled by the <code>rearrange_matrix</code> function. The main function <code>formatting_measure</code> numerically applies masks, determines if pixel values correspond to errors, generates matrices specific to map annotations. It also calls the <code>interp_2d_treated</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/interpolate.py">utils/map/interpolate.py</a></code> to perform 2D interpolation. In summary, the entire script is responsible for generating all the matrices (properties, annotations, etc.) and values displayed in the figures.
</p>

<p align="justify" width="100%">
The complete set of displayed figures is orchestrated by the function <code>plot_and_save_maps</code> in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/plot.py">utils/map/plot.py</a></code>, and it represents: <br>
    <ul>
        <li>Map of material property:</li>
            <ul>
                <li>Image 3: Step 1: raw property map (no selection criterion).</li>
                <li>Image 4: Step 1bis: interpolation of step 1.</li>
                <li>Image 5: Step 2: add the mask (some pixel are removed).</li>
                <li>Image 6: Step 3: interpolate removed pixel values (without increasing resolution) to go back to normal values.</li>
                <li>Image 7: Step 3bis: interpolation of step 3.</li>
                <li>Image 8: Step 4: final result: interpolation of step 3 and remove the area corresponding to the removed pixels on the map.</li>
            </ul> <br>
        <li>Map of reference property:</li>
            <ul>
                <li>Image 1: reference property: step 1.</li>
                <li>Image 2: reference property: step 4.</li>
            </ul>
     </ul>
</p>


<p align="justify" width="100%">
Each cartography is rendered using the functions <code>intermediate_map</code> or <code>final_map</code> (for step 4). Annotations are incorporated into the cartography figures generated by <code>final_map</code> through the <code>annotate</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/plot.py">utils/map/plot.py</a></code>. These annotations include the positions of all measurement points and the probe's trajectory directions. Furthermore, the determination of x and y-axis values is accomplished (for original or interpolated cartographies) using the <code>extent</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/matrix_processing.py">utils/map/matrix_processing.py</a></code>. The resulting figures can be saved in both 'png' and 'txt' formats using the <code>save</code> parameter.
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/map_reader_global.PNG> <br>
    <em>SSPFM map of hysteresis amplitude, with R² in reference property (figure generated with <code>plot_and_save_maps</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/plot.py">utils/map/plot.py</a></code> script)</em>
</p>

## VIII) Toolbox

### VIII.1) Viewers

#### VIII.1.a) Raw file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/raw_file_reader.py">toolbox/raw_file_reader.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/raw_file_reader.py">gui/raw_file_reader.py</a></code>. It allows the graphical visualization of raw measurements from an SSPFM datacube file.
</p>

<p align="justify" width="100%">
User parameters:
</p>

```
    default_user_parameters = {
        'file path in': '',
        'dir path out': '',
        'mode': "classic",
        'verbose': True,
        'show plots': True,
        'save plots': False
    }
```

<p align="justify" width="100%">
&#8226 File management: In input, the algorithm take a SSPFM datacube measurement file. <br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

<p align="justify" width="100%">
As input, SSPFM datacube measurement file is open, and its data is extracted (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii1---input-files">III.1.c) - Extraction</a> of the documentation) and plotted. The selection of the measurement mode is facilitated through the <code>'mode'</code> parameter, with options including: <br>
&#8226 <code>'classic'</code> (Sweep Resonance) <br>
&#8226 <code>'dfrt'</code>
</p>

<p align="center" width="100%">
    <img align="center" width="65%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/raw_signals.PNG> <br>
    <em>Raw measurement of an datacube file (figure generated with <code>plt_signals</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/datacube_to_nanoloop/plot.py">utils/datacube_to_nanoloop/plot.py</a></code> script)</em>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

#### VIII.1.b) Loop file

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/loop_file_reader.py">toolbox/loop_file_reader.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/loop_file_reader.py">gui/loop_file_reader.py</a></code>. It enables the visualization of data from a measurement file in the form of a nanoloop (txt extension).
</p>

<p align="justify" width="100%">
User parameters:
</p>

```
    default_user_parameters = {
        'file path in': '',
        'csv path in': '',
        'dir path out': '',
        'del 1st loop': True,
        'corr': 'offset',
        'pha fwd': 0,
        'pha rev': 180,
        'func': 'cosine',
        'main elec': True,
        'grounded tip': True,
        'positive d33': True,
        'locked elec slope': 'None',
        'verbose': True,
        'show plots': True,
        'save': False,
    }
```

<p align="justify" width="100%">
&#8226 File management: As an input, the algorithm takes a <code>txt_loop</code> file, containing measurement data in the form of nanoloop. The csv measurement sheet path can be specified by the user, otherwise, it is generated by default.<br>
&#8226 Phase calibration parameters: used for nanoloop treatment.<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

<p align="justify" width="100%">
In input, a measurement file in the form of a <code>nanoloop</code> file (generated after the first processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a> of the documentation)) is opened employing the <code>extract_nanoloop_data</code> function from the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file.py</a></code>. Additionally, the corresponding csv measurement sheet is accessed to extract the parameters of the polarization voltage signal. An ex-situ calibration of the phase is performed, using the comprehensive set of user-defined phase processing parameters. Furthermore, the user has the option to exclude the first hysteresis curve from the generated figures if it differs from the others due to the pristine state of the film. Subsequently, the objects <code>MultiLoop</code> and <code>MeanLoop</code> associated with the file are constructed, and the corresponding figures are generated and displayed.
</p>

<p align="justify" width="100%">
For more precisions on post-measurement phase calibration, <code>MultiLoop</code> and <code>MeanLoop</code> objects, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#v---nanoloop">V) Nanoloop</a> of the documentation.
</p>

#### VIII.1.c) Global map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/global_map_reader.py">toolbox/global_map_reader.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/global_map_reader.py">gui/global_map_reader.py</a></code>. It enables the visualization of all material properties measured in the form of cartographies.
</p>

<p align="justify" width="100%">
User parameters:
</p>

```
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'interp fact': 4,
        'interp func': 'linear',
        'revert mask': {'on': False,
                        'off': False,
                        'coupled': False},
        'man mask': {'on': [],
                     'off': [],
                     'coupled': []},
        'ref': {'on': {'meas': 'charac tot fit: area',
                       'min val': None,
                       'max val': 0.005,
                       'fmt': '.5f',
                       'interactive': False},
                'off': {'meas': 'charac tot fit: area',
                        'min val': None,
                        'max val': 0.005,
                        'fmt': '.5f',
                        'interactive': False},
                'coupled': {'meas': 'r_2',
                            'min val': 0.95,
                            'max val': None,
                            'fmt': '.5f',
                            'interactive': False}},
        'verbose': True,
        'show plots': True,
        'save': False,
    }
```

<p align="justify" width="100%">
&#8226 File management: As an input, the algorithm takes a <code>properties</code> SSPFM datacube measurement file.<br>
&#8226 Map interpolation parameters<br>
&#8226 Mask parameters<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

<p align="justify" width="100%">
In input, the directory <code>properties</code> (generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation)), containing the property measurements in the form of text files for all modes (on and off field, coupled), is specified. Subsequently, the data is extracted, with <code>extract_properties</code> function of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code> and a cross-correlation analysis is conducted between the different cartographies. The cartographies are then generated for each of the modes (on and off field, and coupled) and displayed using the <code>main_mapping</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code>. It's worth noting that a different mask is constructed for each mode.
</p>

<p align="justify" width="100%">
&#8226 For the creation of SSPFM cartographies, please consult section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vii---sspfm-mapping">VII) - SSPFM mapping</a> in the documentation. <br>
&#8226 For mask creation, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vii1---sspem-mapping/mask">VII.1) - Mask</a> in the documentation. <br>
&#8226 For cross-correlative analysis, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#viii4-2d-cross-correlation">VII.4) - 2D cross correlation</a> of the documentation.
</p>

#### VIII.1.d) List map reader

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/list_map_reader.py">toolbox/list_map_reader.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/list_map_reader.py">gui/list_map_reader.py</a></code>. It allows for the visualization of a selection of measured properties in the form of cartography on a single figure.
</p>

<p align="justify" width="100%">
User parameters:
</p>

```
    ind_maps = [['off', 'charac tot fit: area'],
                ['off', 'fit pars: ampli_0'],
                ['on', 'charac tot fit: area'],
                ['on', 'fit pars: ampli_0']]
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'ind maps': ind_maps,
        'interp fact': 4,
        'interp func': 'linear',
        'revert mask': False,
        'man mask': [],
        'ref': {'mode': 'off',
                'meas': 'charac tot fit: R_2 hyst',
                'min val': 0.95,
                'max val': None,
                'fmt': '.5f',
                'interactive': False},
        'verbose': True,
        'show plots': True,
        'save': False
    }
```

<p align="justify" width="100%">
&#8226 File management: As an input, the algorithm takes a <code>properties</code> SSPFM datacube measurement file.<br>
&#8226 Measurement selection parameters<br>
&#8226 Map interpolation parameters<br>
&#8226 Mask parameters<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

<p align="justify" width="100%">
The operating principle of this reader differs slightly from that of the global map reader (see Section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#viii1c-global-map-reader">VIII.1.c) - Global map reader</a> in the documentation). In this case, a single mask can be defined by the user, and a list of measures to be mapped is provided by the user. The concept behind this reader is to observe multiple maps of different properties simultaneously (rather than one by one). Therefore, the <code>main_mapping</code> function is not used. In the main function of the script, <code>main_list_map_reader</code>, the mask is constructed, and cross-correlative analysis is performed only between the mapped measures (for cross-correlative analysis, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#viii4-2d-cross-correlation">VII.4) - 2D cross correlation</a> of the documentation.). Then, the figure containing all the different maps is formatted using the <code>formatting_fig</code> function. For each map, the <code>tratment_plot_map</code> function is used to carry out treatments (masking, interpolation, etc.) and generate the map of the corresponding property, making use of functions from the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/map">SSPFM mapping</a> scripts.
</p>

<p align="center" width="100%">
    <img align="center" width="70%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/cross_correlation_list_off_field.PNG> <br>
    <em>Result of cross correlation analysis (figure generated with <code>cross_corr_table</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">toolbox/map_correlation.py</a></code> script)</em>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/map_reader_list.PNG> <br>
    <em>Result of list_map_reader (figure generated with <code>main_list_map_reader</code> function of <code><a href=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/list_map_reader.py">toolbox/list_map_reader.py</a></code> script)</em>
</p>

### VIII.2) Hysteresis clustering (K-Means)

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py">toolbox/hysteresis_clustering.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/hysteresis_clustering.py">gui/hysteresis_clustering.py</a></code>. It facilitates the classification of hysteresis loops associated with each measurement point into clusters. This tool can enable phase separation or the separation of the influences of physically distinct phenomena, such as measurement artifacts.
</p>

#### VIII.2.a) Parameters

```
    default_user_parameters = {
        'dir path in': '',
        'dir path in meas': '',
        'dir path out': '',
        'nb clusters off': 4,
        'nb clusters on': 4,
        'nb clusters coupled': 4,
        'verbose': True,
        'show plots': True,
        'save': False,
    }
```

<p align="justify" width="100%">
&#8226 File management: In the initial phase, the algorithm ingests the <code>best_nanoloops</code> directory along with the <code>properties</code> directory. <br>
&#8226 Clusters: For each measurement (on field, off field, and coupled), the user specifies the number of clusters. <br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of outcomes. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

#### VIII.2.b) Extraction 

<p align="justify" width="100%">
The entirety of data stemming from the best hysteresis loops, both in the on field and off field modes, is extracted from the files residing within the <code>best_nanoloops</code> directory (with the function <code>extract_data</code> of the script). <br>
Vertical offset measurements in the off field mode and the dimensions of the mappings are drawn from the files within the <code>properties</code> directory (with <code>extract_properties</code> function of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>). <br>
The coupled measurements are subsequently generated through the process of differential analysis of on field and off field measurements, with the flexibility to incorporate the vertical offset in the off field mode, a component influenced by the sample's surface contact potential (section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4d---differential-analysis-of-on-and-off-field-hysteresis">VI.4.d) - Differential analysis of on and off field hysteresis</a> in the documentation).
</p>

<p align="justify" width="100%">
For a deeper understanding of the input file management, please refer to the relevant section in the documentation:<br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2b---second-step-of-data-analysis">III.2.b) - Second Step of Data Analysis</a>
</p>

#### VIII.2.c) Treatment

<p align="justify" width="100%">
For each of the modes (on field, off field, and coupled), and for each of the hysteresis associated with each data point, a cluster is assigned using the K-Means methodology. To accomplish this, we import the <a href="https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html">KMeans</a> function from <a href="https://scikit-learn.org/stable/modules/clustering.html#clustering">sklearn.cluster</a>. A reference cluster is established, identified as the one encompassing the maximum number of data points. The index assigned to the other clusters is then computed as the distance between their centroid and that of the reference cluster, respectively. Subsequently, an average hysteresis for each cluster is computed.
</p>

#### VIII.2.d) Figures

<p align="center" width="100%">
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/clustering_all_hyst.PNG>
    <img align="center" width="40%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/clustering_mean_hyst.PNG>
    <img align="center" width="19%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/clustering_carto.PNG> <br>
    <em>Result of hysteresis_clustering (figure generated with <code>main_hysteresis_clustering</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/hysteresis_clustering.py">toolbox/hysteresis_clustering.py</a></code> script)</em>
</p>

<p align="justify" width="100%">
For each mode (on field, off field, and coupled), three figures are generated, each containing: <br>
&#8226 The complete array of hysteresis loops from all datasets, distinguished by colors assigned based on their cluster index. <br>
&#8226 The average hysteresis loops for each cluster, distinguished by colors assigned according to their cluster index. <br>
&#8226 A spatial cartography displaying the assigned clusters. <br>
</p>

### VIII.3) Mean hysteresis

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_hyst.py">toolbox/mean_hyst.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/mean_hyst.py">gui/mean_hyst.py</a></code>. A portion of each of the hysteresis loops associated with each measurement point can be selected using a criterion chosen by the user, and then they are averaged. This algorithm enables phase separation and extraction of the average properties associated with it.
</p>

#### VIII.3.a) Parameters

```
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in meas': '',
        'dir path in loop': '',
        'file path in pars': '',
        'mode': 'off',
        'mask': {'revert mask': False,
                 'man mask': None,
                 'ref': {'prop': 'charac tot fit: area',
                         'mode': 'off',
                         'min val': 0.005,
                         'max val': None,
                         'fmt': '.2f',
                         'interactive': False}},
        'func': 'sigmoid',
        'method': 'least_square',
        'asymmetric': False,
        'inf thresh': 10,
        'sat thresh': 90,
        'del 1st loop': True,
        'pha corr': 'offset',
        'pha fwd': 0,
        'pha rev': 180,
        'pha func': 'cosine',
        'main elec': True,
        'locked elec slope': "None",
        'diff domain': {'min': -5., 'max': 5.},
        'sat mode': 'set',
        'sat domain': {'min': -9., 'max': 9.},
        'interp fact': 4,
        'interp func': 'linear',
        'verbose': True,
        'show plots': True,
        'save': False
    }
```

<p align="justify" width="100%">
&#8226 File management: For input, the algorithm requires the directory generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation). It can be supplemented with the respective folders: <code>properties</code> for material properties, <code>nanoloops</code> containing measurements in the form of nanoloops (generated after the first processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a> of the documentation)), and the text file containing measurement and processing parameters, <code>parameters.txt</code>.<br>
&#8226 Mode: Choose from <code>'off'</code>, <code>'on'</code>, or <code>'coupled'.</code><br>
&#8226 Mask parameters<br>
&#8226 Hysteresis treatment parameters: Utilized for fitting the mean hysteresis.<br>
&#8226 Phase calibration parameters: Employed in nanoloop treatment.<br>
&#8226 Differential parameters: Essential for differential analysis.<br>
&#8226 Saturation parameters: Used to decouple artifacts through saturation analysis.<br>
&#8226 Map interpolation parameters<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of results. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

#### VIII.3.b) Extraction 

<p align="justify" width="100%">
The data of the measured properties (generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation)) is extracted from the folder <code>properties</code> with <code>extract_properties</code> function of the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>. Subsequently, a selection mask is created based on user-provided parameters (either through a list of pixels directly determined by the user, <code>'man mask'</code>, or a condition on the values of a reference property, <code>'ref'</code>). This mask enables the determination of a selection of hysteresis loops associated with the corresponding measurement points.
</p>

<p align="justify" width="100%">
&#8226 For a deeper understanding of the input file management, please refer to the relevant section in the documentation:<br> <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2b---second-step-of-data-analysis">III.2.b) - Second Step of Data Analysis</a> <br>
&#8226 For mask creation, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vii1---sspem-mapping/mask">VII.1) - Mask</a> in the documentation.
</p>

#### VIII.3.c) Find best loop

<p align="justify" width="100%">
Subsequently, for each of the selected measurement points, the finest among the loops is to be extracted with the aid of the <code>find_best_loops</code> function. This function acquires the measurement parameters from the <code>parameters.txt</code> file and invokes the <code>single_script</code> function found in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/nanoloop_to_hyst_s2.py">data_processing/nanoloop_to_hyst_s2.py</a></code> to retrieve data from the <code>nanoloops</code> files and determine the optimum loop, referred to as the <code>best_loop</code>. In the case of a coupled measurement (<code>mode = 'coupled'</code>), this protocol is repeated for the on and off field modes. If the setting <code>electrostatic_offset is True</code>, the offsets in the 'off field' mode are utilized to reconstruct the entirety of the electrostatic component (accounting for the CPD) (section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4d---differential-analysis-of-on-and-off-field-hysteresis">VI.4.d) - Differential analysis of on and off field hysteresis</a> in the documentation).
</p>

<p align="justify" width="100%">
For <code>best_loop</code> detrmination, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vi2---best-loop">VI.2) - Best loop</a> in the documentation.
</p>

#### VIII.3.d) Mean analysis

<p align="justify" width="100%">
&#8226 For <code>mode = 'on'</code> or <code> mode = 'off'</code>: The <code>mean_analysis_on_off</code> function commences by creating a <code>MeanLoop</code> object, composed of the collection of <code>best_loop</code> associated with each measurement point. The mean hysteresis is then constructed and fitted using the <code>hyst_analysis</code> function from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code>, based on the user-defined hysteresis parameters. All properties associated with this mean hysteresis are extracted, and an analysis of electrostatic artifacts is performed using the <code>electrostatic_analysis</code> function from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/analysis.py">utils/nanoloop_to_hyst/analysis.py</a></code>. <br>
&#8226 For <code>mode = 'coupled'</code>: The <code>mean_analysis_coupled</code> function determines the entire differential <code>best_loop</code> set from the combined on and off field pairs, taking into account the off field offset if specified. The complete set of differential <code>best_loop</code> is averaged into a single differential loop, and linear regression is performed on the latter.
</p>

<p align="justify" width="100%">
&#8226 For more precisions on <code>MeanLoop</code> object, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#v3---meanloop">V.3) MeanLoop</a> of the documentation. <br>
&#8226 For hysteresis fitting, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vi3---hysteresis-and-properties">VI.3) - Hysteresis and properties</a> in the documentation. <br>
&#8226 For artifact decoupling, please refer to section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vi4---artifact-decoupling">VI.4) - Artifact decoupling</a> in the documentation.
</p>

#### VIII.3.e) Figures

<p align="justify" width="100%">
The SSPFM mappings, highlighting the selected pixels, are displayed. <br>
&#8226 For <code>mode = 'on'</code> or <code> mode = 'off'</code>: the <code>MeanLoop</code> object associated with the selection (in amplitude, phase, and piezoresponse), the fitted mean hysteresis, and the corresponding electrostatic analyses are presented. <br>
&#8226 For <code>mode = 'coupled'</code>: the mean differential loop and its linear regression are exhibited using the <code>plot_differential_analysis</code> function from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/plot.py">utils/nanoloop_to_hyst/plot.py</a></code>.
</p>

### VIII.4) 2D cross correlation

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">toolbox/map_correlation.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/map_correlation.py">gui/map_correlation.py</a></code>. Correlation between different maps of the sample's properties allow to gain a better understanding of the origin of the signals and the interactions between different physical phenomena. The Pearson product-moment correlation coefficients, which enables us to express the correlation between two maps as a scalar value varying between 1 (perfect correlation, and -1 perfect anti-correlation). For maps with a coefficient close to 0, the correlation between the map is low. The relationship between the correlation coefficient matrix, R, and the covariance matrix, c, is:
</p>

$$ R_{ij} = {c_{ij} \over \sqrt{c_{ii} * c_{jj}}} $$

#### VIII.4.a) Parameters

```
    ind_maps = [['off', 'charac tot fit: area'],
                ['off', 'fit pars: ampli_0'],
                ['on', 'charac tot fit: area'],
                ['on', 'fit pars: ampli_0']]
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in meas': '',
        'dir path in loop': '',
        'dir path in pars': '',
        'ind maps': ind_maps,
        'mask': None,
        'revert mask': False,
        'show plots': True,
        'save': False,
    }
```

<p align="justify" width="100%">
&#8226 File management: For input, the algorithm requires the directory generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation). It can be supplemented with the respective folders: <code>properties</code> for material properties, <code>nanoloops</code> containing measurements in the form of nanoloops (generated after the first processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a> of the documentation)), and the text file containing measurement and processing parameters, <code>parameters.txt</code>.<br>
&#8226 Measurement selection parameters<br>
&#8226 Mask parameters<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of results. <br>
</p>

<p align="justify" width="100%">
&#8226 For a deeper understanding of the input file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2b---second-step-of-data-analysis">III.2.b) - Second Step of Data Analysis</a> <br>
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

#### VIII.4.b) Correlation matrix

<p align="justify" width="100%">
The <code>gen_correlation_array</code> function in the script takes as input a list of property mappings of the sample. It generates a square matrix filled with zeros, with dimensions equal to the number of mappings in the list. For each combination of pairs of measurements, the Pearson product-moment correlation coefficient is calculated using the <a href="https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html">corrcoef</a> function from NumPy, allowing the completion of the correlation matrix.
</p>

<p align="justify" width="100%">
As for the <code>plot_correlation_table</code> function, it takes as input a correlation matrix and generates a figure of it. A correlation matrix is then displayed with indices corresponding to each of the mappings. A gradual color code is associated with the correlation between them. If the cell tends towards: <br>
&#8226 Red: $R_{ij} \longrightarrow 1$, the two mappings are completely correlated <br>
&#8226 White: $R_{ij} \longrightarrow 0$, the two mappings are not correlated at all <br>
&#8226 Blue: $R_{ij} \longrightarrow -1$, the two mappings are completely anti-correlated <br>
</p>

#### VIII.4.c) Workflow

<p align="justify" width="100%">
The data from <code>properties</code>, constituting the property mappings, is extracted using the <code>extract_properties</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>. <br>
&#8226 When <code>'ind maps'</code> is provided by the user as a list of property names, the functions <code>gen_correlation_array</code> and <code>plot_correlation_table</code> are successively called to perform the analysis on the corresponding mappings. <br>
&#8226 If <code>'ind maps' is None</code>, the <code>correlation_analysis_all_maps</code> function is called to carry out the cross-correlation analysis between all maps. Initially, separated correlation analysis is performed for all off field maps and on field maps for all properties. Here too, the functions <code>gen_correlation_array</code> and <code>plot_correlation_table</code> are used to conduct the analysis. Then, a correlation analysis between off field and on field maps is executed. A correlation matrix is created between each on field and off field mapping (of dimensions 2 times the number of properties), and the corresponding figure is generated using <code>plot_correlation_table</code>.
</p>

#### VIII.4.d) Figures

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/cross_correlation_off_field.PNG> <br>
    <em>Result of cross correlation analysis for all off field material properties (figure generated with <code>plot_correlation_table</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">toolbox/map_correlation.py</a></code> script)</em>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/cross_correlation_off_on_field.PNG> <br>
    <em>Result of cross correlation analysis between all on and off field material properties (figure generated with <code>plot_correlation_table</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">toolbox/map_correlation.py</a></code> script)</em>
</p>

### VIII.5) Pixel extremum

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/sort_plot_pixel.py">toolbox/sort_plot_pixel.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/sort_plot_pixel.py">gui/sort_plot_pixel.py</a></code>. This tool, enables to find the extreme pixel values for a material property and perform analysis on it.
</p>

#### VIII.5.a) Parameters

```
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in meas': '',
        'dir path in loop': '',
        'dir path in pars': '',
        'meas key': {'mode': 'off',
                     'meas': 'charac tot fit: area'},
        'list pixels': None,
        'reverse': False,
        'del 1st loop': True,
        'interp fact': 4,
        'interp func': 'linear',
        'verbose': True,
        'show plots': True,
        'save': False
    }
```

<p align="justify" width="100%">
&#8226 File management: For input, the algorithm requires the directory generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation). It can be supplemented with the respective folders: <code>properties</code> for material properties, <code>nanoloops</code> containing measurements in the form of nanoloops (generated after the first processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iv---first-step-of-data-analysis">IV) - First step of data analysis</a> of the documentation)), and the text file containing measurement and processing parameters, <code>parameters.txt</code>.<br>
&#8226 Measurement selection parameters<br>
&#8226 Pixel selection parameters<br>
&#8226 Loop plotting parameter (<code>del_first_loop</code>)<br>
&#8226 Mask parameters<br>
&#8226 Save and plot parameters: Pertaining to the management of display and the preservation of results. <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the input file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii2b---second-step-of-data-analysis">III.2.b) - Second Step of Data Analysis</a> <br>
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

#### VIII.5.b) Workflow

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/workflow_plot_pixel_extrem.PNG> <br>
    <em>Workflow: Pixel extremum</em>
</p>

<p align="justify" width="100%">
The initial step entails the extraction of properties generated after the second processing step (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi---second-step-of-data-analysis">VI) - Second step of data analysis</a> of the documentation), residing within the folder <code>'properties'</code>, accomplished by the <code>extract_properties</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/file.py">utils/nanoloop_to_hyst/file.py</a></code>. The property selected by the user through the <code>'meas key'</code> parameter, serving as a sorting reference, is then singled out among all others. The extraction of processing and measurement parameters from the file <code>'parameters.txt'</code> is carried out using the <code>extract_params</code> function from the script. The measurement files are then sorted under two scenarios: <br>
&#8226 If the <code>list_pixels</code> parameter is <code>None</code>: based on values of the user-chosen reference property. <br>
&#8226 If the <code>list_pixels</code> parameter is <code>[]</code>: according to the file index. If the list is empty, all pixels are considered; otherwise, only the indices listed are considered.
</p>

<p align="justify" width="100%">
Then, for each of the files:
    <ul>
        <li>If <code>mode = 'on'</code> or <code>mode = 'off'</code>:</li>
            <ul>
                <li>An analysis of the entire file selection is performed using the <code>mean_hyst</code> tool (the main function <code>main_mean_hyst</code> from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_hyst.py">toolbox/mean_hyst.py</a></code> is called). The average hysteresis and properties are then determined (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii3-mean-hysteresis">VIII.3) Mean hysteresis</a> of the documentation).</li>
                <li>The nanoloop of the corresponding file (located in the <code>'nanoloops'</code> folder) is extracted with the <code>extract_nanoloop_data</code> function from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file</a></code>, and the main function <code>main_loop_file_reader</code> from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/loop_file_reader.py">toolbox/loop_file_reader.py</a></code> is utilized to create figures in the form of nanoloops.</li>
                <li>The <code>single_analysis</code> function from the script is called, enabling the extraction of the <code>best_loop</code>, the construction, and analysis of the <code>Hysteresis</code> object (fitting and property extraction).</li>
                <li>A comparative figure between the average hysteresis and that of the respective file is constructed with the <code>plot_comparative_hyst</code> function from the script.</li>
            </ul> <br>
        <li>If <code>mode = 'coupled'</code>:</li>
            <ul>
                <li>For each mode (<code>'on'</code> and <code>'off'</code>): The nanoloop of the corresponding file (located in the <code>'nanoloops'</code> folder) is extracted with the <code>extract_nanoloop_data</code> function from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop/file.py">utils/nanoloop/file.py</a></code>, and the <code>best_loop</code> is extracted with the <code>single_script</code> function from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/data_processing/nanoloop_to_hyst_s2.py">data_processing/nanoloop_to_hyst_s2.py</a></code> (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi2---best-loop">VI.2) - Best loop</a> of the documentation). The main function <code>main_loop_file_reader</code> from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/loop_file_reader.py">toolbox/loop_file_reader.py</a></code> is employed to create figures in the form of nanoloops (see section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#viii1b-loop-file">VIII.1.b) Loop file</a> of the documentation).</li>
                <li>An analysis of the entire file selection is performed using the <code>mean_hyst</code> tool (the main function <code>main_mean_hyst</code> from the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_hyst.py">toolbox/mean_hyst.py</a></code> is called). The differential component and average properties are then determined.</li>
                <li>The <code>differential_analysis</code> function in <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/nanoloop_to_hyst/electrostatic.py">utils/nanoloop_to_hyst/electrostatic.py</a></code> is employed to conduct the differential analysis for the respective file (section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vi4d---differential-analysis-of-on-and-off-field-hysteresis">VI.4.d) - Differential analysis of on and off field hysteresis</a> in the documentation).</li>
                <li>The differential components (average and of the respective file) are determined during the corresponding analysis steps.</li>
            </ul> <br>
        <li>The mapping of the reference property is constructed using the <code>plot_and_save_image</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code>, with the pixel corresponding to the highlighted file (section <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#vii3---figures">VII.3) - Figures</a> in the documentation). A histogram of the reference property is generated, and the value of the property for the respective file is highlighted.</li>
    </ul>
</p>
    
#### VIII.5.c) Figures

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/plot_pixel_extrem_hyst.PNG> <br>
    <em>Comparative analysis between mean and single file hysteresis (figure generated with <code>plot_comparative_hyst</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/sort_plot_pixel.py">toolbox/sort_plot_pixel.py</a></code> script)</em>
</p>

<p align="center" width="100%">
    <img align="center" width="100%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/plot_pixel_extrem_map.PNG> <br>
    <em>Mapping of reference property (hysteresis amplitude) (figure generated with <code>plot_and_save_image</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/map/main.py">utils/map/main.py</a></code> script)</em>
</p>

<p align="center" width="100%">
    <img align="center" width="75%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/plot_pixel_extrem_histo.PNG> <br>
    <em>Histogram of reference property (hysteresis amplitude) (figure generated with <code>main_sort_plot_pixel</code> function of <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/sort_plot_pixel.py">toolbox/sort_plot_pixel.py</a></code> script)</em>
</p>

### VIII.6) SPM converter

<p align="justify" width="100%">
The script can be executed directly using the executable file: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">toolbox/spm_converter.py</a></code> or through the graphical user interface: <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/spm_converter.py">gui/spm_converter.py</a></code>.
</p>

<p align="justify" width="100%">
User parameters:
</p>

```
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'mode': "classic",
        'extension': "txt",
        'verbose': True,
    }
```

<p align="justify" width="100%">
As input, SSPFM datacube measurement folder is selected. A new directory is created (<code>'input_directory_name'_datacube_'extension'</code>), and the csv measurement sheet is copied from the input directory into it. Subsequently, each of the SPM datacube files (Bruker) is read, and its data is extracted (refer to Section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#iii1---input-files">III.1.c) - Extraction</a> in the documentation). The choice of measurement mode is simplified through the <code>'mode'</code> parameter, which offers the following options: <br>
&#8226 <code>'classic'</code> (sweep resonance) <br>
&#8226 <code>'dfrt'</code> <br>
Following this, a corresponding new datacube file is generated, with an extension chosen by the user, and is complemented with the raw data from the input file. The available extensions are: <br>
&#8226 <code>'txt'</code> (created using the <a href="https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html">savetxt</a> function of NumPy library) <br>
&#8226 <code>'csv'</code> (with the pandas library, a <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html">DataFrame</a> object containing the data is created, and the file is saved using the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html">to_csv</a> method) <br>
&#8226 <code>'xlsx'</code> (with the pandas library, a <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html">DataFrame</a> object containing the data is created, and the file is saved using the <a href="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html">to_excel</a> method) <br>
</p>

<p align="center" width="100%">
&#8226 For a deeper understanding of the output file management, please refer to the relevant section in the documentation: <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc#iii2c---toolbox">III.2.c) - Toolbox</a>
</p>

## IX) Overall settings

<p align="justify" width="100%">
General settings are linked to the entire PySSPFM application. They are user-modifiable and can be accessed directly in the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/settings.py">settings.py</a></code> file. A comprehensive description is provided for each setting, along with its default value. A collection of settings facilitates the default path management for saved result files as well as for tests and examples (input and output data). Settings are also provided for the extraction and writing of data from SSPFM files. Some settings are linked to the visualization of figures, while others pertain to various processing stages (fitting methods associated with the <code>minimize</code> function of <a href="https://pypi.org/project/lmfit/">lmfit</a> library, etc.).
</p>

<p align="justify" width="100%">
A second file, <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/default_settings.py">default_settings.py</a></code>, contains the default values for some of the settings found in the initial <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/settings.py">settings.py</a></code> file. Only when an example or test is executed will these default settings take precedence over those from <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/settings.py">settings.py</a></code> file, as they are tailored to the input files (path and data) and treatment on which the examples and tests rely. The <code>get_setting</code> function in the script <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/settings.py">settings.py</a></code> determines whether the execution is from an example or test, or not. Accordingly, it selects the corresponding setting from one of the two dictionaries: the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/settings.py">settings.py</a></code> (<code>setting_dict</code>) or the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/default_settings.py">default_settings.py</a></code> (<code>def_setting_dict</code>). It's crucial not to modify the default values in the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/default_settings.py">default_settings.py</a></code> file, as this could lead to the failure of PySSPFM's example and test executions.
</p>

## X) Core scripts

<p align="justify" width="100%">
The entire assemblage of scripts under the <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/utils/core">core</a></code> umbrella comprises functions that are relatively generic and form the foundation for most of the PySSPFM application scripts. These scripts encompass: <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/basic_func.py">basic_func.py</a></code>, which houses a collection of algebraic models on which the performed fits rely. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/curve_hysteresis.py">curve_hysteresis.py</a></code>, responsible for initializing and processing the <code>Hysteresis</code> object (refer to Section <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/README.md#vi3---hysteresis-and-properties">IV.3) - Hysteresis and properties</a> in the documentation). <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/figure.py">figure.py</a></code>, which facilitates the generation of visual representations in a consistent style. This encompasses the creation of graphs, histograms, and mappings through the functions <code>plot_graph</code>, <code>plot_hist</code>, and <code>plot_map</code>. The <code>print_plots</code> function offers advanced control over the display and storage of visual representations. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/fitting.py">fitting.py</a></code>, which is responsible for executing all fits (excluding hysteresis fitting) based on the <a href="https://lmfit.github.io/lmfit-py/fitting.html">minimize</a> function of <a href="https://pypi.org/project/lmfit/">lmfit</a> library. Fit methods like <code>least_sq</code>, <code>least_square</code> (prioritizing speed), or <code>nelder</code> (prioritizing convergence) can be selected with the <code>fit_method</code> setting. <a href="https://lmfit.github.io/lmfit-py/model.html#lmfit.model.Model">Model</a> and <a href="https://lmfit.github.io/lmfit-py/parameters.html#the-parameters-class">Parameters</a> objects of <a href="https://pypi.org/project/lmfit/">lmfit</a> are likewise employed, respectively, for the amalgamation of model functions (e.g., adding an affine or constant component that may correspond to noise) and for the management of parameter initialization prior to the fitting process (initial value, range of variation, etc.). It includes a parent class <code>CurveFit</code> and three subclasses, namely <code>GaussianPeakFit</code>, <code>ShoPeakFit</code>, and <code>ShoPhaseFit</code>, each built upon the parent class to execute Gaussian, Sho, and Sho phase (arctangent) fitting, respectively. The parent class incorporates a set of methods shared by the subclasses, including <code>eval</code> for evaluating the fitted peak at specified x-values, <code>fit</code>, <code>plot</code>, and more. The subclasses invoke the parent class during initialization and enable parameter initialization for fitting, with model-specific initial guesses. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/iterable.py">iterable.py</a></code> for handling iterables. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/noise.py">noise.py</a></code> for noise management. The <code>filter_mean</code> function serves as a filtering mechanism for averaging, offering a choice of filter order to reduce measurement noise. The <code>noise</code> function is used to generate noise of a specific amplitude (widely employed for examples and tests to recreate the most realistic data) using three distribution models: <code>uniform</code>, <code>normal</code>, and <code>laplace</code>. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/peak.py">peak.py</a></code> contains a set of functions for peak handling. <code>detect_peak</code> and <code>find_peaks</code> automatically identify peaks in an array of values, relying on the <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html#scipy.signal.find_peaks">find_peaks</a> function from the scipy.signal library. It also includes functions for guessing noise components (linear component with <code>guess_affine</code> and constant with <code>guess_bckgnd</code>) and determining peak width with <code>width_peak</code>. <br>
&#8226 <code><a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/utils/core/signal.py">signal.py</a></code> comprises two functions: <code>line_reg</code> for linear regression and <code>interpolate</code> for 1D interpolation. <br>
</p>

<div id="references" style="text-align: justify;">
    <h2>References</h2>
    <span id="ref1">&#8226 [1] Jesse, Stephen, Arthur P. Baddorf, and Sergei V. Kalinin. "Switching Spectroscopy Piezoresponse Force Microscopy of Ferroelectric Materials", Applied Physics Letters 88, 6 (2006), 062908. https://doi.org/10.1063/1.2172216</span><br>
    <span id="ref2">&#8226 [2] : Huang, Boyuan, Ehsan Nasr Esfahani, et Jiangyu Li. « Mapping Intrinsic Electromechanical Responses at the Nanoscale via Sequential Excitation Scanning Probe Microscopy Empowered by Deep Data ». National Science Review 6, no 1 (1 janvier 2019): 55 63. https://doi.org/10.1093/nsr/nwy096.</span><br>
    <span id="ref3">&#8226 [3] : Rodriguez, Brian J, Clint Callahan, Sergei V Kalinin, and Roger Proksch. ‘’Dual-Frequency Resonance-Tracking Atomic Force Microscopy’’ Nanotechnology 18, 47 (2007), 475504. https://doi.org/10.1088/0957-4484/18/47/475504.</span><br>
    <span id="ref4">&#8226 [4] : García-Zaldívar, O., F. Calderón-Piñar, C.J. Diliegros-Godines, et F.J. Flores-Ruiz. « Nanomechanical Measurements of PLZT Ceramic during Switching Events ». Ceramics International 48, nᵒ 7 (avril 2022): 10120‑25. https://doi.org/10.1016/j.ceramint.2021.12.222.</span><br>
    <span id="ref5">&#8226 [5] : Neumayer, Sabine M., Sahar Saremi, Lane W. Martin, Liam Collins, Alexander Tselev, Stephen Jesse, Sergei V. Kalinin, et Nina Balke. « Piezoresponse Amplitude and Phase Quantified for Electromechanical Characterization ». Journal of Applied Physics 128, no 17 (7 novembre 2020): 171105. https://doi.org/10.1063/5.0011631.</span><br>
    <span id="ref6">&#8226 [6] : Neumayer, Sabine M, Sahar Saremi, Lane W Martin, Liam Collins, Alexander Tselev, Stephen Jesse, Sergei V Kalinin, et Nina Balke. « Piezoresponse Phase as Variable in Electromechanical Characterization », s. d., 16.</span><br>
    <span id="ref7">&#8226 [7] : Bradler, Stephan, André Schirmeisen, et Bernhard Roling. « Amplitude Quantification in Contact-Resonance-Based Voltage-Modulated Force Spectroscopy ». Journal of Applied Physics 122, no 6 (14 août 2017): 065106. https://doi.org/10.1063/1.4998435.</span><br>
    <span id="ref8">&#8226 [8] : Balke, Nina, Stephen Jesse, Pu Yu, Ben Carmichael, Sergei V Kalinin, and Alexander Tselev. « Quantification of Surface Displacements and Electromechanical Phenomena via Dynamic Atomic Force Microscopy ». Nanotechnology 27, no 42 (21 octobre 2016): 425707. https://doi.org/10.1088/0957-4484/27/42/425707.</span><br>
    <span id="ref9">&#8226 [9] : Jesse S, Lee HN, Kalinin SV. « Quantitative mapping of switching behavior in piezoresponse force microscopy”. REVIEW OF SCIENTIFIC INSTRUMENTS 77, 073702 2006</span><br>
    <span id="ref10">&#8226 [10] : Kim, Sungho, Daehee Seol, Xiaoli Lu, Marin Alexe, et Yunseok Kim. « Electrostatic-Free Piezoresponse Force Microscopy ». Scientific Reports 7, no 1 (mars 2017): 41657. https://doi.org/10.1038/srep41657.</span><br>
    <span id="ref11">&#8226 [11] : Kalinin, Sergei V., et Dawn A. Bonnell. « Local Potential and Polarization Screening on Ferroelectric Surfaces ». Physical Review B 63, no 12 (13 mars 2001): 125411. https://doi.org/10.1103/PhysRevB.63.125411.</span><br>
    <span id="ref12">&#8226 [12] : Chen, Qian Nataly, Yun Ou, Feiyue Ma, et Jiangyu Li. « Mechanisms of Electromechanical Coupling in Strain Based Scanning Probe Microscopy ». Applied Physics Letters 104, no 24 (16 juin 2014): 242907. https://doi.org/10.1063/1.4884422.</span><br>
    <span id="ref13">&#8226 [13] : Kim, Yunseok, Amit Kumar, Alexander Tselev, Ivan I. Kravchenko, Hee Han, Ionela Vrejoiu, Woo Lee, et al. « Nonlinear Phenomena in Multiferroic Nanocapacitors: Joule Heating and Electromechanical Effects ». ACS Nano 5, no 11 (22 novembre 2011): 9104 12. https://doi.org/10.1021/nn203342v.</span><br>
    <span id="ref14">&#8226 [14] : Yu, Junxi, Ehsan Nasr Esfahani, Qingfeng Zhu, Dongliang Shan, Tingting Jia, Shuhong Xie, et Jiangyu Li. « Quadratic Electromechanical Strain in Silicon Investigated by Scanning Probe Microscopy ». Journal of Applied Physics 123, no 15 (21 avril 2018): 155104. https://doi.org/10.1063/1.5023407</span><br>
    <span id="ref15">&#8226 [15] : Balke, Nina, Stephen Jesse, Qian Li, Petro Maksymovych, M. Baris Okatan, Evgheni Strelcov, Alexander Tselev, et Sergei V. Kalinin. « Current and Surface Charge Modified Hysteresis Loops in Ferroelectric Thin Films ». Journal of Applied Physics 118, no 7 (21 août 2015): 072013. https://doi.org/10.1063/1.4927811.</span><br>
    <span id="ref16">&#8226 [16] : Fernández Garrillo, Pablo A., Benjamin Grévin, Nicolas Chevalier, et Łukasz Borowik. « Calibrated Work Function Mapping by Kelvin Probe Force Microscopy ». Review of Scientific Instruments 89, no 4 (avril 2018): 043702. https://doi.org/10.1063/1.5007619.</span><br>
    <span id="ref17">&#8226 [17] : Goswami, Ankur, Kazi M. Alam, Pawan Kumar, Piyush Kar, Thomas Thundat, et Karthik Shankar. « Mapping the Surface Potential, Charge Density and Adhesion of Cellulose Nanocrystals Using Advanced Scanning Probe Microscopy ». Carbohydrate Polymers 246 (octobre 2020): 116393. https://doi.org/10.1016/j.carbpol.2020.116393.</span><br>
    <span id="ref18">&#8226 [18] : Jungk, T., Á. Hoffmann, et E. Soergel. « Consequences of the Background in Piezoresponse Force Microscopy on the Imaging of Ferroelectric Domain Structures ». Journal of Microscopy 227, no 1 (juillet 2007): 72 78. https://doi.org/10.1111/j.1365-2818.2007.01783.x.</span><br>
    <span id="ref19">&#8226 [19] : Jungk, Tobias, Ákos Hoffmann, et Elisabeth Soergel. « Quantitative Analysis of Ferroelectric Domain Imaging with Piezoresponse Force Microscopy ». Applied Physics Letters 89, no 16 (16 octobre 2006): 163507. https://doi.org/10.1063/1.2362984.</span><br>
    <span id="ref20">&#8226 [20] : Jesse, Stephen, Ho Nyung Lee, et Sergei V. Kalinin. « Quantitative Mapping of Switching Behavior in Piezoresponse Force Microscopy ». Review of Scientific Instruments 77, no 7 (juillet 2006): 073702. https://doi.org/10.1063/1.2214699.</span><br>
    <span id="ref21">&#8226 [21] : Kim, Bora, Daehee Seol, Shinbuhm Lee, Ho Nyung Lee, et Yunseok Kim. « Ferroelectric-like Hysteresis Loop Originated from Non-Ferroelectric Effects ». Applied Physics Letters 109, no 10 (5 septembre 2016): 102901. https://doi.org/10.1063/1.4962387.</span><br>
    <span id="ref22">&#8226 [22] : Thèse - Sergio GONZALEZ CASAL (INL) : Electromechanical control of ferroelectric domains in Pb(Zr,Ti)O3 and BiFeO3 thin films</span><br>
    <span id="ref23">&#8226 [23] : Gautier, Brice, et David Albertini. « Détection et contrôle de la ferroélectricité à l’échelle nanométrique ». Métrologie par imagerie et microscopie, juin 2022. https://doi.org/10.51257/a-v1-r6719</span><br>
    <span id="ref24">&#8226 [24] : Bruker application note : Characterizing Ferroelectric Materials with SS-PFM and DCUBE PFM</span><br>
    <span id="ref25">&#8226 [25] : Alikin, Denis, Alexander Abramov, Anton Turygin, Anton Ievlev, Victoria Pryakhina, Dmitry Karpinsky, Qingyuan Hu, et al. « Exploring Charged Defects in Ferroelectrics by the Switching Spectroscopy Piezoresponse Force Microscopy ». Small Methods 6, no 2 (février 2022): 2101289. https://doi.org/10.1002/smtd.202101289. <br>
</div>
