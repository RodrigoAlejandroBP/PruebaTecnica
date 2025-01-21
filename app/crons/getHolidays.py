

from fastapi_utilities import repeat_every,repeat_at
from app.Holidays.Application.AppHolidays  import AppHolidays
from fastapi import FastAPI
from app.database.settings import SessionLocal 
from fastapi_utilities import repeat_every,repeat_at
from app.Holidays.Application.AppHolidays  import AppHolidays
import os
 
# @repeat_every(seconds=60 * 60 * 24) # 1 dia se puede editar para que sea cada 1 dia, hora minutos etc
@repeat_every(seconds=60) #se puede editar para que sea cada 1 dia, hora minutos etc
async def get_holidays():
    try:
        result = AppHolidays().fetch_all_holidays( os.getenv('anio_api'),max_retries=os.getenv('max_retries_api'), retry_delay= os.getenv('delay_api') )
        if not result:
            print('Error al obtener los feriados')  
            
        print("Actualización de feriados realizada correctamente.")
    except Exception as e:
        print('Error al obtener los feriados')  
