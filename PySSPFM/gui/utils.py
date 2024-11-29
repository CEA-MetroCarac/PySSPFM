"""
Util functions for interface graphique exe files
"""

import os
from pathlib import Path
import webbrowser
import tkinter as tk
from tkinter import ttk, Canvas, Scrollbar
from PIL import Image, ImageTk

from PySSPFM.settings import get_setting


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

    # Create a frame for the background
    background_frame = tk.Frame(root)
    background_frame.place(relwidth=1, relheight=1)

    # Apply a ttk style for a more pleasant interface
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 12), anchor='center')
    style.configure('TButton', font=('Arial', 12), anchor='center',
                    borderwidth=4, relief="ridge")
    style.configure('TCheckbutton', font=('Arial', 12), anchor='center')
    style.configure('TEntry', font=('Arial', 12))
    style.configure('Horizontal.TScale', troughcolor='lightgray')
    style.configure('TMenubutton', font=('Arial', 12), anchor='center')


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


def add_grid_separator(root, row):
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
    frame = ttk.Frame(root)
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
    Initialize the main window in fullscreen mode with a scrollbar and ensure
    images are displayed correctly.

    Parameters
    ----------
    wdw_title : str
        Title for the main window.
    logo_path : str, optional
        Path to the logo image file. Uses default setting if None.
    icon_path : str, optional
        Path to the icon image file. Uses default setting if None.

    Returns
    -------
    tuple
        A tuple containing the main window (tk.Tk) and the scrollable frame
        (ttk.Frame).
    """
    logo_path = logo_path or os.path.join(get_setting("default_logo_icon_path"), "logoPySSPFM.png")
    icon_path = icon_path or os.path.join(get_setting("default_logo_icon_path"), "iconPySSPFM.png")

    # Set root
    root = tk.Tk()
    root.title(wdw_title)
    apply_style(root)

    # Configure the canvas and scrollbar
    container = ttk.Frame(root)
    container.grid(row=0, column=0, sticky="nsew")

    canvas = Canvas(container)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Configure grid weights for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a frame on the canvas for content
    scrollable_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Dynamically adjust the size of the scrollable frame
    def configure_scrollable_frame(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_window, width=canvas_width)
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scrollable_frame)

    # Allow scrolling with the mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Set the window icon if an icon path is provided
    if icon_path:
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Failed to load icon: {e}")

    # Add a logo to the top of the scrollable frame if a logo path is provided
    if logo_path:
        try:
            logo_image = Image.open(logo_path)
            logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ttk.Label(scrollable_frame, image=logo_photo)
            logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
            logo_label.pack(side="top", anchor="center", pady=10)
        except Exception as e:
            print(f"Failed to load logo: {e}")

    # Adjust window size and configure fullscreen mode
    adjust_size_wdw(root)

    return root, scrollable_frame


def init_secondary_wdw(parent, wdw_title, icon_path=None):
    """
    Initialize a secondary window with a scrollbar and ensures images are
    displayed correctly, positioning the window to fit its content width,
    centered horizontally, full height, and top aligned.

    Parameters
    ----------
    parent : tk.Tk or tk.Toplevel
        Parent window (can be None for the main window).
    wdw_title : str
        Title for the secondary window.
    icon_path : str, optional
        Path to the icon image file. Uses default setting if None.

    Returns
    -------
    tuple
        A tuple containing the secondary window (tk.Toplevel) and the
        scrollable frame (ttk.Frame).
    """

    icon_path = icon_path or os.path.join(get_setting("default_logo_icon_path"), "iconPySSPFM.png")

    # Set root
    if parent is None:
        root = tk.Tk()
        root.title(f"{wdw_title}")
    else:
        root = tk.Toplevel(parent)
        root.title(f"{wdw_title} (Secondary Window)")
    apply_style(root)

    # Configure the canvas and scrollbar for content scrolling
    container = ttk.Frame(root)
    container.grid(row=0, column=0, sticky="nsew")

    canvas = Canvas(container)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Configure grid weights for resizing
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a frame on the canvas for content, centered dynamically
    scrollable_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # Adjust the position of scrollable_frame dynamically on canvas resize
    def configure_scrollable_frame(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_window, width=canvas_width)
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scrollable_frame)

    # Allow scrolling with the mouse wheel
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Set the window icon if an icon path is provided
    if icon_path:
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Failed to load icon: {e}")

    # Adjust window size based on content
    adjust_size_wdw(root)

    return root, scrollable_frame


def adjust_size_wdw(root):
    """
    Adjusts the size of the tkinter window to 1.5 times its required width and
    full screen height, centering it horizontally at the top of the screen.

    Parameters
    ----------
    root : Tk
        The main window whose size and position need to be adjusted.

    Returns
    -------
    None
    """
    root.update_idletasks()
    width = root.winfo_reqwidth()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.update_idletasks()
    taskbar_height = root.winfo_rooty()
    usable_height = screen_height - taskbar_height

    x = screen_width / 2 - width / 2
    root.geometry(f"{int(width*1.5)}x{usable_height}+{int(x)}+0")


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
    logo_path = logo_path or os.path.join(get_setting("default_logo_icon_path"), "logoPySSPFM.png")

    logo_image = Image.open(logo_path)
    logo_image.thumbnail((128, 128))
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = ttk.Label(root, image=logo_photo)
    logo_label.photo = logo_photo
    logo_label.grid(row=0, column=0, columnspan=3, sticky="ew")

    label_title = ttk.Label(root, text=label, font=("Helvetica", 16))
    label_title.grid(row=1, column=0, columnspan=3, sticky="ew")

    add_grid_separator(root, row=2)


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

    def show_tooltip_button(_, btn):
        if btn in tooltips:
            show_tooltip(buttons[btn], tooltips[btn])

    def hide_tooltip_button(_, btn):
        if btn in tooltips:
            hide_tooltip(tooltips[btn])

    frame = ttk.Frame(root)
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

def create_useful_links_button(frame):
    """
    Creates a set of useful links buttons in a specified frame.

    Parameters
    ----------
    frame : ttk.Frame or similar
        Parent container where the buttons will be added.

    Returns
    -------
    None
    """

    def create_button(parent, text, image_path, image_size, command, pady=5):
        """
        Creates a button with an image and a command in a specified parent frame.

        Parameters
        ----------
        parent : ttk.Frame or similar
            Parent container where the button will be added.
        text : str
            Label text for the button.
        image_path : str
            Path to the image file for the button.
        image_size : tuple of int
            Size of the image (width, height) to resize.
        command : callable
            Function to execute when the button is clicked.
        pady : int, optional
            Padding on the y-axis for the button (default is 5).

        Returns
        -------
        button : ttk.Button
            The created button instance.
        """
        image = Image.open(image_path).resize(image_size)
        tk_image = ImageTk.PhotoImage(image)
        button = ttk.Button(parent, text=text, image=tk_image, compound="right", command=command)
        button.image = tk_image  # Retient la référence pour éviter le garbage collection
        button.pack(pady=pady)
        return button

    logo_icon_path = get_setting("default_logo_icon_path")

    buttons_data = [
        ("Github", os.path.join(logo_icon_path, "github.PNG"), (32, 32),
         lambda: webbrowser.open("https://github.com/CEA-MetroCarac/PySSPFM")),
        ("Documentation", os.path.join(logo_icon_path, "github.PNG"), (32, 32),
         lambda: webbrowser.open("https://github.com/CEA-MetroCarac/PySSPFM/tree/main/doc")),
        ("Measurement Sheet", os.path.join(logo_icon_path, "github.PNG"), (32, 32),
         lambda: webbrowser.open("https://github.com/CEA-MetroCarac/PySSPFM/tree/main/resources")),
        ("Report an issue ?", os.path.join(logo_icon_path, "github.PNG"), (32, 32),
         lambda: webbrowser.open("https://github.com/CEA-MetroCarac/PySSPFM/issues")),
        ("Open Settings", os.path.join(logo_icon_path, "logoPySSPFM.png"), (64, 32),
         lambda: os.startfile(Path.home() / ".pysspfm" / "pysspfm.json") if os.path.exists(
             Path.home() / ".pysspfm" / "pysspfm.json") else print("File not found")),
        ("YouTube tutorials", os.path.join(logo_icon_path, "youtube.PNG"), (32, 32),
         lambda: webbrowser.open("https://github.com/CEA-MetroCarac/PySSPFM")),
        ("Our paper (JAP)", os.path.join(logo_icon_path, "aip.PNG"), (64, 32),
         lambda: webbrowser.open(
             "https://pubs.aip.org/aip/jap/article/135/19/194101/3294052/Enhancing-ferroelectric-characterization-at")),
        ("Zenodo", os.path.join(logo_icon_path, "zenodo.PNG"), (64, 32),
         lambda: webbrowser.open("https://zenodo.org/records/14236355")),
        ("PyPI", os.path.join(logo_icon_path, "pypi.PNG"), (32, 32),
         lambda: webbrowser.open("https://pypi.org/project/PySSPFM/")),
    ]

    for text, image_path, image_size, command in buttons_data:
        create_button(frame, text, image_path, image_size, command)
