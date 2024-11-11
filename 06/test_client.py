# pylint: disable=W0613

import unittest
from unittest.mock import patch, MagicMock
from .client import URLClient


class TestURLClient(unittest.TestCase):
    def test_get_next_url(self):
        """
        Тест корректности извлечения следующего URL
        """
        client = URLClient(3, "urls.txt")
        client.urls = ["http://example.com", "http://example.org"]
        client.url_index = 0

        url1 = client.get_next_url()
        url2 = client.get_next_url()
        url3 = (
            client.get_next_url()
        )  # Должен вернуть None, так как больше нет URL

        self.assertEqual(url1, "http://example.com")
        self.assertEqual(url2, "http://example.org")
        self.assertIsNone(url3)

    @patch("socket.socket")
    def test_send_url_success(self, mock_socket):
        """
        Тест, что URL корректно отправляется на сервер
        """
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

    @patch("socket.socket", side_effect=Exception("Connection error"))
    def test_send_url_error(self, mock_socket):
        """
        Тест на обработку ошибок при отправке URL
        """
        client = URLClient(3, "urls.txt")
        with patch("builtins.print") as mock_print:
            client.send_url("http://example.com")
            mock_print.assert_called_once_with(
                "Error sending URL http://example.com: Connection error"
            )

    @patch("threading.Thread")
    def test_start_threads(self, mock_thread):
        """
        Тест, что создаются и запускаются нужное количество потоков
        """
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        client = URLClient(3, "urls.txt")
        client.start()

        self.assertEqual(mock_thread.call_count, 3)
        mock_thread_instance.start.assert_called()
        mock_thread_instance.join.assert_called()
