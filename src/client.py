import socket


HOST = "127.0.0.1"
PORT = 65431

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"1,2,3")
    data = s.recv(1024).decode()


print(f"Recieved data: {data}")
