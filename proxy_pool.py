# -*- coding: utf-8 -*-


class ProxyPool:
    proxy_pool = []

    def __init__(self, logger):
        logger.info('Initalizing proxy pool')
        self.update(protocol)


    def get(self, protocol=None):
        # if the pool consists of less than 5 proxies, update
        if len(self.proxy_pool) < 5:
            self.update(protocol)
        return self.proxy_pool.pop()


    def update(self, protocol):
        pass

    def delete(self, proxy):
        pass
