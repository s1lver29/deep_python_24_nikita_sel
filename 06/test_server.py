# pylint: disable=W0613

import unittest
from unittest.mock import patch, MagicMock
from .server import Worker, MasterServer


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(
            queue=[], lock=MagicMock(), top_k=5, master=MagicMock()
        )

    def test_is_valid_url(self):
        """
        Тест на проверку метода is_valid_url
        Проверяем, что правильный URL проходит проверку
        """
        valid_url = "http://example.com"
        invalid_url = "example.com"
        self.assertTrue(self.worker.is_valid_url(valid_url))
        self.assertFalse(self.worker.is_valid_url(invalid_url))

    @patch("urllib.request.urlopen")
    def test_process_url(self, mock_urlopen):
        """
        Тест, что ответ корректный ответ сервера обрабатывает корректно
        """
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = (
            b"word1 word2 word1 word3 word2 word2 word4"
        )
        mock_urlopen.side_effect = lambda *args, **kwargs: mock_response

        result = self.worker.process_url("http://example.com")
        expected_result = {"word2": 3, "word1": 2, "word3": 1, "word4": 1}
        self.assertEqual(result, expected_result)

    @patch(
        "urllib.request.urlopen", side_effect=Exception("Error fetching URL")
    )
    def test_process_url_with_error(self, mock_urlopen):
        """
        Тест на некорректную ссылку
        """
        result = self.worker.process_url("http://invalid-url.com")
        self.assertEqual(result, {})


class TestMasterServer(unittest.TestCase):
    def setUp(self):
        self.server = MasterServer(
            host="localhost", port=8080, num_workers=3, top_k=5
        )

    def test_initialization(self):
        """
        Тест, что сервер инициализируется с правильными параметрами
        """
        self.assertEqual(self.server.num_workers, 3)
        self.assertEqual(self.server.top_k, 5)
        self.assertEqual(self.server.total_processed, 0)

    def test_update_statistics(self):
        """
        Тест, что счетчк обновляет количество обработанных URL
        """
        self.server.update_statistics()
        self.assertEqual(self.server.total_processed, 1)
