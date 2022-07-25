import socket
import os
from time import sleep


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8006

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    request = conn.recv(1024).decode()

    conn.sendall("Processing your request...".encode())
    sleep(5)
    conn.sendall("Done processing!".encode())

    conn.close()
