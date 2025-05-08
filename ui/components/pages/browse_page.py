import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging

from app.services.book_services import BookService
from ui.components.pages.searchbar import SearchBar
from ui.components.pages.main_layout import MainLayout

class BrowsePage(MainLayout):
    def __init__(self, master, show_item_detail_callback):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.master = master
        self.show_item_detail_callback = show_item_detail_callback
        self.book_service = BookService()
        self.logger = logging.getLogger(__name__)

        self.current_search_term = ""
        self.current_search_strategy = "keyword"
        self.current_items = []

        # Use pack instead of grid for the main components
        self.content_frame = ctk.CTkFrame(self.content_container, fg_color="#f8f9fa")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Search bar at the top
        self.search_bar = SearchBar(
            self.content_frame,
            search_callback=self._search_items
        )
        self.search_bar.pack(fill="x", padx=10, pady=10)

        # Table frame below search bar
        self.table_frame = ctk.CTkFrame(self.content_frame)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure table_frame to use grid internally
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self._create_table()
        self._load_items()

    def _create_table(self):
        """Create the table to display library items using CTk instead of Treeview"""
        # Main container for the table
        self.table_container = ctk.CTkScrollableFrame(self.table_frame)
        self.table_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Define columns weights
        self.table_container.grid_columnconfigure(0, weight=3)  # Title (wider)
        self.table_container.grid_columnconfigure(1, weight=2)  # Author
        self.table_container.grid_columnconfigure(2, weight=1)  # Type
        self.table_container.grid_columnconfigure(3, weight=1)  # Status
        self.table_container.grid_columnconfigure(4, weight=1)  # Action

        # Headers
        headers = ["Title", "Author", "Type", "Status", "Action"]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(
                self.table_container,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            label.grid(row=0, column=col, padx=10, pady=(10, 15), sticky="w")

        # Add a separator line below headers
        separator = ctk.CTkFrame(self.table_container, height=2, fg_color="#3484A9")
        separator.grid(row=1, column=0, columnspan=5, sticky="ew", padx=5, pady=0)

        # Store references to rows for later updates
        self.table_rows = []

        # Initial empty table
        self._display_items()

    def _display_items(self):
        """Display all items in the table"""
        # Clear existing rows
        for widgets in self.table_rows:
            for widget in widgets:
                widget.destroy()
        self.table_rows = []

        # If no items, show message
        if not self.current_items:
            no_items_row = []
            no_items_label = ctk.CTkLabel(
                self.table_container,
                text="No items found",
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            no_items_label.grid(row=2, column=0, columnspan=5, padx=10, sticky="w")
            no_items_row.append(no_items_label)
            self.table_rows.append(no_items_row)
            return

        for row_idx, item in enumerate(self.current_items, start=2):
            row_widgets = []

            title_label = ctk.CTkLabel(
                self.table_container,
                text=item.get('title', ''),
                anchor="w",
            )
            title_label.grid(row=row_idx, column=0, padx=10, sticky="w")
            row_widgets.append(title_label)

            author_label = ctk.CTkLabel(
                self.table_container,
                text=item.get('author_name', ''),
                anchor="w",
            )
            author_label.grid(row=row_idx, column=1, padx=10, sticky="w")
            row_widgets.append(author_label)

            type_label = ctk.CTkLabel(
                self.table_container,
                text=item.get('item_type', ''),
                anchor="w",
            )
            type_label.grid(row=row_idx, column=2, padx=10, sticky="w")
            row_widgets.append(type_label)

            status_label = ctk.CTkLabel(
                self.table_container,
                text=item.get('availability_status', ''),
                anchor="w",
            )
            status_label.grid(row=row_idx, column=3, padx=10, sticky="w")
            row_widgets.append(status_label)

            # View details button
            view_btn = ctk.CTkButton(
                self.table_container,
                text="View Details",
                font=ctk.CTkFont(size=12),
                width=100,
                height=30,
                fg_color="#2d7a9c",
                hover_color="#3484A9",
                command=lambda item_id=item.get('item_id'): self.show_item_detail_callback(item_id)
            )
            view_btn.grid(row=row_idx, column=4, padx=10, pady=2)
            row_widgets.append(view_btn)

            # Add the row to our tracking list
            self.table_rows.append(row_widgets)

    def _load_items(self):
        """Load all items based on current search settings"""
        try:
            if self.current_search_term:
                self.book_service.set_search_strategy(self.current_search_strategy)
                self.current_items = self.book_service.search(self.current_search_term)
            else:
                self.current_items = self.book_service.get_available_items()

            # Display items in table
            self._display_items()

        except Exception as e:
            self.logger.error(f"Error loading items: {e}")
            messagebox.showerror("Error", f"Failed to load items: {str(e)}")

    def _search_items(self, search_term, search_strategy):
        """Handle search from search bar"""
        self.current_search_term = search_term
        self.current_search_strategy = search_strategy
        self._load_items()

    def refresh(self):
        """Refresh the item list"""
        self._load_items()