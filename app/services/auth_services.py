# app/services/authentication_service.py

from app.controllers.user_controller import UserController
import logging

class AuthenticationService:
    """
    Service class that handles user authentication logic.
    Implements Facade pattern to simplify authentication interactions.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthenticationService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return

        self.user_controller = UserController()
        self.current_user = None
        self.initialized = True
        logging.info("Authentication service initialized")

    def register(self, username, email, password, confirm_password, name, phone_number, role):
        """
        Register a new user
        Returns: (success, message)
        """
        return self.user_controller.register_user(
            username, email, password, confirm_password, name, phone_number, role
        )

    def login(self, username, password):
        """
        Login a user
        Returns: (success, message, user_data)
        """
        success, message, user_data = self.user_controller.login(username, password)
        if success:
            self.current_user = user_data
        return success, message, user_data

    def logout(self):
        """Log out the current user"""
        self.current_user = None
        logging.info("User logged out")
        return True, "Logged out successfully"

    def get_current_user(self):
        """Get the currently logged in user"""
        return self.current_user

    def is_authenticated(self):
        """Check if a user is currently authenticated"""
        return self.current_user is not None

    def has_role(self, role_name):
        """Check if the current user has a specific role"""
        if not self.current_user:
            return False
        return self.current_user.get('role') == role_name

    def check_permission(self, permission_name):
        """
        Check if the current user has a specific permission
        This would require querying the database for the user's permissions
        """
        if not self.current_user:
            return False

        # In a real implementation, this would query the database
        # For now, we'll implement a simple role-based check
        user_role = self.current_user.get('role')

        # Define role-permission mappings (simplified version)
        permission_map = {
            'student': ['borrow_physical_books', 'access_ebooks', 'access_audiobooks', 'reserve_books'],
            'researcher': ['borrow_physical_books', 'access_ebooks', 'access_research_papers',
                          'access_audiobooks', 'reserve_books', 'extend_borrowing'],
            'faculty': ['borrow_physical_books', 'access_ebooks', 'access_research_papers',
                       'access_audiobooks', 'reserve_books', 'extend_borrowing'],
            'guest': ['access_ebooks'],
            'librarian': ['borrow_physical_books', 'access_ebooks', 'access_research_papers',
                         'access_audiobooks', 'reserve_books', 'extend_borrowing',
                         'manage_users', 'manage_catalog'],
            'admin': ['borrow_physical_books', 'access_ebooks', 'access_research_papers',
                      'access_audiobooks', 'reserve_books', 'extend_borrowing',
                      'admin_access', 'manage_users', 'manage_catalog']
        }

        if user_role in permission_map:
            return permission_name in permission_map[user_role]

        return False