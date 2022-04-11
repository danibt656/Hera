from socket import *
import json
from hvap import HVAP_request
import signal
import aiml
import os
import sys
from gtts import gTTS
from playsound import playsound

clientSocket = None
RECV_SIZE = 1024

BRAIN_FILE = "bot_brain.brn"
AIML_XML = "std-startup.xml"
AIML_LOAD = "load aiml b"

ENCODE_FORMAT = 'utf-8'

def generate_request(command, headers):
    request = HVAP_request(command.upper(), headers)
    request= request._to_ascii()
    return request

def handler_SIGINT(signum, frame):
    print('\nClosing client, bye!\n')
    
    if clientSocket is not None:
        clientSocket.close()

    exit(1)

def main():
    # Cargar configuracion
    conf = open('server_conf.json')
    conf = json.load(conf)
    signal.signal(signal.SIGINT, handler_SIGINT)
    kernel = aiml.Kernel()

    # Cargar conexion TCP
    HOST = conf['host']
    PORT = conf['port']
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))

    # Cargar Kernel de AIML
    if os.path.isfile(BRAIN_FILE):
        kernel.bootstrap(brainFile = BRAIN_FILE)
    else:
        kernel.bootstrap(learnFiles = AIML_XML, commands = AIML_LOAD)
        kernel.saveBrain(BRAIN_FILE)
    kernel.learn(AIML_XML)
    kernel.respond(AIML_LOAD)

    #message = input('>> ')
    message = sys.argv[1]

    # Obtener respuesta del kernel
    command = kernel.respond(message)
    command = command.split(' ')[0]

    # Computar cabeceras para request
    headers = []
    instant = kernel.getPredicate('instant')
    if instant != '':
        headers.append(instant)
    location = kernel.getPredicate('location')
    if location != '':
        headers.append(location)

    # Generar y enviar request
    request = generate_request(command, headers)
    clientSocket.send(request.encode())

    # Recibir y procesar respuesta
    response = clientSocket.recv(RECV_SIZE)
    response = str(response, ENCODE_FORMAT).split('\r\n')
    # Ahora
    #   response[0] = codigo+' '+mensaje
    #   response[1] = texto de respuesta
    #   response[2] = ''
    print('\t=> Received: ', response[1])
    voice_obj = gTTS(text=response[1], lang='es', slow=False)
    voice_obj.save("temp/response.mp3")
    playsound("temp/response.mp3")

    print('Limpiando ficheros temporales...')
    dir_name = "./temp/"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))
    print('Ficheros temporales eliminados')

    clientSocket.close()

if __name__ == '__main__':
    main()