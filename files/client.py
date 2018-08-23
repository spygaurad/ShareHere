import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error:
    print("Failed to connect")
    sys.exit()

print("Socket Created")
host = "127.0.0.4"
port = 9998


try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Host could not be resolved")
    sys.exit()

print("Host IP " + ip)
s.connect((ip, port))

welcome = s.recv(1024)
print(welcome.decode())

filename = input("Filename? -> ")
s.send(filename.encode())
print(filename)
# try:
#     s.send(message.encode())
# except socket.error:
#     print("D")
#     sys.exit()

file = s.recv(1024)
filesize = int(file.decode())
print(filesize)
f = open('new_' + filename, 'wb')
data = s.recv(1024)
totalRecv = len(data)
f.write(data)
while totalRecv < filesize:
    data = s.recv(4096)
    print("received ", totalRecv)
    totalRecv += len(data)
    f.write(data)

print("Download Complete!")
f.close()

# close the connection
s.close()
