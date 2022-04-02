"""
Utiliades para el protocolo HVAP
"""
from lib2to3.pgen2.token import COMMA
import logging
from datetime import datetime
import requests, json

# Weather API base URL & Key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "d9eabd7a98b614cff8a11b7e4b2ba540"
KELVIN_TO_CELSIUS = 273

# Codigo error en procesado de comando
COMMAND_ERR = -1

"""
##############################################################
Funciones de atencion a cada comando de voz
"""
def eval_greet(request_obj):
    """
    Saludar
    """
    return HVAP_response('200', 'Hola!')

def eval_how_are_you(request_obj):
    """
    Preguntar que tal
    """
    return HVAP_response('200', 'Bien, gracias! :D')

def eval_time_of_day(request_obj):
    """
    Obtener la hora
    """

    time = datetime.now()
    hour = time.hour
    min = time.minute
    instant = 'mañana'

    if hour < 6:
        instant = 'madrugada'
    if hour >= 13:
        instant = 'tarde'
    if hour >= 21:
        instant = 'noche'

    if hour > 12:
        hour = hour - 12
    if hour == 0:
        hour = 12

    las = 'las'
    if hour == 1:
        las = 'la'

    return HVAP_response('200', f'Son {las} {hour} y {min} de la {instant}')

def eval_date(request_obj):
    """
    Obtener la fecha
    """

    today = datetime.today()
    day = today.weekday() + 1
    day_num = today.day

    when = request_obj.headers[0].upper()
    
    response_text = 'Hoy es '
    if when == 'AYER':
        response_text = 'Ayer fue '
        day -= 1
        day_num -= 1


    Day_dict = {1: 'Lunes', 2: 'Martes', 3: 'Miercoles',
                4: 'Jueves', 5: 'Viernes', 6: 'Sabado',
                7: 'Domingo'}

    Month_dict = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                  5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                  9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre',
                  12: 'Diciembre'}

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        response_text += day_of_the_week + ', ' + str(day_num) + ' de '

    if today.month in Month_dict.keys():
        month_of_the_year = Month_dict[today.month]
        response_text += month_of_the_year

    return HVAP_response('200', response_text)

def eval_weather(request_obj):
    """
    Obtener el tiempo en una ciudad dada
    """

    city = request_obj.headers[0].upper()
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY

    response = requests.get(URL)

    if response.status_code != 200:
        return COMMAND_ERR
            
    data = response.json()
    main = data['main']
    
    # Temperatura
    temp = int(main['temp'] - KELVIN_TO_CELSIUS)
    s1 = ''
    if temp > 1:
        s1 = 's'
    # Sensacion termica
    temp_feel_like = int(main['feels_like'] - KELVIN_TO_CELSIUS)
    s2 = ''
    if temp > 1:
        s2 = 's'
    # Humedad
    humidity = main['humidity']
    # Recomendacion
    recommend = weather_recommendation(temp_feel_like)

    return HVAP_response('200',
                f"La temperatura en {city} es de {temp} grado{s1}, con una sensacion termica de {temp_feel_like} grado{s2}, y una humedad del {humidity} por ciento. "+recommend
            )

def weather_recommendation(temp_feel_like):
    """
    Obtener una recomendacion basada en la sensacion termica
    """

    if temp_feel_like <= 5:
        return 'Recuerda abrigarte!'
    elif temp_feel_like <= 15:
        return 'Hace fresquito!'
    elif temp_feel_like <= 27:
        return 'Hace un dia estupendo!'
    else:
        return 'Cuidado con el bochorno!'

"""
##############################################################
"""

# codigo - mensaje
response_codes = {
    '200': 'OK',
    '400': 'NOT RECOGNIZED',
    '403': 'BAD SYNTAX',
    '500': 'COMMAND ERROR'
}

# comando de voz
commands = {
    'GREET': eval_greet,
    'HWRU': eval_how_are_you,
    'TIME': eval_time_of_day,
    'DATE': eval_date,
    'WEATHER': eval_weather,
}

class HVAP_request:

    def __init__(
        self,
        command,
        headers
    ):
        """ Inicializa una peticion HVAP
        """
        self.command = command
        self.headers = headers

    def _to_ascii(self):
        """ Convierte un objeto Request a un string
        """
        ascii = f'{self.command}\r\n'
        for header in self.headers:
            ascii += f'{header}\r\n'
        
        return ascii


class HVAP_response:

    def __init__(
        self,
        response_code,
        text
    ):
        """ Inicializa una respuesta HVAP
        """
        self.response_code = response_code
        self.response_message = response_codes[(str)(response_code).lower()]
        self.text = text

    def _to_ascii(self):
        """ Convierte un objeto Response a un string
        """
        ascii = f'{self.response_code} {self.response_message}\r\n{self.text}\r\n'
        
        return ascii


def eval_request(toks):
    """
    Evaluar una request como lista de tokens:
        toks[0] -> comando
        toks[1..] -> cabeceras
    Transforma la lista de tokens de vuelta a una HVAP_request
    y llama a la rutina de atencion asociada al comando
    """
    command = toks[0]
    if eval_command(command) is False:
        logging.info("Comando invalido")
        return None

    logging.info("Comando valido")
    request_obj = HVAP_request(command, toks[1:])

    response = commands[command](request_obj)

    if response == COMMAND_ERR:
        response = response_error('500')

    return response._to_ascii()

def eval_command(command):
    """
    Evalua un comando, devuelve True si el comando de voz
    esta soportado por el asistente, y False si no
    """
    ret = None
    try:
        ret = commands[command.upper()]
    except:
        return False
    if ret is not None:
        return True
    return False

def response_error(err_code):
    """
    Devuelve un objeto de HVAP_response asociado a un codigo
    de error determinado, con el texto de respuesta adecuado
    """
    if response_codes[err_code] is None or err_code == '200':
        logging.error('Codigo de error no soportado')
    
    if err_code == '400':
        msg = 'No te he entendido'
    elif err_code == '403':
        msg = 'Por favor, vuelve a preguntar'
    elif err_code == '500':
        msg = 'Ha habido un error, vuelve a intentarlo'
    
    return HVAP_response(err_code, msg)