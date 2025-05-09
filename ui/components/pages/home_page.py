import customtkinter as ctk
from tkinter import messagebox
from ui.components.pages.main_layout import MainLayout
from app.services.recommendation_services import RecommendationService

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
        self.master = master
        self.user = user
        self.recommendation_service = RecommendationService()
        self.create_content()

    def create_content(self):
        self.clear_content()
        self.create_scrollable_content()

    def create_scrollable_content(self):
        self.scroll_container = ctk.CTkFrame(self.content_container, fg_color=BACKGROUND_COLOR)
        self.scroll_container.pack(fill=ctk.BOTH, expand=True)

        self.canvas_frame = ctk.CTkFrame(self.scroll_container, fg_color=BACKGROUND_COLOR)
        self.canvas_frame.pack(fill=ctk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(
            self.canvas_frame,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
            yscrollincrement=10
        )
        self.canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            self.canvas_frame,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.content_frame = ctk.CTkFrame(self.canvas, fg_color=BACKGROUND_COLOR)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw",
            width=self.canvas.winfo_width()
        )

        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.content_frame.bind('<Configure>', self.on_frame_configure)

        self.bind_mousewheel()

        self.create_welcome_section()
        self.create_recommendation_section()
        self.create_trending_section()

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _on_mousewheel(self, event):
        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

    def _on_mousewheel_linux(self, event):
        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            return "break"

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

    def create_recommendation_section(self):
        if not self.user:
            return

        section_frame = ctk.CTkFrame(self.content_frame, fg_color=BACKGROUND_COLOR)
        section_frame.pack(fill=ctk.X, pady=(0, 20), padx=20)

        header_frame = ctk.CTkFrame(section_frame, fg_color=BACKGROUND_COLOR)
        header_frame.pack(fill=ctk.X, pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="Recommended For You",
            font=("Arial", 20, "bold"),
            text_color=TEXT_COLOR
        ).pack(side=ctk.LEFT)

        refresh_button = ctk.CTkButton(
            header_frame,
            text="Refresh",
            width=80,
            fg_color=ACCENT_COLOR,
            hover_color=SECONDARY_COLOR,
            command=self.refresh_recommendations
        )
        refresh_button.pack(side=ctk.RIGHT)

        self.recommendations_container = ctk.CTkScrollableFrame(
            section_frame,
            orientation="horizontal",
            fg_color=BACKGROUND_COLOR,
            height=220
        )
        self.recommendations_container.pack(fill=ctk.X)

        self.load_recommendations()

    def create_trending_section(self):
        section_frame = ctk.CTkFrame(self.content_frame, fg_color=BACKGROUND_COLOR)
        section_frame.pack(fill=ctk.X, pady=(0, 20), padx=20)

        ctk.CTkLabel(
            section_frame,
            text="Trending Now",
            font=("Arial", 20, "bold"),
            text_color=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 10))

        self.trending_container = ctk.CTkScrollableFrame(
            section_frame,
            orientation="horizontal",
            fg_color=BACKGROUND_COLOR,
            height=220
        )
        self.trending_container.pack(fill=ctk.X)

        self.load_trending()

    def load_recommendations(self):
        for widget in self.recommendations_container.winfo_children():
            widget.destroy()

        recommendations = self.recommendation_service.generate_recommendations(self.user['user_id'])

        if not recommendations:
            empty_label = ctk.CTkLabel(
                self.recommendations_container,
                text="Borrow some books to get personalized recommendations!",
                font=("Arial", 14),
                text_color=TEXT_COLOR
            )
            empty_label.pack(pady=20)
            return

        for rec in recommendations[:5]:
            self.create_recommendation_card(rec)

    def load_trending(self):
        for widget in self.trending_container.winfo_children():
            widget.destroy()

        trending_books = self.recommendation_service.repo.get_trending_items()

        if not trending_books:
            empty_label = ctk.CTkLabel(
                self.trending_container,
                text="No trending books found",
                font=("Arial", 14),
                text_color=TEXT_COLOR
            )
            empty_label.pack(pady=20)
            return

        for book in trending_books[:5]:
            self.create_trending_card(book)

    def create_recommendation_card(self, recommendation):
        card = ctk.CTkFrame(
            self.recommendations_container,
            width=180,
            height=180,
            fg_color=OFFWHITE_COLOR,
            corner_radius=12
        )
        card.pack(side=ctk.LEFT, padx=10, pady=5)

        title = (recommendation['title'][:20] + '...') if len(recommendation['title']) > 20 else recommendation['title']
        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14, "bold"),
            text_color=TEXT_COLOR,
            wraplength=160
        ).pack(pady=(10, 5), padx=10)

        ctk.CTkLabel(
            card,
            text=f"by {recommendation['author']}",
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        ).pack(pady=2, padx=10)

        ctk.CTkLabel(
            card,
            text=recommendation['genre'],
            text_color=ACCENT_COLOR,
            font=("Arial", 11)
        ).pack(pady=2, padx=10)

        ctk.CTkLabel(
            card,
            text=recommendation['reason'],
            text_color="#666666",
            font=("Arial", 10),
            wraplength=160
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            card,
            text="View",
            width=80,
            fg_color=BUTTON_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            command=lambda item_id=recommendation['item_id']: self.view_book(item_id)
        ).pack(pady=(5, 10))

    def create_trending_card(self, book):
        card = ctk.CTkFrame(
            self.trending_container,
            width=180,
            height=180,
            fg_color=OFFWHITE_COLOR,
            corner_radius=12
        )
        card.pack(side=ctk.LEFT, padx=10, pady=5)

        title = (book['title'][:20] + '...') if len(book['title']) > 20 else book['title']
        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14, "bold"),
            text_color=TEXT_COLOR,
            wraplength=160
        ).pack(pady=(10, 5), padx=10)

        ctk.CTkLabel(
            card,
            text=f"by {book['author_name']}",
            text_color=TEXT_COLOR,
            font=("Arial", 12)
        ).pack(pady=2, padx=10)

        ctk.CTkLabel(
            card,
            text=book['genre'],
            text_color=ACCENT_COLOR,
            font=("Arial", 11)
        ).pack(pady=2, padx=10)

        ctk.CTkLabel(
            card,
            text=f"🔥 {book['borrow_count']} recent borrows",
            text_color="#666666",
            font=("Arial", 10)
        ).pack(pady=5, padx=10)

        ctk.CTkButton(
            card,
            text="View",
            width=80,
            fg_color=BUTTON_COLOR,
            text_color=BUTTON_TEXT_COLOR,
            command=lambda item_id=book['item_id']: self.view_book(item_id)
        ).pack(pady=(5, 10))

    def refresh_recommendations(self):
        self.load_recommendations()

    def view_book(self, item_id):
        self.master.show_item_detail_page(item_id)