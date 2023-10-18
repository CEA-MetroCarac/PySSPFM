# PySSPFM

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/logoPySSPFM_white.PNG> <br>
</p>

<p align="justify" width="100%"> 
<strong>PySSFPM</strong> is a specific tool devloped in 
<strong>Py</strong>thon dedicated to perform data analysis on <strong>SSPFM</strong> 
(Switching Spectroscopy Piezoresponse Force Microscopy) measurements
with a GUI that aims to be as simple to use as possible and complete to 
accommodate the user's measurement requirements and conditions. The source code is also easily customizable to meet the user's specific needs. Measurements can be processed in both standard SSPFM mode and in SSPFM + DFRT mode.
</p>

## Important

<p align="justify" width="100%">
This library is provided in its current state and remains under active development. It was initially developed from reverse engineering of the Python-based SSPFM measurement processing code originally developed by Bruker. The motivation behind the creation of a new application for SSPFM measurement processing stemmed from several factors : 
</p>

<p align="justify" width="100%">
&#8226; The original code proved to be incompatible with the measurement files (.spm from Bruker) of the library's developer.
</p>

<p align="justify" width="100%">
&#8226; There was a desire to offer the scientific community in the PFM domain an open-source solution that is easily comprehensible, adaptable, and customizable according to individual requirements.
</p>

<p align="justify" width="100%">
&#8226; PySSPFM has been developed with the aim of achieving the most quantitative, comprehensive, and advanced measurement processing compared to other existing solutions.
</p>

<p align="justify" width="100%">
However, while it has shown reliable performance with the data used by the 
library's developer, it's crucial to emphasize that there are no assurances 
that this library will seamlessly process your unique data.
Moreover,  it should be noted that in order to extract data from a Bruker 
SPM file, DLL files must be installed alongside the Nanoscope Analysis 
software (Bruker).
</p>

If you encounter any bugs or issues, you can kindly bring them to the developer's attention by visiting: [PySSPFM issues](https://github.com/CEA-MetroCarac/PySSPFM/issues)

## Overview

<p align="center" width="100%">
    <img align="center" width=80%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20worflow.PNG> <br>
    <em>PySSPFM workflow</em>
</p>

### 0) Measures
<p align="justify" width="100%">
PySSPFM facilitates the processing of a set 
of SSPFM measurement 
data points by simply populating a measurement form (insert the templates). The range of measurement files to be processed may have the extensions:
</p>

* `.spm` (Bruker)
* `.txt`
* `.csv`
* `.xlsx`

### 1) First step of data analysis
<p align="justify" width="100%">
For each of the SSPFM measurement files, amplitude and phase SSPFM 
measurements are extracted for each segment using a user-selected method:
</p>

* `max`: extract maximum or resonance peak (for frequency sweep mode)
* `fit`: perform a fit of the resonance peak based on `SHO` model (for frequency sweep mode)
* `dfrt`: mean of the segment (for dfrt mode)

### 2) Second step of data analysis
<p align="justify" width="100%">
The measurements are then automatically calibrated, and the piezoresponse hysteresis is created. It is subsequently fitted using an algorithm based on the lmfit library, and the piezoelectric and ferroelectric properties are extracted. Five different artifact decorrelation protocols (quadratic components: electrostatic, electrostrictive, and Joule effects) allow for obtaining quantitative piezoelectric and ferroelectric measurements and for acquiring a more comprehensive understanding of material properties, such as the contact surface potential.
</p>

### 3) Mapping
<p align="justify" width="100%">
Once the processing is complete for all the files, maps are generated. 2D 
interpolation tools and masks to mitigate the influence of problematic pixels are also available.
</p>

### 4) Toolbox
<p align="justify" width="100%">
Finally, a toolbox is provided for the analysis of processing results: it 
includes algorithms of:
</p>

* `Machine learning (K-Means)`
* `Phase separation`
* `Mapping cross-correlation`
* `SPM file converter`
* `Viewers`
* `...`

## Usage

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20main%20GUI.PNG> <br>
    <em>PySSPFM GUI main window</em>
</p>

All code executed and parameter adjustments made through the [GUI](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui) can be replicated in executable scripts:
* [Data Processing](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/data_processing)
* [Toolbox](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/toolbox)

You can check the [examples](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/examples) to grasp the utilization of the scripts, and the [tests](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests) to ensure the proper functioning of the scripts.

See the [documentation](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc) for more details on PySSPFM usage.

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

`pytest` to run [tests](https://github.com/CEA-MetroCarac/PySSPFM/tree/main/tests) python files: 

## Citing

In the case you use this library for your work, please think about citing it:
* DOI (to come)
* Hugo Valloire, Patrick Quemere, 2023, November 28, PySSPFM (Version 2023.10).
