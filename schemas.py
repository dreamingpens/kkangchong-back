from typing import Union

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ClubBase(BaseModel):
    creator_id: int
    facility_id: int
    min_capacity: int
    max_capacity: int
    time: datetime
    start_period: datetime
    end_period: datetime
    fee: int
    img_url: Optional[str] = None
    title: str
    content: str

class ClubCreate(ClubBase):
    pass  # This model can be used for creating a club

class Clubs(ClubBase):
    id: int  # Include id for responses

    class Config:
        orm_mode = True

class Subjects(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class Levels(BaseModel):
    id: int
    name: str
    description: str
    class Config:
        orm_mode = True

class DisabilityTypes(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class Facilities(BaseModel):
    id: int
    name: str
    phone: str
    road_address: str
    img_urls: str
    subject_ids: List[int]  # Assuming this will be a list of IDs
    level_ids: List[int]     # Assuming this will be a list of IDs
    disability_type_ids: List[int]  # Assuming this will be a list of IDs

    class Config:
        orm_mode = True