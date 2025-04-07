import psycopg2
from psycopg2 import pool
import logging

class DatabaseController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.config = config or {
            'dbname': 'NexusLibrary',
            'user': 'postgres',
            'password': 'admin',
            'host': 'localhost',
            'port': '5432'
        }
        self.connection_pool = self._create_connection_pool()
        self.initialized = True
        logging.info("DatabaseController initialized")

    def _create_connection_pool(self, min_conn=1, max_conn=10):
        try:
            return psycopg2.pool.SimpleConnectionPool(min_conn, max_conn, **self.config)
        except Exception as e:
            logging.error(f"Failed to create connection pool: {e}")
            raise

    def execute_query(self, query, params=None, fetch_results=False):
        """
        Execute a database query with optional parameters.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
            fetch_results (bool): Whether to fetch and return results

        Returns:
            list or int: Query results as list of dictionaries or number of affected rows
        """
        connection, cursor = None, None
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            connection.commit()

            if fetch_results and cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return cursor.rowcount
        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Query failed: {e}")
            raise
        finally:
            if cursor: cursor.close()
            if connection: self.connection_pool.putconn(connection)

    def close(self):
        """Close all connections in the pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logging.info("Connection pool closed")