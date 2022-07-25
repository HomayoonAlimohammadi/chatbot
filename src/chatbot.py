import socket

HOST = "127.0.0.1"
PORT = 65431

N_CONNECTIONS = 1
print(f"I am accepting connection {N_CONNECTIONS} times...")
for i in range(N_CONNECTIONS):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode()
                buf = data.split(",")
                buf = str(sum(map(int, buf)))
                conn.sendall(buf.encode())
print("I'm done, closing gracefully...")
