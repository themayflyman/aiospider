# -*- coding: utf-8 -*-

from requests import request, RequestException

class ProxyPool:

    def __init__(self):
        self.proxy_pool = []
        self.update()


    def get(self):
        # if the pool consists of less than 5 proxies, update
        if len(self.proxy_pool) < 5:
            self.update()
        # proxy = self.proxy_pool.pop()
        # return proxy


    def update(self):
        # put Proxy() in proxy_pool
        pass

    def delete(self, proxy):
        pass


class Proxy:
    """ A proxy class to represent proxy ip """

    def __init__(self, string=None, **kw):
        if string:
            try:
                self._protocol = string.split('://')[0]
                self._host = string.split('://')[1].split(':')[0]
                self._port = string.split('://')[1].split(':')[1]
            except IndexError:
                raise ValueError('illegal string: {}'.format(string))
        elif kw:
            self._protocol = kw['protocol']
            self._host = kw['host']
            self._port = kw['port']
        else:
            self._protocol = None
            self._host = None
            self._port = None

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
        return self._protocol

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
                'http': self.host + ':' + str(self.port),
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


        
if __name__ == '__main__':
    p = Proxy(protocol='https',host='127.0.0.1',port='1080')
    p1 = Proxy('https://127.0.0.1:1080')
    print(str(p), str(p1))
