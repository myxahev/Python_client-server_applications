from argparse import ArgumentParser
from socket import socket, AF_INET, SOCK_STREAM

parser = ArgumentParser()
parser.add_argument('--port', help='server port', type=int, default=7777)
parser.add_argument('--addr', help='address', type=str, default='localhost')
args = parser.parse_args()

client = socket(AF_INET, SOCK_STREAM)
client.connect((args.addr, args.port))
msg = 'Привет, сервер'
client.send(msg.encode('utf-8'))
data = client.recv(1024)
print('Сообщение от сервера: ', data.decode('utf-8'), ', длиной ', len(data), ' байт')
client.close()