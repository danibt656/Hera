from socket import *
import json


# Cargar configuracion
conf = open('server_conf.json')
conf = json.load(conf)

HOST = conf['host']
PORT = conf['port']

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST, PORT))

request = input('>> ')
clientSocket.send(request.encode())

response = clientSocket.recv(1024)
print('Received: ', response)

clientSocket.close()
