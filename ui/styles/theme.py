import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root):
    style = ttk.Style()

    root.tk_setPalette(background="#6f23ff", foreground="#ffffff")

    style.configure("TButton",
                     background="#333333",
                     foreground="#ffffff",
                     borderwidth=1,
                     padding=6,
                     font=("Arial", 12))
    style.map("TButton",
              background=[('active', '#555555')],
              foreground=[('active', '#ffffff')])

    style.configure("TLabel",
                     background="#6f23ff",
                     foreground="#ffffff",
                     font=("Arial", 14))

    style.configure("TFrame",
                     background="#6f23ff")
