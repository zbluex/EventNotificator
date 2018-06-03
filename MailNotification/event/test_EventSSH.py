import unittest
import EventSSH
import sys, os
sys.path.append("..")
import MailSender


class EventSSHTest(unittest.TestCase):

    def test_exec_cmd1(self):
        """
        exec ls /root, expect result is ""
        :return:
        """
        ES = EventSSH.EventSSH("cat /etc/os-release |grep -i ^name=|cut -d'=' -f 2", "\"Ubuntu\"", "root", "123456", "127.0.0.1")
        ES.pre_step()
        is_happened = ES.is_event_happened()
        self.assertTrue(is_happened)
        ES.create_email_msg()
        ms = MailSender.MailSender()
        ms.mail_send(ES.msg, ES.user_to, ES.user_cc, ES.attachment)
