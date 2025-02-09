import os
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import URL, Column, Date, Numeric, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tournament(Base):
    __tablename__ = "tournaments"

    name = Column(String(255), primary_key=True)
    country = Column(String(2))
    prize_pool = Column(Numeric(18, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    link = Column(String(255))
    logo = Column(String(255))


def insert_events(events_list):
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
    session = Session()

    try:
        for event_dict in events_list:
            event_dict = dict(event_dict)
            # Convert prize_pool from string to Decimal
            prize_pool = (
                Decimal(event_dict["prize_pool"].replace("$", "").replace(",", ""))
                if event_dict["prize_pool"] != "TBD"
                else Decimal("0.00")
            )

            # Convert string dates to date objects
            start_date = (
                datetime.strptime(event_dict["start_date"], "%Y-%m-%d").date()
                if event_dict["start_date"]
                else None
            )
            end_date = (
                datetime.strptime(event_dict["end_date"], "%Y-%m-%d").date()
                if event_dict["end_date"]
                else None
            )

            tournament = Tournament(
                name=event_dict["name"],
                country=event_dict["country"],
                prize_pool=prize_pool,
                start_date=start_date,
                end_date=end_date,
                link=str(event_dict["link"]),
                logo=str(event_dict["logo"]),
            )
            session.add(tournament)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
