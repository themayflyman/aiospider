# -*- coding: utf-8 -*-

import unittest
from .mailer import Mailer


class MailerTestCase(unittest.TestCase):
    """Tests for 'mailer.py'"""

    def setup(self):
        # connect smtp server
        self.m = Mailer(host='',
                        port=0,
                        use_ssl=True,
                        usr='',
                        pwd='',
                        timeout=5)

    def teardown(self):
        # disconnect smtp server
        self.m.close()

    def test_send_email(self):
        self.send_email(to_addr='',
                        from_addr='',
                        subject='',
                        msg='')

