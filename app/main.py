from fastapi import FastAPI
from app.database.settings import SessionLocal 
from .router import holidays_router 
# from  app.crons.getHolidays  import get_holidays
from fastapi_utilities import repeat_every,repeat_at
from app.Holidays.Application.AppHolidays  import AppHolidays
from fastapi import APIRouter 
import os

 
app = FastAPI()

app.include_router(holidays_router) 


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24) #se puede editar para que sea cada 1 dia, hora minutos etc
async def get_holidays():
    try:
        AppHolidays(  SessionLocal,os.getenv('anio')).fetch_all_holidays()
        print("Actualización de feriados realizada correctamente.")
    except Exception as e:
        print(e)

        print('Error al obtener los feriados')  
