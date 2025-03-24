from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base

from database.operations import create_tournament_dict, decide_upsert_or_ignore, get_all_rows, get_db_session
from logger import logger

Base = declarative_base()


class Tournament(Base):
    __tablename__ = "tournaments"

    tournament_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    country = Column(String(2))
    prize_pool = Column(Numeric(18, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    link = Column(String(255))
    logo = Column(String(255))
    vlr_event_id = Column(Integer, unique=True)

    def to_dict(self):
        """Serialize Tournament object to dictionary"""
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "country": self.country,
            "prize_pool": float(self.prize_pool),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "link": self.link,
            "logo": self.logo,
            "vlr_event_id": self.vlr_event_id,
        }


def insert_events(events_list):
    session = get_db_session()
    all_rows = get_all_rows(session, Tournament)

    logger.info(f"Processing {len(events_list)} events for database insertion/update")

    try:
        # Transform all events into standardized tournament dictionaries
        tournaments = [create_tournament_dict(dict(event)) for event in events_list]
        logger.debug(f"Transformed {len(tournaments)} events into tournament format")

        # Get update/insert decisions
        results = decide_upsert_or_ignore(inc_data=tournaments, db_data=all_rows, unique_identifier="vlr_event_id")

        new_count = update_count = ignore_count = 0
        # Process results for INSERT and UPDATE operations
        for tournament_dict, operation, changes in results:
            if operation == "IGNORE":
                ignore_count += 1
                logger.debug(f"Ignoring tournament: {tournament_dict['name']}")
                continue

            if operation == "NEW":
                tournament = Tournament(**tournament_dict)
                session.add(tournament)
                new_count += 1
                logger.debug(f"Adding new tournament: {tournament_dict['name']}")
            else:  # UPDATE
                if changes:
                    change_log = "\n".join(
                        f"  {field}: {old_val} -> {new_val}" for field, (old_val, new_val) in changes.items()
                    )
                    logger.debug(f"Updating tournament: {tournament_dict['name']}\nChanges:\n{change_log}")
                session.query(Tournament).filter_by(vlr_event_id=tournament_dict["vlr_event_id"]).update(
                    tournament_dict
                )
                update_count += 1

        session.commit()
        logger.info(
            f"Database operations completed - New: {new_count}, Updated: {update_count}, Ignored: {ignore_count}"
        )

    except Exception as e:
        session.rollback()
        logger.error(f"Database operation failed: {str(e)}", exc_info=True)
        raise e
    finally:
        session.close()
        logger.debug("Database session closed")


# insert_events(["123"])
