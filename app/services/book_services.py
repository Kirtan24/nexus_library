# services/book_service.py
import logging
from repositories.book_repository import BookRepository
from app.controllers.library_item import LibraryItemFactory

class BookService:
    """
    Service class to manage library items.
    Implements Singleton pattern and Facade pattern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return

        self.repository = BookRepository()
        self.initialized = True
        logging.info("BookService initialized (Singleton)")

    def add_item(self, **kwargs):
        """
        Add a new library item using the factory pattern
        """
        try:
            item_type = kwargs.pop('item_type', None)
            if not item_type:
                return False, "Item type is required"

            # Use the factory to create the appropriate item type
            library_item = LibraryItemFactory.create_item(item_type, **kwargs)

            # Use the repository to add the item to the database
            return self.repository.add_item(library_item)

        except Exception as e:
            logging.error(f"Failed to add library item: {e}")
            return False, str(e)

    def get_item(self, book_id):
        """Get a single library item by ID"""
        return self.repository.get_item(book_id)

    def update_item(self, book_id, item_type, **kwargs):
        """Update library item details"""
        return self.repository.update_item(book_id, item_type, **kwargs)

    def delete_item(self, book_id):
        """Delete a library item if possible"""
        return self.repository.delete_item(book_id)

    def search_items(self, title=None, author=None, genre=None, item_type=None):
        """Search library items by various criteria"""
        return self.repository.search_items(title, author, genre, item_type)

    def update_item_status(self, book_id, status):
        """Update a library item's availability status"""
        return self.repository.update_item_status(book_id, status)

    def get_available_items(self, item_type=None):
        """Get all available library items, optionally filtered by type"""
        return self.repository.get_available_items(item_type)

# Builder pattern implementation for constructing complex library items
class LibraryItemBuilder:
    """Builder pattern for creating library items with many optional parameters"""

    def __init__(self, item_type, title, author_id):
        self.params = {
            'item_type': item_type,
            'title': title,
            'author_id': author_id
        }

    def with_genre(self, genre):
        self.params['genre'] = genre
        return self

    def with_publication_year(self, year):
        self.params['publication_year'] = year
        return self

    def with_availability_status(self, status):
        self.params['availability_status'] = status
        return self

    # PrintedBook specific
    def with_shelf_location(self, location):
        self.params['shelf_location'] = location
        return self

    def with_isbn(self, isbn):
        self.params['isbn'] = isbn
        return self

    # EBook specific
    def with_file_path(self, path):
        self.params['file_path'] = path
        return self

    def with_file_size(self, size):
        self.params['file_size'] = size
        return self

    def with_cover_image(self, image_path):
        self.params['cover_image_path'] = image_path
        return self

    def with_description(self, description):
        self.params['description'] = description
        return self

    # ResearchPaper specific
    def with_abstract(self, abstract):
        self.params['abstract'] = abstract
        return self

    def with_journal_name(self, journal):
        self.params['journal_name'] = journal
        return self

    def with_doi(self, doi):
        self.params['doi'] = doi
        return self

    # AudioBook specific
    def with_audio_file_path(self, path):
        self.params['audio_file_path'] = path
        return self

    def with_narrator(self, narrator):
        self.params['narrator'] = narrator
        return self

    def with_duration(self, duration):
        self.params['duration'] = duration
        return self

    def build(self):
        """Build and return the library item using the factory"""
        return LibraryItemFactory.create_item(**self.params)

    def add_to_library(self):
        """Build the item and add it directly to the library database"""
        try:
            item = self.build()
            service = BookService()
            return service.repository.add_item(item)
        except Exception as e:
            logging.error(f"Failed to add library item: {e}")
            return False, str(e)