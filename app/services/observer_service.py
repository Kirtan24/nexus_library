from app.controllers.db_controller import DatabaseController

class ObserverService:
    def __init__(self):
        self.db = DatabaseController()

    def add(self, user_id: int, item_id: int):
        """Register a user to be notified when an item becomes available"""
        try:
            query = """
                INSERT INTO item_observers (user_id, item_id, status)
                VALUES (%s, %s, 'active')
                ON CONFLICT (user_id, item_id) DO UPDATE
                SET status = 'active'
                RETURNING observer_id
            """
            result = self.db.execute_query(query, (user_id, item_id), True)
            if result:
                print(f"User {user_id} is now observing item {item_id}")
                return result[0]['observer_id']
            return None
        except Exception as e:
            print(f"Error attaching observer: {e}")
            return None

    def remove(self, user_id: int, item_id: int):
        """Completely remove a user from the notification list for an item"""
        try:
            query = """
                DELETE FROM item_observers
                WHERE user_id = %s AND item_id = %s
            """
            self.db.execute_query(query, (user_id, item_id))
            print(f"User {user_id} has been removed from observing item {item_id}")
            return True
        except Exception as e:
            print(f"Error removing observer: {e}")
            return False

    def notify(self, item_id: int):
        """Notify all users who are waiting for this item"""
        try:
            query = """
                SELECT o.observer_id, o.user_id, i.title, u.email, u.name
                FROM item_observers o
                JOIN items i ON o.item_id = i.item_id
                JOIN users u ON o.user_id = u.user_id
                WHERE o.item_id = %s AND o.status = 'active'
            """
            observers = self.db.execute_query(query, (item_id,), True)

            count = 0
            for observer in observers:
                notification_query = """
                    INSERT INTO notifications
                    (user_id, item_id, notification_type, message, status)
                    VALUES (%s, %s, 'availability', %s, 'pending')
                """
                message = f"The item '{observer['title']}' you were interested in is now available."
                self.db.execute_query(
                    notification_query,
                    (observer['user_id'], item_id, message)
                )

                update_query = """
                    UPDATE item_observers
                    SET status = 'notified'
                    WHERE observer_id = %s
                """
                self.db.execute_query(update_query, (observer['observer_id'],))
                count += 1

            print(f"Notified {count} users about item {item_id} availability")
            return count
        except Exception as e:
            print(f"Error notifying observers: {e}")
            return 0