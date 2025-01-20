import requests
from sqlalchemy.orm import Session
from ..Services.HolidaysServices import HolidayService


class AppHolidays:
    """
    Clase para obtener y actualizar datos de feriados desde la API de Chile.

    Args:
        api_url (str): URL base de la API.
        year (int): Año para el cual se quieren obtener los feriados.
    """

    def __init__(self, ):
        #ir a buscar a la BD la url 
        api_url="https://apis.digital.gob.cl/fl/feriados/"
        self.api_url = api_url
        self.year = year

    def fetch_holidays(self):
        """
        Obtiene los feriados para el año especificado desde la API.

        Returns:
            list: Lista de diccionarios, donde cada diccionario representa un feriado.
        """
        url = f"{self.api_url}{self.year}"
        response = requests.get(url)
        response.raise_for_status()  # Levanta una excepción si la solicitud falla
        return response.json()

    def update_local_database(self, data):
        """
        Actualiza una base de datos local con los datos de los feriados.

        Args:
            data (list): Lista de diccionarios con los datos de los feriados.
        """
        # Aquí se implementaría la lógica para insertar o actualizar los datos en la base de datos.
        # Ejemplo con SQLAlchemy:
        holidays_service = HolidayService()

        for feriado in data:
            # Crear un objeto de la clase Holiday (suponiendo que existe)
            holidays_service.create_holiday(
                nombre=feriado['nombre'],
                fecha=feriado['fecha'],
                tipo= 1,
                descripcion=1,
                dia=1,
            )


