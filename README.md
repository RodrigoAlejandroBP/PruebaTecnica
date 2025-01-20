# PruebaTecnica FastAPI
Prueba Tecnica Desarrollador Python

Crear un script en Python que consulte la API de feriados de Chile (https://apis.digital.gob.cl/fl/feriados/2024) para obtener los feriados del año. Manejar errores, como si la API no responde.

Procesar los datos obtenidos de la API y transformarlos a un formato JSON con campos como: nombre del feriado, fecha, tipo, descripción y día de la semana.

Guardar estos datos en una base de datos (puede ser MySQL o Postgres). Manejar conexiones y errores de manera adecuada.

Crear una API REST con FastAPI o Flask que reciba una fecha en formato yyyy-mm-dd y devuelva la información del feriado correspondiente desde la base de datos. Por ejemplo:

json
{
    "nombreFeriado": "Año Nuevo",
    "fecha": "01-01-2024",
    "tipo": "Civil",
    "descripcion": "Año Nuevo",
    "dia_semana": "Miércoles"
}
Entregables: Código fuente, scripts para la base de datos y la documentación de la API (en formato Swagger o similar).
