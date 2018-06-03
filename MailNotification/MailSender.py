import ConfigParser
import smtplib
import re

import email.mime.multipart, email.mime.text, email.header

import logging, log
logger = logging.getLogger("MailSendor")

config = ConfigParser.ConfigParser()
config.read('config.cfg')


class MailSender(object):
    """
    Mail Sender class
    """
    smtp_obj = None
    smtp_server = None
    smtp_port = None
    smtp_user = None
    smtp_passwd = None
    smtp_address = None
    smtp_ssl = False
    user_to = list()
    user_cc = list()

    def __init__(self):
        try:
            self.smtp_server = config.get('profile', 'smtp_server')
            self.smtp_port = config.get('profile', 'smtp_port')
            self.smtp_user = config.get('profile', 'smtp_user')
            self.smtp_passwd = config.get('profile', 'smtp_passwd')
            self.smtp_address = config.get('profile', 'smtp_email_address')
            self.smtp_ssl = config.getboolean('profile', 'smtp_ssl')
            self.user_to = config.get(ConfigParser.DEFAULTSECT, 'user_to')
            self.user_cc = config.get(ConfigParser.DEFAULTSECT, 'user_cc')
        except ConfigParser.Error as e:
            logger.error("Mail Sender get option from config.cfg failed, %s.",
                         e)
            raise
        self.user_to = re.split('[,;]', self.user_to)
        self.user_to = [v.strip(' ') for v in self.user_to]
        self.user_cc = re.split('[,;]', self.user_cc)
        self.user_cc = [v.strip(' ') for v in self.user_cc]
        if self.smtp_address == "":
            start = self.smtp_server.find('.')
            if start != -1:
                self.smtp_address = self.smtp_user + '@' + self.smtp_server[start + 1:]

        logger.debug('email sender address: %s.', self.smtp_address)
        logger.debug('user to send: %s;', self.user_to)
        logger.debug('user to copy: %s.', self.user_cc)

    def _connect(self):
        """
        connect to mail server
        :return: None
        """
        if self.smtp_ssl:
            self.smtp_obj = smtplib.SMTP_SSL()
        else:
            self.smtp_obj = smtplib.SMTP()
        logger.debug("server %s, port %s", self.smtp_server, self.smtp_port)
        self.smtp_obj.connect(self.smtp_server, self.smtp_port)
        self.smtp_obj.ehlo()
        try:
            self.smtp_obj.starttls()
        except smtplib.SMTPResponseException:
            pass
        self.smtp_obj.login(self.smtp_user, self.smtp_passwd)

    def _disconnec(self):
        """
        disconnect from mail server
        :return: None
        """
        self.smtp_obj.close()

    def mail_send(self, message, extra_to=list(), extra_cc=list(), attach=list()):
        """
        send message to mail server

        :param message: TEXT message to be send
        :param extra_to: Extra user to be send, param is a list
        :param extra_cc: Extra user to be copy, param is a list
        :param attach: Attachment file to be send, param is a list
        :return: None
        """

        if not isinstance(message, email.message.Message):
            logger.debug("parameter of message is not a valid email context.")
            raise smtplib.SMTPDataError(0, "parameter of message is not a valid email context.")

        if extra_to is not None and len(extra_to) > 0:
            extra_to = [v.strip(' ') for v in extra_to]
            self.user_to += extra_to

        if extra_cc is not None and len(extra_cc) > 0:
            extra_cc = [v.strip(' ') for v in extra_cc]
            self.user_cc += extra_cc

        if self.smtp_address == "" or len(self.user_to) == 0:
            raise smtplib.SMTPDataError(1, "sender address or destination address is invalid.")

        self._connect()

        try:
            msg = email.mime.multipart.MIMEMultipart()
            msg['Subject'] = message['Subject']
            message['From'] = self.smtp_address
            message['To'] = ','.join(self.user_to)
            message['Cc'] = ','.join(self.user_cc)
            users = self.user_to + self.user_cc
            msg.attach(message)

            for attachment in attach:
                msg.attach(attachment)

            self.smtp_obj.sendmail(self.smtp_address, users, message.as_string())
        finally:
            self._disconnec()

    @staticmethod
    def create_text_message(title, body):
        body += """
Auto Send By Python Mail Notification"""
        msg = email.mime.text.MIMEText(body, 'plain')
        msg['Subject'] = email.header.Header(title)

        return msg
