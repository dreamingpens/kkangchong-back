from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class Club(BaseModel):
    id: int
    location: str
    club_name: str
    active_time: str
    subject: str
    other_objects: str
    disability_type: str
    permission_date: str
