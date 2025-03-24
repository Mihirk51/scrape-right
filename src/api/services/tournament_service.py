import json

from src.database.models.tournaments import Tournament
from src.database.orm import BaseDBManager

db_manager = BaseDBManager()


# def get_tournaments():
#     with db_manager.transaction() as session:
#         tournaments = session.query(Tournament).all()
#     return tournaments


def get_tournaments():
    with db_manager.transaction() as session:
        tournaments = session.query(Tournament).all()
        return json.dumps([t.to_dict() for t in tournaments])


get_tournaments()
