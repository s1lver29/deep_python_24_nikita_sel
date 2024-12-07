# pylint: disable=W0718

import argparse
import socket
import threading
from pathlib import Path


class URLClient:
    def __init__(self, num_threads, urls_file):
        self.num_threads = num_threads
        self.urls = self.load_urls(urls_file)
        self.lock = threading.Lock()
        self.url_index = 0

    def load_urls(self, file_path):
        base_path = Path(__file__).parent
        file_path = Path(base_path / file_path)

        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                url = line.strip()
                if url:
                    yield url

    def get_next_url(self):
        with self.lock:
            try:
                return next(self.urls)
            except StopIteration:
                return None

    def send_url(self, url):
        try:
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as client_socket:
                client_socket.connect(("localhost", 8080))
                client_socket.sendall(url.encode())
                response = client_socket.recv(4096).decode()
                print(f"{url}: {response}")
        except Exception as e:
            raise RuntimeError(f"Error sending URL {url}: {e}") from e

    def run_thread(self):
        try:
            while True:
                url = self.get_next_url()
                if url is None:
                    break

                attempts = 0
                max_retries = 3

                while attempts < max_retries:
                    try:
                        self.send_url(url)
                        break
                    except RuntimeError as e:
                        attempts += 1
                        print(f"Attempt {attempts} failed for {url}: {e}")
                        if attempts == max_retries:
                            print(
                                f"Failed to process {url}"
                                f"after {max_retries} attempts."
                            )
                            break

        except Exception as error_worker:
            print(f"Critical error in worker thread: {error_worker}")

    def start(self):
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.run_thread)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def main():
    parser = argparse.ArgumentParser(description="URL Client")
    parser.add_argument("num_threads", type=int, help="Number of threads")
    parser.add_argument("urls_file", type=str, help="File containing URLs")
    args = parser.parse_args()

    client = URLClient(num_threads=args.num_threads, urls_file=args.urls_file)
    client.start()


if __name__ == "__main__":
    main()
