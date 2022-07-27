from __future__ import annotations
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
import socket
import json
from time import sleep
from typing import Any


def send_request(HOST: str, PORT: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"my request")


def check_done(works: list[Future[Any]]):
    return all([work.done() for work in works])


def main():
    with open("conf.json", "r") as f:
        data = json.load(f)
        HOST = data["HOST"]
        PORT = data["PORT"]
        NUM_THREADS = data["NUM_THREADS"]  # 5
        print(HOST, PORT)
    with ThreadPoolExecutor(NUM_THREADS) as executor:
        works = [executor.submit(send_request, HOST, PORT) for _ in range(NUM_THREADS)]

    sleep(1)
    if not check_done(works):
        print("Something went wrong...")
    else:
        print("Every client got their answer.")


if __name__ == "__main__":
    main()
