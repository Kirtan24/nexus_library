import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.auth_services import AuthenticationService

# Colors
BACKGROUND_COLOR = "#f8f9fa"
OFFWHITE_COLOR = "#f0f0f0"
ACCENT_COLOR = "#6f23ff"
TEXT_COLOR = "#000000"

class MainLayout(ctk.CTkFrame):
    def __init__(self, master, user=None):
        super().__init__(master)
        self.master = master
        self.user = user
        self.auth_service = AuthenticationService()

        self.root = self.master.master
        self.root.title("Nexus Library")
        self.root.geometry("1200x800")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        self.nav_buttons = {}
        self.create_layout()

    def create_layout(self):
        self.create_header()
        self.content_container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.content_container.pack(fill=ctk.BOTH, expand=True)

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=OFFWHITE_COLOR, height=70)
        header_frame.pack(fill=ctk.X)
        header_frame.pack_propagate(False)

        # Logo and app name
        logo_frame = ctk.CTkFrame(header_frame, fg_color=OFFWHITE_COLOR)
        logo_frame.pack(side=ctk.LEFT, padx=20)

        try:
            img_path = os.path.join("assets", "logo", "logo.png")
            logo_img = Image.open(img_path).resize((40, 40))
            logo_img = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(40, 40))
            ctk.CTkLabel(logo_frame, image=logo_img, text="").pack(side=ctk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"Logo load error: {e}")

        ctk.CTkLabel(logo_frame, text="Nexus Library", text_color=TEXT_COLOR, font=("Arial", 22, "bold")).pack(side=ctk.LEFT)

        # Navigation bar
        self.nav_frame = ctk.CTkFrame(header_frame, fg_color=OFFWHITE_COLOR)
        self.nav_frame.pack(side=ctk.RIGHT, padx=20)
        self.create_navigation()

    def create_navigation(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        self.active_menu = None  # Track currently open dropdown

        if self.auth_service.is_authenticated():
            user = self.auth_service.get_current_user()
            permissions = user.get("permissions", [])

            # Grouped navigation structure
            nav_groups = {
                "Library": [
                    {"text": "Search", "command": self.show_search},
                    {"text": "Browse", "command": self.show_browse, "permission": "view_catalog"},
                    {"text": "My Books", "command": self.show_my_books, "permission": "borrow_physical_books"},
                    {"text": "Reservations", "command": self.show_reservations, "permission": "reserve_books"},
                    {"text": "Extensions", "command": self.show_extensions, "permission": "extend_borrowing"},
                ],
                "Digital Access": [
                    {"text": "eBooks", "command": self.show_ebooks, "permission": "access_ebooks"},
                    {"text": "Audiobooks", "command": self.show_audiobooks, "permission": "access_audiobooks"},
                    {"text": "Research", "command": self.show_research, "permission": "access_research_papers"},
                ],
                "Admin Tools": [
                    {"text": "Users", "command": self.show_users, "permission": "manage_users"},
                    {"text": "Items", "command": self.show_manage_items, "permission": "manage_catalog"},
                    {"text": "Authors", "command": self.show_manage_author, "permission": "manage_catalog"},
                    {"text": "Reports", "command": self.show_reports, "permission": "view_reports"},
                    {"text": "Settings", "command": self.show_settings, "permission": "system_config"},
                    {"text": "Admin", "command": self.show_admin, "permission": "admin_access"},
                ],
                "Account": [
                    {"text": "Profile", "command": self.show_profile},
                    {"text": "Logout", "command": self.master.logout}
                ]
            }

            # Always-visible Home button
            self.create_nav_button("Home", self.show_home)

            for group_name, group_items in nav_groups.items():
                filtered_items = [item for item in group_items if item.get("permission") is None or item["permission"] in permissions]
                if filtered_items:
                    self.create_dropdown(group_name, filtered_items)
        else:
            self.create_nav_button("Home", self.show_home)
            self.create_nav_button("Search", self.show_search)
            self.create_nav_button("Browse", self.show_browse)
            self.create_nav_button("Login", self.show_login, solid=True)
            self.create_nav_button("Sign Up", self.show_register, fg_color=OFFWHITE_COLOR, text_color=TEXT_COLOR)


    def create_dropdown(self, label, options):
        button = ctk.CTkButton(
            self.nav_frame,
            text=f"{label} ▼",
            fg_color="transparent",
            hover_color="#eeeeee",
            text_color=TEXT_COLOR,
            font=("Arial", 14),
            width=110,
            height=35,
            command=lambda btn=label, opts=options: self.toggle_dropdown(btn, opts)
        )
        button.pack(side=ctk.LEFT, padx=5)
        self.nav_buttons[label] = button


    def toggle_dropdown(self, label, options):
        if self.active_menu:
            self.active_menu.unpost()
            self.active_menu = None

        btn = self.nav_buttons[label]
        x = btn.winfo_rootx()
        y = btn.winfo_rooty() + btn.winfo_height()

        dropdown = tk.Menu(self.root, tearoff=0, font=("Arial", 12))
        for item in options:
            dropdown.add_command(label=item["text"], command=item["command"])
        dropdown.post(x, y)
        self.active_menu = dropdown

        def close_menu(event):
            if self.active_menu:
                self.active_menu.unpost()
                self.active_menu = None
                self.root.unbind("<Button-1>")

        # Close menu if clicking outside
        self.root.bind("<Button-1>", close_menu)


    def create_nav_button(self, text, command, solid=False, fg_color="transparent", text_color=TEXT_COLOR):
        btn = ctk.CTkButton(
            self.nav_frame,
            text=text,
            command=command,
            fg_color=fg_color if not solid else TEXT_COLOR,
            hover_color="#eeeeee" if not solid else ACCENT_COLOR,
            text_color=text_color if not solid else BACKGROUND_COLOR,
            font=("Arial", 14),
            width=90,
            height=35
        )
        btn.pack(side=ctk.LEFT, padx=5)
        self.nav_buttons[text] = btn

    def create_more_dropdown(self, options, permissions):
        import tkinter as tk
        more_btn = ctk.CTkButton(
            self.nav_frame,
            text="More ▼",
            command=lambda: self.show_dropdown_menu(more_btn, options, permissions),
            fg_color="transparent",
            hover_color="#eeeeee",
            text_color=TEXT_COLOR,
            font=("Arial", 14),
            width=90,
            height=35
        )
        more_btn.pack(side=ctk.LEFT, padx=5)
        self.nav_buttons["More"] = more_btn

    def show_dropdown_menu(self, button, options, permissions):
        import tkinter as tk
        x = button.winfo_rootx()
        y = button.winfo_rooty() + button.winfo_height()
        dropdown = tk.Menu(self.root, tearoff=0)
        for option in options:
            if option.get("permission") is None or option["permission"] in permissions:
                dropdown.add_command(label=option["text"], command=option["command"], font=("Arial", 12))
        dropdown.post(x, y)

    def update_navigation(self):
        self.create_navigation()

    def clear_content(self):
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def set_user(self, user):
        self.user = user
        self.update_navigation()

    # Navigation command wrappers
    def show_home(self): self.master.show_home_page()
    def show_search(self): self.master.show_search_page()
    def show_browse(self): self.master.show_browse_page()
    def show_my_books(self): self.master.show_my_books_page()
    def show_reservations(self): self.master.show_reservations_page()
    def show_extensions(self): self.master.show_extensions_page()
    def show_ebooks(self): self.master.show_ebooks_page()
    def show_audiobooks(self): self.master.show_audiobooks_page()
    def show_research(self): self.master.show_research_page()
    def show_users(self): self.master.show_users_page()
    def show_manage_items(self): self.master.show_manage_items_page()
    def show_manage_author(self): self.master.show_manage_author_page()
    def show_reports(self): self.master.show_extra_page()
    def show_settings(self): self.master.show_settings_page()
    def show_admin(self): self.master.show_admin_page()
    def show_profile(self): self.master.show_profile_page()
    def show_login(self): self.master.show_login_page()
    def show_register(self): self.master.show_register_page()