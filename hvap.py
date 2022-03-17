"""
Utiliades para el protocolo HVAP
"""

# codigo - mensaje
response_codes = {
    '200': 'OK',
    '400': 'NOT RECOGNIZED',
    '403': 'BAD SYNTAX',
}

# comando de voz
commands = {
    'GREET': 1,
    'HWRU': 1,
    'TIME': 1,
    'WEATHER': 1,
    'DATE': 1,
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
        self.response_code = response_code
        self.response_message = commands[(str)(response_code).lower()]
        self.text = text

    def _to_ascii(self):
        ascii = f'{self.response_code} {self.response_message}\r\n{self.text}\r\n'
        
        return ascii


def eval_request(toks):
    if eval_command(toks[0]) is True:
        print("Command valid")

def eval_command(command):
    if commands[command.upper()] == 1:
        return True
    return False