import tkinter as tk
from ui.components.auth.login import LoginPage
from ui.components.auth.register import RegisterPage
from ui.components.pages.home_page import HomePage
from ui.components.pages.search_page import SearchPage

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.geometry("600x600")
        self.master.state('zoomed')
        self.pack(fill=tk.BOTH, expand=True)
        self.show_home_page(None)

    def show_login_page(self):
        self.clear_frame()
        LoginPage(self)

    def show_register_page(self):
        self.clear_frame()
        RegisterPage(self)

    def logout(self):
        self.user_data = None
        self.show_home_page(None)

    def show_home_page(self, user_data=None):
        self.clear_frame()
        HomePage(self, user_data)

    def show_search_page(self):
        self.clear_frame()
        SearchPage(self)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()