import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

from app.controllers.author_controller import AuthorController

BACKGROUND_COLOR = "#f8f9fa"
OFFWHITE_COLOR = "#f0f0f0"
ACCENT_COLOR = "#6f23ff"
TEXT_COLOR = "#000000"

BUTTON_COLOR = "#6f23ff"
BUTTON_HOVER_COLOR = "#5a1dcc"

REFRESH_COLOR = "#f1c40f"
REFRESH_HOVER_COLOR = "#d4ac0d"

TABLE_ODD_COLOR = "#f0f0f0"
TABLE_EVEN_COLOR = "#ffffff"
TABLE_HEADER_COLOR = "#e0e0e0"

class AuthorManagementPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.author_controller = AuthorController()

        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        self.current_author_id = None
        self.is_edit_mode = False
        self.search_term = ctk.StringVar(value="")
        self.search_nationality = ctk.StringVar(value="")

        self.create_ui()

        self.refresh_authors()

    def create_ui(self):
        self.create_header_frame()

        content_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        content_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        self.left_panel = ctk.CTkFrame(content_frame, fg_color=OFFWHITE_COLOR, corner_radius=10)
        self.left_panel.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 10))

        self.right_panel = ctk.CTkFrame(content_frame, fg_color=OFFWHITE_COLOR, corner_radius=10)
        self.right_panel.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=(10, 0))

        self.create_author_form()

        self.create_author_table()

    def create_header_frame(self):
        header_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, height=60)
        header_frame.pack(fill=ctk.X, pady=(0, 10))

        back_button = ctk.CTkButton(
            header_frame,
            text="←",
            command=self.go_back,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=100,
            height=35,
            corner_radius=8
        )
        back_button.pack(side=ctk.LEFT, padx=20, pady=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Author Management",
            font=("Arial", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title_label.pack(side=ctk.LEFT, padx=20)

    def create_author_form(self):
        form_frame = ctk.CTkFrame(self.left_panel, fg_color=OFFWHITE_COLOR)
        form_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        form_title = ctk.CTkLabel(
            form_frame,
            text="Add New Author",
            font=("Arial", 18, "bold"),
            text_color=TEXT_COLOR
        )
        form_title.pack(anchor="w", pady=(0, 20))
        self.form_title_label = form_title

        self.form_container = ctk.CTkScrollableFrame(form_frame, fg_color=OFFWHITE_COLOR, width=400, height=400)
        self.form_container.pack(fill=ctk.BOTH, expand=True, pady=(10, 20))

        self.form_fields = {}

        self.add_form_field({
            "name": "name",
            "label": "Name",
            "required": True
        })

        self.add_form_field({
            "name": "nationality",
            "label": "Nationality",
            "required": False
        })

        self.add_form_field({
            "name": "genres",
            "label": "Genres",
            "required": False,
        })

        self.add_form_field({
            "name": "bio",
            "label": "Biography",
            "required": False,
            "multiline": True
        })

        button_frame = ctk.CTkFrame(form_frame, fg_color=OFFWHITE_COLOR)
        button_frame.pack(fill=ctk.X, pady=(10, 0))

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Author",
            command=self.save_author,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=120,
            height=40,
            corner_radius=8
        )
        self.save_button.pack(side=ctk.LEFT, padx=(0, 10))

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            fg_color="#888888",
            hover_color="#666666",
            text_color="#ffffff",
            width=120,
            height=40,
            corner_radius=8
        )
        self.clear_button.pack(side=ctk.LEFT)

    def add_form_field(self, field):
        field_frame = ctk.CTkFrame(self.form_container, fg_color=OFFWHITE_COLOR)
        field_frame.pack(fill=ctk.X, pady=(0, 15))

        label_text = f"{field['label']}{'*' if field.get('required', False) else ''}"
        label = ctk.CTkLabel(
            field_frame,
            text=label_text,
            font=("Arial", 14),
            text_color=TEXT_COLOR,
            anchor="w",
            width=150
        )
        label.pack(side=ctk.LEFT)

        if field.get("multiline", False):
            input_field = ctk.CTkTextbox(
                field_frame,
                width=250,
                height=150,
                border_width=1,
                border_color="#dddddd",
                fg_color="#ffffff",
                text_color=TEXT_COLOR
            )
        else:
            input_field = ctk.CTkEntry(
                field_frame,
                width=250,
                border_width=1,
                border_color="#dddddd",
                fg_color="#ffffff",
                text_color=TEXT_COLOR
            )

        input_field.pack(side=ctk.LEFT, padx=(10, 0))

        if field.get("help"):
            help_frame = ctk.CTkFrame(self.form_container, fg_color=OFFWHITE_COLOR)
            help_frame.pack(fill=ctk.X, pady=(0, 15))

            help_label = ctk.CTkLabel(
                help_frame,
                text=field["help"],
                font=("Arial", 12, "italic"),
                text_color="#666666",
                anchor="w"
            )
            help_label.pack(side=ctk.RIGHT, padx=(0, 10))

        self.form_fields[field["name"]] = input_field

    def create_author_table(self):
        search_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        search_frame.pack(fill=ctk.X, padx=20, pady=20)

        ctk.CTkLabel(
            search_frame,
            text="Name:",
            font=("Arial", 14),
            text_color=TEXT_COLOR
        ).pack(side=ctk.LEFT, padx=(0, 10))

        search_entry = ctk.CTkEntry(
            search_frame,
            width=150,
            textvariable=self.search_term,
            border_width=1,
            border_color="#dddddd",
            fg_color="#ffffff",
            text_color=TEXT_COLOR
        )
        search_entry.pack(side=ctk.LEFT, padx=(0, 10))

        ctk.CTkLabel(
            search_frame,
            text="Nationality:",
            font=("Arial", 14),
            text_color=TEXT_COLOR
        ).pack(side=ctk.LEFT, padx=(10, 10))

        nationality_entry = ctk.CTkEntry(
            search_frame,
            width=150,
            textvariable=self.search_nationality,
            border_width=1,
            border_color="#dddddd",
            fg_color="#ffffff",
            text_color=TEXT_COLOR
        )
        nationality_entry.pack(side=ctk.LEFT, padx=(0, 10))

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_authors,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=100
        )
        search_button.pack(side=ctk.LEFT)

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.refresh_authors,
            fg_color=REFRESH_COLOR,
            hover_color=REFRESH_HOVER_COLOR,
            text_color="#000000",
            width=100
        )
        refresh_button.pack(side=ctk.LEFT, padx=(10, 0))

        table_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        table_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Nationality", "Genres"),
            show="headings",
            selectmode="browse",
            height=20
        )

        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Nationality", text="Nationality")
        self.table.heading("Genres", text="Genres")

        self.table.column("ID", width=50, anchor="center")
        self.table.column("Name", width=200, anchor="w")
        self.table.column("Nationality", width=150, anchor="w")
        self.table.column("Genres", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        actions_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        actions_frame.pack(fill=ctk.X, padx=20, pady=(0, 20))

        edit_button = ctk.CTkButton(
            actions_frame,
            text="Edit Selected",
            command=self.edit_selected_author,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=120
        )
        edit_button.pack(side=ctk.LEFT, padx=(0, 10))

        delete_button = ctk.CTkButton(
            actions_frame,
            text="Delete Selected",
            command=self.delete_selected_author,
            fg_color="#ff3333",
            hover_color="#cc0000",
            text_color="#ffffff",
            width=120
        )
        delete_button.pack(side=ctk.LEFT, padx=(0, 10))

        view_button = ctk.CTkButton(
            actions_frame,
            text="View Details",
            command=self.view_author_details,
            fg_color="#555555",
            hover_color="#333333",
            text_color="#ffffff",
            width=120
        )
        view_button.pack(side=ctk.LEFT)

    def clear_form(self):
        for name, field in self.form_fields.items():
            if isinstance(field, ctk.CTkTextbox):
                field.delete("1.0", ctk.END)
            else:
                field.delete(0, ctk.END)

        self.is_edit_mode = False
        self.current_author_id = None
        self.form_title_label.configure(text="Add New Author")
        self.save_button.configure(text="Add Author")

    def get_form_values(self):
        values = {}

        for name, field in self.form_fields.items():
            try:
                if isinstance(field, ctk.CTkTextbox):
                    values[name] = field.get("1.0", ctk.END).strip()
                else:
                    values[name] = field.get().strip()
            except tk.TclError:
                values[name] = None

        required_fields = ["name"]
        for field in required_fields:
            if not values.get(field):
                messagebox.showerror("Validation Error", f"{field.capitalize()} is required.")
                return None

        if values.get("genres"):

            genres_list = [genre.strip() for genre in values["genres"].split(",") if genre.strip()]
            values["genres"] = genres_list
        else:
            values["genres"] = None

        return values

    def save_author(self):
        values = self.get_form_values()
        if not values:
            return

        try:
            if self.is_edit_mode and self.current_author_id:

                success, message = self.author_controller.update_author(
                    self.current_author_id,
                    **values
                )
                action = "updated"
            else:

                success, message = self.author_controller.add_author(
                    values["name"],
                    values.get("bio"),
                    values.get("nationality"),
                    values.get("genres")
                )
                action = "added"

            if success:
                messagebox.showinfo("Success", f"Author successfully {action}.")
                self.clear_form()
                self.refresh_authors()
            else:
                if isinstance(message, list):
                    messagebox.showerror("Error", "\n".join(message))
                else:
                    messagebox.showerror("Error", f"Failed to {action[:-1]} author: {message}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_authors(self):
        for item in self.table.get_children():
            self.table.delete(item)

        authors = self.author_controller.get_all_authors()

        for i, author in enumerate(authors):
            author_id = author.get("author_id", "")
            name = author.get("name", "")
            nationality = author.get("nationality", "")


            genres = author.get("genres", [])
            if genres and isinstance(genres, list):
                genres_display = ", ".join(genres)
            elif genres and isinstance(genres, str):

                genres_display = genres
            else:
                genres_display = ""


            tag = "even" if i % 2 == 0 else "odd"
            self.table.insert("", "end", values=(author_id, name, nationality, genres_display), tags=(tag,))

        self.table.tag_configure("odd", background=TABLE_ODD_COLOR)
        self.table.tag_configure("even", background=TABLE_EVEN_COLOR)

    def search_authors(self):
        name_text = self.search_term.get().strip()
        nationality_text = self.search_nationality.get().strip()

        for item in self.table.get_children():
            self.table.delete(item)

        authors = self.author_controller.search_authors(
            name=name_text if name_text else None,
            nationality=nationality_text if nationality_text else None
        )

        for i, author in enumerate(authors):
            author_id = author.get("author_id", "")
            name = author.get("name", "")
            nationality = author.get("nationality", "")


            genres = author.get("genres", [])
            if genres and isinstance(genres, list):
                genres_display = ", ".join(genres)
            elif genres and isinstance(genres, str):

                genres_display = genres
            else:
                genres_display = ""


            tag = "even" if i % 2 == 0 else "odd"
            self.table.insert("", "end", values=(author_id, name, nationality, genres_display), tags=(tag,))

    def edit_selected_author(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an author to edit.")
            return

        author_id = self.table.item(selected[0])["values"][0]

        author = self.author_controller.get_author(author_id)
        if not author:
            messagebox.showerror("Error", "Failed to load author details.")
            return

        self.is_edit_mode = True
        self.current_author_id = author_id
        self.form_title_label.configure(text=f"Edit Author #{author_id}")
        self.save_button.configure(text="Update Author")

        for name, field in self.form_fields.items():
            value = author.get(name, "")


            if name == "genres" and value and isinstance(value, list):
                value = ", ".join(value)

            if value is not None:
                if isinstance(field, ctk.CTkTextbox):
                    field.delete("1.0", ctk.END)
                    field.insert("1.0", str(value))
                else:
                    field.delete(0, ctk.END)
                    field.insert(0, str(value))

    def delete_selected_author(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an author to delete.")
            return

        author_id = self.table.item(selected[0])["values"][0]
        name = self.table.item(selected[0])["values"][1]

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete author '{name}'?"):
            return

        success, message = self.author_controller.delete_author(author_id)

        if success:
            messagebox.showinfo("Success", "Author deleted successfully.")
            self.refresh_authors()
        else:
            if isinstance(message, list):
                messagebox.showerror("Error", "\n".join(message))
            else:
                messagebox.showerror("Error", f"Failed to delete author: {message}")

    def view_author_details(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an item to view.")
            return

        author_id = self.table.item(selected[0])["values"][0]

        author = self.author_controller.get_author(author_id)
        if not author:
            messagebox.showerror("Error", "Failed to load author` details.")
            return

        details_window = tk.Toplevel(self)
        details_window.title(f"Author Details: {author.get('name', '')}")
        details_window.geometry("700x400")
        details_window.transient(self)
        details_window.grab_set()

        canvas = tk.Canvas(details_window, borderwidth=0)
        frame = tk.Frame(canvas)
        vsb = tk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

        tk.Label(frame, text=author.get('name', 'Unknown'), font=("Arial", 16, "bold")).pack(pady=(10, 10))

        def add_info(label, value, multiline=False):
            tk.Label(frame, text=label + ":", font=("Arial", 10, "bold"), anchor="w").pack(fill='x', padx=10)
            if multiline:
                text_widget = tk.Text(frame, height=5, wrap="word")
                text_widget.insert("1.0", value)
                text_widget.config(state="disabled")
                text_widget.pack(fill='x', padx=10, pady=(0, 10))
            else:
                tk.Label(frame, text=value, anchor="w").pack(fill='x', padx=10, pady=(0, 10))

        add_info("ID", author.get('author_id', ''))
        add_info("Name", author.get('name', ''))
        add_info("Nationality", author.get('nationality', 'N/A'))
        add_info("Genres", ', '.join(author.get('genres', [])) if isinstance(author.get('genres'), list) and author.get('genres') else 'N/A')
        add_info("Biography", author.get('bio', 'N/A'), True)

    def add_detail_section(self, parent, title, fields):
        ctk.CTkLabel(
            parent,
            text=title,
            font=("Arial", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(20, 10))

        divider = ctk.CTkFrame(parent, height=2, fg_color="#dddddd")
        divider.pack(fill=ctk.X, pady=(0, 10))

        for field in fields:
            field_frame = ctk.CTkFrame(parent, fg_color="transparent")
            field_frame.pack(fill=ctk.X, pady=(0, 10))

            ctk.CTkLabel(
                field_frame,
                text=f"{field['label']}:",
                font=("Arial", 14, "bold"),
                text_color=TEXT_COLOR,
                width=150,
                anchor="w"
            ).pack(side=ctk.LEFT)

            if field.get("multiline", False):
                value_box = ctk.CTkTextbox(
                    field_frame,
                    width=350,
                    height=100,
                    fg_color="#f9f9f9",
                    text_color=TEXT_COLOR,
                    corner_radius=5
                )
                value_box.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
                value_box.insert("1.0", str(field['value']))
                value_box.configure(state="disabled")
            else:
                ctk.CTkLabel(
                    field_frame,
                    text=str(field['value']),
                    font=("Arial", 14),
                    text_color=TEXT_COLOR,
                    anchor="w"
                ).pack(side=ctk.LEFT, fill=ctk.X, expand=True)

    def go_back(self):
        self.destroy()
        self.master.show_home_page()