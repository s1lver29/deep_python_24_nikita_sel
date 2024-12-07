# pylint: disable=R0902, W0718

import argparse
import json
import socket
import threading
import urllib.parse
import urllib.request
from collections import Counter
from queue import Queue
from time import sleep


class MasterServer:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        self.worker_threads = []
        self.queue = Queue()
        self.total_processed = 0
        self.shutdown_flag = threading.Event()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            sock.bind((self.host, self.port))
            sock.listen(5)
            print(f"Server listening on {self.host}:{self.port}")

            for i in range(self.num_workers):
                self.start_worker(i)

            try:
                while not self.shutdown_flag.is_set():
                    client_socket, address = sock.accept()
                    client_socket.settimeout(10)
                    print(
                        f"Connection from {address}; "
                        f"accept client {client_socket}"
                    )
                    self.queue.put(client_socket)
            except KeyboardInterrupt:
                print("Shutting down server...")
                self.shutdown_flag.set()
            finally:
                self.queue.join()
                print("Server stopped.")

    def start_worker(self, worker_id):
        worker = Worker(self.queue, self.top_k, self, worker_id)
        thread = threading.Thread(target=worker.run, daemon=True)
        self.worker_threads.append(thread)
        thread.start()
        print(f"Worker {worker_id} started.")

    def monitor_workers(self):
        """Мониторинг состояния воркеров и перезапуск при необходимости."""
        while not self.shutdown_flag.is_set():
            for i, thread in enumerate(self.worker_threads):
                if not thread.is_alive():
                    print(f"Worker {i} crashed! Restarting...")
                    self.start_worker(i)
            sleep(1)

    def update_statistics(self):
        self.total_processed += 1
        print(f"Total URLs processed: {self.total_processed}")


class Worker:
    def __init__(self, queue, top_k, master, worker_id):
        self.queue = queue
        self.top_k = top_k
        self.master = master
        self.worker_id = worker_id

    def run(self):
        while not self.master.shutdown_flag.is_set():
            try:
                client_socket = self.queue.get()
                try:
                    url = client_socket.recv(1024).decode().strip()
                    if self.is_valid_url(url):
                        print(f"Processing URL: {url}")
                        top_words = self.process_url(url)
                        response = json.dumps(top_words)
                        client_socket.sendall(response.encode())
                        self.master.update_statistics()
                    else:
                        error_message = "Invalid URL"
                        client_socket.sendall(error_message.encode())
                except Exception as error:
                    print(f"Worker {self.worker_id} error: {error}")
                    try:
                        client_socket.sendall(
                            json.dumps({"error": "Processing failed"}).encode()
                        )
                    except Exception as send_error:
                        print(
                            f"Worker {self.worker_id} "
                            f"failed to send error: {send_error}"
                        )
                finally:
                    client_socket.close()
                    self.queue.task_done()
            except Exception as error:
                print(f"Worker down: {error}. Restarting...")
                continue

    def is_valid_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def process_url(self, url):
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                content = response.read().decode("utf-8")
                words = content.split()
                word_counts = Counter(words)
                top_words = dict(word_counts.most_common(self.top_k))
                return top_words
        except Exception as error:
            print(f"Error fetching URL {url}: {error}")
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

    monitor_thread = threading.Thread(
        target=server.monitor_workers, daemon=True
    )
    monitor_thread.start()

    server.start_server()


if __name__ == "__main__":
    main()
