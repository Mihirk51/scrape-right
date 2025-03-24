from datetime import date
from typing import Optional

from pydantic import BaseModel, HttpUrl, condecimal


class TournamentBase(BaseModel):
    name: str
    country: str
    prize_pool: condecimal(max_digits=18, decimal_places=2)
    start_date: date
    end_date: date
    link: Optional[HttpUrl] = None
    logo: Optional[HttpUrl] = None
    vlr_event_id: Optional[int] = None


class TournamentCreate(TournamentBase):
    """Schema for creating a tournament. `tournament_id` is omitted because it's auto-generated."""

    pass


class TournamentResponse(TournamentBase):
    """Schema for returning tournament data, including the `tournament_id`."""

    tournament_id: int

    class Config:
        from_attributes = True