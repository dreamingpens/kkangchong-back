from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date
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
    start_period = Column(Date)
    end_period = Column(Date)
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
    subject_ids = Column(Integer, ForeignKey("subjects.id"))
    level_ids = Column(Integer, ForeignKey("levels.id"))
    disability_type_ids = Column(Integer, ForeignKey("recommended_targets.id"))

class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Levels(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class RecommendedTargets(Base):
    __tablename__ = 'recommended_targets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)