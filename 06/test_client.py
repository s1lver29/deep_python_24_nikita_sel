# pylint: disable=W0613, C2801

import unittest
from unittest.mock import MagicMock, patch

from .client import URLClient


class TestURLClient(unittest.TestCase):
    def setUp(self):
        print(f"\nStart test {self.id()}")

    def tearDown(self):
        print(f"End test {self.id()}")

    def test_get_next_url(self):
        """
        Тест корректности извлечения следующего URL.
        Проверяет, что URLs извлекаются последовательно и что None возвращается,
        если URL больше нет.
        """
        client = URLClient(3, "urls.txt")
        client.urls = iter(["http://example.com", "http://example.org"])

        url1 = client.get_next_url()
        url2 = client.get_next_url()
        url3 = client.get_next_url()  # Ожидается None, так как больше URL нет.

        self.assertEqual(url1, "http://example.com")
        self.assertEqual(url2, "http://example.org")
        self.assertIsNone(url3)

    @patch("socket.socket")
    def test_send_url_success(self, mock_socket):
        """
        Тест, что URL корректно отправляется на сервер и ответ обрабатывается.
        """
        # Настройка мока сокета
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = b'{"word1": 10, "word2": 5}'

        client = URLClient(3, "urls.txt")
        with patch("builtins.print") as mock_print:
            client.send_url("http://example.com")

            mock_socket_instance.connect.assert_called_once_with(
                ("localhost", 8080)
            )
            mock_socket_instance.sendall.assert_called_once_with(
                b"http://example.com"
            )
            mock_print.assert_called_once_with(
                'http://example.com: {"word1": 10, "word2": 5}'
            )

    @patch("socket.socket")
    def test_send_url_error(self, mock_socket):
        """
        Тест на корректную обработку ошибок при отправке URL.
        Проверяется, что исключение логируется.
        """
        client = URLClient(3, "urls.txt")
        url = "http://example.com"

        # Настройка мока для выброса исключения при попытке подключения
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = RuntimeError(
            "Connection error"
        )

        with patch("builtins.print"):
            with self.assertRaises(RuntimeError) as context:
                client.send_url(url)

        self.assertEqual(
            str(context.exception),
            f"Error sending URL {url}: Connection error",
        )

    @patch("threading.Thread")
    def test_start_threads(self, mock_thread):
        """
        Тест, что создаётся и запускается правильное количество потоков.
        """
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        client = URLClient(3, "urls.txt")
        client.start()

        self.assertEqual(mock_thread.call_count, 3)
        mock_thread_instance.start.assert_called()
        mock_thread_instance.join.assert_called()

    @patch("socket.socket")
    def test_multiple_threads(self, mock_socket):
        """
        Тест, что URL-ы корректно отправляются на
        сервер при использовании разных количеств потоков.
        """
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = b"OK"

        client = URLClient(3, "urls.txt")
        client.get_next_url = MagicMock(
            side_effect=["http://example.com", "http://example.org"]
        )

        client.start()

        expected_calls = [
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.com"),
            unittest.mock.call().__enter__().recv(4096),
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.org"),
            unittest.mock.call().__enter__().recv(4096),
        ]
        mock_socket.assert_has_calls(expected_calls, any_order=True)

        del client

        client_1 = URLClient(10, "urls.txt")
        client_1.get_next_url = MagicMock(
            side_effect=[
                "http://example.com",
                "http://example.org",
                "http://example.ru",
                "http://example.en",
            ]
        )

        client_1.start()

        expected_calls = [
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.com"),
            unittest.mock.call().__enter__().recv(4096),
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.org"),
            unittest.mock.call().__enter__().recv(4096),
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.ru"),
            unittest.mock.call().__enter__().recv(4096),
            unittest.mock.call().__enter__().connect(("localhost", 8080)),
            unittest.mock.call().__enter__().sendall(b"http://example.en"),
            unittest.mock.call().__enter__().recv(4096),
        ]
        mock_socket.assert_has_calls(expected_calls, any_order=True)
