from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.settings import get_db
from app.Holidays.Domain.Model.Holidays import Holidays
from ..Services.HolidaysServices import HolidayService
from datetime import date

from fastapi import APIRouter

holidays_router = APIRouter(prefix="/holidays", tags=["holidays"])


@holidays_router.put("/feriados/id/{holiday_id}", response_model=Holidays)
def update_holiday(holiday_id: int,  db: Session = Depends(get_db)):
    db_holiday = HolidayService(db).update_holiday(holiday_id, Holidays.dict(exclude_unset=True))
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return db_holiday

@holidays_router.delete("/feriados/id/{holiday_id}")
def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    db_holiday = HolidayService(db).delete_holiday(holiday_id)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return {"message": "Feriado eliminado"}




@holidays_router.get("/feriados/id/{holiday_id}", response_model=Holidays)
def read_holiday(holiday_id: int, db: Session = Depends(get_db)):
    db_holiday = HolidayService(db).get_holiday(holiday_id)
    if db_holiday is None:
        raise HTTPException(status_code=404, detail="Feriado no encontrado")
    return db_holiday

    
@holidays_router.get("/feriados/{fecha_inicio}/{fecha_fin}")
def get_holidays_between_dates(fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    holidays = HolidayService(db).get_holidays_between_dates(fecha_inicio, fecha_fin)
    return holidays

@holidays_router.get("/feriados/fecha/{fecha}")
def get_holidays_by_date(fecha: date, db: Session = Depends(get_db)):
    holidays = HolidayService(db).get_holidays_by_date(fecha)
    return holidays