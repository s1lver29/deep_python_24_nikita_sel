import unittest
from unittest.mock import mock_open, patch

import aiohttp
from aioresponses import aioresponses

from .fetcher import URLFetcher, load_urls_from_file


class TestURLFetcher(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_success(self):
        with aioresponses() as mocked:
            mocked.get("http://example.com", status=200, body="Success")

            fetcher = URLFetcher(concurrency=2)
            async with aiohttp.ClientSession() as session:
                result = await fetcher.fetch(session, "http://example.com")

            self.assertEqual(result, "Success")
            self.assertEqual(fetcher.success_count, 1)
            self.assertEqual(fetcher.error_count, 0)
            self.assertEqual(fetcher.total_urls, 1)

    async def test_fetch_failure(self):
        with aioresponses() as mocked:
            mocked.get("http://example.com", status=404, body="Not Found")

            fetcher = URLFetcher(concurrency=2)
            async with aiohttp.ClientSession() as session:
                result = await fetcher.fetch(session, "http://example.com")

            self.assertEqual(result, "Not Found")
            self.assertEqual(fetcher.success_count, 0)
            self.assertEqual(fetcher.error_count, 1)
            self.assertEqual(fetcher.total_urls, 1)

    async def test_fetch_exception(self):
        with aioresponses() as mocked:
            mocked.get(
                "http://example.com",
                exception=aiohttp.ClientError("Network error"),
            )

            fetcher = URLFetcher(concurrency=2)
            async with aiohttp.ClientSession() as session:
                result = await fetcher.fetch(session, "http://example.com")

            self.assertIsNone(result)
            self.assertEqual(fetcher.success_count, 0)
            self.assertEqual(fetcher.error_count, 1)
            self.assertEqual(fetcher.total_urls, 1)

    async def test_fetch_in_batches(self):
        with aioresponses() as mocked:
            # Mocking 3 successful responses
            mocked.get("http://example.com/1", status=200, body="Success")
            mocked.get("http://example.com/2", status=200, body="Success")
            mocked.get("http://example.com/3", status=200, body="Success")

            fetcher = URLFetcher(concurrency=2)
            urls = [
                "http://example.com/1",
                "http://example.com/2",
                "http://example.com/3",
            ]
            await fetcher.fetch_in_batches(urls)

            self.assertEqual(fetcher.success_count, 3)
            self.assertEqual(fetcher.error_count, 0)
            self.assertEqual(fetcher.total_urls, 3)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="http://example.com/1\nhttp://example.com/2\n",
    )
    def test_load_urls_from_file(self, mock_file):
        urls = load_urls_from_file("dummy_file.txt")
        self.assertEqual(
            urls, ["http://example.com/1", "http://example.com/2"]
        )
        mock_file.assert_called_once_with(
            "dummy_file.txt", "r", encoding="utf-8"
        )
