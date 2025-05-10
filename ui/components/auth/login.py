import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.services.auth_services import AuthenticationService

# Theme Colors
PRIMARY_COLOR = "#6f23ff"
BACKGROUND_COLOR = "#f8f8f8"
TEXT_COLOR = "#000000"
PLACEHOLDER_COLOR = "#888888"
BORDER_COLOR = "#a875ff"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.auth_service = AuthenticationService()

        self.root = self.master.master
        self.root.title("Login - Nexus Library")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        self.create_ui()

    def create_ui(self):
        container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, corner_radius=20)
        container.place(relx=0.5, rely=0.5, anchor="center")

        try:
            img_path = os.path.join("assets", "logo", "logo.png")
            logo_img = Image.open(img_path)
            logo_img = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(100, 100))
            label_logo = ctk.CTkLabel(container, image=logo_img, text="", fg_color=BACKGROUND_COLOR)
            label_logo.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        ctk.CTkLabel(container, text="Login", text_color=TEXT_COLOR, font=("Arial", 36, "bold")).pack(pady=10)

        self.username_entry = self.create_entry(container, "Username", width=300)
        self.password_entry = self.create_entry(container, "Password", show="*", width=300)

        button_frame = ctk.CTkFrame(container, fg_color=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        login_button = ctk.CTkButton(button_frame, text="Login", font=("Arial", 16, "bold"), fg_color=TEXT_COLOR, text_color=BACKGROUND_COLOR, command=self.validate_login)
        login_button.pack(side=ctk.LEFT, padx=10)

        back_button = ctk.CTkButton(button_frame, text="Back", font=("Arial", 16, "bold"), fg_color=TEXT_COLOR, text_color=BACKGROUND_COLOR, width=80,command=self.master.show_home_page)
        back_button.pack(side=ctk.LEFT)

        options_frame = ctk.CTkFrame(container, fg_color=BACKGROUND_COLOR)
        options_frame.pack()

        ctk.CTkLabel(options_frame, text="Don't have an account?", text_color=TEXT_COLOR, font=("Arial", 12)).pack(side=ctk.LEFT)
        signup_link = ctk.CTkLabel(options_frame, text="Sign Up", text_color=TEXT_COLOR, font=("Arial", 12, "bold", "underline"), cursor="hand2")
        signup_link.pack(side=ctk.LEFT, padx=5)
        signup_link.bind("<Button-1>", lambda event: self.master.show_register_page())

    def create_entry(self, parent, placeholder, show=None, width=300):
        frame = ctk.CTkFrame(parent, fg_color=BACKGROUND_COLOR)
        frame.pack(anchor='w', pady=5)

        ctk.CTkLabel(frame, text=placeholder, text_color=TEXT_COLOR, font=("Arial", 14)).pack(anchor='w')

        entry = ctk.CTkEntry(frame, font=("Arial", 12), fg_color="#ffffff", text_color=TEXT_COLOR, width=width, corner_radius=8, border_color=PLACEHOLDER_COLOR)
        entry.pack(anchor='w')
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, ctk.END)
                entry.configure(text_color=TEXT_COLOR)
                if show:
                    entry.configure(show=show)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(text_color=PLACEHOLDER_COLOR, show=None)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry

    def reset_form(self):
        self.username_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.username_entry.insert(0, "Username")
        self.password_entry.insert(0, "Password")

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "Username" or not username:
            messagebox.showerror("Error", "Please enter a valid username.")
            return

        if password == "Password" or not password:
            messagebox.showerror("Error", "Please enter a valid password.")
            return

        success, message, user_data = self.auth_service.login(username, password)
        self.master.user_data = user_data
        print(user_data)
        if success:
            self.master.show_home_page(user_data)
        else:
            messagebox.showerror("Error", message)
            self.reset_form()