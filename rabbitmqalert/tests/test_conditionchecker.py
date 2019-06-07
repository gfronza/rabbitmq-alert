#! /usr/bin/python2
# -*- coding: utf8 -*-

import argparse
import mock
import unittest

from rabbitmqalert import apiclient
from rabbitmqalert import argumentsparser
from rabbitmqalert import conditionchecker


class ConditionCheckerTestCase(unittest.TestCase):

    def test_check_queue_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=None)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_queue_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=self.construct_response_queue())

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_ready(self):
        response = self.construct_response_queue()
        response["messages_ready"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_unacknowledged(self):
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages(self):
        response = self.construct_response_queue()
        response["messages"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_beneath_consumers(self):
        response = self.construct_response_queue()
        response["consumers"] = 0
        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_queue_consumers_connected"] = 1
        arguments["conditions"]["foo"]["conditions_queue_consumers_connected"] = 1

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_queue_conditions(arguments)

        notifier.send_notification.assert_called_once()

    def test_check_consumer_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=None)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_consumer_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_consumer_conditions_not_sends_notification_when_exceeding_consumers_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=self.construct_response_consumers())

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_consumer_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_consumer_conditions_sends_notification_when_beneath_consumers(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_consumer_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_connection_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=None)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_connection_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_connection_conditions_not_sends_notification_when_exceeding_connections_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=self.construct_response_connections())

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_connection_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_connection_conditions_sends_notification_when_beneath_connections(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_connection_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_node_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=None)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_node_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_node_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=self.construct_response_nodes())

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_node_conditions(self.construct_arguments())

        notifier.send_notification.assert_not_called()

    def test_check_node_conditions_sends_notification_when_beneath_nodes_running(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_node_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

    def test_check_node_conditions_sends_notification_when_exceeding_mem_used(self):
        response = self.construct_response_nodes()
        response[0]["mem_used"] = 2 * pow(1024, 2)

        logger = mock.MagicMock()
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = conditionchecker.ConditionChecker(logger, client, notifier)
        rmqa.check_node_conditions(self.construct_arguments())

        notifier.send_notification.assert_called_once()

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

    @staticmethod
    def construct_response_queue():
        return {
            "messages_ready": 0,
            "messages_unacknowledged": 0,
            "messages": 0,
            "consumers": 0
        }

    @staticmethod
    def construct_response_consumers():
        return {
            "consumer_foo": {},
            "consumer_bar": {}
        }

    @staticmethod
    def construct_response_connections():
        return {
            "connection_foo": {},
            "connection_bar": {}
        }

    @staticmethod
    def construct_response_nodes():
        return [
            { "mem_used": 500000 },
            { "mem_used": 500000 }
        ]


if __name__ == "__main__":
    unittest.main()
