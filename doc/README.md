# PySSPFM Documentation

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/logoPySSPFM_white.PNG> <br>
</p>

## Introduction

Insérer le workflow et le file management overview

L'application PySSPFM se décompose en deux étapes de traitements des mesures et une toolbox qui permet d'effectuer des traitements supplémenaires.

## GUI

<p align="justify" width="100%"> 
The graphical user interface <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">codes</a> have been crafted using the <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a> library. The <a href="https://pypi.org/project/Pillow">PIL library</a> is employed to open and display the application's logo and icon on the graphical interfaces.
</p>

### Main window

<p align="center" width="100%">
    <img align="center" width="30%" src=https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/PySSPFM%20main%20GUI.PNG> <br>
    <em>PySSPFM GUI main window</em>
</p>

The graphical user interface of the main window constitutes the menu of the PySSPFM application. It can be launched directly from the <a href="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/PySSPFM/gui/main.py">interface code</a> or from the PySSPFM.exe file. It encompasses an array of buttons, each corresponding to an executable script. A secondary window is subsequently opened for the selected script. The interface can be closed either using the <img src="https://github.com/CEA-MetroCarac/PySSPFM/blob/main/doc/_static/Exit%20Button.PNG" width="60"> button or the close button in the upper right corner.
 
### Secondary window

L'interface graphique de la fenêtre secondaire est propre à chacun des scripts python excécutables en question et constitue leur menu spécifique.
Elle peut être lancée directement à partir du code de l'interface en question ou à partir du menu principal.
La plupart du temps, elles contiennent, une première section de file management pour sélectionner le chemin des fichiers d'entrée et de sortie, avec un bouton browse ou select pour choisir de manière intéractive le chemin dans l'explorateur de fichier. Dans la plupart des cas, une fois le chemin d'entrée sélectionné, les chemins en sortie sont remplis automatiquement en fonction du path management par défaut. Cependant, le chemin peut être modifiable.
Ensuite des sections sont attribués aux paramètres propres à l'étape du traitement. En fonction du type de variable, le paramètre peut être rensigné dans un champ, par un checkbutton, une jauge etc. L'utilisateur est guidé grâce à une aide lorsque la souris est passée sur le bouton. Le nom du paramètre, une description résumée et globale ainsi que ses valeurs possibles et ses conditions d'activation sont rensignées.
Enfin, dans la plupart des cas, une dernière section permet à l'utilisateur de choisir si'l souhaite afficher les résultats du traitement dans la console (verbose), afficher à l'écran les figures (show plots) ou encore les sauvegarder (save).
Le traitement peut être exécuté grâce au bouton "Start" et l'interface contient aussi un bouton "Exit".

## Input file

### Datacube files

### Measurement sheet

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

