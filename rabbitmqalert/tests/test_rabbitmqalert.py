#! /usr/bin/python2
# -*- coding: utf8 -*-

import argparse
import mock
import unittest

from rabbitmqalert import apiclient
from rabbitmqalert import argumentsparser
from rabbitmqalert import rabbitmqalert


class RabbitMQAlertTestCase(unittest.TestCase):

    def setUp(self):
        rabbitmqalert.argumentsparser_real = rabbitmqalert.argumentsparser
        rabbitmqalert.conditionchecker_real = rabbitmqalert.conditionchecker
        rabbitmqalert.logger_real = rabbitmqalert.logger

    def tearDown(self):
        rabbitmqalert.argumentsparser = rabbitmqalert.argumentsparser_real
        rabbitmqalert.conditionchecker = rabbitmqalert.conditionchecker_real
        rabbitmqalert.logger = rabbitmqalert.logger_real

    def test_setup_arguments_returns_parser(self):
        parser = rabbitmqalert.setup_arguments()
        self.assertIsInstance(parser, argparse.ArgumentParser)

    def test_main_runs_check_queue_conditions_when_ready_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_ready_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_unack_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_unack_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_total_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_total_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_queue_consumers_connected_in_queue_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_queue_consumers_connected"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_queue_conditions.assert_called()

    def test_main_runs_check_node_conditions_when_nodes_running_in_generic_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_nodes_running"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_node_conditions.assert_called()

    def test_main_runs_check_node_conditions_when_node_memory_used_in_generic_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_node_memory_used"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_node_conditions.assert_called()

    def test_main_runs_check_connection_conditions_when_open_connections_in_generic_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_open_connections"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_connection_conditions.assert_called()

    def test_main_runs_check_consumer_conditions_when_consumers_connected_in_generic_conditions(self):
        client = mock.MagicMock()
        notifier = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.conditionchecker = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_consumers_connected"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rabbitmqalert.conditionchecker.ConditionChecker().check_consumer_conditions.assert_called()

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
