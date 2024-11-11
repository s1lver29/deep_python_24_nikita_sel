# pylint: disable=R0902, W0718

import threading
import socket
import urllib.request
import urllib.parse
from collections import Counter
import json
import argparse


class MasterServer:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        self.worker_threads = []
        self.queue = []
        self.lock = threading.Lock()
        self.total_processed = 0

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        for _ in range(self.num_workers):
            worker = Worker(self.queue, self.lock, self.top_k, self)
            thread = threading.Thread(target=worker.run)
            self.worker_threads.append(thread)
            thread.start()

        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            with self.lock:
                self.queue.append(client_socket)

    def update_statistics(self):
        with self.lock:
            self.total_processed += 1
            print(f"Total URLs processed: {self.total_processed}")


class Worker:
    def __init__(self, queue, lock, top_k, master):
        self.queue = queue
        self.lock = lock
        self.top_k = top_k
        self.master = master

    def run(self):
        while True:
            client_socket = None
            with self.lock:
                if self.queue:
                    client_socket = self.queue.pop(0)

            if client_socket:
                try:
                    url = client_socket.recv(1024).decode().strip()
                    if self.is_valid_url(url):
                        print(f"Processing URL: {url}")
                        top_words = self.process_url(url)
                        response = json.dumps(top_words)
                        client_socket.sendall(response.encode())
                        self.master.update_statistics()
                    else:
                        error_message = json.dumps({"error": "Invalid URL"})
                        client_socket.sendall(error_message.encode())
                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    client_socket.close()

    def is_valid_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def process_url(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode("utf-8")
                words = content.split()
                word_counts = Counter(words)
                top_words = dict(word_counts.most_common(self.top_k))
                return top_words
        except Exception as e:
            print(f"Error fetching URL {url}: {e}")
            return {}


def main():
    parser = argparse.ArgumentParser(description="Master-Worker Server")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        required=True,
        help="Number of worker threads",
    )
    parser.add_argument(
        "-k",
        "--top_k",
        type=int,
        required=True,
        help="Top K most frequent words",
    )
    args = parser.parse_args()

    server = MasterServer(
        host="localhost", port=8080, num_workers=args.workers, top_k=args.top_k
    )
    server.start_server()


if __name__ == "__main__":
    main()
