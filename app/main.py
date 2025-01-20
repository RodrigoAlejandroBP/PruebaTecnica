from fastapi import FastAPI
from app.database.settings import SessionLocal 
from .router import holidays_router 

app = FastAPI()
app.include_router(holidays_router) 

# Dependency function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
