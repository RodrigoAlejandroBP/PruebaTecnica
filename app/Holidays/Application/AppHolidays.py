import requests
from sqlalchemy.orm import Session
from ..Services.HolidaysServices import HolidayService
import os
import requests
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # Establece el locale a español de España (UTF-8)


class AppHolidays:
    """
    Clase para obtener y actualizar datos de feriados desde la API de Chile.

    """
    def __init__(self, db: Session, year: int):
        self.db = db
        self.year = year
        self.holidays_service = HolidayService()

        # Obtener la URL de la API utilizando el servicio CommonParameterService
        api_url_param = os.getenv('URL_API')
        self.api_url = api_url_param if api_url_param else "https://apis.digital.gob.cl/fl/feriados/"

    def get_date(self,date, holidays_data):
        """
        Busca feriados en una lista de datos JSON por fecha.

        Args:
            fecha (str): Fecha en formato 'AAAA-MM-DD' a buscar.
            datos_feriados (list): Lista de diccionarios con información de los feriados.

        Returns:
            list: Lista de diccionarios con los feriados encontrados en la fecha indicada.
        """

        return list(filter(lambda x: x['fecha'] == date, holidays_data))



    def fetch_specific_holidays(self,date_to_search):
        """
        Obtiene los feriados para el año especificado desde la API.

        Returns:
            list: Lista de diccionarios, donde cada diccionario representa un feriado.
        """
        try:

            local_holidays = self.holidays_service.get_holidays_from_db(date_to_search)  # Nueva función para buscar en la BD
            if local_holidays:
                return local_holidays


            url = f"{self.api_url}{self.year}"
            response = requests.get(url)
            response.raise_for_status()

            data = self.get_date(date_to_search, response.json())
            self.update_local_database( data)
            return data
        except requests.exceptions.RequestException as e:
            # Manejar la excepción, por ejemplo, registrarla en un log
            print(f"Error al obtener los feriados: {e}")
            return []

    def fetch_all_holidays(self):
        """
        Obtiene los feriados para el año especificado desde la API.

        Returns:
            list: Lista de diccionarios, donde cada diccionario representa un feriado.
        """
        try:
            url = f"{self.api_url}{self.year}"

            ##Headers en caso de bloqueo por caso de scrapping, borrar en caso de llegar.
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'ACCEPT-ENCODING' : 'gzip, deflate, br',
            'REFERER' : 'https://www.google.com/'
            }

            response = requests.get(url,headers=headers)
            response.raise_for_status()
            self.update_local_database((response.json()))
            
            
            return response.json()
        except requests.exceptions.RequestException as e:
            # Manejar la excepción, por ejemplo, registrarla en un log
            print(f"Error al obtener los feriados: {e}")
            return []

    def update_local_database(self, data):
        """
        Actualiza una base de datos local con los datos de los feriados utilizando el servicio HolidayService.

        Args:
            data (list): Lista de diccionarios con los datos de los feriados.
        """

        for feriado in data:
            fecha = datetime.strptime(feriado['fecha'],"%Y-%m-%d" )
            if not fecha:
                continue 
            
            # Utilizar el método create_holiday del servicio para persistir el objeto
            self.holidays_service.create_holiday(nombreFeriado=feriado['nombre'], fecha=feriado['fecha'], tipo=feriado['tipo'], descripcion=feriado['comentarios'],dia_semana= fecha.strftime("%A"),irrenunciable=feriado['irrenunciable'])
        return True 