#!/usr/bin/bash
# -*- coding:utf-8 -*-
import abc
import sys
sys.path.append('..')
import log, logging
logger = logging.getLogger("EventBase")


class EventBase(object):
    __metaclass__ = abc.ABCMeta
    name = None
    errmsg = None
    msg = None
    attachment = list()
    user_to = list()
    user_cc = list()

    def __init__(self):
        self.name = self.__class__.__name__

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
