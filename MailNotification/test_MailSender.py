# -*- coding:utf-8 -*-
import unittest
import HTMLTestRunner
import MailSender
import smtplib


class MailSenderTest(unittest.TestCase):
    def setUp(self):
        self.ms = MailSender.MailSender()

    def test_send_mail(self):
        msg = self.ms.create_text_message("python unittest is working", "testcase(test_send_mail).")
        self.assertIsNotNone(msg)
        self.ms.mail_send(msg)

    def test_send_without_msg(self):
        try:
            self.ms.mail_send(None)
        except Exception as e:
            if not (isinstance(e, smtplib.SMTPDataError) and e.smtp_code == 0):
                raise

    def test_smtp_address_invalid(self):
        is_except_happened = False
        address = self.ms.smtp_address
        try:
            self.ms.smtp_address = ""
            msg = self.ms.create_text_message("python unittest is working", """testcase(test_smtp_address_invalid) 
smtp_address is %s""" % self.ms.smtp_address)
            self.ms.mail_send(msg)
        except Exception as e:
            is_except_happened = True
            if not (isinstance(e, smtplib.SMTPDataError) and e.smtp_code == 1):
                raise
        finally:
            self.ms.smtp_address = address

        if not is_except_happened:
            raise AssertionError("Exception should be raised.")


if __name__ == "__main__":
    suit = unittest.TestSuite()
    suit.addTest(unittest.makeSuite(MailSenderTest))

    with open('HTMLReport.html', 'w') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, verbosity=2, title='Mail Sender Test Report',
                                               description='generated by HTMLTestRunner')
        runner.run(suit)
