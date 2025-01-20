from typing import Protocol
from ..Model import Holiday
import date 
from typing import Optional

class IHoliday(Protocol):
    def get_all_holidays(self) -> list[Holiday]:
        """Obtiene todos los feriados."""
        ...
    def get_holiday_by_date(self, date: date) -> Optional[Holiday]:
        """Obtiene un feriado por fecha."""
        ...
    def create_holiday(self, holiday: Holiday) -> Holiday:
        """Crea un nuevo feriado."""
        ...
    # ... otros métodos (update, delete)