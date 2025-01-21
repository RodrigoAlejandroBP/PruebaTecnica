from pydantic import BaseModel
from datetime import date
from typing import Optional

class HolidayResponse(BaseModel):
    # id: Optional[int]= None
    nombreFeriado: str
    fecha: date
    tipo: str
    descripcion: Optional[str] = None  # Campo opcional que puede ser None
    dia_semana:  str
    # irrenunciable:  Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True  # Esto habilita `from_orm()` para trabajar correctamente

        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }
        schema_extra = {
            "example": {
                "id": 1,
                "nombreFeriado": "Día de Todos los Santos",
                "fecha": "2024-11-01",
                "descripcion": "Día de Todos los Santos"
            }
        }

        
class YearlyHolidays(BaseModel):
    # id: Optional[int]= None
    nombreFeriado: str
    fecha: date
    tipo: str
    descripcion: Optional[str] = None  # Campo opcional que puede ser None
    dia_semana:  str
    # irrenunciable:  Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True  # Esto habilita `from_orm()` para trabajar correctamente
        schema_extra = {
            "example": {
                "id": 1,
                "nombreFeriado": "Día de Todos los Santos",
                "fecha": "2024-11-01",
                "descripcion": "Día de Todos los Santos"
            }
        }

        