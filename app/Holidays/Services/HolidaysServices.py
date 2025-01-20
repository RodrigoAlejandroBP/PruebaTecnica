from Domain.abstract.Holidays import IHoliday
from Domain.model.Holidays import Holiday
from ..database.settings import SessionLocal
import date 
from typing import Optional

class HolidayService(IHoliday):
    def __init__(self):
        self.session = SessionLocal()


    def get_all_holidays(self) -> list[Holiday]:
        return self.session.query(Holiday).all()

    def get_holiday_by_date(self, date: date) -> Optional[Holiday]:
        return self.query(Holiday).filter(Holiday.date == date).first()


    def create_holiday(self, nombre, fecha, tipo, descripcion):
        new_holiday = Holiday(nombre=nombre, fecha=fecha, tipo=tipo, descripcion=descripcion)
        self.session.add(new_holiday)
        self.session.commit()
        self.session.refresh(new_holiday)  # Actualiza el objeto con los datos de la base de datos
        return new_holiday

    def get_holiday(self, holiday_id):
        return self.session.query(Holiday).filter_by(id=holiday_id).first()

    def update_holiday(self, holiday_id, nombre, fecha, tipo, descripcion):
        holiday = self.get_holiday(holiday_id)
        if holiday:
            holiday.nombre = nombre
            holiday.fecha = fecha
            holiday.tipo = tipo
            holiday.descripcion = descripcion
            self.session.commit()
            self.session.refresh(holiday)
            return holiday

    def delete_holiday(self, holiday_id):
        holiday = self.get_holiday(holiday_id)
        if holiday:
            self.session.delete(holiday)
            self.session.commit()