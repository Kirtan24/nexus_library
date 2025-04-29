class LibraryItemFactory:
    """
    Factory pattern implementation for creating different types of library items.
    """
    @staticmethod
    def create_item(item_type, **kwargs):
        """
        Create a library item based on the item_type

        Args:
            item_type: Type of the item to create ('PrintedBook', 'EBook', etc.)
            **kwargs: Parameters for the item

        Returns:
            Dictionary with item details
        """
        if item_type == 'PrintedBook':
            return {
                'title': kwargs.get('title'),
                'author_id': kwargs.get('author_id'),
                'genre': kwargs.get('genre'),
                'publication_year': kwargs.get('publication_year'),
                'availability_status': kwargs.get('availability_status', 'Available'),
                'item_type': 'PrintedBook',
                'shelf_location': kwargs.get('shelf_location'),
                'isbn': kwargs.get('isbn')
            }
        elif item_type == 'EBook':
            return {
                'title': kwargs.get('title'),
                'author_id': kwargs.get('author_id'),
                'genre': kwargs.get('genre'),
                'publication_year': kwargs.get('publication_year'),
                'availability_status': kwargs.get('availability_status', 'Available'),
                'item_type': 'EBook',
                'file_path': kwargs.get('file_path'),
                'file_size': kwargs.get('file_size'),
                'cover_image_path': kwargs.get('cover_image_path'),
                'description': kwargs.get('description')
            }
        elif item_type == 'ResearchPaper':
            return {
                'title': kwargs.get('title'),
                'author_id': kwargs.get('author_id'),
                'genre': kwargs.get('genre'),
                'publication_year': kwargs.get('publication_year'),
                'availability_status': kwargs.get('availability_status', 'Available'),
                'item_type': 'ResearchPaper',
                'abstract': kwargs.get('abstract'),
                'file_path': kwargs.get('file_path'),
                'journal_name': kwargs.get('journal_name'),
                'doi': kwargs.get('doi')
            }
        elif item_type == 'AudioBook':
            return {
                'title': kwargs.get('title'),
                'author_id': kwargs.get('author_id'),
                'genre': kwargs.get('genre'),
                'publication_year': kwargs.get('publication_year'),
                'availability_status': kwargs.get('availability_status', 'Available'),
                'item_type': 'AudioBook',
                'audio_file_path': kwargs.get('audio_file_path'),
                'narrator': kwargs.get('narrator'),
                'duration': kwargs.get('duration'),
                'description': kwargs.get('description')
            }
        else:
            raise ValueError(f"Unknown item type: {item_type}")