#!/usr/bin/bash
# -*- coding:utf-8 -*-
import abc
import sys
import logging
sys.path.append('..')
from log import logger


class EventBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        self.err_msg = ""
        self.ret_msg = ""
        self.msg = None
        self.attachment = list()
        self.user_to = list()
        self.user_cc = list()
        self.re_trigger = False
        self.time_interval = None

        user_to = kwargs.get("user_to", list())
        if len(user_to) > 0:
            self.user_to = user_to
        user_cc = kwargs.get("user_cc", list())
        if len(user_cc) > 0:
            self.user_cc = user_cc
        self.re_trigger = bool(kwargs.get("re_trigger", False))
        time_interval = int(kwargs.get("time_interval", -1))
        if time_interval >= 0:
            self.time_interval = time_interval


    @abc.abstractmethod
    def pre_step(self):
        """
        Event prepare step.
        :return: None
        """
        pass

    @abc.abstractmethod
    def is_event_happened(self):
        """
        Event trigger step, judge whether event is happened.
        :return: boolean
        """
        pass

    @abc.abstractmethod
    def create_email_msg(self):
        """
        Event create email message step.
        :return: email.message
        """
        pass

    @abc.abstractmethod
    def post_step(self):
        """
        Event post step.
        :return:
        """
        pass
