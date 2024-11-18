# pylint: disable=W0718

import argparse
import asyncio

import aiohttp


class URLFetcher:
    def __init__(self, concurrency: int):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)
        self.total_urls = 0
        self.success_count = 0
        self.error_count = 0

    async def fetch(self, session, url):
        async with self.semaphore:
            print(f"Starting request to {url}")
            try:
                async with session.get(url) as response:
                    data = await response.text()
                    if response.status == 200:
                        self.success_count += 1
                        print(
                            f"Successfully fetched {url} "
                            f"with status {response.status}"
                        )
                    else:
                        self.error_count += 1
                        print(
                            f"Error fetching {url}: status {response.status}"
                        )
                    return data
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None

    async def fetch_in_batches(self, urls):
        async with aiohttp.ClientSession() as session:
            for i in range(0, len(urls), self.concurrency):
                batch = urls[i:i + self.concurrency]
                tasks = [self.fetch(session, url) for url in batch]
                await asyncio.gather(*tasks)

        print("\n=== Summary ===")
        print(f"Total URLs: {self.total_urls}")
        print(f"Successfully fetched: {self.success_count}")
        print(f"Failed: {self.error_count}")


def load_urls_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls


async def main(concurrency, filename):
    urls = load_urls_from_file(filename)
    fetcher = URLFetcher(concurrency)
    await fetcher.fetch_in_batches(urls)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asynchronous URL fetcher")
    parser.add_argument(
        "concurrency", type=int, help="Number of concurrent requests"
    )
    parser.add_argument("filename", type=str, help="File with list of URLs")

    args = parser.parse_args()
    asyncio.run(main(args.concurrency, args.filename))
