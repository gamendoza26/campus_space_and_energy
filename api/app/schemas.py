from pydantic import BaseModel
from datetime import datetime

class DataBase(BaseModel):
    timestamp: datetime
    room: str
    co2: float

class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int

    class Config:
        orm_mode = True
