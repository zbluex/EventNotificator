#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import platform
from log import logger
import log
from EventList import EventList
import MailSender
import threading
import time
import argparse

# global variable
time_interval = None
log_filepath = None
dry_run = False


def event_trigger(event):
    """
    event trigger function. trigger event information, judge whether
    is happened.
    trigger time interval get from event.time_trigger, global variable
    time_trigger or 60 seconds.
    :param event: object init from class EventBase
    :return: None
    """
    while True:
        event.pre_step()
        try:
            is_happened = event.is_event_happened()
            if is_happened:
                event.create_email_msg()
                if dry_run is False:
                    ms = MailSender.MailSender()
                    ms.mail_send(event.msg, event.user_to, event.user_cc, event.attachment)
        except Exception as e:
            logger.error("error happened when trigger event[%s], error %s.", event.name, e)
            is_happened = True
            event.err_msg = e
        finally:
            event.post_step()
        if is_happened:
            if event.err_msg == "":
                logger.info("Event[%s] trigger.", event.name)
            if event.err_msg != "" or not event.re_trigger:
                return
        if event.time_interval is not None:
            time.sleep(event.time_interval)
        elif time_interval is not None:
            time.sleep(time_interval)
        else:
            time.sleep(60)


def init_thread():
    threads = list()
    for event in EventList:
        t = threading.Thread(target=event_trigger, args=(event,))
        threads.append(t)
    return threads


def trigger_event(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def args_parser():

    parser = argparse.ArgumentParser(
        description="This tool is used to trigger events. When event "
                    "triggered, it will send email "
                    "to notice specified persons.",
        epilog="Author: zbluex@gmail.com")
    parser.add_argument("-t", "--time_interval", type=int,
                        help="set to specified default time interval of "
                             "Event trigger, unit is second.")
    parser.add_argument('-l', '--logfile', type=str,
                        help='specified log file path.')
    parser.add_argument('-d', '--dry_run', action='store_true',
                        help='set dry run mode which will not send email.')
    args = parser.parse_args()
    logger.debug("%s", args)
    if args.time_interval is not None:
        global time_interval
        time_interval = args.time_interval

    if args.logfile is not None:
        _path = os.getcwd() + os.path.sep + args.logfile
        _dir_path = os.path.dirname(_path)
        if not os.path.exists(_dir_path):
            logger.error("dirpath(%s) is not exist.", _dir_path)
            exit(1)
        global log_filepath
        log_filepath = _path
        log.set_log_filepath(log_filepath)

    if args.dry_run is True:
        global dry_run
        dry_run = args.dry_run
        logger.info("Dry run mode.")

    return args


def start_threads():
    threads = init_thread()
    trigger_event(threads)


def main():
    args = args_parser()

    logger.info("Start trigger Event:")
    for event in EventList:
        logger.info("%s", event.name)

    start_threads()


if __name__ == "__main__":
    main()
