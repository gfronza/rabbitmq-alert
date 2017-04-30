#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
import rabbitmqalert
from collections import namedtuple
import ConfigParser

class rabbitMqAlertTestCase(unittest.TestCase):
    MockOptions = namedtuple(
        "Foo",
        "host, port, vhost, queue, ready_queue_size, unack_queue_size,\
        total_queue_size, consumers_connected, nodes_running, node_memory_used,\
        email_to, email_from, email_subject, email_server, slack_url,\
        slack_channel, slack_username"
    )

    def setUp(self):
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2
        rabbitmqalert.os_real = rabbitmqalert.os
        rabbitmqalert.optparse.sys.argv[1:] = []

    def tearDown(self):
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real
        rabbitmqalert.os = rabbitmqalert.os_real
        rabbitmqalert.optparse.sys.argv[1:] = []

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

    def test_setup_options_returns_non_default_options_when_options_given_and_no_config_file(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = [
            "--host", "foo-host",
            "--port", "foo-port",
            "--username", "foo-username",
            "--password", "foo-password",
            "--vhost", "foo-vhost",
            "--queues", "foo-queues",
            "--check-rate",  "10",
            "--ready-queue-size", "20",
            "--unacknowledged-queue-size", "30",
            "--total-queue-size", "40",
            "--consumers-connected", "50",
            "--nodes-running", "60",
            "--node-memory-used", "70",
            "--email-to", "foo-email-to",
            "--email-from", "foo-email-from",
            "--email-subject", "foo-email-subject",
            "--email-server", "foo-email-server",
            "--slack-url", "foo-slack-url",
            "--slack-channel", "foo-slack-channel",
            "--slack-username", "foo-slack-username"
        ]

        rabbitmqalert.optparse.sys.argv[1:] = options
        options_result = rmqa.setup_options()

        self.assertEquals("foo-host", options_result.host)
        self.assertEquals("foo-port", options_result.port)
        self.assertEquals("foo-username", options_result.username)
        self.assertEquals("foo-password", options_result.password)
        self.assertEquals("foo-vhost", options_result.vhost)
        self.assertEquals("foo-queues", options_result.queues)
        self.assertEquals(10, options_result.check_rate)
        self.assertEquals(20, options_result.ready_queue_size)
        self.assertEquals(30, options_result.unack_queue_size)
        self.assertEquals(40, options_result.total_queue_size)
        self.assertEquals(50, options_result.consumers_connected)
        self.assertEquals(60, options_result.nodes_running)
        self.assertEquals(70, options_result.node_memory_used)
        self.assertEquals("foo-email-to", options_result.email_to)
        self.assertEquals("foo-email-from", options_result.email_from)
        self.assertEquals("foo-email-subject", options_result.email_subject)
        self.assertEquals("foo-email-server", options_result.email_server)
        self.assertEquals("foo-slack-url", options_result.slack_url)
        self.assertEquals("foo-slack-channel", options_result.slack_channel)
        self.assertEquals("foo-slack-username", options_result.slack_username)

    def test_setup_options_exits_with_error_when_config_file_not_found(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = ["--config", "foo.ini"]

        rabbitmqalert.os.path.isfile = mock.MagicMock(return_value=False)
        rabbitmqalert.optparse.sys.argv[1:] = options

        with self.assertRaises(SystemExit) as se:
            rmqa.setup_options()

        self.assertEqual(se.exception.code, 1)

    def test_setup_options_returns_options_when_config_file_found(self):
        rmqa = rabbitmqalert.RabbitMQAlert()
        options = ["--config", "foo.ini"]

        config_file_options = {
            "Server": {
                "host": "foo-host",
                "port": "foo-port",
                "username": "foo-username",
                "password": "foo-password",
                "vhost": "foo-vhost",
                "queues": "foo-queues",
                "check_rate": "10"
            },
            "Conditions": {
                "ready_queue_size": "20",
                "unack_queue_size": "30",
                "total_queue_size": "40",
                "consumers_connected": "50",
                "nodes_running": "60",
                "node_memory_used": "70"
            },
            "Email": {
                "to": "foo-email-to",
                "from": "foo-email-from",
                "subject": "foo-email-subject",
                "host": "foo-email-host"
            },
            "Slack": {
                "url": "foo-slack-url",
                "channel": "foo-slack-channel",
                "username": "foo-slack-username"
            }
        }
        parser = ConfigParser.ConfigParser()
        parser._sections = config_file_options

        rabbitmqalert.os.path.isfile = mock.MagicMock(return_value=True)
        rabbitmqalert.ConfigParser.ConfigParser = mock.MagicMock(return_value=parser)
        rabbitmqalert.optparse.sys.argv[1:] = options
        options_result = rmqa.setup_options()

        self.assertEquals("foo-host", options_result.host)
        self.assertEquals("foo-port", options_result.port)
        self.assertEquals("foo-username", options_result.username)
        self.assertEquals("foo-password", options_result.password)
        self.assertEquals("foo-vhost", options_result.vhost)
        self.assertEquals("foo-queues", options_result.queues)
        self.assertEquals(10, options_result.check_rate)
        self.assertEquals(20, options_result.ready_queue_size)
        self.assertEquals(30, options_result.unack_queue_size)
        self.assertEquals(40, options_result.total_queue_size)
        self.assertEquals(50, options_result.consumers_connected)
        self.assertEquals(60, options_result.nodes_running)
        self.assertEquals(70, options_result.node_memory_used)
        self.assertEquals("foo-email-to", options_result.email_to)
        self.assertEquals("foo-email-from", options_result.email_from)
        self.assertEquals("foo-email-subject", options_result.email_subject)
        self.assertEquals("foo-email-host", options_result.email_server)
        self.assertEquals("foo-slack-url", options_result.slack_url)
        self.assertEquals("foo-slack-channel", options_result.slack_channel)
        self.assertEquals("foo-slack-username", options_result.slack_username)

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

    def construct_response_node(self):
        return [
            { "mem_used": 500000 },
            { "mem_used": 500000 }
        ]

if __name__ == "__main__":
    unittest.main()
