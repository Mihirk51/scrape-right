__all__ = ("get_db_session", "get_all_rows")

from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.declarative import declarative_base

from src.database.orm import BaseDBManager

Base = declarative_base()


def get_db_session():
    """
    Create and return a database session.

    Returns:
        SQLAlchemy session object
    """
    db_manager = BaseDBManager()
    return db_manager.get_session()


def create_tournament_dict(event_dict):
    """Helper function to create a standardized tournament dictionary"""
    return {
        "name": event_dict["name"],
        "country": event_dict["country"],
        "prize_pool": convert_string_to_decimal(event_dict["prize_pool"]),
        "start_date": convert_string_to_date(event_dict["start_date"]),
        "end_date": convert_string_to_date(event_dict["end_date"]),
        "link": str(event_dict["link"]),
        "logo": str(event_dict["logo"]),
        "vlr_event_id": event_dict["vlr_event_id"],
    }


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
    return Decimal(value.replace("$", "").replace(",", "")) if value != "TBD" else Decimal("0.00")


def convert_string_to_date(value):
    """
    Convert a string to a date object.

    Args:
        value: String to convert

    Returns:
        Date object
    """
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None


def decide_upsert_or_ignore(inc_data: dict, db_data: dict, unique_identifier: str):
    """
    Compare incoming data with database data and decide whether to insert, update, or ignore.

    Args:
        inc_data: List of dictionaries containing incoming data
        db_data: List of dictionaries containing existing database data
        unique_identifier: Key to match records between inc_data and db_data

    Returns:
        list: List of tuples containing (item, action, changes) where:
            - item: The incoming data dictionary
            - action: 'NEW', 'UPDATE', or 'IGNORE'
            - changes: Dictionary of field changes {field: (old_value, new_value)} or None
    """
    db_dict = {item[unique_identifier]: item for item in db_data}
    results = []

    for inc_item in inc_data:
        db_item = db_dict.get(inc_item[unique_identifier])

        if not db_item:
            results.append((inc_item, "NEW", None))
            continue

        # Track specific field changes
        field_changes = {}
        for key, new_value in inc_item.items():
            if key != unique_identifier:
                old_value = db_item.get(key)
                if new_value != old_value:
                    field_changes[key] = (old_value, new_value)

        if field_changes:
            results.append((inc_item, "UPDATE", field_changes))
        else:
            results.append((inc_item, "IGNORE", None))

    return results
