#!/usr/bin/bash
# -*- coding:utf-8 -*-
import EventBase
import logging
logger = logging.getLogger("EventSSH")


class EventSSH(EventBase.EventBase):

    def __init__(self, *args, **kwargs):
        super(EventSSH, self).__init__()

    def pre_step(self):
        pass

    def is_event_happened(self):
        pass

    def create_email_msg(self):
        pass

    def post_step(self):
        pass
