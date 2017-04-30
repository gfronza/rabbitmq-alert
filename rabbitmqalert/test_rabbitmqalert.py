#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
import rabbitmqalert
from collections import namedtuple


class RabbitMQAlertTestCase(unittest.TestCase):
    MockOptions = namedtuple(
        "Foo",
        "host, port, vhost, queue, ready_queue_size, unack_queue_size,\
        total_queue_size, consumers_connected, nodes_running, node_memory_used,\
        email_to, email_from, email_subject, email_server, slack_url,\
        slack_channel, slack_username"
    )

    def setUp(self):
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2

    def tearDown(self):
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real

    def test_check_queue_conditions_messages_ready_not_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_ready_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages_ready"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_unacknowledged_not_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_unacknowledged_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_not_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_queue()
        response["messages"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_connection_conditions_messages_unacknowledged_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_connection()
        response["consumers_connected"] = 2
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_messages_unacknowledged_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_connection()
        response.pop("consumer_foo")
        response.pop("consumer_bar")
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_messages_nodes_running_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_messages_nodes_running_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        response.pop()
        response.pop()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_messages_node_memory_exceeding_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        response[0]["mem_used"] = 2000000
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_messages_node_memory_beneath_option(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        response = self.construct_response_node()
        rmqa.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(options)

        rmqa.send_notification.assert_not_called()

    def test_send_notification_sends_email_when_email_to_is_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rmqa.send_notification(options, "")
        rabbitmqalert.urllib2 = mock.MagicMock()

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_sends_email_when_email_to_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options_missing_email()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rmqa.send_notification(options, "")
        rabbitmqalert.urllib2 = mock.MagicMock()

        rabbitmqalert.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_when_options_are_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options_complete()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_sends_to_slack_when_an_option_not_set(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = self.construct_options_missing_slack()
        rmqa.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.urllib2.urlopen.assert_not_called()

    def construct_options_complete(self):
        options = self.MockOptions(
            host="foo",
            port=1,
            vhost="foo",
            queue="foo",
            ready_queue_size=1,
            unack_queue_size=1,
            total_queue_size=1,
            consumers_connected=1,
            nodes_running=1,
            node_memory_used=1,
            email_to="foo@foobar.com",
            email_from="bar@foobar.com",
            email_subject="foo %s %s",
            email_server="mail.foobar.com",
            slack_url="http://foo.com",
            slack_channel="channel",
            slack_username="username"
        )

        return options

    def construct_options_missing_email(self):
        options = self.MockOptions(
            host="foo",
            port=1,
            vhost="foo",
            queue="foo",
            ready_queue_size=1,
            unack_queue_size=1,
            total_queue_size=1,
            consumers_connected=1,
            nodes_running=1,
            node_memory_used=1,
            email_to=None,
            email_from="bar@foobar.com",
            email_subject="foo %s %s",
            email_server="mail.foobar.com",
            slack_url="http://foo.com",
            slack_channel="channel",
            slack_username="username"
        )

        return options

    def construct_options_missing_slack(self):
        options = self.MockOptions(
            host="foo",
            port=1,
            vhost="foo",
            queue="foo",
            ready_queue_size=1,
            unack_queue_size=1,
            total_queue_size=1,
            consumers_connected=1,
            nodes_running=1,
            node_memory_used=1,
            email_to="foo@foobar.com",
            email_from="bar@foobar.com",
            email_subject="foo %s %s",
            email_server="mail.foobar.com",
            slack_url=None,
            slack_channel="channel",
            slack_username="username"
        )

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
