import customtkinter as ctk
from ui.components.pages.main_layout import MainLayout

BACKGROUND_COLOR = "#f8f9fa"
TEXT_COLOR = "#000000"
ACCENT_COLOR = "#6f23ff"
BLACK_COLOR = "#000000"
OFFWHITE_COLOR = "#f0f0f0"
SECONDARY_COLOR = "#a875ff"
BUTTON_COLOR = "#000000"
BUTTON_TEXT_COLOR = "#f8f9fa"

class HomePage(MainLayout):
    def __init__(self, master, user=None):
        super().__init__(master, user)
        self.root.title("Nexus Library - Home")

        self.create_content()

    def create_content(self):
        self.clear_content()

        self.create_scrollable_content()

    def create_scrollable_content(self):
        self.scroll_container = ctk.CTkFrame(self.content_container, fg_color=BACKGROUND_COLOR)
        self.scroll_container.pack(fill=ctk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(self.scroll_container, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.scroll_container, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.content_frame = ctk.CTkFrame(self.canvas, fg_color=BACKGROUND_COLOR)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw", width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', self.on_canvas_configure)

        self.bind_mousewheel()

        self.create_welcome_section()

    def on_canvas_configure(self, event):
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # For Windows
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # For Linux
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # For Linux

    def create_welcome_section(self):
        welcome_frame = ctk.CTkFrame(self.content_frame, fg_color=BACKGROUND_COLOR)
        welcome_frame.pack(fill=ctk.X, pady=20, padx=20)

        hero_frame = ctk.CTkFrame(welcome_frame, fg_color=BACKGROUND_COLOR)
        hero_frame.pack(pady=30)

        hero_title = ctk.CTkLabel(
            hero_frame,
            text="Welcome to Nexus Library",
            font=("Arial", 36, "bold"),
            text_color=TEXT_COLOR
        )
        hero_title.pack()

        hero_subtitle = ctk.CTkLabel(
            hero_frame,
            text="A Smart and Secure Digital Library Management System",
            font=("Arial", 18),
            text_color=TEXT_COLOR
        )
        hero_subtitle.pack(pady=10)

    def create_feature_cards(self):
        features_frame = ctk.CTkFrame(self.content_frame, fg_color=BACKGROUND_COLOR)
        features_frame.pack(fill=ctk.X, padx=20)

        features_label = ctk.CTkLabel(
            features_frame,
            text="Discover Library Features",
            font=("Arial", 24, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        features_label.pack(anchor="w", pady=(30, 20))

        cards_frame = ctk.CTkFrame(features_frame, fg_color=BACKGROUND_COLOR)
        cards_frame.pack(fill=ctk.X)

        features = [
            {
                "title": "Digital Collections",
                "description": "Access e-books, research papers, and journals from anywhere.",
                "command": self.show_digital_collections
            },
            {
                "title": "Smart Recommendations",
                "description": "Discover new books based on your reading history and interests.",
                "command": self.show_recommendations
            },
            {
                "title": "Borrowing & Reservations",
                "description": "Reserve physical books, track due dates, and manage extensions.",
                "command": self.show_borrowing
            },
            {
                "title": "Research Resources",
                "description": "Access specialized databases and academic resources.",
                "command": self.show_research_resources
            }
        ]

        for i, feature in enumerate(features):
            card = ctk.CTkFrame(cards_frame, fg_color="#ffffff", corner_radius=10)
            card.pack(side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=10, pady=10)

            title = ctk.CTkLabel(
                card,
                text=feature["title"],
                font=("Arial", 18, "bold"),
                text_color=TEXT_COLOR
            )
            title.pack(anchor="w", padx=20, pady=(20, 10))

            description = ctk.CTkLabel(
                card,
                text=feature["description"],
                font=("Arial", 14),
                text_color=TEXT_COLOR,
                wraplength=250
            )
            description.pack(anchor="w", padx=20, pady=(0, 20))

            button = ctk.CTkButton(
                card,
                text="Explore",
                command=feature["command"],
                fg_color=ACCENT_COLOR,
                text_color="#ffffff",
                hover_color=SECONDARY_COLOR,
                font=("Arial", 14),
                width=120,
                height=35
            )
            button.pack(anchor="w", padx=20, pady=(0, 20))

            card.bind("<Button-1>", lambda e, cmd=feature["command"]: cmd())
            title.bind("<Button-1>", lambda e, cmd=feature["command"]: cmd())
            description.bind("<Button-1>", lambda e, cmd=feature["command"]: cmd())

    def create_popular_books_section(self):
        """Create a section displaying popular books"""
        popular_section = ctk.CTkFrame(self.content_frame, fg_color=BACKGROUND_COLOR)
        popular_section.pack(fill=ctk.X, padx=20, pady=30)

        popular_label = ctk.CTkLabel(
            popular_section,
            text="Popular This Week",
            font=("Arial", 24, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        popular_label.pack(anchor="w", pady=(0, 20))

        books_frame = ctk.CTkFrame(popular_section, fg_color=BACKGROUND_COLOR)
        books_frame.pack(fill=ctk.X)

        for i in range(5):
            book_card = ctk.CTkFrame(books_frame, fg_color="#ffffff", corner_radius=10)
            book_card.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)

            book_cover = ctk.CTkFrame(book_card, width=120, height=180, fg_color=SECONDARY_COLOR)
            book_cover.pack(padx=15, pady=15)
            book_cover.pack_propagate(False)

            book_title = ctk.CTkLabel(
                book_card,
                text=f"Book Title {i+1}",
                font=("Arial", 16, "bold"),
                text_color=TEXT_COLOR
            )
            book_title.pack(pady=(0, 5))

            book_author = ctk.CTkLabel(
                book_card,
                text=f"Author {i+1}",
                font=("Arial", 14),
                text_color=TEXT_COLOR
            )
            book_author.pack(pady=(0, 15))

    def perform_search(self):
        search_text = self.search_entry.get()
        self.master.show_search_results_page(search_text)

    def show_digital_collections(self):
        self.master.show_digital_collections_page()

    def show_recommendations(self):
        self.master.show_recommendations_page()

    def show_borrowing(self):
        self.master.show_borrowing_page()

    def show_research_resources(self):
        self.master.show_research_resources_page()
