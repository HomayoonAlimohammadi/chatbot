import socket
import json


with open("conf.json", "r") as f:
    data = json.load(f)
    HOST = data["HOST"]
    PORT = data["PORT"]
    print(HOST, PORT)


for i in range(5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"my request")
        data = s.recv(1024).decode()
