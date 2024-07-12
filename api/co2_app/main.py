from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
database = Database(DATABASE_URL)

app = FastAPI()

class CO2Data(BaseModel):
    timestamp: str
    co2: float

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/co2data/")
async def create_co2data(data: CO2Data):
    query = "INSERT INTO co2_data (timestamp, co2) VALUES (:timestamp, :co2)"
    values = {"timestamp": data.timestamp, "co2": data.co2}
    await database.execute(query=query, values=values)
    return {"status": "success"}
