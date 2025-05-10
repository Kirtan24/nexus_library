from app.controllers.user_controller import UserController
import logging

class AuthenticationService:
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
        # self.current_user = {'user_id': 2, 'username': 'admin_1', 'role': 'admin', 'permissions': ['access_ebooks', 'view_catalog', 'borrow_physical_books', 'access_audiobooks', 'reserve_books', 'access_research_papers', 'extend_borrowing', 'manage_users', 'manage_catalog', 'add_items', 'edit_items', 'delete_items', 'admin_access', 'view_reports', 'system_config']}
        self.current_user = None
        self.initialized = True
        logging.info("Authentication service initialized")

    def register(self, username, email, password, confirm_password, name, phone_number, role):
        return self.user_controller.register_user(
            username, email, password, confirm_password, name, phone_number, role
        )

    def login(self, username, password):
        # success, message, user_data = self.user_controller.login(username, password)
        # success = True
        # message = "Login successful"
        # user_data = {
        #     'user_id': 2,
        #     'username': 'admin_1',
        #     'role': 'admin',
        #     'permissions': ['access_ebooks', 'view_catalog', 'borrow_physical_books', 'access_audiobooks', 'reserve_books', 'access_research_papers', 'extend_borrowing', 'manage_users', 'manage_catalog', 'add_items', 'edit_items', 'delete_items', 'admin_access', 'view_reports', 'system_config']
        # }
        success, message, user_data = self.user_controller.login(username, password)
        if success:
            self.current_user = user_data
        return success, message, user_data

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def is_authenticated(self):
        return self.current_user is not None

    def has_role(self, role_name):
        if not self.current_user:
            return False
        return self.current_user.get('role') == role_name

    def check_permission(self, permission_name):
        if not self.current_user:
            return False

        user_permissions = self.current_user.get('permissions', [])
        return permission_name in user_permissions
