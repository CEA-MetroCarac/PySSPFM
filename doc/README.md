# PySSPFM Documentation

## Introduction

Insérer le workflow et le file management overview

L'application PySSPFM se décompose en deux étapes de traitements des mesures et une toolbox qui permet d'effectuer des traitements supplémenaires.

## GUI

<p align="justify" width="100%"> 
Les codes <a href="https://github.com/CEA-MetroCarac/PySSPFM/tree/main/PySSPFM/gui">d'interface graphique</a> on été développés avec la librairie <a href="https://docs.python.org/fr/3/library/tkinter.html">Tkinter</a>. La librairie <a href="https://pypi.org/project/Pillow">PIL</a> est utilisée pour ouvrir et afficher le logo et l'icone de l'application sur les interfaces graphiques.
</p>

### Main window

L'interface graphique de la fenêtre principale constitu le menu de l'application PySSPFM. 
Elle peut être lancée directement à partir du code de l'interface ou à partir du fichier PySSPFM.exe.
Elle contient un ensemble de boutons, pour chacun des scripts exécutables. Une fenêtre secondaire est alors ouverte pour le script en question.
L'interface peut être fermée par le bouton "Exit" ou par la croix en haut à droite.
 
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

