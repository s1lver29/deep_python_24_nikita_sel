# pylint: disable=E0401, C0413

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

import aiohttp
from aioresponses import aioresponses

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
)

from fetcher import URLFetcher, load_urls_from_file, main  # noqa: E402


class TestURLFetcher(unittest.IsolatedAsyncioTestCase):

    async def test_fetch_success(self):
        """
        Тест для проверки успешного выполнения запроса.
        """
        with aioresponses() as mocked:
            mocked.get("http://example.com", status=200, body="Success")

            fetcher = URLFetcher(concurrency=2)
            await fetcher.fetch("http://example.com")

            self.assertEqual(fetcher.success_count, 1)
            self.assertEqual(fetcher.error_count, 0)
            self.assertEqual(fetcher.total_urls, 1)
            mocked.assert_called_once_with("http://example.com", method="GET")

    async def test_fetch_failure(self):
        """
        Тест для проверки неуспешного выполнения запроса (статус 404).
        """
        with aioresponses() as mocked:
            mocked.get("http://example.com", status=404, body="Not Found")

            fetcher = URLFetcher(concurrency=2)
            await fetcher.fetch("http://example.com")

            self.assertEqual(fetcher.success_count, 0)
            self.assertEqual(fetcher.error_count, 1)
            self.assertEqual(fetcher.total_urls, 1)
            mocked.assert_called_once_with("http://example.com", method="GET")

    async def test_fetch_exception(self):
        """
        Тест для проверки обработки исключения при выполнении запроса.
        """
        with aioresponses() as mocked:
            mocked.get(
                "http://example.com",
                exception=aiohttp.ClientError("Network error"),
            )

            fetcher = URLFetcher(concurrency=2)
            await fetcher.fetch("http://example.com")

            self.assertEqual(fetcher.success_count, 0)
            self.assertEqual(fetcher.error_count, 1)
            self.assertEqual(fetcher.total_urls, 1)
            mocked.assert_called_once_with("http://example.com", method="GET")

    async def test_fetch_in_batches(self):
        """
        Тест для проверки метода fetch_all с несколькими URL-адресами.
        """
        with aioresponses() as mocked:
            # Mocking 3 successful responses
            mocked.get("http://example.com/1", status=200, body="Success1")
            mocked.get("http://example.com/2", status=200, body="Success2")
            mocked.get("http://example.com/3", status=200, body="Success3")

            fetcher = URLFetcher(concurrency=2)
            urls = [
                "http://example.com/1",
                "http://example.com/2",
                "http://example.com/3",
            ]
            await fetcher.fetch_all(urls)

            self.assertEqual(fetcher.success_count, 3)
            self.assertEqual(fetcher.error_count, 0)
            self.assertEqual(fetcher.total_urls, 3)
            mocked.assert_any_call("http://example.com/1", method="GET")
            mocked.assert_any_call("http://example.com/2", method="GET")
            mocked.assert_any_call("http://example.com/3", method="GET")

    async def test_main(self):
        """
        Тест для проверки основной функции main.
        """
        file_path = "dummy_file.txt"

        base_path = Path(__file__).parent
        file_path = Path(base_path / file_path)
        with (
            patch("fetcher.load_urls_from_file") as mock_load_urls,
            patch("fetcher.URLFetcher.fetch_all") as mock_fetch_all,
        ):
            mock_load_urls.return_value = [
                "http://example.com/1",
                "http://example.com/2",
            ]
            await main(2, file_path)

            mock_load_urls.assert_called_once_with(file_path)
            mock_fetch_all.assert_called_once()

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="http://example.com/1\nhttp://example.com/2\n",
    )
    def test_load_urls_from_file(self, mock_file):
        """
        Тест для проверки загрузки URL-адресов из файла.
        """
        file_path = "dummy_file.txt"

        base_path = Path(__file__).parent
        file_path = Path(base_path / file_path)

        urls = list(load_urls_from_file(file_path))
        self.assertEqual(
            urls, ["http://example.com/1", "http://example.com/2"]
        )
        mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")

    async def test_fetch_all_with_different_concurrency(self):
        """
        Тест для проверки метода fetch_all с
        разным количеством воркеров/ссылок.
        """
        max_urls = 50

        for concurrency in [1, 3, 7, 10]:
            with aioresponses() as mocked:
                for count_urls in range(1, max_urls, 10):
                    for i in range(count_urls):
                        mocked.get(
                            f"http://example.com/{i}",
                            status=200,
                            body=f"Success{i}",
                        )

                    fetcher = URLFetcher(concurrency=concurrency)
                    urls = [
                        f"http://example.com/{i}" for i in range(count_urls)
                    ]
                    await fetcher.fetch_all(urls)

                    self.assertEqual(fetcher.success_count, count_urls)
                    self.assertEqual(fetcher.error_count, 0)
                    self.assertEqual(fetcher.total_urls, count_urls)
                    for i in range(count_urls):
                        mocked.assert_any_call(
                            f"http://example.com/{i}", method="GET"
                        )

                    del fetcher

    async def test_fetch_all_with_mixed_responses(self):
        """
        Тест для проверки метода fetch_all со
        смешанными ответами (успешными и неуспешными).
        """
        with aioresponses() as mocked:
            # Mocking mixed responses
            mocked.get("http://example.com/1", status=200, body="Success1")
            mocked.get("http://example.com/2", status=404, body="Not Found")
            mocked.get("http://example.com/3", status=200, body="Success3")
            mocked.get("http://example.com/4", status=500, body="Server Error")
            mocked.get("http://example.com/5", status=200, body="Success5")

            fetcher = URLFetcher(concurrency=2)
            urls = [f"http://example.com/{i}" for i in range(1, 6)]
            await fetcher.fetch_all(urls)

            self.assertEqual(fetcher.success_count, 3)
            self.assertEqual(fetcher.error_count, 2)
            self.assertEqual(fetcher.total_urls, 5)
            for i in range(1, 6):
                mocked.assert_any_call(f"http://example.com/{i}", method="GET")
