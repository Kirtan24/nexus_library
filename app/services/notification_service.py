from app.controllers.db_controller import DatabaseController


class NotificationService:
    def __init__(self):
        self.db = DatabaseController()

    async def get_pending_notifications(self, user_id: int):
        """Fetch all pending in-app notifications for a user"""
        query = """
            SELECT n.*, i.title as item_title
            FROM notifications n
            JOIN items i ON n.item_id = i.item_id
            WHERE n.user_id = %s AND n.status = 'pending'
            ORDER BY n.created_at DESC
        """
        return await self.db.execute_query(query, (user_id,), fetch_results=True)

    async def mark_as_read(self, notification_id: int):
        """Mark a notification as read"""
        query = """
            UPDATE notifications
            SET status = 'read'
            WHERE notification_id = %s
        """
        await self.db.execute_query(query, (notification_id,))