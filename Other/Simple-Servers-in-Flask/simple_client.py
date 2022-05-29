import socket


ip_v4 = '127.0.0.1'
port = 444

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_v4, port))

msg = input("Enter Message")

while msg != 'quit':
    client_socket.send(msg.encode())
    msg = client_socket.recv(2048).decode()
    print(msg)
    msg=input('Enter message')
client_socket.close()
