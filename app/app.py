import tkinter as tk
from ui.components.auth.login import LoginPage
from ui.components.auth.register import RegisterPage
from ui.components.pages.home_page import HomePage
from ui.components.pages.main_layout import MainLayout
from ui.components.pages.manage_items_page import ItemManagementPage
from ui.components.pages.manage_author_page import AuthorManagementPage
from ui.components.pages.browse_page import BrowsePage
from ui.components.pages.book_details import BookDetailView
from ui.components.pages.my_books import MyBorrowedBooksPage
from ui.components.pages.reservation_page import ReservationsPage
from ui.components.pages.extra_page import DataTable
from app.services.auth_services import AuthenticationService

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_data = None
        self.auth_service = AuthenticationService()
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
        self.auth_service.logout()
        self.clear_frame()
        MainLayout(self)
        self.show_home_page(None)

    def update_main_layout(self):
        for widget in self.winfo_children():
            if isinstance(widget, MainLayout):
                widget.set_user(None)
                widget.update_navigation()

    def show_extra_page(self):
        self.clear_frame()
        DataTable(self)

    def show_home_page(self, user_data=None):
        self.clear_frame()
        HomePage(self, user_data)

    def show_browse_page(self):
        self.clear_frame()
        # DataTable(self)
        BrowsePage(self, self.show_item_detail_page)

    def show_item_detail_page(self, item_id):
        print(item_id)
        print(self.user_data['user_id'])
        BookDetailView(self, item_id, self.user_data['user_id'])

    def show_my_books_page(self):
        self.clear_frame()
        MyBorrowedBooksPage(self, self.user_data['user_id'])

    def show_reservations_page(self):
        self.clear_frame()
        ReservationsPage(self, self.user_data['user_id'])


    def show_manage_items_page(self):
        self.clear_frame()
        ItemManagementPage(self)

    def show_manage_author_page(self):
        self.clear_frame()
        AuthorManagementPage(self)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()