#!/usr/bin/bash
# -*- coding:utf-8 -*-
import abc
import sys
import logging
sys.path.append('..')
import log

logger = logging.getLogger("EventBase")


class EventBase(object):
    __metaclass__ = abc.ABCMeta
    name = ""
    err_msg = ""
    ret_msg = ""
    msg = None
    attachment = list()
    user_to = list()
    user_cc = list()

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        user_to = kwargs.get("user_to", list())
        if len(user_to) > 0:
            self.user_to = user_to
        user_cc = kwargs.get("user_cc", list())
        if len(user_cc) > 0:
            self.user_cc = user_cc

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
