#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp


class Downloader:
    """
    Downloader creates a aiohttp client session and takes an event loop. 
    To download content, simply pass a node of whose data needs to be downloaded    to the download method.
    """
    def __init__(self, loop):
        self._timeout = 0

        self.session = loop.run_until_complete(self._create_session())

        self.proxy = ''

        self.headers = {}
        self.proxy_pool = None

    async def _create_session(self):
        session = aiohttp.ClientSession()
        return session

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if isinstance(value, int):
            self._timeout = value
        else:
            raise ValueError('timeout must be a integer.')

    def set_proxy(self):
        self.proxy = self.proxy_pool.get()

    async def download(self, node):
        """
        Downloading a node and returing the http response

        Params:
            node: a node object which consists of the key information of the
                  data we need to download

        Returns:
            response: an http response

        """
        async with self.session.request(method=node.get('method'), 
                                        url=node.get('url'), 
                                        data=node.get('data'),
                                        json=node.get('json'), 
                                        proxy=self.proxy,
                                        headers=self.headers) as resp:
            return await resp

    async def close(self):
        """close the download session and it must be done in an event loop"""
        await self.session.close()
