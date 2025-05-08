from abc import ABC, abstractmethod

class SearchStrategy(ABC):
    @abstractmethod
    def build_query(self, search_term):
        pass

class KeywordSearchStrategy(SearchStrategy):
    def build_query(self, search_term):
        query = """
        SELECT i.*, a.name as author_name
        FROM items i
        JOIN authors a ON i.author_id = a.author_id
        WHERE
            i.title ILIKE %s OR
            a.name ILIKE %s OR
            i.genre ILIKE %s
        ORDER BY i.title
        """
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        return query, params

class AuthorSearchStrategy(SearchStrategy):
    def build_query(self, search_term):
        query = """
        SELECT i.*, a.name as author_name
        FROM items i
        JOIN authors a ON i.author_id = a.author_id
        WHERE a.name ILIKE %s
        ORDER BY i.title
        """
        params = (f'%{search_term}%',)
        return query, params

class GenreSearchStrategy(SearchStrategy):
    def build_query(self, search_term):
        query = """
        SELECT i.*, a.name as author_name
        FROM items i
        JOIN authors a ON i.author_id = a.author_id
        WHERE i.genre ILIKE %s
        ORDER BY i.title
        """
        params = (f'%{search_term}%',)
        return query, params