import customtkinter as ctk

class SearchBar(ctk.CTkFrame):
    def __init__(self, master, search_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.search_callback = search_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Search for books, authors, or genres...",
            width=400,
            height=40,
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")

        self.strategy_var = ctk.StringVar(value="keyword")
        self.strategy_dropdown = ctk.CTkOptionMenu(
            self,
            values=["keyword", "author", "genre"],
            variable=self.strategy_var,
            width=120,
            height=40,
            dynamic_resizing=False
        )
        self.strategy_dropdown.grid(row=0, column=1, padx=5, pady=10)

        self.search_button = ctk.CTkButton(
            self,
            text="Search",
            width=80,
            height=40,
            command=self._on_search
        )
        self.search_button.grid(row=0, column=2, padx=5, pady=10)

        self.clear_button = ctk.CTkButton(
            self,
            text="Clear",
            width=80,
            height=40,
            fg_color="#D35B58",
            hover_color="#C34C49",
            command=self._on_clear
        )
        self.clear_button.grid(row=0, column=3, padx=(5, 0), pady=10)

        self.search_entry.bind("<Return>", lambda event: self._on_search())

    def _on_search(self):
        search_term = self.search_var.get().strip()
        search_strategy = self.strategy_var.get()

        if search_term:
            self.search_callback(search_term, search_strategy)

    def _on_clear(self):
        self.search_var.set("")
        self.strategy_var.set("keyword")
        self.search_callback("", "keyword")