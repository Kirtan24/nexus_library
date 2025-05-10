import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os
from app.services.auth_services import AuthenticationService

BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#000000"
PLACEHOLDER_COLOR = "#888888"
BORDER_COLOR = "#a875ff"

USER_ROLES = ["Select Role", "Guest", "Student", "Researcher", "Faculty", "Librarian"]

class RegisterPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.auth_service = AuthenticationService()

        self.root = self.master.master
        self.root.title("Register - Nexus Library")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        self.create_ui()

    def create_ui(self):

        container = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center")


        try:
            img_path = os.path.join("assets", "logo", "logo.png")
            logo_img = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(100, 100))
            ctk.CTkLabel(container, image=logo_img, text="", fg_color=BACKGROUND_COLOR).pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")


        ctk.CTkLabel(container, text="Register", text_color=TEXT_COLOR, font=("Arial", 36, "bold")).pack(pady=10)


        self.role_var = ctk.StringVar(value=USER_ROLES[0])
        self.create_labeled_widget(container, "Select User Role",
            ctk.CTkComboBox(container, values=USER_ROLES, variable=self.role_var,
                           fg_color="#ffffff", text_color=TEXT_COLOR, width=410))

        fields_frame = ctk.CTkFrame(container, fg_color=BACKGROUND_COLOR)
        fields_frame.pack(pady=10)


        row1 = ctk.CTkFrame(fields_frame, fg_color=BACKGROUND_COLOR)
        row1.pack(fill="x", pady=5)
        self.name_entry = self.create_labeled_entry(row1, "Full Name", "Full Name", side=ctk.LEFT)
        self.username_entry = self.create_labeled_entry(row1, "Username", "Username", side=ctk.RIGHT)


        row2 = ctk.CTkFrame(fields_frame, fg_color=BACKGROUND_COLOR)
        row2.pack(fill="x", pady=5)
        self.email_entry = self.create_labeled_entry(row2, "Email Address", "Email Address", side=ctk.LEFT)
        self.phone_entry = self.create_labeled_entry(row2, "Phone Number", "Phone Number", side=ctk.RIGHT)


        row3 = ctk.CTkFrame(fields_frame, fg_color=BACKGROUND_COLOR)
        row3.pack(fill="x", pady=5)
        self.password_entry = self.create_labeled_entry(row3, "Password", "Password", side=ctk.LEFT, show="*")
        self.confirm_password_entry = self.create_labeled_entry(row3, "Confirm Password", "Confirm Password", side=ctk.RIGHT, show="*")


        button_frame = ctk.CTkFrame(container, fg_color=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        login_button = ctk.CTkButton(button_frame, text="Register", font=("Arial", 16, "bold"), fg_color=TEXT_COLOR, text_color=BACKGROUND_COLOR, command=self.register_user)
        login_button.pack(side=ctk.LEFT, padx=10)

        back_button = ctk.CTkButton(button_frame, text="Back", font=("Arial", 16, "bold"), fg_color=TEXT_COLOR, text_color=BACKGROUND_COLOR,width=80, command=self.master.show_home_page)
        back_button.pack(side=ctk.LEFT)


        login_frame = ctk.CTkFrame(container, fg_color=BACKGROUND_COLOR)
        login_frame.pack()
        ctk.CTkLabel(login_frame, text="Already have an account?", text_color=TEXT_COLOR,
                    font=("Arial", 12)).pack(side=ctk.LEFT)

        login_link = ctk.CTkLabel(login_frame, text="Login", text_color=TEXT_COLOR,
                                 font=("Arial", 12, "bold", "underline"), cursor="hand2")
        login_link.pack(side=ctk.LEFT, padx=5)
        login_link.bind("<Button-1>", lambda event: self.master.show_login_page())

    def create_labeled_widget(self, parent, label_text, widget, side=None):
        """Create a labeled widget with a consistent layout"""
        frame = ctk.CTkFrame(parent, fg_color=BACKGROUND_COLOR)
        if side:
            frame.pack(side=side, padx=10)
        else:
            frame.pack(fill='x', pady=5)

        ctk.CTkLabel(frame, text=label_text, text_color=TEXT_COLOR,
                    font=("Arial", 14)).pack(anchor='w')
        widget.pack(pady=2)
        return widget

    def create_labeled_entry(self, parent, label_text, placeholder, side=None, show=None):
        """Create a labeled entry field with placeholder behavior"""
        frame = ctk.CTkFrame(parent, fg_color=BACKGROUND_COLOR)
        frame.pack(side=side, padx=10)

        ctk.CTkLabel(frame, text=label_text, text_color=TEXT_COLOR, font=("Arial", 14)).pack(anchor='w')

        entry = ctk.CTkEntry(frame, font=("Arial", 12), fg_color="#ffffff", text_color=PLACEHOLDER_COLOR,
                            width=200, corner_radius=8, border_color=PLACEHOLDER_COLOR)
        entry.pack(pady=2)
        entry.insert(0, placeholder)


        entry.bind("<FocusIn>", lambda e: self.on_entry_focus_in(e, entry, placeholder, show))
        entry.bind("<FocusOut>", lambda e: self.on_entry_focus_out(e, entry, placeholder))

        return entry

    def on_entry_focus_in(self, event, entry, placeholder, show):
        if entry.get() == placeholder:
            entry.delete(0, ctk.END)
            entry.configure(text_color=TEXT_COLOR)
            if show:
                entry.configure(show=show)

    def on_entry_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(text_color=PLACEHOLDER_COLOR, show=None)

    def register_user(self):

        data = {
            'role': self.role_var.get(),
            'name': self.name_entry.get(),
            'username': self.username_entry.get(),
            'email': self.email_entry.get(),
            'phone': self.phone_entry.get(),
            'password': self.password_entry.get(),
            'confirm_password': self.confirm_password_entry.get()
        }


        if data['role'] == USER_ROLES[0]:
            messagebox.showerror("Error", "Please select a valid user role!")
            return

        if not all([data['name'], data['username'], data['email'], data['password'], data['confirm_password']]):
            messagebox.showerror("Error", "All fields except phone number are required!")
            return


        success, message = self.auth_service.register(
            data['username'], data['email'], data['password'], data['confirm_password'],
            data['name'], data['phone'], data['role'].lower()
        )

        if success:
            messagebox.showinfo("Success", f"User {data['username']} registered successfully as {data['role']}")
            self.master.show_login_page()
        else:
            error_message = "\n".join(message) if isinstance(message, list) else message
            messagebox.showerror("Registration Failed", error_message)