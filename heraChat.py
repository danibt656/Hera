
# Comandos de HVAP
GREET_COMMAND = 'GREET'
HWRU_COMMAND = 'HWRU'
TIME_COMMAND = 'TIME'
DATE_COMMAND = 'DATE'
WEATHER_COMMAND = 'WEATHER'


"""
Obtiene el comando de respuesta para un mensaje
introducido por el usuario

Args:
    message: Texto plano con peticion del usuario
Return:
    comando de protocolo HVAP apropiado a la peticion
"""
def get_request_command(message):
    msg_case = message.upper()
    # Saludos
    if 'HOLA' in msg_case:
        return GREET_COMMAND, None
    if 'COMO ESTAS' in msg_case or "QUE TAL" in msg_case:
        return HWRU_COMMAND, None

    # Tiempo
    if 'TIEMPO EN' in msg_case:
        city = get_city_as_plain_text(msg_case, 'TIEMPO EN')
        return WEATHER_COMMAND, {'location':city}
    elif 'TIEMPO HACE EN' in msg_case:
        city = get_city_as_plain_text(msg_case, 'TIEMPO HACE EN')
        return WEATHER_COMMAND, {'location':city}
    elif 'TEMPERATURA EN' in msg_case:
        city = get_city_as_plain_text(msg_case, 'TEMPERATURA EN')
        return WEATHER_COMMAND, {'location':city}
    elif 'TIEMPO QUE HACE EN' in msg_case:
        city = get_city_as_plain_text(msg_case, 'TIEMPO QUE HACE EN')
        return WEATHER_COMMAND, {'location':city}

    # Hora
    if 'HORA' in msg_case:
        return TIME_COMMAND, None

    # Fecha
    if 'FECHA' in msg_case or 'QUE DIA ES' in msg_case \
        or 'QUE DIA ESTAMOS' in msg_case or 'QUE DIA FUE' in msg_case:
        instant = ''
        # Ayer
        if 'AYER' in msg_case:
            instant = 'AYER'

        return DATE_COMMAND, {'instant':instant}

def get_city_as_plain_text(msg_case, prompt):
    city = msg_case.split(prompt,1)[1]

    import string
    city_clean = city.translate(str.maketrans('', '', string.punctuation))
    
    return city_clean