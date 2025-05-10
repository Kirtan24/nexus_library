import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from ui.components.pages.main_layout import MainLayout
from app.controllers.user_controller import UserController
from PIL import Image, ImageTk
import os

class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.master = master
        self.user_data = user_data
        self.user_controller = UserController()

        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.configure(fg_color="#ffffff")

        self.create_widgets()

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="← Back",
            command=self.go_back,
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="#6f23ff",
            font=("Arial", 14),
            width=80,
            height=35,
            corner_radius=8,
            border_width=1,
            border_color="#6f23ff"
        )
        self.back_button.pack(side="left", padx=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="My Profile",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.create_profile_header()

        self.tabview = ctk.CTkTabview(self.main_container, width=600)
        self.tabview.pack(pady=20)

        self.tabview.add("Profile Info")
        self.tabview.add("Change Password")

        self.tabview.tab("Profile Info").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Change Password").grid_columnconfigure(0, weight=1)

        self.create_profile_info_tab()
        self.create_change_password_tab()

    def create_profile_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="#ffffff")
        header_frame.pack(fill="x", pady=(0, 20))

        profile_pic_frame = ctk.CTkFrame(header_frame, width=80, height=80, fg_color="#e0e0e0", corner_radius=40)
        profile_pic_frame.pack(side="left", padx=(0, 20))

        try:
            user_icon = ctk.CTkImage(
                light_image=Image.open(os.path.join("assets", "icons", "user.png")).resize((40, 40)),
                size=(40, 40)
            )
            ctk.CTkLabel(profile_pic_frame, image=user_icon, text="").place(relx=0.5, rely=0.5, anchor="center")
        except:

            ctk.CTkLabel(profile_pic_frame, text="👤", font=("Arial", 24)).place(relx=0.5, rely=0.5, anchor="center")

        user_info_frame = ctk.CTkFrame(header_frame, fg_color="#ffffff")
        user_info_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            user_info_frame,
            text=self.user_data.get('name', 'User'),
            font=("Arial", 20, "bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            user_info_frame,
            text=f"@{self.user_data.get('username', 'username')}",
            text_color="#666666",
            anchor="w"
        ).pack(fill="x")

        role_label = ctk.CTkLabel(
            user_info_frame,
            text=self.user_data.get('role', 'User').capitalize(),
            text_color="#ffffff",
            fg_color=self.get_role_color(self.user_data.get('role', 'user')),
            corner_radius=10,
            font=("Arial", 12),
            padx=10,
            pady=2
        )
        role_label.pack(anchor="w", pady=(5, 0))

    def get_role_color(self, role):
        role_colors = {
            'admin': '#d32f2f',
            'librarian': '#1976d2',
            'student': '#388e3c',
            'faculty': '#f57c00',
            'researcher': '#7b1fa2',
            'guest': '#455a64'
        }
        return role_colors.get(role.lower(), '#757575')

    def create_profile_info_tab(self):
        tab = self.tabview.tab("Profile Info")

        fields = [
            {"label": "Username", "value": self.user_data.get('username', ''), "editable": False},
            {"label": "Email", "value": self.user_data.get('email', ''), "editable": True, "key": "email"},
            {"label": "Full Name", "value": self.user_data.get('name', ''), "editable": True, "key": "name"},
            {"label": "Phone Number", "value": self.user_data.get('phone_number', ''), "editable": True, "key": "phone_number"},
            {"label": "Account Type", "value": self.user_data.get('role', '').capitalize(), "editable": False},
            {"label": "Member Since", "value": "2023-01-01", "editable": False}
        ]

        self.profile_entries = {}

        for i, field in enumerate(fields):
            frame = ctk.CTkFrame(tab, fg_color="#ffffff")
            frame.grid(row=i, column=0, sticky="ew", pady=(0, 10))

            label = ctk.CTkLabel(frame, text=field["label"] + ":", width=120, anchor="e")
            label.pack(side="left", padx=(0, 10))

            if field["editable"]:
                entry = ctk.CTkEntry(
                    frame,
                    placeholder_text=field["value"],
                    fg_color="#f5f5f5",
                    border_width=0,
                    corner_radius=5,
                    width=300
                )
                entry.insert(0, field["value"])
                entry.pack(side="left", fill="x", expand=True)
                self.profile_entries[field["key"]] = entry
            else:
                value_label = ctk.CTkLabel(
                    frame,
                    text=field["value"],
                    text_color="#333333",
                    anchor="w"
                )
                value_label.pack(side="left", fill="x", expand=True)


        update_btn = ctk.CTkButton(
            tab,
            text="Update Profile",
            command=self.update_profile,
            fg_color="#4caf50",
            hover_color="#388e3c"
        )
        update_btn.grid(row=len(fields)+1, column=0, pady=(20, 0))

    def create_change_password_tab(self):
        tab = self.tabview.tab("Change Password")

        current_frame = ctk.CTkFrame(tab, fg_color="#ffffff")
        current_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(
            current_frame,
            text="Current Password:",
            width=120,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.current_password_entry = ctk.CTkEntry(
            current_frame,
            placeholder_text="Enter current password",
            show="•",
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=5,
            width=300
        )
        self.current_password_entry.pack(side="left", fill="x", expand=True)

        new_frame = ctk.CTkFrame(tab, fg_color="#ffffff")
        new_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(
            new_frame,
            text="New Password:",
            width=120,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.new_password_entry = ctk.CTkEntry(
            new_frame,
            placeholder_text="Enter new password",
            show="•",
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=5,
            width=300
        )
        self.new_password_entry.pack(side="left", fill="x", expand=True)

        confirm_frame = ctk.CTkFrame(tab, fg_color="#ffffff")
        confirm_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        ctk.CTkLabel(
            confirm_frame,
            text="Confirm Password:",
            width=120,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.confirm_password_entry = ctk.CTkEntry(
            confirm_frame,
            placeholder_text="Confirm new password",
            show="•",
            fg_color="#f5f5f5",
            border_width=0,
            corner_radius=5,
            width=300
        )
        self.confirm_password_entry.pack(side="left", fill="x", expand=True)

        requirements = [
            "• At least 8 characters",
            "• At least one uppercase letter",
            "• At least one lowercase letter",
            "• At least one number"
        ]

        for i, req in enumerate(requirements):
            ctk.CTkLabel(
                tab,
                text=req,
                text_color="#666666",
                font=("Arial", 11),
                anchor="w"
            ).grid(row=3+i, column=0, sticky="w", pady=(0, 5))


        update_btn = ctk.CTkButton(
            tab,
            text="Change Password",
            command=self.change_password,
            fg_color="#2196f3",
            hover_color="#1976d2"
        )
        update_btn.grid(row=7, column=0, pady=(20, 0))

    def update_profile(self):
        updates = {}

        for key, entry in self.profile_entries.items():
            new_value = entry.get().strip()
            if new_value and new_value != self.user_data.get(key, ''):
                updates[key] = new_value

        if not updates:
            messagebox.showinfo("Info", "No changes to update")
            return

        success, message = self.user_controller.update_profile(
            self.user_data['user_id'],
            updates.get('name'),
            updates.get('email'),
            updates.get('phone_number')
        )

        if success:
            messagebox.showinfo("Success", "Profile updated successfully")

            for key, value in updates.items():
                self.user_data[key] = value
        else:
            messagebox.showerror("Error", message)

    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not current_password:
            messagebox.showerror("Error", "Please enter your current password")
            return

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match")
            return

        if len(new_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            return

        success, message = self.user_controller.change_password(
            self.user_data['user_id'],
            current_password,
            new_password,
            confirm_password
        )

        if success:
            messagebox.showinfo("Success", "Password changed successfully")

            self.current_password_entry.delete(0, 'end')
            self.new_password_entry.delete(0, 'end')
            self.confirm_password_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", message)

    def go_back(self):
        self.master.show_home_page(self.user_data)