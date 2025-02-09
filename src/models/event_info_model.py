_all__ = ("EventSchema",)

from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator, model_validator
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Pydantic model for validation
class EventSchema(BaseModel):
    name: str
    status: str
    prize_pool: str
    start_date: str | None
    end_date: str | None
    country: str
    link: HttpUrl
    logo: HttpUrl

    @field_validator("prize_pool")
    def validate_prize_pool(cls, v):
        if not v.startswith("$") and v != "TBD":
            raise ValueError("Prize pool must start with $")
        return v

    @field_validator("country")
    def validate_country(cls, v):
        if len(v) != 2:
            raise ValueError("Country code must be 2 characters")
        return v.lower()

    @model_validator(mode="after")
    def validate_dates(self):
        try:
            if not self.start_date or not self.end_date:
                return self

            # Validate date formats
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d")

            # Check if start date is after end date
            if start_date > end_date:
                raise ValueError("Start date cannot be after end date")

        except ValueError as e:
            if str(e) == "Start date cannot be after end date":
                raise ValueError(str(e))
            raise ValueError('Invalid date format. Expected: "YYYY-MM-DD"')

        return self
