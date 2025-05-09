import customtkinter as ctk
from tkinter import messagebox
from app.repositories.book_repository import BookRepository
from app.services.observer_service import ObserverService
from app.controllers.db_controller import DatabaseController
from app.repositories.borrow_repository import BorrowRepository

class ReservationsPage(ctk.CTkFrame):
    def __init__(self, master, user_id, back_callback=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.user_id = user_id
        self.back_callback = back_callback
        self.book_repo = BookRepository()
        self.observer_service = ObserverService()
        self.db = DatabaseController()
        self.borrow_repo = BorrowRepository()

        self.create_widgets()
        self.load_reservations()

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=10)

        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="←",
            command=self.go_back,
            fg_color="#6f23ff",
            hover_color="#5a1dcc",
            text_color="#ffffff",
            width=100,
            height=35,
            corner_radius=8
        )
        self.back_button.pack(side="left", padx=5)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="My Reservations",
            font=("Arial", 20, "bold")
        )
        self.title_label.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(
            self.header_frame,
            text="Refresh",
            width=80,
            command=self.load_reservations
        )
        self.refresh_button.pack(side="right", padx=5)

        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)

        self.active_tab = self.tabview.add("Active Reservations")
        self.notified_tab = self.tabview.add("Available Notifications")

        self.active_tab.grid_columnconfigure(0, weight=1)
        self.notified_tab.grid_columnconfigure(0, weight=1)

    def go_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            self.master.show_home_page()

    def load_reservations(self):
        for widget in self.active_tab.winfo_children():
            widget.destroy()
        for widget in self.notified_tab.winfo_children():
            widget.destroy()

        self.load_active_reservations()
        self.load_notified_reservations()

    def load_active_reservations(self):
        """Load books user is waiting for (status = 'active')"""
        query = """
            SELECT o.item_id, o.created_at as reservation_date,
                   i.title, i.author_id, i.availability_status,
                   a.name as author_name
            FROM item_observers o
            JOIN items i ON o.item_id = i.item_id
            LEFT JOIN authors a ON i.author_id = a.author_id
            WHERE o.user_id = %s AND o.status = 'active'
            ORDER BY o.created_at DESC
        """
        reservations = self.db.execute_query(query, (self.user_id,), True)

        if not reservations:
            empty_label = ctk.CTkLabel(
                self.active_tab,
                text="You don't have any active reservations",
                font=("Arial", 14)
            )
            empty_label.pack(pady=50)
            return

        for i, reservation in enumerate(reservations):
            self.create_reservation_card(
                self.active_tab,
                reservation,
                is_active=True
            )

    def load_notified_reservations(self):
        """Load books that became available (status = 'notified')"""
        try:
            query = """
                SELECT o.item_id, o.created_at as reservation_date,
                       n.created_at as notification_date,
                       i.title, i.author_id, i.availability_status,
                       a.name as author_name
                FROM item_observers o
                JOIN items i ON o.item_id = i.item_id
                LEFT JOIN authors a ON i.author_id = a.author_id
                LEFT JOIN notifications n ON o.item_id = n.item_id AND n.user_id = o.user_id
                WHERE o.user_id = %s AND o.status = 'notified'
                ORDER BY n.created_at DESC
            """
            reservations = self.db.execute_query(query, (self.user_id,), True)

            if not reservations:
                empty_label = ctk.CTkLabel(
                    self.notified_tab,
                    text="You don't have any availability notifications",
                    font=("Arial", 14)
                )
                empty_label.pack(pady=50)
                return

            for i, reservation in enumerate(reservations):
                self.create_reservation_card(
                    self.notified_tab,
                    reservation,
                    is_active=False
                )

        except Exception as e:
            print(f"Error loading notified reservations: {e}")
            error_label = ctk.CTkLabel(
                self.notified_tab,
                text="Error loading notifications",
                font=("Arial", 14),
                text_color="red"
            )
            error_label.pack(pady=50)

    def create_reservation_card(self, parent, reservation, is_active):
        """Create a reservation card UI element"""
        card = ctk.CTkFrame(parent)
        card.pack(fill="x", pady=5, padx=5)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkLabel(
            info_frame,
            text=reservation['title'],
            font=("Arial", 14, "bold"),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text=f"Author: {reservation.get('author_name', 'Unknown')}",
            anchor="w"
        ).pack(fill="x")

        status_text = "Available Now!" if not is_active else "Waiting for availability"
        status_color = "#2E8B57" if not is_active else "#4682B4"

        ctk.CTkLabel(
            info_frame,
            text=f"Status: {status_text}",
            text_color=status_color,
            anchor="w"
        ).pack(fill="x")

        date_label = "Reserved on" if is_active else "Notified on"
        date_value = reservation['reservation_date'] if is_active else reservation.get('notification_date', reservation['reservation_date'])

        ctk.CTkLabel(
            info_frame,
            text=f"{date_label}: {date_value.strftime('%Y-%m-%d %H:%M') if date_value else 'N/A'}",
            anchor="w"
        ).pack(fill="x")

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(side="right", padx=10)

        if is_active:
            ctk.CTkButton(
                action_frame,
                text="Cancel Reservation",
                fg_color="#D35B58",
                command=lambda item_id=reservation['item_id']: self.cancel_reservation(item_id)
            ).pack(pady=2)
        else:
            ctk.CTkButton(
                action_frame,
                text="Borrow Now",
                fg_color="#2E8B57",
                command=lambda item_id=reservation['item_id']: self.borrow_reserved_book(item_id)
            ).pack(pady=2)

            ctk.CTkButton(
                action_frame,
                text="Dismiss",
                fg_color="#708090",
                command=lambda item_id=reservation['item_id']: self.dismiss_notification(item_id)
            ).pack(pady=2)

    def cancel_reservation(self, item_id):
        """Cancel an active reservation"""
        try:
            success = self.observer_service.remove(self.user_id, item_id)
            if success:
                messagebox.showinfo("Success", "Reservation cancelled")
                self.load_reservations()
            else:
                messagebox.showerror("Error", "Failed to cancel reservation")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel reservation: {str(e)}")

    def borrow_reserved_book(self, item_id):
        """Borrow a book that became available"""
        messagebox.showinfo("Borrow", "Redirecting to borrow page...")
        self.observer_service.remove(self.user_id, item_id)
        self.master.show_item_detail_page(item_id)
        self.load_reservations()

    def dismiss_notification(self, item_id):
        """Dismiss a notification without borrowing"""
        try:
            success = self.observer_service.remove(self.user_id, item_id)
            if success:
                messagebox.showinfo("Success", "Notification dismissed")
                self.load_reservations()
            else:
                messagebox.showerror("Error", "Failed to dismiss notification")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to dismiss notification: {str(e)}")