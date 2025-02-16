__all__ = ("get_db_session", "get_all_rows")

import os
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def get_db_session():
    """
    Create and return a database session.

    Returns:
        SQLAlchemy session object
    """
    load_dotenv()
    url_obj = URL.create(
        "mssql+pyodbc",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        query={"driver": "ODBC Driver 17 for SQL Server"},
    )

    engine = create_engine(url_obj)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


def get_all_rows(session, model):
    """
    Get all rows from a database table as a list of dictionaries.

    Args:
        session: SQLAlchemy session
        model: SQLAlchemy model class

    Returns:
        List of dictionaries containing table data
    """
    rows = session.query(model).all()
    session.close()
    result = []

    for row in rows:
        row_dict = {}
        for column in row.__table__.columns:
            value = getattr(row, column.name)
            # Handle special data types
            if isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, datetime):
                value = value.isoformat()
            row_dict[column.name] = value
        result.append(row_dict)

    return result


def convert_string_to_decimal(value):
    """
    Convert a string to a Decimal object.

    Args:
        value: String to convert

    Returns:
        Decimal object
    """
    return (
        Decimal(value.replace("$", "").replace(",", ""))
        if value != "TBD"
        else Decimal("0.00")
    )


def convert_string_to_date(value):
    """
    Convert a string to a date object.

    Args:
        value: String to convert

    Returns:
        Date object
    """
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None
