from socket import *


SERVER_NAME = '127.0.0.1'
PORT = 8181

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((SERVER_NAME, PORT))

request = input('>> ')
clientSocket.send(request.encode())

response = clientSocket.recv(1024)
print('Received: ', response)

clientSocket.close()
