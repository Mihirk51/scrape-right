from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

from database.operations import (
    convert_string_to_date,
    convert_string_to_decimal,
    get_all_rows,
    get_db_session,
)

Base = declarative_base()


class Tournament(Base):
    __tablename__ = "tournaments"

    tournament_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    country = Column(String(2))
    prize_pool = Column(Numeric(18, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    link = Column(String(255))
    logo = Column(String(255))


def insert_events(events_list):
    session = get_db_session()
    get_all_rows(session, Tournament)

    try:
        tournaments = []
        for event_dict in events_list:
            event_dict = dict(event_dict)
            # Convert prize_pool from string to Decimal
            prize_pool = convert_string_to_decimal(event_dict["prize_pool"])

            # Convert string dates to date objects
            start_date = convert_string_to_date(event_dict["start_date"])
            end_date = convert_string_to_date(event_dict["end_date"])

            tournament = Tournament(
                name=event_dict["name"],
                country=event_dict["country"],
                prize_pool=prize_pool,
                start_date=start_date,
                end_date=end_date,
                link=str(event_dict["link"]),
                logo=str(event_dict["logo"]),
            )
            tournaments.append(tournament)

        bulk_upsert(session=session, objects=tournaments, pk_name="tournament_id")
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


insert_events(["123"])
