# -*- coding: utf-8 -*-

import unittest
from .downloader import Downloader
from .item import Node


class DownloaderTestCase(unittest.TestCase):

    def setup(self):
        self.node_base = Node(url='www.baidu.com')
        self.dowloader = Downloader(self.node_base)
        self.loop = asyncio.get_event_loop()

    def teardown(self):
        self.loop.run_until_complete(self.downloader.close())

    def test_download(self):
        download_task = asyncio.ensure_future(self.downloader.download(
                                              self.node_base))
        self.loop.run_until-complete(download_task)
        self.asserEquals(download_task.result().status_code, 200)


if __name__ == '__main__':
    unittest.main()
