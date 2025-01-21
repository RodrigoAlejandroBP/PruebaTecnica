from ..Domain.abstract.IHoliday import IHoliday
from ..Domain.Model.Holidays import Holidays
from app.database.settings import SessionLocal
from datetime import date
from typing import Optional
from sqlalchemy import or_, and_, extract

class HolidayService(IHoliday):
    def __init__(self):
        self.session = SessionLocal()

    def get_all_holidays(self,year):
        return  self.session.query(Holidays).filter(extract('year', Holidays.fecha) == int(year)).all()


    def get_holiday_by_date(self, date: date):
        return self.session.query(Holidays.nombreFeriado, Holidays.fecha, Holidays.tipo, Holidays.descripcion, Holidays.dia_semana).filter(Holidays.fecha == date).first()

    def create_holiday(self, nombreFeriado, fecha, tipo, descripcion, dia_semana, irrenunciable):
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
        # Verificar si existe un feriado con la misma fecha o si se cambio uno de los feriados de dia para no pisarlos
        existing_holiday = (
            self.session.query(Holidays)
            .filter(
                or_(
                    # Buscar por fecha y nombreFeriado
                    and_(Holidays.fecha == fecha,
                         Holidays.nombreFeriado == nombreFeriado),
                    # O buscar por nombreFeriado y tipo
                    and_(Holidays.nombreFeriado ==
                         nombreFeriado, Holidays.tipo == tipo,extract('year', Holidays.fecha) == int(fecha.year)  )
                )
            )
            .first()
        )
        if existing_holiday:
            if existing_holiday.fecha.strftime("%d/%m/%Y") != fecha.strftime("%d/%m/%Y"):
                # Si existe, retornar None o un mensaje de error
                self.session.delete(existing_holiday)
            else:
                print(
                    f"Ya existe un feriado con la misma fecha: { fecha.strftime('%d/%m/%Y')} ")
                return None

        # Si no existe, crear el nuevo feriado o actualizarlo ya que lo movieron en chile
        new_holiday = Holidays(nombreFeriado=nombreFeriado, fecha=fecha, tipo=tipo,
                               descripcion=descripcion, dia_semana=dia_semana, irrenunciable=irrenunciable)
        self.session.add(new_holiday)
        self.session.commit()
        self.session.refresh(new_holiday)
        return new_holiday

    def get_holidays_between_dates(self, fecha_inicio, fecha_fin):
        """
        Obtiene todos los feriados que ocurren entre dos fechas específicas.

        - **fecha_inicio**: Fecha inicial del rango (formato: datetime.date).
        - **fecha_fin**: Fecha final del rango (formato: datetime.date).
        
        **Returns**:
        - Lista de objetos `Holidays` que ocurren entre las fechas especificadas.
        """
        
        return (
            self.session.query(Holidays)
            .filter(Holidays.fecha >= fecha_inicio, Holidays.fecha <= fecha_fin)
            .all()
        )
        


    def get_holiday(self, holiday_id):
        return self.session.query(Holidays).filter_by(id=holiday_id).first()

    
    ##Metodo para actualizar un feriado
    def update_holiday(self, holiday_id, nombreFeriado, fecha, tipo, descripcion, dia_semana, irrenunciable):
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
        return None

    def delete_holiday(self, holiday_id):
        holiday = self.get_holiday(holiday_id)
        if holiday:
            self.session.delete(holiday)
            self.session.commit()
            return True
        return None
