from fastapi import HTTPException
from app.Holidays.Domain.Model.HolidaysResponse import HolidayResponse, YearlyHolidays
from ..Application.AppHolidays import AppHolidays
from datetime import date
from typing import List  # Asegúrate de importar List

from fastapi import APIRouter

holidays_router = APIRouter(prefix="/holidays", tags=["holidays"])

@holidays_router.delete("/feriados/id/{Feriado_id}")
def delete_holiday(Feriado_id: int):
    """
    Elimina un feriado existente.

    - **Feriado_id**: ID único del feriado a eliminar.
    
    **Response**:
    - Mensaje de confirmación si el feriado fue eliminado exitosamente.
    - Error 404 si el feriado no se encuentra.

    **Ejemplo de respuesta exitosa**:
    ```json
    {
        "message": "Feriado eliminado"
    }
    ```
    """
    db_holiday = AppHolidays().delete_holiday(Feriado_id)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return {"message": "Feriado eliminado"}

@holidays_router.get("/feriados/id/{Feriado_id}", response_model=HolidayResponse)
def read_holiday(Feriado_id: int):
    """
    Obtiene los detalles de un feriado específico mediante su identificador.

    - **Feriado_id**: ID único del feriado.
    
    **Response**:
    - Devuelve el objeto del feriado con los campos:
        - `id`: Identificador del feriado.
        - `nombreFeriado`: Nombre del feriado.
        - `fecha`: Fecha del feriado.
        - `descripcion`: Descripción adicional.
        - `tipo`: Tipo del feriado.
        - `dia_semana`: Día de la semana del feriado.

    **Ejemplo de respuesta**:
    ```json
    {
        "id": 1,
        "nombreFeriado": "Año Nuevo",
        "fecha": "2024-01-01",
        "descripcion": "Sin Comentario",
        "tipo": "Civil",
        "dia_semana": "lunes"
    }
    ```
    """
    db_holiday = AppHolidays().get_holiday(Feriado_id)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return db_holiday

@holidays_router.get("/feriados/{fecha_inicio}/{fecha_fin}", response_model=List[HolidayResponse])
def get_holidays_between_dates(fecha_inicio: date, fecha_fin: date):
    """
    Obtiene todos los feriados que ocurren entre dos fechas específicas.

    - **fecha_inicio**: Fecha inicial del rango (formato: YYYY-MM-DD).
    - **fecha_fin**: Fecha final del rango (formato: YYYY-MM-DD).
    
    **Response**:
    - Lista de objetos de feriados con los campos:
        - `nombreFeriado`: Nombre del feriado.
        - `fecha`: Fecha del feriado.
        - `descripcion`: Descripción adicional.
        - `tipo`: Tipo de feriado (e.g., "Civil", "Religioso").
        - `dia_semana`: Día de la semana del feriado.

    **Ejemplo de respuesta**:
    ```json
    [
        {
            "nombreFeriado": "Año Nuevo",
            "fecha": "2024-01-01",
            "descripcion": "Sin Comentario",
            "tipo": "Civil",
            "dia_semana": "lunes"
        },
        {
            "nombreFeriado": "Viernes Santo",
            "fecha": "2024-03-29",
            "descripcion": "Sin Comentario",
            "tipo": "Religioso",
            "dia_semana": "viernes"
        }
    ]
    ```
    """
    holidays = AppHolidays().get_holidays_between_dates(fecha_inicio, fecha_fin)
    if holidays is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    
    return holidays

@holidays_router.get("/traer-todos-los-feriados/", response_model=List[YearlyHolidays])
def get_all_holidays(year: int):
    """
    Obtiene todos los feriados de un año específico.

    - **year**: Año de los feriados a obtener.
    
    **Response**:
    - Lista de feriados con los campos:
        - `nombreFeriado`: Nombre del feriado.
        - `fecha`: Fecha del feriado.
        - `descripcion`: Descripción adicional.
        - `tipo`: Tipo de feriado.
        - `dia_semana`: Día de la semana.

    **Ejemplo de respuesta**:
    ```json
    [
        {
            "nombreFeriado": "Año Nuevo",
            "fecha": "2024-01-01",
            "descripcion": "Sin Comentario",
            "tipo": "Civil",
            "dia_semana": "lunes"
        },
        {
            "nombreFeriado": "Día del Trabajo",
            "fecha": "2024-05-01",
            "descripcion": "Sin Comentario",
            "tipo": "Civil",
            "dia_semana": "miércoles"
        }
    ]
    ```
    """
    holidays = AppHolidays().get_all_holidays(year)
    if holidays is None or holidays == []:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    
    return holidays

@holidays_router.get("/feriados/{fecha}", response_model=HolidayResponse)
def get_holidays_by_date(fecha: date):
    """
    Obtiene los feriados que ocurren en una fecha específica.

    - **fecha**: Fecha del feriado (formato: YYYY-MM-DD).
    
    **Response**:
    - Lista de objetos de feriados con los campos:
        - `nombreFeriado`: Nombre del feriado.
        - `fecha`: Fecha del feriado.
        - `descripcion`: Descripción adicional.
        - `tipo`: Tipo de feriado.
        - `dia_semana`: Día de la semana del feriado.

    **Ejemplo de respuesta**:
    ```json
    [
        {
            "nombreFeriado": "Año Nuevo",
            "fecha": "2024-01-01",
            "descripcion": "Sin Comentario",
            "tipo": "Civil",
            "dia_semana": "lunes"
        }
    ]
    ```
    """
    holidays = AppHolidays().get_holiday_by_date(fecha)
    if holidays is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return holidays
