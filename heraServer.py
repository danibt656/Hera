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
BACKLOG = 4
BUFFSIZE = 1024

serverSocket = None

def init_server():
    try:
        sockfd = socket(AF_INET, SOCK_STREAM)
        logging.info('Creating socket')
    except socket.error as err:
        error(f'Failed to create socket with error: {err}')

    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind((HOST, PORT))
    sockfd.listen(BACKLOG)
    logging.info('Socket is now listening')
    
    return sockfd


def accept_connections(serverSocket):
    connectionfd, address = serverSocket.accept()
    
    request = connectionfd.recv(BUFFSIZE)
    request = request.decode()
    
    thread = threading.Thread(target=process_request, args=(connectionfd,request,))
    thread.start()

def process_request(connectionfd, request):
    logging.info(f'Init service [{threading.current_thread()}]')

    eval_request(request.split('\r\n'))
    response = request.encode()

    connectionfd.sendall(response)
    connectionfd.close()
    logging.info(f'Finishing service [{threading.current_thread()}]')
    

def handler_SIGINT(signum, frame):
    print('\n')
    logging.info('Closing server, bye!\n')
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

