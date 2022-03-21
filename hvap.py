"""
Utiliades para el protocolo HVAP
"""
import logging

"""
##############################################################
Funciones de atencion a cada comando de voz
"""
def eval_greet(request_obj):
    return HVAP_response('200', 'Hola!')

def eval_how_are_you(request_obj):
    return HVAP_response('200', 'Bien, gracias! :D')

def eval_time_of_day(request_obj):
    return HVAP_response('200', 'Son las 8:00 pm')

def eval_date(request_obj):
    return HVAP_response('200', 'Hoy es 22 de Septiembre')

def eval_weather(request_obj):
    return HVAP_response('200', 'Hace frio :(')
"""
##############################################################
"""

# codigo - mensaje
response_codes = {
    '200': 'OK',
    '400': 'NOT RECOGNIZED',
    '403': 'BAD SYNTAX',
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
    
    return HVAP_response(err_code, msg)