class LibraryItemFactory:
    """
    Factory pattern implementation for creating different types of library items.
    """
    @staticmethod
    def create_item(item_type, **kwargs):
        """
        Create a library item based on the item_type
        """
        base_fields = {
            'title': kwargs.get('title'),
            'author_id': kwargs.get('author_id'),
            'genre': kwargs.get('genre'),
            'publication_year': kwargs.get('publication_year'),
            'availability_status': kwargs.get('availability_status', 'Available'),
            'item_type': item_type
        }

        if item_type == 'PrintedBook':
            return {
                **base_fields,
                'shelf_location': kwargs.get('shelf_location'),
                'isbn': kwargs.get('isbn')
            }
        elif item_type == 'EBook':
            return {
                **base_fields,
                'cover_image_url': kwargs.get('cover_image_url'),
                'description': kwargs.get('description')
            }
        elif item_type == 'ResearchPaper':
            return {
                **base_fields,
                'abstract': kwargs.get('abstract'),
                'journal_name': kwargs.get('journal_name'),
                'doi': kwargs.get('doi')
            }
        elif item_type == 'AudioBook':
            return {
                **base_fields,
                'narrator': kwargs.get('narrator'),
                'duration': kwargs.get('duration'),
                'description': kwargs.get('description')
            }
        else:
            raise ValueError(f"Unknown item type: {item_type}")