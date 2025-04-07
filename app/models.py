from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Permission:
    permission_id: int
    permission_name: str
    description: Optional[str] = None

@dataclass
class Role:
    role_id: int
    role_name: str
    description: Optional[str] = None
    permissions: List[Permission] = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []

@dataclass
class User:
    username: str
    email: str
    name: str
    phone_number: Optional[str] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    account_status: str = "active"
    roles: List[Role] = None

    def __post_init__(self):
        if self.roles is None:
            self.roles = []

    def add_role(self, role: Role):
        """Add a role to the user"""
        if role not in self.roles:
            self.roles.append(role)

    def has_permission(self, permission_name: str) -> bool:
        """Check if the user has a specific permission"""
        for role in self.roles:
            for permission in role.permissions:
                if permission.permission_name == permission_name:
                    return True
        return False

    def has_role(self, role_name: str) -> bool:
        """Check if the user has a specific role"""
        for role in self.roles:
            if role.role_name.lower() == role_name.lower():
                return True
        return

@dataclass
class Author:
    author_id: int
    name: str
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None

@dataclass
class Book:
    book_id: int
    title: str
    authors: List[Author]
    published_date: Optional[datetime] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    available_copies: int = 0

    def __post_init__(self):
        if self.authors is None:
            self.authors = []

@dataclass
class BorrowRecord:
    record_id: int
    user: User
    book: Book
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    fine_amount: float = 0.0

    def is_overdue(self) -> bool:
        """Check if the book is overdue"""
        return self.return_date is None and datetime.now() > self.due_date

    def calculate_fine(self, daily_fine_rate: float) -> float:
        """Calculate the fine for overdue books"""
        if self.is_overdue():
            overdue_days = (datetime.now() - self.due_date).days
            self.fine_amount = overdue_days * daily_fine_rate
        return self.fine_amount

@dataclass
class Author:
    author_id: int
    name: str
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None

@dataclass
class Book:
    book_id: int
    title: str
    authors: List[Author] = field(default_factory=list)
    published_date: Optional[datetime] = None
    isbn: Optional[str] = None
    genre: Optional[str] = None
    format: str = "PrintedBook"
    availability_status: str = "Available"

@dataclass
class BorrowRecord:
    borrow_id: int
    user_id: int
    book: Book
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    fine_amount: float = 0.0

    def is_overdue(self) -> bool:
        """Check if the book is overdue"""
        return self.return_date is None and datetime.now() > self.due_date

    def calculate_fine(self, daily_fine_rate: float) -> float:
        """Calculate the fine for overdue books"""
        if self.is_overdue():
            overdue_days = (datetime.now() - self.due_date).days
            self.fine_amount = max(0, overdue_days * daily_fine_rate)
        return self.fine_amount

@dataclass
class Reservation:
    reservation_id: int
    user_id: int
    book: Book
    reservation_date: datetime = field(default_factory=datetime.utcnow)
    status: str = "Pending"

@dataclass
class LateFee:
    late_fee_id: int
    user_id: int
    borrow_id: int
    fine_amount: float
    paid: bool = False
    payment_date: Optional[datetime] = None

@dataclass
class Notification:
    notification_id: int
    user_id: int
    message: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "Unread"

@dataclass
class Recommendation:
    recommendation_id: int
    user_id: int
    book: Book
    recommended_reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
