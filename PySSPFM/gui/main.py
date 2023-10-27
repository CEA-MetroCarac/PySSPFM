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
from PySSPFM.gui.map_correlation import main as main_tool_2_a
from PySSPFM.gui.hysteresis_clustering import main as main_tool_2_b
from PySSPFM.gui.mean_hyst import main as main_tool_2_c
from PySSPFM.gui.sort_plot_pixel import main as main_tool_2_d
from PySSPFM.gui.spm_converter import main as main_tool_3_a
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
        "Step 1: seg to loop:\n"
        "PFM amplitude and phase are extracted for each segment, "
        "piezoresponse nanoloops / hysteresis are constructed from these "
        "points",
        "Step 2: hyst to map:\n"
        "piezoresponse nanoloops / hysteresis are fitted to extract "
        "ferroelectric measurement and are plotted it in map",
    ]
    create_section(root, "Data processing", labels, functions,
                   strg_title=strg_title, strg_functions=strg_functions)

    # Toolbox - 1 - Readers
    labels = ["Global map", "List map", "Loop file", "Raw file"]
    functions = [main_tool_1_a, main_tool_1_b, main_tool_1_c,
                 main_tool_1_d]
    strg_title = "Readers are usefull to create figures of sspfm results"
    strg_functions = [
        "Generate all sspfm maps of ferroelectric sample properties\n"
        "- Generate all sspfm maps from extraction of ferroelectric "
        "measurements in txt files",
        "Module used to generate sspfm maps of selected ferroelectric "
        "measurements\n"
        "- Generate multi sspfm maps from extraction of ferroelectric "
        "measurements in txt files",
        "Extraction and visualisation of .txt file datas of local hysteresis "
        "of the sample surface",
        "Viewing of raw signal of a sspfm file in a graphic",
    ]
    create_section(root, "Toolbox - 1 - Readers", labels, functions,
                   strg_title=strg_title, strg_functions=strg_functions)

    # Toolbox - 2 - Map / multi-loop tools
    labels = ["Map correlation", "Hysteresis clustering", "Mean hysteresis",
              "Plot sort pixel"]
    functions = [main_tool_2_a, main_tool_2_b, main_tool_2_c,
                 main_tool_2_d]
    strg_title = "Map and multi-loop tools allow to go deeper into sspfm " \
                 "measurement analysis by trying to identify and separate " \
                 "phases, determining origins of contrast mapping ..."
    strg_functions = [
        "Cross correlation coefficient analysis for sspfm maps\n"
        "- Generate cross correlation coefficient array between a selected "
        "set of ferroelectric measurements in order to determine origins "
        "of contrast mapping",
        "Clustering with machine learning approach (K-Means) of hysteresis:\n"
        "- Perform a clustering analysis (K-Means) for all best hysteresis "
        "(for each pixel, one hysteresis for each mode) of a sspfm measurement "
        "in order to separate phases and different physical signal "
        "contributions",
        "Perform mean of hysteresis loops (on / off / coupled) by reading a "
        "set of txt file loops defined by the user",
        "Find extremum value of sspfm map of a measurement and "
        "plot hysteresis of associated files"
    ]
    create_section(root, "Toolbox - 2 - Map / multi-loop tools", labels,
                   functions, strg_title=strg_title,
                   strg_functions=strg_functions)

    # Toolbox - 3 - File management
    strg_title = "File management tools allow to manipulate sspfm data files."
    strg_functions = [
        "Conversion of raw_datas.spm (sspfm datacube file) to raw_datas.txt"
    ]
    create_section(root, "Toolbox - 3 - File management", ["SPM converter"],
                   [main_tool_3_a], strg_title=strg_title,
                   strg_functions=strg_functions)

    def quit_application():
        root.quit()

    # Exit button
    quit_button = ttk.Button(root, text="Exit", command=quit_application)
    quit_button.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    main()
