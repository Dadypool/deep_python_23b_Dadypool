"Homework 6 with clients"

import socket
import threading
import queue


def send_request(urls_queue, server_address, server_port):
    "Client thread for sending requests to server and printing response"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_address, server_port))
        except Exception:
            print(f"{threading.current_thread().name} can't connect to server")
            return

        while True:
            try:
                url = urls_queue.get(timeout=2)
            except queue.Empty:
                break

            try:
                client_socket.send(url.encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8")
                print(f"{threading.current_thread().name} {url}: {response}")
            except Exception:
                print(f"{threading.current_thread().name} {url}: Error")


def main(num_threads, filename, server_address, server_port):
    "Main function. Puts urls in Queue and starts client_threads"

    urls_queue = queue.Queue(maxsize=num_threads + 5)

    for i in range(num_threads):
        thread = threading.Thread(
            target=send_request,
            name=f"Client-{i}",
            args=(urls_queue, server_address, server_port),
        )
        thread.start()

    with open(filename, "r", encoding="UTF-8") as file:
        for line in file.read().splitlines():
            try:
                urls_queue.put(line, timeout=5)
            except queue.Full:
                print("Queue is full, something went wrong")
                break
    urls_queue.put(None)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Client")
    parser.add_argument("num_threads", type=int, help="Number of threads")
    parser.add_argument("filename", type=str, default="urls.txt", help="File with URLs")
    args = parser.parse_args()

    HOST = "127.0.0.1"
    PORT = 5000

    main(args.num_threads, args.filename, HOST, PORT)
