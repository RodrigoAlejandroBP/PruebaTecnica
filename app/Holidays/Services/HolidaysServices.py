from ..Domain.abstract.IHoliday import IHoliday
from ..Domain.Model.Holidays import Holidays
from  app.database.settings import SessionLocal
from datetime import date
from typing import Optional

class HolidayService(IHoliday):
    def __init__(self):
        self.session = SessionLocal()


    def get_all_holidays(self) -> list[Holidays]:
        # return db.query(Holidays).all() 

        return self.session.query(Holidays).all()

    def get_holiday_by_date(self, date: date,descripcion) -> Optional[Holidays]:
        return self.query(Holidays).filter(Holidays.date == date and Holidays.descripcion == descripcion).first()


    def create_holiday(self, nombreFeriado, fecha, tipo, descripcion,dia_semana,irrenunciable):
        """
        Crea un nuevo feriado en la base de datos, validando que no exista otro con la misma fecha.

        Args:
            nombre: Nombre del feriado.
            fecha: Fecha del feriado.
            tipo: Tipo de feriado.
            descripcion: Descripción del feriado.

        Returns:
            El objeto del feriado creado o None si ya existe un feriado con esa fecha.
        """

        # Verificar si existe un feriado con la misma fecha
        existing_holiday = self.session.query(Holidays).filter_by(fecha=fecha,nombreFeriado=nombreFeriado).first()

        if existing_holiday and existing_holiday.fecha != fecha:
            # Si existe, retornar None o un mensaje de error
            self.session.delete(existing_holiday)
        else: 
            raise ValueError("Feriado ya existe para esa fecha")

        # Si no existe, crear el nuevo feriado o actualizarlo ya que lo movieron en chile
        new_holiday = Holidays(nombreFeriado=nombreFeriado, fecha=fecha, tipo=tipo, descripcion=descripcion,dia_semana=dia_semana,irrenunciable=irrenunciable)
        self.session.add(new_holiday)
        self.session.commit()
        self.session.refresh(new_holiday)
        return new_holiday

    def get_holiday(self, holiday_id):
        return self.session.query(Holidays).filter_by(id=holiday_id).first()

    def update_holiday(self, holiday_id, nombreFeriado, fecha, tipo, descripcion,dia_semana,irrenunciable):
        holiday = self.get_holiday(holiday_id)
        if holiday:
            holiday.nombreFeriado = nombreFeriado
            holiday.fecha = fecha
            holiday.tipo = tipo
            holiday.descripcion = descripcion
            holiday.dia_semana = dia_semana
            holiday.irrenunciable = irrenunciable

            self.session.commit()
            self.session.refresh(holiday)
            return holiday

    def delete_holiday(self, holiday_id):
        holiday = self.get_holiday(holiday_id)
        if holiday:
            self.session.delete(holiday)
            self.session.commit()