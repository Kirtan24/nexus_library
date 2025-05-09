import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

from app.controllers.library_controller import LibraryController

# Colors
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

class ItemManagementPage(ctk.CTkFrame):
    """
    Page for managing library items (books, ebooks, papers, audiobooks)
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.library_controller = LibraryController()

        # Configure the frame
        self.pack(fill=ctk.BOTH, expand=True)
        self.configure(fg_color=BACKGROUND_COLOR)

        # Initialize variables
        self.current_item_id = None
        self.is_edit_mode = False
        self.current_item_type = ctk.StringVar(value="PrintedBook")
        self.search_type = ctk.StringVar(value="All Types")
        self.search_term = ctk.StringVar(value="")

        # Create UI components
        self.create_ui()

        # Load initial data
        self.refresh_items()

    def create_ui(self):
        """Create the main UI layout"""
        # Create top frame with title and back button
        self.create_header_frame()

        # Create main content with left panel (form) and right panel (table)
        content_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        content_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        # Left Panel - Item Form
        self.left_panel = ctk.CTkFrame(content_frame, fg_color=OFFWHITE_COLOR, corner_radius=10)
        self.left_panel.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 10))

        # Right Panel - Item Table and Search
        self.right_panel = ctk.CTkFrame(content_frame, fg_color=OFFWHITE_COLOR, corner_radius=10)
        self.right_panel.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True, padx=(10, 0))

        # Create form
        self.create_item_form()

        # Create table
        self.create_item_table()

    def create_header_frame(self):
        """Create header with title and back button"""
        header_frame = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR, height=60)
        header_frame.pack(fill=ctk.X, pady=(0, 10))

        # Back button
        back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            command=self.go_back,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=100,
            height=35,
            corner_radius=8
        )
        back_button.pack(side=ctk.LEFT, padx=20, pady=10)

        # Page title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Library Item Management",
            font=("Arial", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title_label.pack(side=ctk.LEFT, padx=20)

    def create_item_form(self):
        """Create form for adding/editing library items"""
        form_frame = ctk.CTkFrame(self.left_panel, fg_color=OFFWHITE_COLOR)
        form_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Title section
        form_title = ctk.CTkLabel(
            form_frame,
            text="Add New Item",
            font=("Arial", 18, "bold"),
            text_color=TEXT_COLOR
        )
        form_title.pack(anchor="w", pady=(0, 20))
        self.form_title_label = form_title

        # Item type selector
        type_frame = ctk.CTkFrame(form_frame, fg_color=OFFWHITE_COLOR)
        type_frame.pack(fill=ctk.X, pady=(0, 15))

        ctk.CTkLabel(
            type_frame,
            text="Item Type:",
            font=("Arial", 14),
            text_color=TEXT_COLOR
        ).pack(side=ctk.LEFT, padx=(0, 10))

        item_types = ["PrintedBook", "EBook", "ResearchPaper", "AudioBook"]
        type_dropdown = ctk.CTkComboBox(
            type_frame,
            values=item_types,
            variable=self.current_item_type,
            width=200,
            command=self.on_type_change
        )
        type_dropdown.pack(side=ctk.LEFT)

        # Form fields container with scrolling if needed
        self.form_container = ctk.CTkScrollableFrame(form_frame, fg_color=OFFWHITE_COLOR, width=400, height=400)
        self.form_container.pack(fill=ctk.BOTH, expand=True, pady=(10, 20))

        # Will hold all our form field widgets
        self.form_fields = {}

        # Create dynamic form based on initial type
        self.create_form_fields()

        # Action buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color=OFFWHITE_COLOR)
        button_frame.pack(fill=ctk.X, pady=(10, 0))

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Add Item",
            command=self.save_item,
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

    def create_form_fields(self):
        """Create form fields based on the selected item type"""
        # Clear existing fields
        for widget in self.form_container.winfo_children():
            widget.destroy()

        # Common fields for all item types
        common_fields = [
            {"name": "title", "label": "Title", "required": True},
            {"name": "author_id", "label": "Author ID", "required": True},
            {"name": "genre", "label": "Genre", "required": False},
            {"name": "publication_year", "label": "Publication Year", "required": False},
            {"name": "availability_status", "label": "Status", "required": False,
             "dropdown": ["Available", "Unavailable", "Borrowed", "Reserved"]},
        ]

        # Type-specific fields
        type_fields = {
            "PrintedBook": [
                {"name": "isbn", "label": "ISBN", "required": False},
                {"name": "shelf_location", "label": "Shelf Location", "required": False},
                {"name": "total_copies", "label": "Total Copies", "required": True},
                {"name": "available_copies", "label": "Available Copies", "required": True},
            ],
            "EBook": [
                {"name": "description", "label": "Description", "required": False, "multiline": True}
            ],
            "ResearchPaper": [
                {"name": "abstract", "label": "Abstract", "required": False, "multiline": True},
                {"name": "journal_name", "label": "Journal Name", "required": False},
                {"name": "doi", "label": "DOI", "required": False}
            ],
            "AudioBook": [
                {"name": "narrator", "label": "Narrator", "required": False},
                {"name": "duration_minutes", "label": "Duration (min)", "required": False},
                {"name": "description", "label": "Description", "required": False, "multiline": True}
            ]
        }

        # Combine common fields with selected type fields
        selected_type = self.current_item_type.get()
        all_fields = common_fields + type_fields.get(selected_type, [])

        # Create entry fields
        for field in all_fields:
            self.add_form_field(field)

    def add_form_field(self, field):
        """Add a single form field to the form container"""
        field_frame = ctk.CTkFrame(self.form_container, fg_color=OFFWHITE_COLOR)
        field_frame.pack(fill=ctk.X, pady=(0, 15))

        # Label - Add asterisk if required
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

        # Field (entry, dropdown or textbox)
        if "dropdown" in field:
            input_field = ctk.CTkComboBox(
                field_frame,
                values=field["dropdown"],
                width=250
            )
            input_field.set(field["dropdown"][0])
        elif field.get("multiline", False):
            input_field = ctk.CTkTextbox(
                field_frame,
                width=250,
                height=100,
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

        # Store reference to input field
        self.form_fields[field["name"]] = input_field

    def create_item_table(self):
        """Create the table for displaying library items"""
        # Search/filter section
        search_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        search_frame.pack(fill=ctk.X, padx=20, pady=20)

        ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=("Arial", 14),
            text_color=TEXT_COLOR
        ).pack(side=ctk.LEFT, padx=(0, 10))

        search_entry = ctk.CTkEntry(
            search_frame,
            width=200,
            textvariable=self.search_term,
            border_width=1,
            border_color="#dddddd",
            fg_color="#ffffff",
            text_color=TEXT_COLOR
        )
        search_entry.pack(side=ctk.LEFT, padx=(0, 10))

        type_dropdown = ctk.CTkComboBox(
            search_frame,
            values=["All Types", "PrintedBook", "EBook", "ResearchPaper", "AudioBook"],
            variable=self.search_type,
            width=150
        )
        type_dropdown.pack(side=ctk.LEFT, padx=(0, 10))

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_items,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=100
        )
        search_button.pack(side=ctk.LEFT)

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            command=self.refresh_items,
            fg_color=REFRESH_COLOR,
            hover_color=REFRESH_HOVER_COLOR,
            text_color="#ffffff",
            width=100
        )
        refresh_button.pack(side=ctk.LEFT, padx=(10, 0))

        # Create table frame
        table_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        table_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Create treeview for items table
        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Title", "Author", "Type", "Status"),
            show="headings",
            selectmode="browse",
            height=20
        )

        # Configure column widths and headings
        self.table.heading("ID", text="ID")
        self.table.heading("Title", text="Title")
        self.table.heading("Author", text="Author")
        self.table.heading("Type", text="Type")
        self.table.heading("Status", text="Status")

        self.table.column("ID", width=50, anchor="center")
        self.table.column("Title", width=150, anchor="w")
        self.table.column("Author", width=150, anchor="w")
        self.table.column("Type", width=80, anchor="center")
        self.table.column("Status", width=80, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        # Pack table and scrollbar
        self.table.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Create bottom buttons for item actions
        actions_frame = ctk.CTkFrame(self.right_panel, fg_color=OFFWHITE_COLOR)
        actions_frame.pack(fill=ctk.X, padx=20, pady=(0, 20))

        edit_button = ctk.CTkButton(
            actions_frame,
            text="Edit Selected",
            command=self.edit_selected_item,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text_color="#ffffff",
            width=120
        )
        edit_button.pack(side=ctk.LEFT, padx=(0, 10))

        delete_button = ctk.CTkButton(
            actions_frame,
            text="Delete Selected",
            command=self.delete_selected_item,
            fg_color="#ff3333",
            hover_color="#cc0000",
            text_color="#ffffff",
            width=120
        )
        delete_button.pack(side=ctk.LEFT, padx=(0, 10))

        view_button = ctk.CTkButton(
            actions_frame,
            text="View Details",
            command=self.view_item_details,
            fg_color="#555555",
            hover_color="#333333",
            text_color="#ffffff",
            width=120
        )
        view_button.pack(side=ctk.LEFT)

    def on_type_change(self, event=None):
        """Handle change in selected item type"""
        self.create_form_fields()

    def clear_form(self):
        """Clear all form fields"""
        for name, field in self.form_fields.items():
            if isinstance(field, ctk.CTkTextbox):
                field.delete("1.0", ctk.END)
            elif isinstance(field, ctk.CTkComboBox):
                # For comboboxes, set to first value
                values = field._values
                if values:
                    field.set(values[0])
            else:
                field.delete(0, ctk.END)

        # Reset edit mode
        self.is_edit_mode = False
        self.current_item_id = None
        self.form_title_label.configure(text="Add New Item")
        self.save_button.configure(text="Add Item")

    def get_form_values(self):
        """Extract values from all form fields"""
        values = {"item_type": self.current_item_type.get()}

        for name, field in self.form_fields.items():
            try:
                if isinstance(field, ctk.CTkTextbox):
                    values[name] = field.get("1.0", ctk.END).strip()
                else:
                    values[name] = field.get()
            except tk.TclError:
                values[name] = None  # or skip setting it entirely


        # Validate required fields
        required_fields = ["title", "author_id"]
        for field in required_fields:
            if not values.get(field):
                messagebox.showerror("Validation Error", f"{field.capitalize()} is required.")
                return None

        # Convert numeric fields
        try:
            if values.get("publication_year") and values["publication_year"]:
                values["publication_year"] = int(values["publication_year"])
            if values.get("duration") and values["duration"]:
                values["duration"] = int(values["duration"])
            if values.get("author_id") and values["author_id"]:
                values["author_id"] = int(values["author_id"])
            if values.get("total_copies") and values["total_copies"]:
                values["total_copies"] = int(values["total_copies"])
            if values.get("available_copies") and values["available_copies"]:
                values["available_copies"] = int(values["available_copies"])
        except ValueError:
            messagebox.showerror("Input Error", "Numeric fields should contain numbers only.")
            return None

        return values

    def save_item(self):
        """Save or update an item based on edit mode"""
        values = self.get_form_values()
        print(values)
        if not values:
            return

        try:
            if self.is_edit_mode and self.current_item_id:
                # Update existing item
                success, message = self.library_controller.update_item(
                    self.current_item_id,
                    **values
                )
                action = "updated"
            else:
                # Add new item
                success, message = self.library_controller.add_item(
                    values["item_type"],
                    values["title"],
                    values["author_id"],
                    **{k: v for k, v in values.items() if k not in ["item_type", "title", "author_id"]}
                )
                action = "added"

            if success:
                messagebox.showinfo("Success", f"Item successfully {action}.")
                self.clear_form()
                self.refresh_items()
            else:
                messagebox.showerror("Error", f"Failed to {action[:-1]} item: {message}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_items(self):
        """Refresh the items table"""
        # Clear existing items
        for item in self.table.get_children():
            self.table.delete(item)

        # Get all items
        items = self.library_controller.search_items()

        # Add items to table
        for i, item in enumerate(items):
            item_id = item.get("item_id", "")
            title = item.get("title", "")
            author = item.get("author_name", "Unknown")
            item_type = item.get("item_type", "")
            status = item.get("availability_status", "Unknown")

            # Insert with alternating row colors
            tag = "even" if i % 2 == 0 else "odd"
            self.table.insert("", "end", values=(item_id, title, author, item_type, status), tags=(tag,))

        # Configure alternating row colors
        self.table.tag_configure("odd", background=TABLE_ODD_COLOR)
        self.table.tag_configure("even", background=TABLE_EVEN_COLOR)

    def search_items(self):
        """Search items based on filters"""
        search_text = self.search_term.get().strip()
        item_type = self.search_type.get()

        # Clear existing items
        for item in self.table.get_children():
            self.table.delete(item)

        # Apply search filters
        type_filter = None if item_type == "All Types" else item_type
        items = self.library_controller.search_items(
            title=search_text if search_text else None,
            item_type=type_filter
        )

        # Add items to table
        for i, item in enumerate(items):
            item_id = item.get("item_id", "")
            title = item.get("title", "")
            author = item.get("author_name", "Unknown")
            item_type = item.get("item_type", "")
            status = item.get("availability_status", "Unknown")

            # Insert with alternating row colors
            tag = "even" if i % 2 == 0 else "odd"
            self.table.insert("", "end", values=(item_id, title, author, item_type, status), tags=(tag,))

    # def edit_selected_item(self):
    #     """Load the selected item into the form for editing"""
    #     selected = self.table.selection()
    #     if not selected:
    #         messagebox.showinfo("Info", "Please select an item to edit.")
    #         return

    #     # Get item ID from the selected row
    #     item_id = self.table.item(selected[0])["values"][0]

    #     # Fetch item details
    #     item = self.library_controller.get_item(item_id)
    #     print(item)
    #     if not item:
    #         messagebox.showerror("Error", "Failed to load item details.")
    #         return

    #     self.is_edit_mode = True
    #     self.current_item_id = item_id
    #     self.form_title_label.configure(text=f"Edit Item #{item_id}")
    #     self.save_button.configure(text="Update Item")

    #     self.current_item_type.set(item["item_type"])
    #     self.on_type_change()

    #     # Populate form fields with item data
    #     for name, field in self.form_fields.items():
    #         print(name, field)
    #         value = item.get(name, "")
    #         if value is not None:
    #             if isinstance(field, ctk.CTkTextbox):
    #                 field.delete("1.0", ctk.END)
    #                 field.insert("1.0", str(value))
    #             elif isinstance(field, ctk.CTkEntry):
    #                 field.delete(0, ctk.END)
    #                 field.insert(0, str(value))
    #             elif isinstance(field, ctk.CTkComboBox):
    #                 field.set(str(value))

    def edit_selected_item(self):
        """Load the selected item into the form for editing"""
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an item to edit.")
            return

        item_id = self.table.item(selected[0])["values"][0]

        item = self.library_controller.get_item(item_id)
        if not item:
            messagebox.showerror("Error", "Failed to load item details.")
            return

        print("Item data received:", item)

        self.is_edit_mode = True
        self.current_item_id = item_id
        self.form_title_label.configure(text=f"Edit Item #{item_id}")
        self.save_button.configure(text="Update Item")

        # Set the item type first
        self.current_item_type.set(item["item_type"])
        # Recreate form fields for the correct type
        self.create_form_fields()

        # Give the UI a moment to update
        self.update_idletasks()

        # Populate ALL form fields with item data
        for name, field in self.form_fields.items():
            value = item.get(name, "")
            print(f"Setting field {name} to {value}")  # Debug print

            if value is not None:
                try:
                    if isinstance(field, ctk.CTkTextbox):
                        field.delete("1.0", ctk.END)
                        field.insert("1.0", str(value))
                    elif isinstance(field, ctk.CTkEntry):
                        field.delete(0, ctk.END)
                        field.insert(0, str(value))
                    elif isinstance(field, ctk.CTkComboBox):
                        # Try to set the value, fall back to first option if not available
                        if str(value) in field._values:
                            field.set(str(value))
                        elif field._values:
                            field.set(field._values[0])
                except Exception as e:
                    print(f"Error setting field {name}: {e}")  # Debug print

    def delete_selected_item(self):
        """Delete the selected item"""
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an item to delete.")
            return

        # Get item ID from the selected row
        item_id = self.table.item(selected[0])["values"][0]
        title = self.table.item(selected[0])["values"][1]

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'?"):
            return

        # Delete the item
        success, message = self.library_controller.delete_item(item_id)

        if success:
            messagebox.showinfo("Success", "Item deleted successfully.")
            self.refresh_items()
        else:
            messagebox.showerror("Error", f"Failed to delete item: {message}")

    def view_item_details(self):
        """Show detailed view of the selected item in a simple Tkinter window"""
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select an item to view.")
            return

        item_id = self.table.item(selected[0])["values"][0]

        item = self.library_controller.get_item(item_id)
        if not item:
            messagebox.showerror("Error", "Failed to load item details.")
            return

        # Create a new top-level window
        details_window = tk.Toplevel(self)
        details_window.title(f"Item Details: {item.get('title', 'Details')}")
        details_window.geometry("500x500")
        details_window.transient(self)
        details_window.grab_set()

        # Create a scrollable canvas + frame
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

        # Title
        tk.Label(frame, text=item.get('title', 'Unknown Title'), font=("Arial", 16, "bold")).pack(pady=(10, 10))

        def add_info(label, value, multiline=False):
            tk.Label(frame, text=label + ":", font=("Arial", 10, "bold"), anchor="w").pack(fill='x', padx=10)
            if multiline:
                text_widget = tk.Text(frame, height=4, wrap="word")
                text_widget.insert("1.0", value)
                text_widget.config(state="disabled")
                text_widget.pack(fill='x', padx=10, pady=(0, 10))
            else:
                tk.Label(frame, text=value, anchor="w").pack(fill='x', padx=10, pady=(0, 10))

        # Basic info
        add_info("ID", item.get('item_id', ''))
        add_info("Type", item.get('item_type', ''))
        add_info("Author", item.get('author_name', 'Unknown'))
        add_info("Genre", item.get('genre', 'N/A'))
        add_info("Publication Year", item.get('publication_year', 'N/A'))
        add_info("Status", item.get('availability_status', 'Unknown'))

        # Type-specific
        item_type = item.get('item_type', '')
        if item_type == 'PrintedBook':
            add_info("ISBN", item.get('isbn', 'N/A'))
            add_info("Shelf Location", item.get('shelf_location', 'N/A'))
        elif item_type == 'EBook':
            add_info("Cover URL", item.get('cover_image_url', 'N/A'))
            add_info("Description", item.get('description', 'N/A'), multiline=True)
        elif item_type == 'ResearchPaper':
            add_info("Journal", item.get('journal_name', 'N/A'))
            add_info("DOI", item.get('doi', 'N/A'))
            add_info("Abstract", item.get('abstract', 'N/A'), multiline=True)
        elif item_type == 'AudioBook':
            add_info("Narrator", item.get('narrator', 'N/A'))
            add_info("Duration (min)", item.get('duration_minutes', 'N/A'))
            add_info("Description", item.get('description', 'N/A'), multiline=True)


    def add_detail_section(self, parent, title, fields):
        """Add a section of details to the details view"""
        # Section title
        ctk.CTkLabel(
            parent,
            text=title,
            font=("Arial", 16, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(20, 10))

        # Section divider
        divider = ctk.CTkFrame(parent, height=2, fg_color="#dddddd")
        divider.pack(fill=ctk.X, pady=(0, 10))

        # Fields
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
        """Navigate back to the previous page"""
        self.destroy()
        self.master.show_home_page()
