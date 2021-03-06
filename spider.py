#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import asyncio
import queue
import logging
from logging.handlers import QueueHandler, QueueListener

from downloader import Downloader
from proxy_pool import ProxyPool
from mailer import Mailer
from utils import load_object
import conf

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


# TODO(@JoJo): test
class Spider:
    """
    A spider class for crawling jobs, costume the settings in settings.py
    """

    name = ''
    enable_proxy = False

    def __init__(self):
        self.loop = asyncio.get_event_loop()

        self._max_retry = conf.SPIDER['max_retry']

        self.nodes = asyncio.Queue(-1) # no limit on size
        self.failed_nodes = asyncio.Queue(-1)

        self.log_queue = queue.Queue(-1)
        self.log_queue_listener, self.logger = self._get_logger()

        self.mailer = Mailer(conf.EMAIL['host'],
                             conf.EMAIL['port'],
                             conf.EMAIL['use_ssl'],
                             conf.EMAIL['usr'],
                             conf.EMAIL['pwd'],
                             conf.SPIDER['timeout'])
        self.mailer.envelope['Subject'] = conf.EMAIL['Subject']
        self.mailer.envelope['To'] = conf.EMAIL['To']
        self.mailer.envelope['From'] = conf.EMAIL['From']

        self.downloader = Downloader(self.loop)
        self.downloader.timeout = conf.SPIDER['timeout']
        if self.enable_proxy:
            self.downloader.proxy_pool = ProxyPool()
            self.downloader.set_proxy()

        self.pipelines = []

        for pipeline_path in sorted(conf.PIPELINES):
            pipeline_cls = load_object(pipeline_path)
            self.pipelines.append(pipeline_cls())

        self._concurrency = 1

    @property
    def max_retry(self):
        return self._max_retry

    @max_retry.setter
    def max_retry(self, value):
        if isinstance(value, int):
            if value < 0:
                raise ValueError('max retry must be posstive.')
            else:
                self._max_retry = value
        else:
            raise ValueError('max retry must be an integer.')

    @property
    def concurrency(self):
        return self._concurrency

    @concurrency.setter
    def concrrency(self, value):
        if isinstance(value, int):
            if value < 1:
                raise ValueError('concurrency should at least be 1.')
            else:
                self._concurrency = value
        else:
            raise ValueError('concurrency must be an integer.')

    def add_node(self, node):
        self.nodes.put_nowait(node)

    def parse(self, response=None):
        """
        Parsing the response content and returning scrapped data.

        Args:
            response: the response object passed from the downloader
        
        Returns:
            list: a list of items of scrapped data
        """
        return list()

    async def worker(self):
        """
        A worker coroutine that fetch a node from node_queue each time and
        process it. If the node is failed to be processed, worker will put it
        back to the queue for retrying or put it in the failed_node_queue if
        the retried times exceed the set retry time.
        """
        while True:
            node = await self.nodes.get()
            if node['retry'] > self._max_retry:
                self.logger.info('Node %s failed: Exceeded %s retries',
                                 node['id'], self._max_retry)
                self.failed_nodes.put(node)
            else:
                try:
                    response = await self.downloader.download(node)
                    self.logger.debug('Node %s response content: %s',
                                      node['id'], response)
                    items = self.parse(response)
                    for _ in range(len(items)):
                        item = items.pop()
                        for pipeline in self.pipelines:
                            item = pipeline.process_item(item)
                        items.append(item)
                    self.logger.info('Node %s succeeded, retried %s times',
                                     node['id'], node['retry'])
                except Exception as exception:
                    if exception in conf.EXCEPTIONS:
                        self.logger.info('Node %s failed: %s',
                                         node['id'], type(exception).__name__)
                    else:
                        self.logger.exception('Node %s failed:', node['id'])
                    node['retry'] += 1
                    self.nodes.put(node)

            self.nodes.task_done()

    async def main(self):
        """ Pack workers of set concurreny """
        workers = []
        for _ in range(self._concurrency):
            # In Python 3.7+
            # task = asyncio.create_task(self.worker())
            worker = asyncio.ensure_future(self.worker())
            workers.append(worker)

        await self.nodes.join()

        # cancel all workers when the job is done
        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)

    def launch(self):
        for pipeline in self.pipelines:
            pipeline.open_spider()
        self.log_queue_listener.start()
        self.logger.info('%s spider launched', self.name)
        try:
            asyncio.run(self.main())
        except AttributeError:
            self.loop.run_until_complete(self.main())
        self.logger.info('%s spider finished tasks', self.name)

    def close(self):
        self.logger.info('%s spider closing...', self.name)
        # close downloader session
        session_closed = self.loop.create_task(self.downloader.close())
        self.loop.run_until_complete(session_closed)
        self.loop.close()

        for pipeline in self.pipelines:
            pipeline.close_spider()

        self.log_queue_listener.stop()

        self.mailer.close()
        self.logger.info('%s spider closed', self.name)

    def _get_logger(self):
        """
        log_queue_listener is passed a queue and some handlers, and it fires up
        an internal thread which listens to its queue for LogRecords sent from
        QueueHandlers.

        For more information, see
        https://docs.python.org/3/howto/logging-cookbook.html
        -'Dealing with handlers that block'
        """
        log_queue_handler = QueueHandler(self.log_queue)
        logger = logging.getLogger(self.name)
        logger.setLevel(conf.LOG['log_level'])
        logger.addHandler(log_queue_handler)

        fmt = "%(asctime)-15s %(levelname)s %(lineno)d %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        log_path = conf.LOG['log_path']
        fh = logging.FileHandler(log_path)
        fh.setFormatter(formatter)

        log_queue_listener = QueueListener(self.log_queue, fh)

        return log_queue_listener, logger


if __name__ == '__main__':
    from item import Node
    n1 = Node()
    n1['id'] = 'baidu'
    n1['url'] = 'https://www.baidu.com'
    n1['method'] = 'GET'
    s = Spider()
    s.add_node(n1)
    s.launch()
    s.close()
