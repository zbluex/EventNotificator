import unittest
import EventSSH
import email
import sys, os
sys.path.append("..")


class EventSSHTest(unittest.TestCase):

    def test_exec_cmd1(self):
        """
        exec ls /root, expect result is ""
        :return:
        """
        es = EventSSH.EventSSH("cat /etc/os-release |grep -i ^name=|cut -d'=' -f 2", "\"Ubuntu\"", "root", "123456", "127.0.0.1")
        es.pre_step()
        try:
            is_happened = es.is_event_happened()
            self.assertTrue(is_happened)
            self.assertEqual(es.err_msg, "")
            es.create_email_msg()
            self.assertIsInstance(es.msg, email.message.Message)
            self.assertTrue(es.ret_msg == "\"Ubuntu\"")
        finally:
            es.post_step()
