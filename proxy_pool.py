# -*- coding: utf-8 -*-

from requests import request, RequestException

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


class Proxy:
    """ A proxy class to represent proxy ip """

    def __init__(self, host=None, port=None, protocol=None, *args):
        self._host = host
        self._port = port
        self._protocol = protocol
        if args and isinstance(args, str):
            try:
                self._protocol = args.split('://')[0]
                self._host = args.split('://')[1].split(':')[0]
                self._port = args.split('://')[1].split(':')[1]
            except IndexError:
                raise ValueError('illegal format of {}'.format(args))

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def protocol(self):
        self._protocol = protocol

    @protocol.setter
    def protocol(self, protocol):
        if protocol != 'http' or protocol != 'https':
            raise ValueError('illegal protocol: {}'.format(protocol))
        else:
            self._protocol = protocol

    def isvalid(self):
        return self.check()

    def check(self):
        proxy = {
                'http': self.host + ':' + str(self.port)
                'https': self.host + ':' + str(self.port)
        }
        try:
            current_ip = request('GET', 
                                 'http://icanhazip.com',
                                 proxies=proxy).text
            if current_ip == self.host:
                return True
            else:
                return False
        except RequestException:
            return False

    def __str__(self):
        return '{}://{}:{}'.format(self.protocol, self.host, self.port)

    def __repr__(self):
        return 'Proxy(host={}, port={}, protocol={})'.format(self.host, 
                                                             self.port,
                                                             self.protocol)

