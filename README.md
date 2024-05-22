# PySSPFM

<p align="center" width="100%">
    <img align="center" width="70%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/circular_diagram.png> <br>
</p>

<p align="justify" width="100%"> 
<strong>PySSFPM</strong> is a specific tool developed in 
<strong>Py</strong>thon dedicated to perform data analysis on <strong>SSPFM</strong> (Switching Spectroscopy Piezoresponse Force Microscopy) measurements with a GUI that aims to be as simple to use as possible and complete to accommodate the user's measurement requirements and conditions. The source code was developed to be easily customizable in order to meet the user's specific needs. Measurements can be processed in both standard SSPFM including fixed-frequency measurements on or off resonance, or with frequency sweeping to reconstruct the resonance peak, as well as SSPFM-DFRT (Dual Frequency Resonance Tracking) mode.
</p>

## Important

<p align="justify" width="100%">
This library is provided in its current state and remains under active development. The motivation behind the creation of the new PySSPFM application for SSPFM measurement processing stemmed from several factors : 
</p>

<p align="justify" width="100%">
&#8226; The original code we used (developped by Bruker) proved to be incompatible with the measurement files (.spm from Bruker) of the library's developer.
</p>

<p align="justify" width="100%">
&#8226; There was a desire to offer the scientific community in the PFM domain an open-source solution that is easily comprehensible, adaptable, and customizable according to individual requirements. All developments adhere to the PEP-8 development standard and are accompanied by comprehensive, internal script documentation.
</p>

<p align="justify" width="100%">
&#8226; PySSPFM has been developed with the aim of achieving the most quantitative and advanced measurement processing compared to other existing solutions.
</p>

<p align="justify" width="100%">
However, while it has shown reliable performance with the data used by the library's developer, it's crucial to emphasize that there are no assurances that this library will seamlessly process your unique data. Moreover,  it should be noted that in order to extract data from a Bruker SPM file, DLL (Dynamic Link Library) files must be installed alongside the Nanoscope Analysis software (Bruker).
</p>

<p align="justify" width="100%">
If you encounter any bugs or issues, you can kindly bring them to the developer's attention by visiting: <a href="https://github.com/CEA-MetroCarac/PySSPFM/issues">PySSPFM issues</a>.
</p>

## Overview

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/scheme_workflow_pysspfm.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

### 0) Measures
<p align="justify" width="100%">
PySSPFM facilitates the processing of a set of SSPFM measurement data points by simply populating a measurement form (template for: <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/resources/measurement%20sheet%20model%20SSPFM.csv">measurement sheet model SSPFM</a>). The range of measurement files to be processed may have the extensions: <br>
&#8226 <code>.spm</code> (Bruker) <br>
&#8226 <code>.txt</code> <br>
&#8226 <code>.csv</code> <br>
&#8226 <code>.xlsx</code> <br>
</p>

### 1) First step of data analysis
<p align="justify" width="100%">
For each of the SSPFM measurement files, amplitude and phase are extracted for each segment using a user-selected method: <br>
&#8226 <code>max</code>: extract maximum or resonance peak (for frequency sweep mode) <br>
&#8226 <code>fit</code>: perform a fit of the resonance peak based on SHO (Simple Harmonic Oscillator) model (for frequency sweep mode) <br>
&#8226 <code>single_freq</code>: mean of the segment (for single frequency mode, in or out of resonance) <br>
&#8226 <code>dfrt</code>: mean of the segment (for DFRT mode) <br>
</p>

### 2) Second step of data analysis
<p align="justify" width="100%">
The measurements are then automatically calibrated, and the piezoresponse hysteresis is created. It is subsequently fitted using an algorithm based on the <a href="https://pypi.org/project/lmfit/">lmfit</a> library, and the piezoelectric and ferroelectric properties are extracted. Five different artifact decorrelation protocols (quadratic components: electrostatic, electrostrictive, and joules effects) allow for obtaining quantitative piezoelectric and ferroelectric measurements and for acquiring a more comprehensive understanding of material properties, such as the contact surface potential.
</p>

### 3) Mapping
<p align="justify" width="100%">
Once the processing is complete for all the files, maps are generated. 2D interpolation tools and masks to mitigate the influence of problematic pixels are also available.
</p>

### 4) Toolbox
<p align="justify" width="100%">
Finally, a toolbox is provided for the analysis of processing results: it 
includes algorithms of:
</p>

<p align="justify" width="100%">
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/curve_clustering.py">Machine learning (K-Means)</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/mean_hyst.py">Phase separation</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/map_correlation.py">Mapping cross-correlation</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/toolbox/spm_converter.py">SPM file converter</a> <br>
&#8226 ...
</p>

<p align="justify" width="100%">
See the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc">documentation</a> for more details on PySSPFM workflow.
</p>

## Usage

<p align="center" width="100%">
    <img align="center" width="15%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/gui_main.PNG> <br>
    <em>PySSPFM GUI main window</em>
</p>

<p align="justify" width="100%">
All code executed and parameter adjustments made through the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">GUI</a> can be replicated in executable scripts: <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing">Data Processing</a> <br>
&#8226 <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox">Toolbox</a> <br>
Then, user can adjust parameters directly either in a pre-filled json file, in a toml file or in the excecutable python code.
</p>

<p align="justify" width="100%">
You can check the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples">examples</a> (based on both real and simulated SSPFM measurements) to grasp the utilization of the scripts, and the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests">tests</a> to ensure the proper functioning of the scripts. The examples and tests follow the same directory structure as the main PySSPFM scripts.
</p>

<p align="justify" width="100%">
See the <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc">documentation</a> for more details on PySSPFM usage.
</p>

## Installation

### From PyPI

```bash
pip install PySSPFM
```
### From GitHub

#### With poetry

```bash
poetry add git+https://github.com/CEA-MetroCarac/PySSPFM.git
```

#### With pip

```bash
pip install git+https://github.com/CEA-MetroCarac/PySSPFM.git
```

### Optional dependencies

<p align="justify" width="100%">
&#8226 <a href="https://pypi.org/project/pytest/">pytest</a> to run <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests">tests</a> python files. <br>
&#8226 <a href="https://pypi.org/project/toml/">toml</a> to load user parameters directly from toml file, for excecutable python script. <br>
&#8226 Nanoscope Analysis software (Bruker) installed on computer to extract data from SSPFM Bruker measurement files (spm extension).
</p>

## Citing

<p align="justify" width="100%">
In the case you use this library for your work, please think about citing it: <br>
&#8226 DOI: <a href="https://doi.org/10.1063/5.0197226">https://doi.org/10.1063/5.0197226</a> <br>
&#8226 Hugo Valloire, Patrick Quemere, 2024, May 22, PySSPFM (Version 2024.06).
</p>

