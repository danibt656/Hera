from socket import *
import json
from hvap import HVAP_request
import signal

def generate_request(command):
    request = HVAP_request(command.upper(),["Day: now"])
    request= request._to_ascii()
    return request

def handler_SIGINT(signum, frame):
    print('\nClosing client, bye!\n')
    exit(1)

def main():
    # Cargar configuracion
    conf = open('server_conf.json')
    conf = json.load(conf)
    signal.signal(signal.SIGINT, handler_SIGINT)

    HOST = conf['host']
    PORT = conf['port']

    command = input('>> ')

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((HOST, PORT))

    request = generate_request(command)

    clientSocket.send(request.encode())

    response = clientSocket.recv(1024)
    response.decode()
    print('Received: ', response)

    clientSocket.close()

if __name__ == '__main__':
    main()