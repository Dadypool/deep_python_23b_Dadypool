"Tests for client.py"

import unittest
import queue
from unittest.mock import patch, call
from io import StringIO
from collections import Counter
import json

import server


class TestClient(unittest.TestCase):
    "Class with Tests for client"

    @patch("queue.Queue", autospec=True)
    @patch("threading.Lock", autospec=True)
    @patch("threading.Thread", autospec=True)
    @patch("socket.socket", autospec=True)
    def test_main_thread(self, mock_socket, mock_thread, mock_lock, mock_queue):
        "Tests master thread for starting worker threads and putting sockets in queue"

        num_workers = 3
        k = 3

        accept_immitation = [("conn2", "addr2"), ("conn1", "addr1")]
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.accept.side_effect = (
            lambda *_, **__: accept_immitation.pop()
            if accept_immitation
            else (None, None)
        )

        mock_thread_instance = mock_thread.return_value
        mock_lock_instance = mock_lock.return_value
        mock_queue_instance = mock_queue.return_value

        expected_thread_calls = [
            call(
                target=server.worker,
                name=f"Worker-{i}",
                args=(k, mock_queue_instance, mock_lock_instance, [0]),
            )
            for i in range(num_workers)
        ]

        expected_queue_calls = [call((c, a)) for c, a in reversed(accept_immitation)]

        with patch("sys.stdout", new=StringIO()) as mock_out:
            server.master("127.0.0.1", 5000, num_workers, k)

            self.assertEqual(
                f"Server listening on 127.0.0.1:5000 with {num_workers} workers\n"
                + "Accepted connection from addr1\nAccepted connection from addr2\n",
                mock_out.getvalue(),
            )

        mock_socket_instance.bind.assert_called_once_with(("127.0.0.1", 5000))
        mock_socket_instance.listen.assert_called_once()
        mock_socket_instance.settimeout.assert_called_once_with(10)
        self.assertEqual(mock_socket_instance.accept.call_count, 3)

        self.assertEqual(mock_thread.call_count, num_workers)
        self.assertEqual(mock_thread.call_args_list, expected_thread_calls)
        self.assertEqual(mock_thread_instance.start.call_count, num_workers)
        mock_thread_instance.assert_not_called()

        self.assertEqual(mock_queue_instance.put.call_count, 2)
        self.assertEqual(mock_queue_instance.put.call_args_list, expected_queue_calls)

    @patch("queue.Queue", autospec=True)
    @patch("threading.Lock", autospec=True)
    @patch("server.get_top_k", autospec=True)
    @patch("socket.socket", autospec=True)
    def test_worker_thread(self, mock_socket, mock_func, mock_lock, mock_queue):
        "Tests worker thread for recv requests and send response"

        k = 3

        recv_immitation = [
            b"",
            "response2".encode("utf-8"),
            b"",
            "response1".encode("utf-8"),
        ]
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.side_effect = lambda *_, **__: recv_immitation.pop()

        queue_immitation = [(mock_socket_instance, None), (mock_socket_instance, None)]

        def side_eff_get(*_, **__):
            "Side effect function for queue.get"

            if queue_immitation:
                return queue_immitation.pop()
            raise queue.Empty

        mock_queue_instance = mock_queue.return_value
        mock_queue_instance.get.side_effect = side_eff_get

        mock_lock_instance = mock_lock.return_value
        mock_func.return_value = "resp"

        with patch("sys.stdout", new=StringIO()) as mock_out:
            server.worker(k, mock_queue_instance, mock_lock_instance, [0])

            self.assertEqual(
                "Total requests handled: 1\nTotal requests handled: 2\n",
                mock_out.getvalue(),
            )

        self.assertEqual(mock_socket_instance.recv.call_count, 4)
        self.assertEqual(mock_socket_instance.send.call_count, 2)
        mock_socket_instance.send.assert_called_with("resp")

        self.assertEqual(mock_queue_instance.get.call_count, 3)
        mock_queue_instance.get.assert_called_with(timeout=10)

        self.assertEqual(mock_lock_instance.__enter__.call_count, 2)

        self.assertEqual(mock_func.call_count, 2)

    @patch("server.BeautifulSoup", autospec=True)
    @patch("re.findall", autospec=True)
    @patch("server.urlopen", autospec=True)
    def test_get_top_k(self, _, mock_re_findall, __):
        "Tests get_top_k function"

        k = 2

        words = ["Words", "words", "Words", "words", "nums"]
        mock_re_findall.return_value = words
        excepted_result = json.dumps(dict(Counter(words).most_common(k))).encode(
            "utf-8"
        )
        self.assertEqual(server.get_top_k("url", k), excepted_result)
