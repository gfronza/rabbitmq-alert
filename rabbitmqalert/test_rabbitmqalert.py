#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
import rabbitmqalert
import optionsresolver


class RabbitMQAlertTestCase(unittest.TestCase):
    def setUp(self):
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2
        optionsresolver.OptionsResover.setup_options_real = optionsresolver.OptionsResover.setup_options

    def tearDown(self):
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real
        optionsresolver.OptionsResover.setup_options = optionsresolver.OptionsResover.setup_options_real

    def test_check_queue_conditions_not_send_notification_when_not_exceeding_options(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_ready_send_notification_when_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages_ready"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_unacknowledged_send_notification_when_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_send_notification_when_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_connection_conditions_open_connections_not_send_notification_when_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_connection()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_open_connections_send_notification_when_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_connection()
        response.pop("connection_foo")
        response.pop("connection_bar")
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_consumer_conditions_consumers_connected_not_send_notification_when_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_consumer()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_consumers_connected_send_notification_when_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_consumer()
        response.pop("consumer_foo")
        response.pop("consumer_bar")
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_not_send_notification_when_normal(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_send_notification_when_nodes_running_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        response.pop()
        response.pop()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_send_notification_when_node_memory_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        response[0]["mem_used"] = 2000000
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_send_notification_sends_email_when_email_to_is_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_calles_login_when_email_password_is_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        options["email_password"] = "password"
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().login.assert_called_once()

    def test_send_notification_not_call_login_when_email_password_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().login.assert_not_called()

    def test_send_notification_sends_email_with_ssl_when_email_ssl_is_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        options["email_ssl"] = True
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_called_once()

    def test_send_notification_not_send_email_when_email_to_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        options["email_to"] = None
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_and_telegram_when_options_are_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.urllib2.urlopen.assert_called()

    def test_send_notification_not_send_to_slack_when_any_option_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        options["slack_url"] = None
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # Assure only telegram is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_not_send_to_telegram_when_any_option_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options()
        options["telegram_bot_id"] = None
        optionsresolver.OptionsResover.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # Assure only slack is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    @staticmethod
    def construct_options():
        options = {
            "host": "foo",
            "port": 1,
            "vhost": "foo",
            "queue": "foo",
            "queues": ["foo"],
            "conditions": {
                "foo": {
                    "ready_queue_size": 0,
                    "unack_queue_size": 0,
                    "total_queue_size": 0,
                    "consumers_connected": 1,
                    "open_connections": 1,
                    "nodes_running": 1,
                    "node_memory_used": 1
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

        return options

    @staticmethod
    def construct_response_queue():
        return {
            "messages_ready": 0,
            "messages_unacknowledged": 0,
            "messages": 0
        }

    @staticmethod
    def construct_response_connection():
        return {
            "connection_foo": {},
            "connection_bar": {}
        }

    @staticmethod
    def construct_response_consumer():
        return {
            "consumer_foo": {},
            "consumer_bar": {}
        }

    @staticmethod
    def construct_response_node():
        return [
            { "mem_used": 500000 },
            { "mem_used": 500000 }
        ]

if __name__ == "__main__":
    unittest.main()
