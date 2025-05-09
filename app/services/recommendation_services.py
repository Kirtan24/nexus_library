from app.repositories.recommendation_repository import RecommendationRepository

class RecommendationService:
    def __init__(self):
        self.repo = RecommendationRepository()

    def generate_recommendations(self, user_id):
        """Generate personalized recommendations"""
        recommendations = self.repo.get_recommendations(user_id)

        formatted = []
        for item in recommendations:
            formatted.append({
                'item_id': item['item_id'],
                'title': item['title'],
                'author': item['author_name'],
                'genre': item['genre'],
                'reason': self._get_recommendation_reason(item, user_id)
            })

        return formatted

    def _get_recommendation_reason(self, item, user_id):
        """Generate a human-readable reason for the recommendation"""
        history = self.repo.get_user_borrow_history(user_id)

        genre_count = sum(1 for h in history if h['genre'] == item['genre'])
        if genre_count > 0:
            return f"Because you enjoy {item['genre']} books"

        author_count = sum(1 for h in history if h['author_id'] == item['author_id'])
        if author_count > 0:
            return f"Because you like books by {item['author_name']}"

        trending = self.repo.get_trending_items()
        if any(t['item_id'] == item['item_id'] for t in trending):
            return "Popular choice right now"

        return "You might enjoy this"