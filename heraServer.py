from socket import *
import logging
import json
import signal
import threading
from hvap import *


# Cargar configuracion
conf = open('server_conf.json')
conf = json.load(conf)
HOST = conf['host']
PORT = conf['port']
BACKLOG = conf['max_clients']
BUFFSIZE = 1024

# Variables globales
serverSocket = None

def init_server():
    try:
        sockfd = socket(AF_INET, SOCK_STREAM)
    except socket.error as err:
        error(f'No se pudo crear socket por error: {err}')

    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind((HOST, PORT))
    sockfd.listen(BACKLOG)
    logging.info('Servidor en escucha')
    
    return sockfd


def accept_connections(serverSocket):
    connectionfd, _ = serverSocket.accept()
    
    request = connectionfd.recv(BUFFSIZE)
    request = request.decode()
    
    thread = threading.Thread(target=process_request, args=(connectionfd,request,))
    thread.start()

def process_request(connectionfd, request):
    logging.info(f'Nuevo servicio [{threading.current_thread()}]')

    response = eval_request(request.split('\r\n'))

    if response is None:
        response = response_error('400')._to_ascii()

    connectionfd.sendall(response.encode())
    connectionfd.close()
    logging.info(f'Cerrando servicio [{threading.current_thread()}]')
    

def handler_SIGINT(signum, frame):
    print('\n')
    logging.info('Cerrando servidor\n')
    serverSocket.close()
    exit(1)

if __name__ == '__main__':
    # Set up logger
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    if serverSocket is None:
        serverSocket = init_server()

    signal.signal(signal.SIGINT, handler_SIGINT)

    while True:
        accept_connections(serverSocket)

