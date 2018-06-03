import log
import logging
import event.EventSSH as ES
import MailSender
import threading
import time

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


def main():
    threads = init_thread()
    trigger_event(threads)


if __name__ == "__main__":
    EventList = [
        ES.EventSSH("date +%S", "30", "root", "123456", "127.0.0.1", time_interval=0),
        ES.EventSSH("cat /etc/os-release |grep -i ^name=|cut -d'=' -f 2", "\"Ubuntu\"", "root", "123456", "127.0.0.1")
    ]
    main()
