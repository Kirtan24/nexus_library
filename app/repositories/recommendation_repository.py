from app.controllers.db_controller import DatabaseController
from collections import defaultdict
import heapq

class RecommendationRepository:
    def __init__(self):
        self.db = DatabaseController()

    def get_user_borrow_history(self, user_id):
        query = """
            SELECT i.item_id, i.title, i.genre, i.author_id, a.name as author_name,
                   COUNT(*) as borrow_count
            FROM borrow_records br
            JOIN items i ON br.item_id = i.item_id
            JOIN authors a ON i.author_id = a.author_id
            WHERE br.user_id = %s
            GROUP BY i.item_id, i.title, i.genre, i.author_id, a.name
            ORDER BY borrow_count DESC
        """
        return self.db.execute_query(query, (user_id,), True)

    def get_trending_items(self, days=30, limit=10):
        query = """
            SELECT i.item_id, i.title, i.genre, i.author_id, a.name as author_name,
                   COUNT(*) as borrow_count
            FROM borrow_records br
            JOIN items i ON br.item_id = i.item_id
            JOIN authors a ON i.author_id = a.author_id
            WHERE br.borrow_date >= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY i.item_id, i.title, i.genre, i.author_id, a.name
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (days, limit), True)

    def get_similar_items(self, item_id):
        query = """
            WITH target AS (
                SELECT genre, author_id FROM items WHERE item_id = %s
            )
            SELECT i.item_id, i.title, i.genre, i.author_id, a.name as author_name
            FROM items i
            JOIN authors a ON i.author_id = a.author_id
            JOIN target t ON i.genre = t.genre OR i.author_id = t.author_id
            WHERE i.item_id != %s
            ORDER BY
                CASE WHEN i.genre = t.genre AND i.author_id = t.author_id THEN 1
                     WHEN i.genre = t.genre THEN 2
                     ELSE 3
                END
            LIMIT 10
        """
        return self.db.execute_query(query, (item_id, item_id), True)

    def get_recommendations(self, user_id, limit=10):
        user_history = self.get_user_borrow_history(user_id)

        trending_items = self.get_trending_items()

        genre_weights = defaultdict(int)
        for item in user_history:
            if item['genre']:
                genre_weights[item['genre']] += item['borrow_count']

        author_weights = defaultdict(int)
        for item in user_history:
            author_weights[item['author_id']] += item['borrow_count']

        query = """
            SELECT i.item_id, i.title, i.genre, i.author_id, a.name as author_name
            FROM items i
            JOIN authors a ON i.author_id = a.author_id
            WHERE i.availability_status = 'Available'
        """
        all_items = self.db.execute_query(query, (), True)

        scored_items = []
        for item in all_items:
            score = 0

            if item['genre'] in genre_weights:
                score += genre_weights[item['genre']] * 2

            if item['author_id'] in author_weights:
                score += author_weights[item['author_id']] * 3

            for trending in trending_items:
                if item['item_id'] == trending['item_id']:
                    score += trending['borrow_count'] * 5
                    break

            scored_items.append((score, item))

        top_items = heapq.nlargest(limit, scored_items, key=lambda x: x[0])
        return [item for (score, item) in top_items]