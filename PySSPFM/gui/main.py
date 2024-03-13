"""
--> Executable Script
Main graphical interface (window) of PySSPFM: call all other exe of PySSPFM
"""

from tkinter import ttk

from PySSPFM.gui.datacube_to_nanoloop_s1 import main as main_data_proc_1
from PySSPFM.gui.nanoloop_to_hyst_s2 import main as main_data_proc_2
from PySSPFM.gui.global_map_reader import main as main_tool_1_a
from PySSPFM.gui.list_map_reader import main as main_tool_1_b
from PySSPFM.gui.loop_file_reader import main as main_tool_1_c
from PySSPFM.gui.raw_file_reader import main as main_tool_1_d
from PySSPFM.gui.spm_data_extractor import main as main_tool_1_e
from PySSPFM.gui.phase_offset_analyzer import main as main_tool_2_a
from PySSPFM.gui.map_correlation import main as main_tool_3_a
from PySSPFM.gui.curve_clustering import main as main_tool_3_b
from PySSPFM.gui.mean_hyst import main as main_tool_3_c
from PySSPFM.gui.sort_plot_pixel import main as main_tool_3_d
from PySSPFM.gui.spm_converter import main as main_tool_4_a
from PySSPFM.gui.meas_sheet_generator import main as main_tool_4_b
from PySSPFM.gui.utils import \
    add_section_separator, init_main_wdw, create_section


def main():
    """
    Main function for creating the main interface.

    Returns
    -------
    None
    """

    root = init_main_wdw(wdw_title="Main Interface")

    # Main title
    title_label = ttk.Label(root, text="PySSPFM: Main Interface",
                            font=("Helvetica", 16))
    title_label.pack(pady=10)
    add_section_separator(root)

    # Data processing section
    labels = ["Processing Step 1", "Processing Step 2"]
    functions = [main_data_proc_1, main_data_proc_2]
    strg_title = "SSPFM data processing from raw sspfm files in two steps"
    strg_functions = [
        "Step 1: datacube to nanoloop:\n"
        "PFM amplitude and phase are extracted for each segment, "
        "piezoresponse nanoloops are constructed from these points",
        "Step 2: nanoloop to hyst:\n"
        "piezoresponse nanoloops are extracted to construct hysteresis which "
        "are fitted to extract sample properties",
    ]
    create_section(root, "Data processing", labels, functions,
                   strg_title=strg_title, strg_functions=strg_functions)

    # Toolbox - 1 - Readers
    labels = ["Global map", "List map", "Loop file", "Raw file",
              "SPM data extractor"]
    functions = [main_tool_1_a, main_tool_1_b, main_tool_1_c,
                 main_tool_1_d, main_tool_1_e]
    strg_title = "Readers are usefull to create figures or extract sspfm data"
    strg_functions = [
        "Generate all sspfm maps of sample properties\n"
        "- Generate all sspfm maps from extraction of sample properties "
        "in txt files",
        "Module used to generate sspfm maps of selected sample properties\n"
        "- Generate multi sspfm maps from extraction of sample properties"
        " in txt files",
        "Extraction and visualisation of .txt file data of local nanoloops "
        "of the sample surface",
        "Viewing of raw signal of a sspfm file in a graphic",
        "Extract all the data contained in an SPM file",
    ]
    create_section(root, "Toolbox - 1 - Readers", labels, functions,
                   strg_title=strg_title, strg_functions=strg_functions)

    # Toolbox - 2 - Phase tools
    labels = ["Phase offset analyzer"]
    functions = [main_tool_2_a]
    strg_title = "Phase tools allow to perform phase analysis on sspfm " \
                 "measurement"
    strg_functions = [
        "Automatic determination of phase offset for a list of raw sspfm "
        "measurement file"
    ]
    create_section(root, "Toolbox - 2 - Phase tools", labels,
                   functions, strg_title=strg_title,
                   strg_functions=strg_functions)

    # Toolbox - 3 - Map / multi-loop tools
    labels = ["Map correlation", "Curve clustering", "Mean hysteresis",
              "Sort and plot pixel"]
    functions = [main_tool_3_a, main_tool_3_b, main_tool_3_c,
                 main_tool_3_d]
    strg_title = "Map and multi-loop tools allow to go deeper into sspfm " \
                 "measurement analysis by trying to identify and separate " \
                 "phases, determining origins of contrast mapping ..."
    strg_functions = [
        "Cross correlation coefficient analysis for sspfm maps\n"
        "- Generate cross correlation coefficient array between a selected "
        "set of sample properties in order to determine origins of contrast "
        "mapping",
        "Clustering with machine learning approach (K-Means) of curve:\n"
        "- Perform a clustering analysis (K-Means) for all best hysteresis "
        "(for each pixel, one hysteresis for each mode) of a sspfm measurement "
        "in order to separate phases and different physical signal "
        "contributions.\n"
        "Curves can be generated using one or more measurements, including "
        "piezoresponse, amplitude, phase, resonance frequency, or "
        "quality factor.",
        "Perform mean of hysteresis loops (on / off / coupled) by reading a "
        "set of txt file nanoloops defined by the user",
        "Find extremum value of sspfm map of a property and "
        "plot hysteresis of associated files"
    ]
    create_section(root, "Toolbox - 3 - Map / multi-loop tools", labels,
                   functions, strg_title=strg_title,
                   strg_functions=strg_functions)

    # Toolbox - 4 - File management
    strg_title = "File management tools allow to manipulate sspfm data files " \
                 "or measurement sheet based on data extraction of SPM files."
    strg_functions = [
        "Conversion of raw_data.spm (sspfm datacube file) to raw_data.txt",
        "Generate a CSV measurement sheet from a model and SSPFM raw file "
        "data extraction",
    ]
    create_section(root, "Toolbox - 4 - File management",
                   ["SPM converter", "Measurement sheet generator"],
                   [main_tool_4_a, main_tool_4_b], strg_title=strg_title,
                   strg_functions=strg_functions)

    def quit_application():
        root.quit()

    # Exit button
    quit_button = ttk.Button(root, text="Exit", command=quit_application)
    quit_button.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    main()
