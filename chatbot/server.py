from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import socket
from typing import Any
import json


class NoSocketAvailableException(Exception):
    ...


class ChatBot:
    """
    ChatBot class for accepting requests and establishing connections with the client.
    """

    def __init__(self, host: str, port: int, n_threads: int = 5) -> None:
        self._host = host
        self._port = port
        self._n_threads = n_threads
        self.works: list[Any] = []  # kheili bade!

    def run(self) -> None:
        """
        Function that gets the chatbot instance running.
        """
        try:
            print("ChatBot is starting quickly...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self._host, self._port))
            self.accept_connection()
        except Exception as e:
            print(e)
            # TODO: user some logging tool or...
            raise NoSocketAvailableException

    def accept_connection(self) -> None:
        """
        Function that accepts new connections and pass it to the handler.
        """
        self.socket.listen()
        with ThreadPoolExecutor(self._n_threads) as executor:
            while True:
                try:
                    conn, addr = self.socket.accept()
                    print(f"New Connection with address {addr} was added.")
                    work = executor.submit(self.handler, conn)
                    self.works.append(work)
                except KeyboardInterrupt as e:
                    print(e)
                    self.shutdown()
                    break

    def handler(self, conn: socket.socket) -> None:
        """
        Handles a given connection.
        Closes the connection at the end.
        """
        sleep(1)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # TODO: Check for the connection not being closed.
                conn.sendall("Done".encode())

    def shutdown(self) -> None:
        """
        Shutdown the chatbot after ensuring all the connections are dealt with.
        """
        print("ChatBot is shuttoing down gracefully...")
        # TODO: maybe the client closes the connection and...
        self.socket.close()
        for work in self.works:
            if not work.done():
                print("Something Went wrong...")
                break
        else:
            print("All Done.")


def main() -> None:
    with open("conf.json", "r") as f:
        data = json.load(f)
        HOST = data["HOST"]
        PORT = data["PORT"]
    chatbot = ChatBot(HOST, PORT)
    chatbot.run()


if __name__ == "__main__":
    main()
