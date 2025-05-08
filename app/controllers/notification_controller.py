from services.notification_service import NotificationService

class NotificationController:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_pending_notifications(self, user_id):
        """Get all pending notifications for a user"""
        return self.notification_service.get_pending_notifications(user_id)

    def mark_as_read(self, notification_id):
        """Mark a notification as read"""
        return self.notification_service.mark_as_read(notification_id)