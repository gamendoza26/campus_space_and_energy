from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()

# Database configuration
SQLALCHEMY_DATABASE_URL = "postgresql://dkb34:nana7kwame9@localhost/co2_data_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class CO2Reading(Base):
    __tablename__ = "co2_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    room = Column(String, index=True)
    co2 = Column(Integer)

Base.metadata.create_all(bind=engine)

class CO2Data(BaseModel):
    timestamp: datetime
    room: str
    co2: int

@app.post("/co2_data/")
async def create_co2_data(data: CO2Data):
    db = SessionLocal()
    try:
        db_reading = CO2Reading(**data.dict())
        db.add(db_reading)
        db.commit()
        db.refresh(db_reading)
        return {"message": "Data saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="vcm-41372.vm.duke.edu", port=8000)
