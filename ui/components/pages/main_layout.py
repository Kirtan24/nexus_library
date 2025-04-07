import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.auth_services import AuthenticationService

BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#000000"
ACCENT_COLOR = "#6f23ff"
BLACK_COLOR = "#000000"
OFFWHITE_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#a875ff"
BUTTON_COLOR = "#000000"
BUTTON_TEXT_COLOR = "#f8f9fa"

class MainLayout(ctk.CTkFrame):
    """Base layout class that handles header, content area, and footer"""
    def __init__(self, master, user=None):
        super().__init__(master)
        self.master = master
        self.user = user

        self.root = self.master.master
        self.root.title("Nexus Library")
        self.root.geometry("1200x800")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        self.create_layout()

        self.content_area = None

    def create_layout(self):
        self.create_header()

        self.content_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.content_container.pack(fill=ctk.BOTH, expand=True)

        self.create_footer()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=OFFWHITE_COLOR, height=70)
        header_frame.pack(fill=ctk.X)

        header_frame.pack_propagate(False)

        logo_frame = ctk.CTkFrame(header_frame, fg_color=OFFWHITE_COLOR)
        logo_frame.pack(side=ctk.LEFT, padx=20)

        try:
            img_path = os.path.join("assets", "logo", "logo.png")
            logo_img = Image.open(img_path)
            logo_img = logo_img.resize((40, 40))
            logo_img = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(40, 40))
            logo_label = ctk.CTkLabel(logo_frame, image=logo_img, text="")
            logo_label.pack(side=ctk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")

        app_name = ctk.CTkLabel(logo_frame, text="Nexus Library", text_color="#000000", font=("Arial", 22, "bold"))
        app_name.pack(side=ctk.LEFT)

        nav_frame = ctk.CTkFrame(header_frame, fg_color=OFFWHITE_COLOR)
        nav_frame.pack(side=ctk.RIGHT, padx=20)

        nav_options = [
            {"text": "Home", "command": self.show_home},
            {"text": "Search", "command": self.show_search},
            {"text": "Browse", "command": self.show_browse},
            {"text": "My Books", "command": self.show_my_books},
            # {"text": self.user.username, "command": self.show_profile}
        ]

        for option in nav_options:
            btn = ctk.CTkButton(
                nav_frame,
                text=option["text"],
                command=option["command"],
                fg_color="transparent",
                hover_color="#eeeeee",
                text_color="#000000",
                font=("Arial", 14),
                width=90,
                height=40
            )
            btn.pack(side=ctk.LEFT, padx=5)

        if self.user:
            user_btn = ctk.CTkButton(
                nav_frame,
                text=f"Logout",
                command=self.master.logout,
                fg_color="#000000",
                text_color=BACKGROUND_COLOR,
                hover_color=ACCENT_COLOR,
                font=("Arial", 14),
                width=80,
                height=35
            )
            user_btn.pack(side=ctk.LEFT, padx=10)
        else:
            login_btn = ctk.CTkButton(
                nav_frame,
                text="Login",
                command=self.show_login,
                fg_color="#000000",
                text_color=BACKGROUND_COLOR,
                hover_color=ACCENT_COLOR,
                font=("Arial", 14),
                width=60,
                height=35
            )
            login_btn.pack(side=ctk.LEFT, padx=5)
            register_btn = ctk.CTkButton(
                nav_frame,
                text="Sign Up",
                command=self.show_register,
                fg_color=OFFWHITE_COLOR,
                text_color="#000000",
                hover_color="#eeeeee",
                font=("Arial", 14),
                width=60,
                height=35
            )
            register_btn.pack(side=ctk.LEFT)

    def create_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", height=50)
        footer_frame.pack(fill=ctk.X, side=ctk.BOTTOM)
        footer_frame.pack_propagate(False)

        copyright_text = ctk.CTkLabel(
            footer_frame,
            text="© 2025 Nexus Library. All rights reserved.",
            font=("Arial", 12),
            text_color="#666666"
        )
        copyright_text.pack(side=ctk.LEFT, padx=20)

        links_frame = ctk.CTkFrame(footer_frame, fg_color="#f0f0f0")
        links_frame.pack(side=ctk.RIGHT, padx=20)

        footer_links = ["Privacy Policy", "Terms of Service"]

        for link in footer_links:
            link_label = ctk.CTkLabel(
                links_frame,
                text=link,
                font=("Arial", 12),
                text_color="#666666",
                cursor="hand2"
            )
            link_label.pack(side=ctk.LEFT, padx=10)
            link_label.bind("<Button-1>", lambda e, l=link: self.show_footer_page(l))

    def show_home(self):
        self.master.show_home_page()

    def show_search(self):
        self.master.show_search_page()

    def show_browse(self):
        self.master.show_browse_page()

    def show_my_books(self):
        self.master.show_my_books_page()

    def show_profile(self):
        self.master.show_profile_page()

    def show_login(self):
        self.master.show_login_page()

    def show_register(self):
        self.master.show_register_page()

    def show_footer_page(self, page):
        self.master.show_page(page.lower().replace(" ", "_"))

    def clear_content(self):
        """Clear the content container to prepare for new content"""
        for widget in self.content_container.winfo_children():
            widget.destroy()