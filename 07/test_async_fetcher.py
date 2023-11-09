"Homework 7. Tests for async URL Fetcher"

import unittest
from unittest.mock import patch, call, AsyncMock

import warnings

import async_fetcher

warnings.filterwarnings("ignore")


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    "Class with Tests"

    @patch("asyncio.create_task", autospec=True)
    @patch("asyncio.Queue", autospec=True)
    @patch("async_fetcher.fetch_worker", spec=True)
    @patch("async_fetcher.url_producer", spec=True)
    async def test_main(self, mock_producer, mock_worker, mock_que, mock_create_task):
        "Tests main coroutine"

        mock_que.return_vlaue = AsyncMock()
        mock_que_instance = mock_que.return_value

        mock_task = mock_create_task.return_value

        await async_fetcher.main(5, "test.txt")

        mock_producer.assert_awaited_once_with(mock_que_instance, "test.txt")

        self.assertEqual(mock_worker.call_count, 5)
        mock_worker.assert_called_with(mock_que_instance)

        self.assertEqual(mock_create_task.call_count, 5)

        self.assertEqual(mock_task.cancel.call_count, 5)

    @patch("asyncio.Queue", autospec=True)
    async def test_producer(self, mock_que):
        "Tests producer coroutine"

        mock_que.return_vlaue = AsyncMock()
        mock_que_instance = mock_que.return_value

        mock_file = AsyncMock()
        mock_file.__aenter__.return_value = mock_file
        mock_file.__aiter__.return_value = ["Hello", "world"]

        with patch("aiofiles.open", autospec=True, return_value=mock_file) as mock_open:
            await async_fetcher.url_producer(mock_que_instance, "test.txt")

            mock_open.assert_called_once_with("test.txt", "r")

            mock_file.__aenter__.assert_awaited_once()
            mock_file.__aiter__.assert_called_once()

            mock_que_instance.put.assert_awaited()
            self.assertEqual(mock_que_instance.put.call_count, 2)
            self.assertEqual(
                mock_que_instance.put.call_args_list,
                [call.put("Hello"), call.put("world")],
            )
