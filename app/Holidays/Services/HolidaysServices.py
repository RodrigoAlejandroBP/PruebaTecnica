from ..Domain.abstract.IHoliday import IHoliday
from ..Domain.Model.Holidays import Holidays
from app.database.settings import SessionLocal
from datetime import date
from typing import Optional
from sqlalchemy import or_, and_, extract

class HolidayService(IHoliday):
    def __init__(self):
        self.session = SessionLocal()

    def get_all_holidays(self, year):
        """
        Obtiene todos los feriados para un año específico.

        Args:
            year: El año del que se quieren obtener los feriados.

        Returns:
            Lista de objetos `Holidays` que ocurren en el año especificado.
        """
        return self.session.query(Holidays).filter(extract('year', Holidays.fecha) == int(year)).all()

    def get_holiday_by_date(self, date: date):
        """
        Obtiene un feriado específico por su fecha.

        Args:
            date: La fecha del feriado a obtener.

        Returns:
            Un diccionario con los campos:
            - `nombreFeriado`: Nombre del feriado.
            - `fecha`: Fecha del feriado.
            - `tipo`: Tipo del feriado.
            - `descripcion`: Descripción del feriado.
            - `dia_semana`: Día de la semana en que cae el feriado.
        """
        return self.session.query(Holidays.nombreFeriado, Holidays.fecha, Holidays.tipo, Holidays.descripcion, Holidays.dia_semana).filter(Holidays.fecha == date).first()

    def create_holiday(self, nombreFeriado, fecha, tipo, descripcion, dia_semana, irrenunciable):
        """
        Crea un nuevo feriado en la base de datos, validando que no exista otro con la misma fecha.

        Args:
            nombreFeriado: Nombre del feriado.
            fecha: Fecha del feriado.
            tipo: Tipo de feriado.
            descripcion: Descripción del feriado.
            dia_semana: Día de la semana en que cae el feriado.
            irrenunciable: Si el feriado es irrenunciable.

        Returns:
            El objeto del feriado creado o None si ya existe un feriado con esa fecha.
        """
        # Verificar si existe un feriado con la misma fecha o si se cambió un feriado de día para no pisarlos
        existing_holiday = (
            self.session.query(Holidays)
            .filter(
                or_(
                    # Buscar por fecha y nombreFeriado
                    and_(Holidays.fecha == fecha,
                         Holidays.nombreFeriado == nombreFeriado),
                    # O buscar por nombreFeriado y tipo
                    and_(Holidays.nombreFeriado == nombreFeriado, Holidays.tipo == tipo, extract('year', Holidays.fecha) == int(fecha.year))
                )
            )
            .first()
        )
        if existing_holiday:
            if existing_holiday.fecha.strftime("%d/%m/%Y") != fecha.strftime("%d/%m/%Y"):
                # Si existe, eliminarlo
                self.session.delete(existing_holiday)
            else:
                print(f"Ya existe un feriado con la misma fecha: { fecha.strftime('%d/%m/%Y')} ")
                return None

        # Si no existe, crear el nuevo feriado
        new_holiday = Holidays(nombreFeriado=nombreFeriado, fecha=fecha, tipo=tipo,
                               descripcion=descripcion, dia_semana=dia_semana, irrenunciable=irrenunciable)
        self.session.add(new_holiday)
        self.session.commit()
        self.session.refresh(new_holiday)
        return new_holiday

    def get_holidays_between_dates(self, fecha_inicio, fecha_fin):
        """
        Obtiene todos los feriados que ocurren entre dos fechas específicas.

        Args:
            fecha_inicio: Fecha inicial del rango (formato: datetime.date).
            fecha_fin: Fecha final del rango (formato: datetime.date).
        
        Returns:
            Lista de objetos `Holidays` que ocurren entre las fechas especificadas.
        """
        return (
            self.session.query(Holidays)
            .filter(Holidays.fecha >= fecha_inicio, Holidays.fecha <= fecha_fin)
            .all()
        )

    def get_holiday(self, holiday_id):
        """
        Obtiene un feriado específico por su ID.

        Args:
            holiday_id: El ID del feriado a obtener.

        Returns:
            El objeto `Holidays` correspondiente al ID proporcionado.
        """
        return self.session.query(Holidays).filter_by(id=holiday_id).first()

    def update_holiday(self, holiday_id, nombreFeriado, fecha, tipo, descripcion, dia_semana, irrenunciable):
        """
        Actualiza los detalles de un feriado existente.

        Args:
            holiday_id: El ID del feriado a actualizar.
            nombreFeriado: Nuevo nombre del feriado.
            fecha: Nueva fecha del feriado.
            tipo: Nuevo tipo de feriado.
            descripcion: Nueva descripción del feriado.
            dia_semana: Nuevo día de la semana del feriado.
            irrenunciable: Nuevo valor de irrenunciable.

        Returns:
            El objeto `Holidays` actualizado, o None si el feriado no existe.
        """
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
        """
        Elimina un feriado existente por su ID.

        Args:
            holiday_id: El ID del feriado a eliminar.

        Returns:
            True si el feriado fue eliminado, o None si no se encontró.
        """
        holiday = self.get_holiday(holiday_id)
        if holiday:
            self.session.delete(holiday)
            self.session.commit()
            return True
        return None
