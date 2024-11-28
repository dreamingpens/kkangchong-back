from database import Base
from sqlalchemy import Column, Integer, String

class Clubs(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    club_name = Column(String)
    active_time = Column(String)
    subject = Column(String)
    other_objects = Column(String)
    disability_type = Column(String)
    permission_date = Column(String)