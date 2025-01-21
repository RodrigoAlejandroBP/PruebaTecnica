from fastapi import FastAPI
from app.database.settings import SessionLocal 
from .router import holidays_router 
from fastapi_utilities import repeat_every,repeat_at
from app.Holidays.Application.AppHolidays  import AppHolidays
from fastapi import APIRouter 
from app.database.settings import Base, engine
import os
from  app.crons.getHolidays  import get_holidays
 
app = FastAPI()

app.include_router(holidays_router) 
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def cron_get_holidays():
    try:
         get_holidays()
    except Exception as e:
        print(e)
        print('Error al obtener los feriados')