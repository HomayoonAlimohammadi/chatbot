from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time
import socket
from queue import Queue
from typing import Any
import json


class ChatBot:
    def __init__(self, host: str, port: int, n_threads: int = 5) -> None:
        self._host = host
        self._port = port
        self._n_threads = n_threads
        self.works: list[Any] = []

    def run(self) -> None:
        print("ChatBot is starting quickly...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self._host, self._port))
        self.listen()

    def listen(self) -> None:
        self.socket.listen()
        with ThreadPoolExecutor(self._n_threads) as executor:
            while True:
                try:
                    conn, addr = self.socket.accept()
                    work = executor.submit(self.handler, conn)
                    self.works.append(work)
                except KeyboardInterrupt as e:
                    self.stop()

    def handler(self, conn: socket.socket) -> None:
        sleep(1)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall("Done".encode())

    def stop(self):
        print("ChatBot is shuttoing down gracefully...")
        self.socket.close()
        for work in self.works:
            if not work.done():
                print("Something Went wrong...")
                break
        else:
            print("All Done.")


def main():
    with open("conf.json", "r") as f:
        data = json.load(f)
        HOST = data["HOST"]
        PORT = data["PORT"]
    chatbot = ChatBot(HOST, PORT)
    chatbot.run()
    sleep(2)
    chatbot.stop()


if __name__ == "__main__":
    main()
