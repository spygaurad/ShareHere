import socket
import sys
from _thread import *
import os

host = '127.0.0.4'
port = 9998

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket Created")

try:
    s.bind((host, port))

except socket.error:
    print("Binding Failed")
    sys.exit()

print("Socket is ready")
s.listen(10)

def clientthread(conn):
    welcome_message = 'Welcome to server. Type something and hit enter \n'
    conn.send(welcome_message.encode())

    file = conn.recv(1024)
    filename = file.decode()
    if os.path.isfile('media'+filename):
        print("exists")
        size = str(os.path.getsize('media' + filename))
        conn.send(size.encode())
        print(size)
        with open(filename, 'rb') as f:
            bytesToSend = f.read(4096)
            print(bytesToSend)
            conn.send(bytesToSend)
            while bytesToSend != "":
                bytesToSend = f.read(4096)
                conn.send(bytesToSend)
    else:
        conn.send(b"File does not exist ")
    conn.close()


while True:
    print("hello")
    conn, addr = s.accept()
    print("Connected with " + addr[0] + ":" + str(addr[1]))
    start_new_thread(clientthread, (conn,))

s.close()
