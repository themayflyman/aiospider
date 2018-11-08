# -*- coding: utf-8 -*-

import smtplib
from email.message import EmailMessage


class Mailer:
    """
    A mailer merely for sending text email
    """
    def __init__(self, host='localhost', port=0, use_ssl=False, usr=None, 
                 pwd=None, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._usr = usr
        self._pwd = pwd
        self.envelope = EmailMessage()

        if use_ssl:
            self.server = smtplib.SMTP_SSL(self.host, self.port, 
                                           timeout=self.timeout)
        else:
            self.server = smtplib.SMTP(self.host, self.port, 
                                           timeout=self.timeout)

    def login(self, usr, pwd):
        self._usr = usr
        self._pwd = pwd

    def send(self, msg, to_addr=None, from_addr=None, subject=None):
        if self._usr and self._pwd:
            self.server.login(self._usr, self._pwd)
        if to_addr and from_addr and subject:
            self.envelope['Subject'] = subject
            self.envelope['From'] = from_addr
            self.envelope['To'] = to_addr
        self.envelope.set_content(msg)

        s.send_message(self.envelope)

    def close(self):
        self.server.quit()
