"""
Util functions for interface graphique exe files
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from PySSPFM import DEFAULT_LOGO_PATH, DEFAULT_ICON_PATH


def apply_style(root):
    """
    Apply custom styles to the tkinter GUI.

    Parameters
    ----------
    root: tk.Tk or Frame
        The root tkinter window.

    Returns
    -------
    None
    """

    # Create a blue-colored frame for the background
    background_frame = tk.Frame(root, bg="lightblue")
    background_frame.place(relwidth=1, relheight=1)

    # Apply a ttk style for a more pleasant interface
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12), anchor='center',
                    background='lightblue')
    style.configure('TButton', font=('Arial', 12), anchor='center',
                    borderwidth=4, relief="ridge", background='lightblue')
    style.configure('TCheckbutton', font=('Arial', 12), anchor='center',
                    background='lightblue')
    style.configure('TEntry', font=('Arial', 12), background='lightblue')
    style.configure('Horizontal.TScale', background='lightblue',
                    troughcolor='lightgray')
    style.configure('TMenubutton', font=('Arial', 12), anchor='center',
                    background='lightblue')
    style.configure('bluelight.TFrame', background='lightblue')


def hide_tooltip(tooltip_wdw):
    """
    Close the tooltip window.

    Parameters
    ----------
    tooltip_wdw : tk.Toplevel
        The tooltip window to be closed.
    """
    tooltip_wdw.destroy()


def show_tooltip(widget, message):
    """
    Display a tooltip with the specified message when hovering over a widget.

    Parameters
    ----------
    widget : tk.Widget
        The widget to which the tooltip is attached.
    message : str
        The message to display in the tooltip.
    """

    # Get the coordinates of the widget's text
    x, y, _, _ = widget.bbox("insert")

    # Adjust coordinates (25 is an arbitrary offset)
    x += widget.winfo_rootx() + 25
    y += widget.winfo_rooty() + 25

    # Create a tooltip window
    tooltip = tk.Toplevel(widget)

    # Remove the window border
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{x}+{y}")

    # Create a label with left alignment
    label = tk.Label(tooltip, text=message, background="lightyellow",
                     relief="solid", borderwidth=1, anchor="w", justify="left")
    label.pack()

    # Bind the hide_tooltip function with "Leave" event (mouse leaves widget)
    widget.bind("<Leave>", lambda event, t=tooltip: hide_tooltip(t))


def grid_item(item, row, column=0, sticky=None, increment=True,
              columnspan=None, rowspan=None):
    """
    Place an item in a grid and increment the row number if specified.

    Parameters
    ----------
    item : tkinter.Widget
        The item to be placed in the grid.
    row : int
        The row where the item should be placed.
    column : int, optional
        The column where the item should be placed (default is 0).
    sticky : str, optional
        A string specifying how the item should stick to the grid cell
        (default is None).
    increment : bool, optional
        If True, increment the row number by 1 after placing the item
        (default is True).
    columnspan : int, optional
        The number of columns that the item should span (default is None).
    rowspan : int, optional
        The number of rows that the item should span (default is None).

    Returns
    -------
    int
        The updated row number after placing the item.
    """
    item.grid(row=row, column=column, sticky=sticky, columnspan=columnspan,
              rowspan=rowspan)
    if increment:
        row += 1
    return row


def add_section_separator(root):
    """
    Add a horizontal separator to the given root frame.

    Parameters
    ----------
    root : tk.Tk or tk.Frame
        The root frame or window to which the separator should be added.
    """
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x', padx=10, pady=10)


def add_separator_grid(root, row):
    """
    Add a separator label in a grid layout.

    Parameters
    ----------
    root : tk.Tk or tk.Frame
        The root frame or window to which the separator label should be added.
    row : int
        The row in the grid where the separator label should be placed.

    Returns
    -------
    int
        The updated row value after adding the separator label.
    """
    label = ttk.Label(root, text="", font=("Helvetica", 16))
    label.grid(row=row, column=1, sticky="e")
    row += 1
    return row


def create_frame(root, title=None, row=1, column=1):
    """
    Create a frame within a tkinter root window with an optional title.

    Parameters
    ----------
    root : tk.Tk or tk.Frame
        The root frame or window where the new frame should be created.
    title : str, optional
        The title to be displayed within the frame (default is None).
    row : int, optional
        The row in the grid where the new frame should be placed (default is 1).
    column : int, optional
        The column in the grid where the new frame should be placed
        (default is 1).

    Returns
    -------
    ttk.Frame
        The created frame.
    """
    frame = ttk.Frame(root, style="bluelight.TFrame")
    frame.grid(row=row, column=column, sticky='e')

    if title:
        title_label = ttk.Label(frame, text=title, font=("Helvetica", 14))
        title_label.pack()

    return frame


def extract_var(string_var):
    """
    Extracts a variable from a string representation.

    Parameters
    ----------
    string_var : StringVar
        The string representation of the variable.

    Returns
    -------
    variable
        The extracted variable. If the string is empty or invalid,
        None is returned.
    """
    if string_var.get() not in ["", "None", None]:
        try:
            variable = eval(string_var.get())
        except (NameError, SyntaxError):
            variable = string_var.get()
    else:
        variable = None

    return variable


def init_main_wdw(wdw_title, logo_path=None, icon_path=None):
    """
    Initialize the main window.

    Parameters
    ----------
    wdw_title : str
        Title for the main window.
    logo_path : str, optional
        Path to the logo image file (default is None).
    icon_path : str, optional
        Path to the icon image file (default is None).

    Returns
    -------
    tk.Tk
        The initialized main window.
    """

    logo_path = logo_path or DEFAULT_LOGO_PATH
    icon_path = icon_path or DEFAULT_ICON_PATH

    root = tk.Tk()
    root.title(wdw_title)
    apply_style(root)

    # Logo and icon PySSPFM
    logo_image = Image.open(logo_path)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ttk.Label(root, image=logo_photo)
    logo_label.photo = logo_photo
    logo_label.pack()
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)

    return root


def init_secondary_wdw(parent, wdw_title, icon_path=None):
    """
    Initialize a secondary window.

    Parameters
    ----------
    parent : tk.Tk or tk.Toplevel
        Parent window (can be None for the main window).
    wdw_title : str
        Title for the secondary window.
    icon_path : str, optional
        Path to the icon image file (default is None).

    Returns
    -------
    tk.Tk
        The initialized secondary window.
    """

    icon_path = icon_path or DEFAULT_ICON_PATH

    if parent is None:
        root = tk.Tk()
        root.title(f"{wdw_title}")
    else:
        root = tk.Toplevel(parent)
        root.title(f"{wdw_title} (Secondary Window)")
    apply_style(root)

    # Icon PySSPFM
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)

    return root


def wdw_main_title(root, label, logo_path=None):
    """
    Set up the main window title with logo and label.

    Parameters
    ----------
    root : tk.Tk or tk.Frame
        The main tkinter window.
    label : str
        The label to display in the window.
    logo_path : str, optional
        Path to the logo image file (default is None).

    Returns
    -------
    None
    """
    logo_path = logo_path or DEFAULT_LOGO_PATH

    logo_image = Image.open(logo_path)
    logo_image.thumbnail((128, 128))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = ttk.Label(root, image=logo_photo)
    logo_label.photo = logo_photo
    logo_label.grid(row=0, column=0, columnspan=3, sticky="ew")

    label_title = ttk.Label(root, text=label, font=("Helvetica", 16))
    label_title.grid(row=1, column=0, columnspan=3, sticky="ew")

    add_separator_grid(root, row=2)


def create_section(app, title, labs, funcs, strg_title=None,
                   strg_functions=None):
    """
    Create a section with buttons to open different interfaces.

    Parameters
    ----------
    app : tk.Tk or tk.Toplevel
        The root or top-level tkinter window.
    title : str
        Title for the section.
    labs : list of str
        List of button names.
    funcs : list of callable
        List of functions to execute when buttons are clicked.
    strg_title : str, optional
        Tooltip message for the section title (default is None).
    strg_functions : list of str, optional
        Tooltip messages for the buttons (default is None).

    Returns
    -------
    None
    """
    title_lab = ttk.Label(app, text=title, font=("Helvetica", 14))
    if strg_title is not None:
        title_lab.bind(
            "<Enter>",
            lambda event, mess=strg_title: show_tooltip(title_lab, mess))
    title_lab.pack()
    buttons_section(labs, funcs, app, strg_functions=strg_functions)
    add_section_separator(app)


def buttons_section(names, functions, root, title=None, strg_functions=None):
    """
    Create a section with buttons to open different interfaces.

    Parameters
    ----------
    names : list of str
        List of button names.
    functions : list of callable
        List of functions to execute when buttons are clicked.
    root : tk.Tk or tk.Toplevel
        The root or top-level tkinter window.
    title : str, optional
        Title for the section.
    strg_functions : list of str, optional
        Tooltip messages for the buttons (default is None).

    Returns
    -------
    None
    """
    def open_interface(lab, app):
        lab(parent=app)

    def show_tooltip_button(event, btn):
        if btn in tooltips:
            show_tooltip(buttons[btn], tooltips[btn])

    def hide_tooltip_button(event, btn):
        if btn in tooltips:
            hide_tooltip(tooltips[btn])

    frame = ttk.Frame(root, style="bluelight.TFrame")
    frame.pack(pady=10)

    buttons = {}
    tooltips = {}

    if title:
        title_label = ttk.Label(frame, text=title, font=("Helvetica", 12))
        title_label.pack()

    for cont, (name, function) in enumerate(zip(names, functions)):
        button = ttk.Button(
            frame, text=name,
            command=lambda tool=function: open_interface(tool, root))
        buttons[f"{cont}"] = button
        button.pack(fill="x", padx=10)

        if strg_functions is not None and cont < len(strg_functions):
            tooltips[f"{cont}"] = strg_functions[cont]
            button.bind(
                "<Enter>",
                lambda event, btn=f"{cont}": show_tooltip_button(event, btn))
            button.bind(
                "<Leave>",
                lambda event, btn=f"{cont}": hide_tooltip_button(event, btn))
