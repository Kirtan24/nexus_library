import customtkinter as ctk
from PIL import Image, ImageTk
from ui.components.pages.main_layout import MainLayout

BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#000000"
ACCENT_COLOR = "#6f23ff"
BLACK_COLOR = "#000000"
OFFWHITE_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#a875ff"
BUTTON_COLOR = "#000000"
BUTTON_TEXT_COLOR = "#f8f9fa"

class SearchPage(MainLayout):
    def __init__(self, master, user=None):
        super().__init__(master, user)
        self.root.title("Nexus Library - Search")