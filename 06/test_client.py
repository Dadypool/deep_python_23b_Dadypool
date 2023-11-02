"Tests for client.py"

import unittest
from unittest.mock import patch, mock_open, call
from io import StringIO

import client


class TestClient(unittest.TestCase):
    "Class with Tests for client"

    @patch("queue.Queue", autospec=True)
    @patch("threading.Thread", autospec=True)
    def test_threads_inits(self, mock_thread, mock_que):
        "Tests threads calling and calls args"

        num_threads = 3
        filename = "urls.txt"
        server_address = "127.0.0.1"
        server_port = 5000

        mock_thread_instance = mock_thread.return_value
        mock_queue_instance = mock_que.return_value

        expected_calls = [
            call(
                target=client.send_request,
                name=f"Client-{i}",
                args=(mock_queue_instance, server_address, server_port),
            )
            for i in range(num_threads)
        ]

        with patch("builtins.open"):
            client.main(num_threads, filename, server_address, server_port)

        self.assertEqual(mock_thread.call_count, num_threads)
        self.assertEqual(mock_thread.call_args_list, expected_calls)
        self.assertEqual(mock_thread_instance.start.call_count, num_threads)
        mock_thread_instance.assert_not_called()

    @patch("builtins.open", new_callable=mock_open, read_data="url1\nurl2\nurl3")
    @patch("queue.Queue", autospec=True)
    def test_file_and_queue(self, mock_queue, mock_file):
        "Tests file and queue managing"

        num_threads = 3
        filename = "urls.txt"
        server_address = "127.0.0.1"
        server_port = 5000

        mock_queue_instance = mock_queue.return_value
        expected_calls = [call("url1"), call("url2"), call("url3")]

        with patch("threading.Thread", autospec=True):
            client.main(num_threads, filename, server_address, server_port)

        mock_file.assert_called_once_with(filename, "r", encoding="UTF-8")

        mock_queue.assert_called_once()
        mock_queue_instance.assert_not_called()
        self.assertEqual(mock_queue_instance.put.call_count, 3)
        self.assertEqual(mock_queue_instance.put.call_args_list, expected_calls)

    @patch("queue.Queue", autospec=True)
    @patch("socket.socket", autospec=True)
    def test_client_thread(self, mock_socket, mock_queue):
        "Tests client thread"

        server_address = "127.0.0.1"
        server_port = 5000

        response_immitation = ["resp2".encode("utf-8"), "resp1".encode("utf-8")]
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.side_effect = (
            lambda *_, **__: response_immitation.pop()
        )

        queue_immitation = ["url2", "url1"]
        mock_queue_instance = mock_queue.return_value
        mock_queue_instance.get.side_effect = lambda *_, **__: queue_immitation.pop()
        mock_queue_instance.empty.side_effect = lambda *_, **__: not queue_immitation

        with patch("sys.stdout", new=StringIO()) as mock_out:
            client.send_request(mock_queue_instance, server_address, server_port)
            self.assertEqual(
                "MainThread url1: resp1\nMainThread url2: resp2\n", mock_out.getvalue()
            )

        mock_socket.assert_called_once()
        mock_socket_instance.connect.assert_called_once_with(
            (server_address, server_port)
        )
        self.assertEqual(mock_socket_instance.recv.call_count, 2)
        mock_socket_instance.recv.assert_called_with(1024)
        self.assertEqual(mock_queue_instance.empty.call_count, 3)
        self.assertEqual(mock_queue_instance.get.call_count, 2)
        mock_queue_instance.get.assert_called_with(timeout=2)
