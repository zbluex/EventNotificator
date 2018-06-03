import os
import multiprocessing
import platform
import log
import logging
import event.EventSSH as ES
import MailSender
import threading
import time
import argparse


logger = logging.getLogger("MailNotificator")

# global variable
time_interval = None

def event_trigger(event):
    """
    event trigger function. trigger event information, judge whether is happened.
    trigger time interval get from event.time_trigger, global variable time_trigger or 60 seconds.
    :param event: object init from class EventBase
    :return: None
    """
    is_happened = False
    while True:
        event.pre_step()
        try:
            is_happened = event.is_event_happened()
            if is_happened:
                event.create_email_msg()
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

    parser = argparse.ArgumentParser(description="This tool is used to trigger events. "
                                                 "When event triggered, "
                                                 "it will send email to notice specified persons.",
                                     epilog="Author: zbluex@gmail.com")
    parser.add_argument("-t", "--time_interval", type=int, help="set to specified default time interval of "
                                                                "Event trigger, unit is second.")
    parser.add_argument('-d', '--daemon', action='store_true', help='set program run as a daemon.')
    parser.add_argument('-l', '--logfile', type=file, help='specified log file path.')
    args = parser.parse_args()
    logger.debug("%s", args)
    if args.time_interval is not None:
        global time_interval
        time_interval = args.time_interval

    if args.logfile is not None:
        pass

    return args


def start_threads():
    threads = init_thread()
    trigger_event(threads)


def main():
    args = args_parser()
    # TODO: test code
    if args.daemon:
        is_win = platform.platform().lower().find("windows")
        is_linux = platform.platform().lower().find("linux")
        if is_win == 0:
            pass
        elif is_linux == 0:
            pid = os.fork()
            if pid > 0:
                logger.info("end")
                exit(0)
            else:
                time.sleep(2)
                logger.info("sleep end")

    else:
        start_threads()


if __name__ == "__main__":
    EventList = [
        ES.EventSSH("echo $(($(date +%S)>30))", "1", "root", "123456", "127.0.0.1", time_interval=0),
        ES.EventSSH("cat /etc/os-release |grep -i ^name=|cut -d'=' -f 2", "\"Ubuntu\"", "root", "123456", "127.0.0.1")
    ]
    main()