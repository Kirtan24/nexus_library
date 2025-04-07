from app.models import User, Role
from app.repositories.user_repository import UserRepository
import logging
import re

class UserController:
    def __init__(self):
        self.user_repository = UserRepository()
        logging.info("User controller initialized")

    def validate_registration_data(self, username, email, password, confirm_password, name, phone_number, role):
        errors = []

        if not re.match(r'^[a-zA-Z0-9_]{4,20}$', username):
            errors.append("Username must be 4-20 characters and contain only letters, numbers, and underscores")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Please enter a valid email address")

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number")

        if password != confirm_password:
            errors.append("Passwords do not match")

        if not re.match(r'^[a-zA-Z\s\-]{2,50}$', name):
            errors.append("Please enter a valid name (2-50 characters, letters only)")

        if phone_number and not re.match(r'^\+?[0-9]{10,15}$', phone_number):
            errors.append("Please enter a valid phone number (10-15 digits)")

        valid_roles = ["student", "researcher", "faculty", "guest", "librarian", "admin"]
        if role.lower() not in valid_roles:
            errors.append(f"Invalid role. Must be one of: {', '.join(valid_roles)}")

        return errors

    def register_user(self, username, email, password, confirm_password, name, phone_number, role):
        validation_errors = self.validate_registration_data(
            username, email, password, confirm_password, name, phone_number, role
        )

        if validation_errors:
            return False, validation_errors

        success, message = self.user_repository.register_user(
            username, email, password, name, phone_number, role
        )

        if success:
            logging.info(f"User {username} registered successfully")
            user = User(
                username=username,
                email=email,
                name=name,
                phone_number=phone_number
            )
            user.add_role(Role(role_id=None, role_name=role))
            return True, message
        else:
            logging.error(f"User registration failed: {message}")
            return False, [message]

    def login(self, username, password):
        success, message, user_data = self.user_repository.verify_login(username, password)

        if success and user_data:
            logging.info(f"User {username} logged in successfully")
            return True, message, user_data
        else:
            logging.warning(f"Login failed for user {username}: {message}")
            return False, message, None

    def update_profile(self, user_id, name=None, email=None, phone_number=None):
        success, message = self.user_repository.update_user(user_id, name, email, phone_number)
        if success:
            logging.info(f"User {user_id} profile updated")
        else:
            logging.error(f"Profile update failed for user {user_id}: {message}")
        return success, message

    def change_password(self, user_id, current_password, new_password, confirm_new_password):
        if new_password != confirm_new_password:
            return False, "New passwords do not match"

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', new_password):
            return False, "New password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number"

        success, message = self.user_repository.change_password(user_id, current_password, new_password)
        if success:
            logging.info(f"Password changed for user {user_id}")
        else:
            logging.warning(f"Password change failed for user {user_id}: {message}")
        return success, message