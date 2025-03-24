import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

Base = declarative_base()


class BaseDBManager:
    """
    Base class for database operations.
    """

    def __init__(self, base=Base, pool_size=20, max_overflow=10):
        self.base = base
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self._setup_connection()

    def _setup_connection(self):
        """
        Set up the database connection.
        """
        load_dotenv()
        db_url = f"mssql+pyodbc://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?driver=ODBC Driver 17 for SQL Server"
        self.engine = create_engine(
            db_url, poolclass=QueuePool, pool_size=self.pool_size, max_overflow=self.max_overflow
        )
        self.base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """
        Get a database session.
        """
        return self.Session()

    def close(self):
        """
        Close the database connection.
        """
        self.engine.dispose()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @contextmanager
    def transaction(self):
        """
        Provide a transactional scope around a series of operations.
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
