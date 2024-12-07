# pylint: disable=W0613

import json
import socket
import threading
import unittest
from queue import Queue
from time import sleep
from unittest.mock import MagicMock, patch

from .server import MasterServer, Worker


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.master_mock = MagicMock()
        self.worker = Worker(
            queue=Queue(), top_k=5, master=self.master_mock, worker_id=0
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
        mock_response.read.return_value = (
            b"word1 word2 word1 word3 word2 word2 word4"
        )
        mock_urlopen.return_value.__enter__.return_value = mock_response

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
            host="localhost", port=8080, num_workers=2, top_k=5
        )
        self.server_thread = threading.Thread(
            target=self.server.start_server, daemon=True
        )
        self.server_thread.start()
        sleep(1)

    def tearDown(self):
        self.server.shutdown_flag.set()
        self.server_thread.join(timeout=2)

    def test_valid_url_processing(self):
        """Тест, что сервер корректно обрабатывает валидный URL
        и возвращает непустой словарь с топ-словами."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8080))

        url = "http://example.com"
        client_socket.sendall(url.encode())

        response = client_socket.recv(4096).decode()
        response_data = json.loads(response)

        self.assertIsInstance(response_data, dict)
        self.assertGreater(len(response_data), 0)

        client_socket.close()

    def test_invalid_url_processing(self):
        """Тест, что сервер возвращает сообщение об ошибке
        при обработке невалидного URL."""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 8080))

        url = "invalid_url"
        client_socket.sendall(url.encode())

        response = client_socket.recv(4096).decode()

        self.assertEqual(response, "Invalid URL")

        client_socket.close()

    def test_multiple_requests(self):
        """Тест, что сервер корректно обрабатывает несколько
        запросов, включая валидные и невалидные URL."""
        urls = ["http://example.com", "http://example.org", "invalid_url"]
        responses = []

        for url in urls:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("localhost", 8080))
            client_socket.sendall(url.encode())
            response = client_socket.recv(4096).decode()
            responses.append(response)
            client_socket.close()

        self.assertEqual(len(responses), 3)
        self.assertEqual(responses[2], "Invalid URL")

        valid_responses = [json.loads(resp) for resp in responses[:2]]
        for resp in valid_responses:
            self.assertIsInstance(resp, dict)
            self.assertGreater(len(resp), 0)
