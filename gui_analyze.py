import tkinter as tk
from tkinter import simpledialog


def input_occupy():
    """
        Function that ask for occupy percentage reference.
    :return: Occupy percentage reference.
    """
    root = tk.Tk()
    root.withdraw()
    # the input dialog
    occupy = simpledialog.askstring(title="occupy", prompt='please set the occupy percentage reference')
    return occupy
