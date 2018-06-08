#!/usr/bin/bash
# -*- coding:utf-8 -*-
import paramiko
import EventBase
import sys

sys.path.append('..')
import MailSender
from log import logger


class EventSSH(EventBase.EventBase):
    """
    EventSSH Event can connect to a host via ssh protocol, execute cmd,
    and compare result with expect.
    """
    def __init__(self, cmd, expect, user, passwd, host, port=22, *args, **kwargs):
        super(EventSSH, self).__init__(*args, **kwargs)
        self._cmd = cmd
        self._user = user
        self._passwd = passwd
        self._host = host
        self._port = port
        self._expect = expect
        self._ssh = None
        self.name = "Name(%s)--Cmd(%s)--Host(%s)" % (self.name, self._cmd, self._host)
        self._extra_cmd = kwargs.get("extra_cmd", None)

    def pre_step(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=self._host, port=self._port,
                          username=self._user, password=self._passwd)

    def is_event_happened(self):
        _, stdout, stderr = self._ssh.exec_command(self._cmd)

        err = stderr.read()
        if err != "":
            self.err_msg = err[0:-1]
            return True

        result = stdout.read()
        self.ret_msg = result[0:-1]
        logger.debug("result:\n%s\nexpect:\n%s.\n", self.ret_msg, self._expect)
        if self.ret_msg.strip(" ") == self._expect.strip(" "):
            return True
        else:
            return False

    def _create_attachment_msg(self):
        if self._extra_cmd is None:
            return

        for cmd in self._extra_cmd:
            msg_str = ""
            _, stdout, stderr = self._ssh.exec_command(cmd)
            ret = stdout.read()
            if ret != "":
                msg_str += "stdout:\n" + ret
            ret = stderr.read()
            if ret != "":
                msg_str += "stderr:\n" + ret
            if msg_str != "":
                msg = MailSender.MailSender.create_text_message(cmd, msg_str)
                self.attachment.append(msg)

    def create_email_msg(self):
        body = "cmd:\n%s\n" % self._cmd
        body += "host:\n%s\n" % self._host
        body += "user:\n%s\n" % self._user
        title = "Event[%s]" % self.name
        if self.err_msg == "":
            title += " triggered"
            body += "result:\n%(result)s\nexpect:\n%(expect)s\n" % \
                   {"result": self.ret_msg, "expect": self._expect}
            if self.ret_msg == self._expect:
                body += "result is equal to expect.\n"
            else:
                body += "result is not equal to expect.\n"
        else:
            title += " Error Occur"
            body += "error occur:\n%(err)s\n" % {"err": self.err_msg}
        self.msg = MailSender.MailSender.create_text_message(title, body)
        self._create_attachment_msg()

    def post_step(self):
        self._ssh.close()
