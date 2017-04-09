#! /usr/bin/python2
#! -*- coding: utf8 -*-

import unittest
import mock
import rabbitmqalert
from collections import namedtuple

class rabbitMqAlertTestCase(unittest.TestCase):
    def setUp(self):
        rabbitmqalert.send_notification_real = rabbitmqalert.send_notification
    
    def tearDown(self):
        rabbitmqalert.send_notification = rabbitmqalert.send_notification_real
        
    def test_check_queue_conditions_messages_ready_not_exceeding_option(self):
        response = self.construct_response_queue()
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_ready_exceeding_option(self):
        response = self.construct_response_queue()
        response["messages_ready"] = 2
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_unacknowledged_not_exceeding_option(self):
        response = self.construct_response_queue()
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_unacknowledged_exceeding_option(self):
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_called_once()

    def test_check_queue_conditions_messages_not_exceeding_option(self):
        response = self.construct_response_queue()
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_not_called()

    def test_check_queue_conditions_messages_exceeding_option(self):
        response = self.construct_response_queue()
        response["messages"] = 2
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_queue_conditions(options)

        rabbitmqalert.send_notification.assert_called_once()

    def test_check_connection_conditions_messages_unacknowledged_exceeding_option(self):
        response = self.construct_response_connection()
        response["consumers_connected"] = 2
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_connection_conditions(options)

        rabbitmqalert.send_notification.assert_not_called()

    def test_check_connection_conditions_messages_unacknowledged_beneath_option(self):
        response = self.construct_response_connection()
        response.pop("consumer_foo")
        response.pop("consumer_bar")
        rabbitmqalert.send_request = mock.MagicMock(return_value=response)

        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)

        rabbitmqalert.send_notification = mock.MagicMock()
        rabbitmqalert.check_connection_conditions(options)

        rabbitmqalert.send_notification.assert_called_once()

    def test_send_notification_sends_email_when_email_to_option_exists(self):
        options = self.construct_options()
        rabbitmqalert.setup_options = mock.MagicMock(return_value=options)
        
        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.send_notification(options, "")
        rabbitmqalert.urllib2 = mock.MagicMock()
        
        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()
        
    def construct_options(self):
        Options = namedtuple(
            "Foo",
            "host, port, vhost, queue, ready_queue_size, unack_queue_size,\
            total_queue_size, consumers_connected, nodes_running, node_memory_used,\
            email_to, email_from, email_subject, email_server, slack_url,\
            slack_channel, slack_username"
        )
        options = Options(
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

    def construct_response_queue(self):
        return {
            "messages_ready": 0,
            "messages_unacknowledged": 0,
            "messages": 0
        }

    def construct_response_connection(self):
        return {
            "consumer_foo": {},
            "consumer_bar": {}
        }
if __name__ == "__main__":
    unittest.main()