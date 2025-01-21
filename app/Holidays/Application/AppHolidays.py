import requests
from sqlalchemy.orm import Session
from ..Services.HolidaysServices import HolidayService
import os
import requests
from datetime import datetime, date
import locale
import time

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # Establece el locale a español de España (UTF-8)


class AppHolidays:
    """
    Clase para obtener y actualizar datos de feriados desde la API de Chile.
    """

    def __init__(self,):
        self.holidays_service = HolidayService()

        # Obtener la URL de la API utilizando el servicio CommonParameterService
        api_url_param = os.getenv('URL_API')
        self.api_url = api_url_param if api_url_param else "https://apis.digital.gob.cl/fl/feriados/"

    ## En caso de necesitar lógica externa o validaciones exclusivas de la capa de aplicación sin afectar reglas de negocio
    # Por eso se utiliza en la capa de aplicación.
    def delete_holiday(self, holiday_id):
        return self.holidays_service.delete_holiday(holiday_id)

    def get_holiday(self, holiday_id):
        return self.holidays_service.get_holiday(holiday_id)

    def get_holidays_between_dates(self, fecha_inicio, fecha_fin):
        return self.holidays_service.get_holidays_between_dates(fecha_inicio, fecha_fin)

    def get_all_holidays(self, year):
        # Intentar obtener los feriados desde la base de datos
        self.fetch_all_holidays(year=year)
        holidays = self.holidays_service.get_all_holidays(year)
        
        # Si no existen feriados en la base de datos, intentamos obtenerlos desde la API
        if not holidays:
            if self.fetch_all_holidays(year=year):
                holidays = self.holidays_service.get_all_holidays(year)
            else:
                raise Exception("Error al obtener los feriados")
        
        return holidays

    def get_holiday_by_date(self, date):
        return self.holidays_service.get_holiday_by_date(date)

    def fetch_specific_holidays(self, date_to_search):
        """
        Obtiene los feriados para una fecha específica desde la API o la base de datos local.

        Args:
            date_to_search: Fecha a buscar en los feriados.

        Returns:
            Lista de feriados para la fecha proporcionada.
        """
        try:
            # Intentar buscar en la base de datos local primero
            local_holidays = self.holidays_service.get_holidays_from_db(date_to_search)
            if local_holidays:
                return local_holidays

            # Si no se encuentran feriados, obténlos desde la API
            url = f"{self.api_url}{self.year}"
            response = requests.get(url)
            response.raise_for_status()

            data = self.get_date(date_to_search, response.json())
            self.update_local_database(data)
            return data
        except requests.exceptions.RequestException as e:
            # Manejar la excepción, por ejemplo, registrarla en un log
            print(f"Error al obtener los feriados: {e}")
            return []

    def fetch_all_holidays(self, year, max_retries=3, retry_delay=2):
        """
        Obtiene todos los feriados para el año especificado desde la API con reintentos en caso de error.

        Args:
            year: El año de los feriados.
            max_retries: Número máximo de reintentos en caso de error.
            retry_delay: Tiempo en segundos entre intentos.

        Returns:
            Lista de feriados obtenidos desde la API o de la base de datos local.
        """
        retries = 0
        while retries < int(max_retries):
            try:
                url = f"{self.api_url}{year}"

                # Headers para evitar bloqueo por scrapping, opcional
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
                    'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'ACCEPT-ENCODING': 'gzip, deflate, br',
                    'REFERER': 'https://www.google.com/'
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()

                response_update = self.update_local_database(response.json())
                
                if response_update:
                    return response_update

                raise Exception("Ya existe un feriado con la misma fecha")

            except requests.exceptions.RequestException as e:
                retries += 1  # Incrementa el contador de intentos
                print(f"Error al obtener los feriados (Intento {retries}): {e}")

                if retries < int(max_retries):
                    print(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(int(retry_delay))
                    continue
                raise Exception("Máximo intentos superados")

    def update_local_database(self, data):
        """
        Actualiza la base de datos local con los datos de los feriados obtenidos.

        Args:
            data: Lista de diccionarios con los datos de los feriados.

        Returns:
            True si la base de datos se actualiza correctamente.
        """
        for feriado in data:
            fecha = datetime.strptime(feriado['fecha'], "%Y-%m-%d")
            if not fecha:
                continue
            
            # Utiliza el servicio para crear un nuevo feriado en la base de datos
            self.holidays_service.create_holiday(
                nombreFeriado=feriado['nombre'].capitalize(),
                fecha=fecha,
                tipo=feriado['tipo'].capitalize(),
                descripcion=feriado['comentarios'].capitalize() if feriado['comentarios'] else 'Sin Comentario',
                dia_semana=fecha.strftime("%A").capitalize(),
                irrenunciable=feriado['irrenunciable']
            )
        return True
