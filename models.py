from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
import enum

class RepeatType(enum.Enum):
    weekly = 'weekly'
    monthly_by_position = 'monthly_by_position'
    monthly_by_date = 'monthly_by_date'

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Clubs(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    facility_id = Column(Integer)
    min_capacity = Column(Integer)
    max_capacity = Column(Integer)
    time = Column(DateTime)
    repeat = Column(Enum(RepeatType))
    start_period = Column(DateTime)
    end_period = Column(DateTime)
    fee = Column(Integer)
    img_url = Column(String)
    title = Column(String)
    content = Column(String)

class Club_members(Base):
    __tablename__ = 'club_members'

    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

class Facilities(Base):
    __tablename__ = 'facility'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    road_address = Column(String)
    img_urls = Column(String)
    subject_ids = Column(String, ForeignKey("subjects.id"))
    level_ids = Column(String, ForeignKey("levels.id"))
    disability_type_ids = Column(String, ForeignKey("disability_types.id"))

class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Levels(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class DisabilityTypes(Base):
    __tablename__ = 'disability_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)