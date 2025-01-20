from typing import Protocol
from app.Holidays.Domain.Model.Holidays import Holidays
from datetime import date
from typing import Optional

class IHoliday(Protocol):
    def get_all_holidays(self) -> list[Holidays]:
        """Obtiene todos los feriados."""
        ...
    def get_holiday_by_date(self, date: date) -> Optional[Holidays]:
        """Obtiene un feriado por fecha."""
        ...
    def create_holiday(self, holiday: Holidays) -> Holidays:
        """Crea un nuevo feriado."""
        ...
    # ... otros métodos (update, delete)