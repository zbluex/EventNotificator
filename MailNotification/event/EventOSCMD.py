#!/usr/bin/bash
# -*- coding:utf-8 -*-
import EventBase
import os, sys

sys.path.append('..')
import MailSender
from log import logger


class EventOSCmd(EventBase.EventBase):
    """
    EventOSCmd can execute cmd in host and compare result with expect.
    """
    def __init__(self, cmd, expect, *args, **kwargs):
        super(EventOSCmd, self).__init__(*args, **kwargs)
        self._cmd = cmd
        self._expect = expect
        self._extra_cmd = kwargs.get("extra_cmd", None)
        self.name = "Name(%s)--Cmd(%s)" % (self.name, self._cmd)

    def pre_step(self):
        pass

    def is_event_happened(self):
        ret = os.popen(self._cmd)
        ret_str = ret.read()
        if ret_str != "":
            self.ret_msg = ret_str[0:-1]
        else:
            self.ret_msg = ""

        if self.ret_msg == self._expect:
            return True

        return False

    def _create_attachment_msg(self):
        if self._extra_cmd is None:
            return

        for cmd in self._extra_cmd:
            msg_str = ""
            ret = os.popen(self._cmd)
            ret = ret.read()
            if ret != "":
                msg_str += "result:\n" + ret
            if msg_str != "":
                msg = MailSender.MailSender.create_text_message(cmd, msg_str)
                self.attachment.append(msg)

    def create_email_msg(self):
        body = "cmd:\n%s\n" % self._cmd
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
        pass
