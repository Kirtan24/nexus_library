import psycopg2
import logging

class DatabaseController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        if getattr(self, 'initialized', False):
            return

        self.config = config or {
            'dbname': 'NexusLibrary',
            'user': 'postgres',
            'password': 'admin',
            'host': 'localhost',
            'port': '5432'
        }

        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **self.config)
            logging.info("Database connection pool created.")
        except Exception as e:
            logging.error(f"Failed to create connection pool: {e}")
            raise

        self.initialized = True

    def execute_query(self, query, params=None, fetch_results=False):
        """
        Execute a database query with optional parameters.

        Args:
            query (str): SQL query to execute.
            params (tuple, optional): Parameters for the query.
            fetch_results (bool): Whether to fetch and return results.

        Returns:
            list or int: Query results as list of dictionaries or number of affected rows.
        """
        conn, cursor = None, None
        try:
            conn = self.connection_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()

            if fetch_results and cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]

            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Query execution failed: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                self.connection_pool.putconn(conn)

    def close(self):
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logging.info("All database connections closed.")