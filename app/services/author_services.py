import logging
from repositories.author_repository import AuthorRepository

class AuthorService:
    """
    Service class to manage authors.
    Implements Facade pattern to simplify interactions with the AuthorRepository.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthorService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return

        self.repository = AuthorRepository()
        self.initialized = True
        logging.info("AuthorService initialized")

    def add_author(self, name, bio=None, nationality=None, genres=None):
        """Add a new author"""
        return self.repository.add_author(name, bio, nationality, genres)

    def get_author(self, author_id):
        """Get a single author by ID"""
        return self.repository.get_author(author_id)

    def update_author(self, author_id, name=None, bio=None, nationality=None, genres=None):
        """Update author details"""
        return self.repository.update_author(author_id, name, bio, nationality, genres)

    def delete_author(self, author_id):
        """Delete an author if possible"""
        return self.repository.delete_author(author_id)

    def search_authors(self, name=None, nationality=None):
        """Search authors by name or nationality"""
        return self.repository.search_authors(name, nationality)

    def get_all_authors(self):
        """Fetch all authors alphabetically"""
        return self.repository.get_all_authors()
