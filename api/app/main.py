from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/data/")
def create_data(data: schemas.DataCreate, db: Session = Depends(database.get_db)):
    db_data = models.Data(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

