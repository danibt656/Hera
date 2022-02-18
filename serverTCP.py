from socket import *
from logging import info, error
import json


# Cargar configuracion
conf = open('server_conf.json')
conf = json.load(conf)

HOST = conf['host']
PORT = conf['port']
BACKLOG = 4
BUFFSIZE = 1024


def init_server():
    try:
        sockfd = socket(AF_INET, SOCK_STREAM)
        info('Creating socket')
    except socket.error as err:
        error(f'Failed to create socket with error: {err}')

    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind((HOST, PORT))
    sockfd.listen(BACKLOG)
    info('Socket is now listening')
    
    return sockfd


def accept_connections(serverSocket):
    connectionfd, address = serverSocket.accept()
    
    request = connectionfd.recv(BUFFSIZE)
    
    response = process_request(request)

    connectionfd.sendall(response)
    connectionfd.close()

def process_request(request):
    return request.upper()


if __name__ == '__main__':
    serverSocket = init_server()

    while True:
        accept_connections(serverSocket)

