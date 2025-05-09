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