#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp


class Downloader:
    """
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
        async with self.session.request(method=node.get('method'), 
                                        url=node.get('url'), 
                                        data=node.get('data'),
                                        json=node.get('json'), 
                                        proxy=self.proxy,
                                        headers=self.headers) as resp:
            return await resp

    async def close(self):
        await self.session.close()
