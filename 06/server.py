"Homework 6 with server"

import socket
import threading
import queue

import re
from collections import Counter

import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup


def master(server_address, server_port, num_workers, k):
    "Master thread. Starts worker_threads and listen for clients"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_address, server_port))
        server_socket.listen()
        server_socket.settimeout(10)
        print(
            f"Server listening on {server_address}:{server_port} with {num_workers} workers"
        )

        sockets_queue = queue.Queue()
        lock = threading.Lock()
        total = [0]

        for i in range(num_workers):
            worker_thread = threading.Thread(
                target=worker, name=f"Worker-{i}", args=(k, sockets_queue, lock, total)
            )
            worker_thread.start()

        while True:
            try:
                client_socket, addr = server_socket.accept()

                if not client_socket:
                    break

                print(f"Accepted connection from {addr}")
                sockets_queue.put((client_socket, addr))
            except socket.timeout:
                break


def worker(k, sockets_queue, lock, total):
    "Worker thread for handling clients requests"

    while True:
        try:
            client_socket, _ = sockets_queue.get(timeout=10)

            with client_socket:
                while True:
                    url = client_socket.recv(1024).decode("utf-8").strip()

                    if not url:
                        break

                    response_data = get_top_k(url, k)
                    client_socket.send(response_data)

                    with lock:
                        total[0] += 1
                        print(f"Total requests handled: {total[0]}")
        except queue.Empty:
            break


def get_top_k(url, k):
    "Fetch url and count top k words"

    try:
        with urlopen(url) as response:
            html = response.read().decode("utf-8")

            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            words = re.findall(r"\w+", text)
            word_count = Counter(words)
            top_words = dict(word_count.most_common(k))

            response_data = json.dumps(top_words).encode("utf-8")
            return response_data
    except HTTPError:
        return "HTTP Error".encode("utf-8")
    except URLError:
        return "URL Error".encode("utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Master-Worker Server")
    parser.add_argument(
        "-w", "--workers", type=int, default=3, help="Number of workers"
    )
    parser.add_argument(
        "-k", "--top_k", type=int, default=10, help="Top K words to return"
    )
    args = parser.parse_args()

    HOST = "127.0.0.1"
    PORT = 5000

    master = threading.Thread(
        target=master, name="Master", args=(HOST, PORT, args.workers, args.top_k)
    )
    master.start()
    master.join()
