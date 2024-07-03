from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    room = Column(String)
    co2 = Column(Float)

