# pylint: disable=W0718

import argparse
import asyncio
from collections import Counter

import aiohttp


class URLFetcher:
    def __init__(self, concurrency: int):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)
        self.total_urls = 0
        self.success_count = 0
        self.error_count = 0

    async def fetch(self, url):
        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                print(f"Starting request to {url}")
                self.total_urls += 1
                try:
                    async with session.get(url) as response:
                        data = await response.text()
                        if response.status == 200:
                            self.success_count += 1
                            print(
                                f"Successfully fetched {url} "
                                f"with status {response.status}"
                            )
                            self.print_top_words(url, data)
                        else:
                            self.error_count += 1
                            print(
                                f"Error fetching {url}: "
                                f"status {response.status}"
                            )
                        return None
                except aiohttp.ClientError as e:
                    self.error_count += 1
                    print(f"Network error fetching {url}: {e}")
                except Exception as e:
                    self.error_count += 1
                    print(f"Unexpected error fetching {url}: {e}")

    def print_top_words(self, url, text) -> None:
        words = text.lower().split()
        word_counter = Counter(words)
        print(f"{url}: {dict(word_counter.most_common(5))}")

    async def fetch_all(self, urls):
        queue = asyncio.Queue()
        for url in urls:
            queue.put_nowait(url)

        async def worker():
            while True:
                url = await queue.get()
                try:
                    await self.fetch(url)
                finally:
                    queue.task_done()

        workers = [
            asyncio.create_task(worker()) for _ in range(self.concurrency)
        ]
        await queue.join()

        for worker in workers:
            worker.cancel()

        print("\n=== Summary ===")
        print(f"Total URLs: {self.total_urls}")
        print(f"Successfully fetched: {self.success_count}")
        print(f"Failed: {self.error_count}")


def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()
            if url:
                yield url


async def main(concurrency, filename):
    fetcher = URLFetcher(concurrency)
    urls = load_urls_from_file(filename)
    await fetcher.fetch_all(urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asynchronous URL fetcher")
    parser.add_argument(
        "concurrency", type=int, help="Number of concurrent requests"
    )
    parser.add_argument("filename", type=str, help="File with list of URLs")

    args = parser.parse_args()
    asyncio.run(main(args.concurrency, args.filename))
