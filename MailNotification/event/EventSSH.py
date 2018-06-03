#!/usr/bin/bash
# -*- coding:utf-8 -*-
import paramiko
import EventBase
import logging
import sys
sys.path.append('..')
import MailSender
logger = logging.getLogger("EventSSH")
paramiko_logger = logging.getLogger("paramiko.transport")
paramiko_logger.setLevel(logging.ERROR)


class EventSSH(EventBase.EventBase):
    _host = None
    _port = None
    _user = None
    _passwd = None
    _cmd = None
    _ssh = None
    _expect = None

    def __init__(self, cmd, expect, user, passwd, host, port=22, *args, **kwargs):
        super(EventSSH, self).__init__(*args, **kwargs)
        self._cmd = cmd
        self._user = user
        self._passwd = passwd
        self._host = host
        self._port = port
        self._expect = expect

    def pre_step(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=self._host, port=self._port,
                          username=self._user, password=self._passwd)

    def is_event_happened(self):
        _, stdout, stderr = self._ssh.exec_command(self._cmd)

        err = stderr.read()
        if err != "":
            self.errmsg = err
            return True

        result = stdout.read()
        self.ret_msg = result[0:-1]
        logger.debug("result:\n%s\nexpect:\n%s.\n", self.ret_msg, self._expect)
        if self.ret_msg.strip(" ") == self._expect.strip(" "):
            return True
        else:
            return False

    def create_email_msg(self):
        title = "Event[%s] " % self.name + "triggered"
        body = "cmd:\n%(cmd)s\nresult:\n%(result)s\nexpect:\n%(expect)s\n" % \
               {"cmd": self._cmd, "result": self.ret_msg, "expect": self._expect}
        if self.ret_msg == self._expect:
            body += "result is equal to expect.\n"
        else:
            body += "result is not equal to expect.\n"
        self.msg = MailSender.MailSender.create_text_message(title, body)

    def post_step(self):
        self._ssh.close()
