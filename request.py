# -*- coding: utf-8 -*-
""" A Request class represents each request for spider to crawl."""


class Request:

    def __init__(self, url):
        self.url = url

        self.request_body = ''
        self.priority = 0
        self.charset = ''
        self.protocol = 'http'

    @staticmethod
    def json(json):
        pass

