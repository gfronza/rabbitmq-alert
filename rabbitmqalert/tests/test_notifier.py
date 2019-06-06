#! /usr/bin/python2
# -*- coding: utf8 -*-

import mock
import unittest

from rabbitmqalert import rabbitmqalert
from rabbitmqalert import notifier


class NotifierTestCase(unittest.TestCase):

    def setUp(self):
        notifier.urllib2_real = notifier.urllib2

    def tearDown(self):
        notifier.urllib2 = notifier.urllib2_real

    def test_send_notification_does_not_send_email_when_email_to_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_email_when_email_to_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        notifier_object = notifier.Notifier(logger, self.construct_arguments())

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_calls_login_when_email_password_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_password"] = "password"

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().login.assert_called_once()

    def test_send_notification_does_not_call_login_when_email_password_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        notifier_object = notifier.Notifier(logger, self.construct_arguments())

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().login.assert_not_called()

    def test_send_notification_sends_email_with_ssl_when_email_ssl_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_ssl"] = True

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP_SSL().sendmail.assert_called_once()

    def test_send_notification_does_not_send_email_with_ssl_when_email_ssl_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_ssl"] = False

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP_SSL().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_and_telegram_when_arguments_are_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        notifier_object = notifier.Notifier(logger, self.construct_arguments())

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        self.assertEquals(2, notifier.urllib2.urlopen.call_count)

    def test_send_notification_does_not_send_to_slack_when_any_argument_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["slack_url"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        # only telegram is called
        notifier.urllib2.urlopen.assert_called_once()

    def test_send_notification_does_not_send_to_telegram_when_any_argument_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        # only slack is called
        notifier.urllib2.urlopen.assert_called_once()

    def test_send_notification_uses_host_alias_when_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["server_host_alias"] = "bar-host"

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo bar-host foo\n\nbar-host - ")

    def test_send_notification_does_not_use_host_alias_when_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["server_host_alias"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        notifier.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo foo-host foo\n\nfoo-host - ")

    def test_send_notification_logs_info_when_email_is_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_email_not_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        notifier_object = notifier.Notifier(logger, arguments)

        notifier.smtplib = mock.MagicMock()
        notifier.urllib2 = mock.MagicMock()
        notifier_object.send_notification("")

        logger.info.assert_not_called()

    @staticmethod
    def construct_arguments():
        arguments = {
            "config_file": None,
            "server_scheme": "http",
            "server_host": "foo-host",
            "server_port": 1,
            "server_host_alias": "bar-host",
            "server_vhost": "foo",
            "server_queue": "foo",
            "server_queues": ["foo"],
            "server_queues_discovery": False,
            "server_check_rate": 1,
            "generic_conditions": {
                "conditions_consumers_connected": 1,
                "conditions_open_connections": 1,
                "conditions_nodes_running": 1,
                "conditions_node_memory_used": 1
            },
            "conditions": {
                "foo": {
                    "conditions_ready_queue_size": 0,
                    "conditions_unack_queue_size": 0,
                    "conditions_total_queue_size": 0,
                    "conditions_queue_consumers_connected": 0,
                }
            },
            "email_to": ["foo@foobar.com"],
            "email_from": "bar@foobar.com",
            "email_subject": "foo %s %s",
            "email_server": "mail.foobar.com",
            "email_password": "",
            "email_ssl": False,
            "slack_url": "http://foo.com",
            "slack_channel": "channel",
            "slack_username": "username",
            "telegram_bot_id": "foo_bot",
            "telegram_channel": "foo_channel"
        }

        return arguments


if __name__ == "__main__":
    unittest.main()
