"""
--> Executable Script
Graphical interface for vector clustering
 (run vector_clustering.main_vector_clustering)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from PySSPFM.settings import get_setting
from PySSPFM.toolbox.vector_clustering import \
    main_vector_clustering as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title)
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def main(parent=None):
    """
    Create a graphical user interface for input parameters.

    Parameters
    ----------
    parent : tk.Tk or tk.Toplevel, optional
        The parent window, if provided, creates a secondary window.

    Returns
    -------
    None
    """
    # Create the main or secondary window
    title = "Vector clustering"
    app = init_secondary_wdw(parent=parent, wdw_title=title)

    default_user_pars = {'object': 'loop',
                         'relative': False,
                         'pca': True,
                         'method': 'kmeans'}
    default_loop_pars = {'label meas': ['piezoresponse'],
                         'nb clusters off': 4,
                         'nb clusters on': 4,
                         'nb clusters coupled': 4}
    default_curve_pars = {'extension': 'spm',
                          'mode': 'classic',
                          'label meas': ['deflection'],
                          'nb clusters': 4}

    # Set default parameter values
    default_parameters = {
        'dir path in': '',
        'dir path in prop': '',
        'dir path out': '',
        'user_pars': default_user_pars,
        'loop_pars': default_loop_pars,
        'curve_pars': default_curve_pars,
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_params = {
            'object': object_var.get(),
            'relative': relative_var.get(),
            'pca': pca_var.get(),
            'method': method_var.get()
        }
        loop_params = {
            'label meas': extract_var(label_meas_loop_var),
            'nb clusters off': clust_off_var.get(),
            'nb clusters on': clust_on_var.get(),
            'nb clusters coupled': clust_coupled_var.get()
        }
        curve_params = {
            'extension': extension_var.get(),
            'mode': mode_var.get(),
            'label meas': extract_var(label_meas_curve_var),
            'nb clusters': clust_var.get()
        }
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path in prop'] = extract_var(dir_path_prop_var)
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters["user_pars"] = user_params
        user_parameters["loop_pars"] = loop_params
        user_parameters["curve_pars"] = curve_params
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Create out directory if not exist
        if user_parameters['save'] is True:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Data analysis
        start_time = datetime.now()
        main_script(user_parameters["user_pars"],
                    user_parameters["loop_pars"],
                    user_parameters["curve_pars"],
                    user_parameters['dir path in'],
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dir_path_out=user_parameters['dir path out'],
                    dir_path_in_props=user_parameters['dir path in prop'])

        # Save parameters
        if user_parameters['save']:
            save_user_pars(
                user_parameters, user_parameters['dir path out'],
                start_time=start_time, verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_prop():
        dir_path_prop = filedialog.askdirectory()
        dir_path_prop_var.set(dir_path_prop)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Vector clustering
    wdw_main_title(app, title)

    row = 3

    # Section title: File management
    label_file = ttk.Label(app, text="File management", font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # Directory (in)
    label_in = ttk.Label(app, text="Directory (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    dir_path_in_var = tk.StringVar()
    dir_path_in_var.set(user_parameters['dir path in'])
    entry_in = ttk.Entry(app, textvariable=dir_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in\n" \
           "- Summary: Input Directory for Vector Files " \
           "(default: 'best_nanoloops')\n" \
           "- Description: This parameter specifies the directory path for " \
           "the vector files, to perform clustering analysis.\n" \
           "- Value: String representing the directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="vector_clustering", lvl=1, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input properties directory path
    def generate_default_input_props_dir(input_dir):
        properties_folder_name = get_setting('default_properties_folder_name')
        if input_dir != "":
            root, _ = os.path.split(input_dir)
            input_props_dir = os.path.join(root, properties_folder_name)
        else:
            input_props_dir = ""
        return input_props_dir

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Function to update the default input properties dir path when input
    # dir changes
    def update_default_input_props_dir():
        input_dir = dir_path_in_var.get()
        def_input_props_dir = generate_default_input_props_dir(input_dir)
        dir_path_prop_var.set(def_input_props_dir)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind the function (input prop dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_props_dir())

    # Directory properties (in)
    default_input_dir = dir_path_in_var.get()
    default_input_props_dir = generate_default_output_dir(default_input_dir)
    label_prop = ttk.Label(app, text="Directory properties (in) (*):")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    dir_path_prop_var = tk.StringVar()
    dir_path_prop_var.set(default_input_props_dir)
    entry_prop = ttk.Entry(app, textvariable=dir_path_prop_var)
    row = grid_item(entry_prop, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_prop\n" \
           "- Summary: Properties files directory " \
           "(optional, default: properties)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the properties files.\n" \
           "For loop clustering : text file generated after the 2nd step of " \
           "the analysis.\n" \
           "For curve clustering : CSV measurement file " \
           "(measurement sheet model).\n" \
           "- Value: It should be a string representing a directory path."
    entry_prop.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_prop, mess))
    browse_button_prop = ttk.Button(app, text="Browse", command=browse_dir_prop)
    row = grid_item(browse_button_prop, row, column=2)

    # Directory (out)
    default_input_dir = dir_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_dir)
    label_out = ttk.Label(app, text="Directory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    dir_path_out_var.set(default_output_dir)
    entry_out = ttk.Entry(app, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for analysis results figures " \
           "(optional, default: toolbox directory in the same root)\n" \
           "- Description: This parameter specifies the directory where the " \
           "figures generated as a result of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(app, text="Select", command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(app, row=row)

    # Section title: Common parameters
    label_common = ttk.Label(app, text="Common parameters",
                             font=("Helvetica", 14))
    row = grid_item(label_common, row, column=0, sticky="ew", columnspan=3)
    strg = "These parameters are always active and are common."
    label_common.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_common, mess))

    # Object
    label_object = ttk.Label(app, text="Object:")
    row = grid_item(label_object, row, column=0, sticky="e", increment=False)
    object_var = ttk.Combobox(app, values=["loop", "curve"])
    object_var.set(user_parameters['user_pars']['object'])
    row = grid_item(object_var, row, column=1, sticky="ew")
    strg = "- Name: object\n" \
           "- Summary: Name of the object processed with clustering " \
           "analysis.\n" \
           "- Description: This parameter determines the name of the object " \
           "used to perform the clustering.\n" \
           "Implemented objects are Loops (best nanoloops associated with " \
           "each pixel) or Curves (raw SSPFM measurements associated with " \
           "each pixel).\n" \
           "- Value: A string with two possible values:\n" \
           "\t--> 'loop': Loop clustering\n" \
           "\t--> 'curve': Curve clustering"
    object_var.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(object_var, mess))

    # Relative
    label_relative = ttk.Label(app, text="Relative:")
    row = grid_item(label_relative, row, column=0, sticky="e", increment=False)
    relative_var = tk.BooleanVar()
    relative_var.set(user_parameters['user_pars']['relative'])
    chck_relative = ttk.Checkbutton(app, variable=relative_var)
    row = grid_item(chck_relative, row, column=1, sticky="w")
    strg = "- Name: relative\n" \
           "- Summary: Activation key for relative clustering analysis.\n" \
           "- Description: This parameter serves as an activation key to " \
           "perform clustering analysis on relative vectors (all vectors " \
           "vary between 0 and 1). Always active for combined vectors of " \
           "multiple measurements.\n" \
           "- Value: Boolean (True or False)."
    chck_relative.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(chck_relative, mess))

    # PCA
    label_pca = ttk.Label(app, text="PCA:")
    row = grid_item(label_pca, row, column=0, sticky="e", increment=False)
    pca_var = tk.BooleanVar()
    pca_var.set(user_parameters['user_pars']['pca'])
    chck_pca = ttk.Checkbutton(app, variable=pca_var)
    row = grid_item(chck_pca, row, column=1, sticky="w")
    strg = "- Name: pca\n" \
           "- Summary: Activation key for performing PCA before clustering " \
           "analysis.\n" \
           "- Description: This parameter serves as an activation key to " \
           "perform PCA (Principal Component Analysis) before clustering " \
           "analysis.\n" \
           "- Value: Boolean (True or False)."
    chck_pca.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(chck_pca, mess))

    # Method
    label_method = ttk.Label(app, text="Method:")
    row = grid_item(label_method, row, column=0, sticky="e", increment=False)
    method_var = ttk.Combobox(app, values=["kmeans", "gmm"])
    method_var.set(user_parameters['user_pars']['method'])
    row = grid_item(method_var, row, column=1, sticky="ew")
    strg = "- Name: method\n" \
           "- Summary: Name of the method used to perform the clustering.\n" \
           "- Description: This parameter determines the method used to " \
           "perform the clustering. Implemented methods are K-Means or " \
           "Gaussian Mixture Model. (GMM).\n" \
           "- Value: A string with two possible values:\n" \
           "\t--> 'kmeans': K-Means clustering\n" \
           "\t--> 'gmm': Gaussian Mixture Model clustering"
    method_var.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(method_var, mess))
    row = add_grid_separator(app, row=row)

    # Section title: Loop parameters
    label_loop_meas = ttk.Label(app, text="Loop parameters",
                                font=("Helvetica", 14))
    row = grid_item(label_loop_meas, row, column=0, sticky="ew", columnspan=3)
    strg = "These parameters are common to a loop object process.\n" \
           "Active if: object is 'loop'"
    label_loop_meas.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_loop_meas, mess))

    # Measure
    label_name_loop = ttk.Label(app, text="Name(s):")
    row = grid_item(label_name_loop, row, column=0, sticky="e", increment=False)
    label_meas_loop_var = tk.StringVar()
    label_meas_loop_var.set(str(user_parameters['loop_pars']['label meas']))
    entry_label_meas_loop = ttk.Entry(app, textvariable=label_meas_loop_var)
    row = grid_item(entry_label_meas_loop, row, column=1, sticky="ew")
    strg = "- Name: label_meas\n" \
           "- Summary: List of Measurement Name for Loops\n" \
           "- Description: This parameter contains a list of measurement " \
           "name in order to create the loop to be analyzed using a machine " \
           "learning algorithm of clustering.\n" \
           "If several name are filled, the loop will be normalized and " \
           "concatenated.\n" \
           "Choose from : piezoresponse, amplitude, phase, res freq " \
           "and q fact\n" \
           "- Value: A list containing strings.\n" \
           "\t- For example: ['piezoresponse'] or ['amplitude', 'phase']"
    entry_label_meas_loop.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_label_meas_loop, mess))

    # Function to update the label text when the slider is moved
    def update_nb_clusters_off(_):
        clust_off_label.config(text=str(clust_off_var.get()))

    # Function to update the label text when the slider is moved
    def update_nb_clusters_on(_):
        clust_on_label.config(text=str(clust_on_var.get()))

    # Function to update the label text when the slider is moved
    def update_nb_clusters_coupled(_):
        clust_coupled_label.config(text=str(clust_coupled_var.get()))

    # Nb clusters (off)
    label_off = ttk.Label(app, text="Nb clusters (off):")
    row = grid_item(label_off, row, column=0, sticky="e", increment=False)
    clust_off_var = \
        tk.IntVar(value=user_parameters['loop_pars']['nb clusters off'])
    scale_off = ttk.Scale(app, from_=1, to=30, variable=clust_off_var,
                          orient="horizontal", length=30,
                          command=update_nb_clusters_off)
    row = grid_item(scale_off, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_off\n" \
           "- Summary: Number of Clusters for Off Field Loop\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the off-field loop. " \
           "Machine learning algorythm of clustering\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the off-field loop.\n" \
           "- Active if: Used in the analysis of off-field loop."
    scale_off.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(scale_off, mess))
    clust_off_label = ttk.Label(app, text=str(clust_off_var.get()))
    row = grid_item(clust_off_label, row, column=2, sticky="w")

    # Nb clusters (on)
    label_on = ttk.Label(app, text="Nb clusters (on):")
    row = grid_item(label_on, row, column=0, sticky="e", increment=False)
    clust_on_var = \
        tk.IntVar(value=user_parameters['loop_pars']['nb clusters on'])
    scale_on = ttk.Scale(app, from_=1, to=30, variable=clust_on_var,
                         orient="horizontal", length=30,
                         command=update_nb_clusters_on)
    row = grid_item(scale_on, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_on\n" \
           "- Summary: Number of Clusters for On Field Loop\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the on-field loop. " \
           "Machine learning algorythm of clustering\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the on-field loop.\n" \
           "- Active if: Used in the analysis of on-field loop."
    scale_on.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(scale_on, mess))
    clust_on_label = ttk.Label(app, text=str(clust_on_var.get()))
    row = grid_item(clust_on_label, row, column=2, sticky="w")

    # Nb clusters (coupled)
    label_coupled = ttk.Label(app, text="Nb clusters (coupled):")
    row = grid_item(label_coupled, row, column=0, sticky="e", increment=False)
    clust_coupled_var = \
        tk.IntVar(value=user_parameters['loop_pars']['nb clusters coupled'])
    scale_coupled = ttk.Scale(app, from_=1, to=30, variable=clust_coupled_var,
                              orient="horizontal", length=30,
                              command=update_nb_clusters_coupled)
    row = grid_item(scale_coupled, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_coupled\n" \
           "- Summary: Number of Clusters for Differential Component\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the differential component. " \
           "Machine learning algorythm of clustering\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the differential component.\n" \
           "- Active if: Used in the analysis of differential component only " \
           "for piezoresponse loop."
    scale_coupled.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(scale_coupled, mess))
    clust_coupled_label = ttk.Label(app, text=str(clust_coupled_var.get()))
    row = grid_item(clust_coupled_label, row, column=2, sticky="w")
    row = add_grid_separator(app, row=row)

    # Section title: Curve parameters
    label_meas_curve = ttk.Label(
        app, text="Curve parameters", font=("Helvetica", 14))
    row = grid_item(label_meas_curve, row, column=0, sticky="ew", columnspan=3)
    strg = "These parameters are common to a curve object process.\n" \
           "Active if: object is 'curve'"
    label_meas_curve.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(label_meas_curve, mess))

    # Extension
    label_ext = ttk.Label(app, text="Extension:")
    row = grid_item(label_ext, row, column=0, sticky="e", increment=False)
    extension_var = ttk.Combobox(app, values=["spm", "txt", "csv", "xlsx"])
    extension_var.set(user_parameters['curve_pars']['extension'])
    row = grid_item(extension_var, row, column=1, sticky="ew")
    strg = "- Name: extension\n" \
           "- Summary: Extension of curve files in input.\n" \
           "- Description: This parameter determines the extension type of " \
           "curve files.\n" \
           "- Value: A string with four possible values:\n" \
           "\t--> 'spm': for 'spm' curve file extension\n" \
           "\t--> 'txt': for 'txt' curve file extension\n" \
           "\t--> 'csv': for 'csv' curve file extension\n" \
           "\t--> 'xlsx': for 'xlsx' curve file extension"
    extension_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(extension_var, mess))

    # Mode
    label_mode = ttk.Label(app, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(app, values=["classic", "dfrt"])
    mode_var.set(user_parameters['curve_pars']['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Treatment used for segment data analysis " \
           "(extraction of PFM measurements).\n" \
           "- Description: This parameter determines the treatment method " \
           "used for segment data analysis, specifically for the extraction " \
           "of PFM measurements.\n" \
           "- Value: A string with two possible values: " \
           "'classic' (sweep or single_freq) or 'dfrt'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))

    # Measure
    label_name_curve = ttk.Label(app, text="Name(s):")
    row = grid_item(label_name_curve, row, column=0, sticky="e",
                    increment=False)
    label_meas_curve_var = tk.StringVar()
    label_meas_curve_var.set(str(user_parameters['curve_pars']['label meas']))
    entry_label_meas_curve = ttk.Entry(app, textvariable=label_meas_curve_var)
    row = grid_item(entry_label_meas_curve, row, column=1, sticky="ew")
    strg = "- Name: label_meas\n" \
           "- Summary: List of Measurement Name for Curves\n" \
           "- Description: This parameter contains a list of measurement " \
           "name in order to create the curve to be analyzed using a machine " \
           "learning algorithm of clustering.\n" \
           "If several name are filled, the curve will be normalized and " \
           "concatenated.\n" \
           "Choose from : deflection, height, amplitude, phase ...\n" \
           "- Value: A list containing strings.\n" \
           "\t- For example: ['deflection'] or ['deflection', 'height']"
    entry_label_meas_curve.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_label_meas_curve, mess))

    # Function to update the label text when the slider is moved
    def update_nb_clusters(_):
        clust_label.config(text=str(clust_var.get()))

    # Nb clusters
    label_cluster_nb = ttk.Label(app, text="Nb clusters:")
    row = grid_item(label_cluster_nb, row, column=0, sticky="e",
                    increment=False)
    clust_var = tk.IntVar(value=user_parameters['curve_pars']['nb clusters'])
    scale_clust = ttk.Scale(app, from_=1, to=30, variable=clust_var,
                            orient="horizontal", length=30,
                            command=update_nb_clusters)
    row = grid_item(scale_clust, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters\n" \
           "- Summary: Number of Clusters for Curve\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the curves. " \
           "Machine learning algorythm of clustering\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the curves.\n" \
           "- Active if: Used in the analysis of curves."
    scale_clust.bind("<Enter>",
                     lambda event, mess=strg: show_tooltip(scale_clust, mess))
    clust_label = ttk.Label(app, text=str(clust_var.get()))
    row = grid_item(clust_label, row, column=2, sticky="w")
    row = add_grid_separator(app, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(app, text="Save and plot", font=("Helvetica", 14))
    row = grid_item(label_chck, row, column=0, sticky="ew", columnspan=3)

    # Verbose
    label_verb = ttk.Label(app, text="Verbose:")
    row = grid_item(label_verb, row, column=0, sticky="e", increment=False)
    verbose_var = tk.BooleanVar()
    verbose_var.set(user_parameters['verbose'])
    chck_verb = ttk.Checkbutton(app, variable=verbose_var)
    row = grid_item(chck_verb, row, column=1, sticky="w")
    strg = "- Name: verbose\n" \
           "- Summary: Activation key for printing verbosity during " \
           "analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for printing verbose information during the analysis.\n" \
           "- Value: Boolean (True or False)."
    chck_verb.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_verb, mess))

    # Show plots
    label_show = ttk.Label(app, text="Show plots:")
    row = grid_item(label_show, row, column=0, sticky="e", increment=False)
    show_plots_var = tk.BooleanVar()
    show_plots_var.set(user_parameters['show plots'])
    chck_show = ttk.Checkbutton(app, variable=show_plots_var)
    row = grid_item(chck_show, row, column=1, sticky="w")
    strg = "- Name: show_plots\n" \
           "- Summary: Activation key for generating matplotlib figures " \
           "during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for generating matplotlib figures during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_show.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_show, mess))

    # Save
    label_save = ttk.Label(app, text="Save:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(app, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_save.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_save, mess))
    row = add_grid_separator(app, row=row)

    # Submit button
    submit_button = ttk.Button(app, text="Start", command=launch)
    row = grid_item(submit_button, row, column=0, sticky="e", increment=False)

    def quit_application():
        app.destroy()

    # Exit button
    quit_button = ttk.Button(app, text="Exit", command=quit_application)
    grid_item(quit_button, row, column=1, sticky="ew", increment=False)

    app.mainloop()


if __name__ == '__main__':
    main()
