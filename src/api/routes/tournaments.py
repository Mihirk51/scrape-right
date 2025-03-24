from flask import Blueprint

from src.api.services.tournament_service import get_tournaments

tournaments_bp = Blueprint("tournaments", __name__, url_prefix="/tournaments")


@tournaments_bp.route("/", methods=["GET"])
def get_all_tournaments():
    tournaments = get_tournaments()
    return tournaments
