#! /usr/bin/python2
# -*- coding: utf8 -*-

from collections import namedtuple
import mock
import unittest

from rabbitmqalert import argumentsparser
from rabbitmqalert.models import argument
from rabbitmqalert import rabbitmqalert


class ArgumentsParserTestCase(unittest.TestCase):

    def setUp(self):
        argumentsparser.os_real = argumentsparser.os
        argumentsparser.apiclient.ApiClient_real = argumentsparser.apiclient.ApiClient
        argumentsparser.argument.Argument_real = argumentsparser.argument.Argument
        argumentsparser.argument.Argument.files_have_group_real = argumentsparser.argument.Argument.files_have_group
        argumentsparser.argument.ConfigParser.ConfigParser_real = argumentsparser.argument.ConfigParser.ConfigParser
        argumentsparser.argument.os_real = argumentsparser.argument.os

        rabbitmqalert.argparse_real = rabbitmqalert.argparse

    def tearDown(self):
        argumentsparser.os = argumentsparser.os_real
        argumentsparser.apiclient.ApiClient = argumentsparser.apiclient.ApiClient_real
        argumentsparser.argument.Argument = argumentsparser.argument.Argument_real
        argumentsparser.argument.Argument.files_have_group = argumentsparser.argument.Argument.files_have_group_real
        argumentsparser.argument.ConfigParser.ConfigParser = argumentsparser.argument.ConfigParser.ConfigParser_real
        argumentsparser.argument.os = argumentsparser.argument.os_real

        rabbitmqalert.argparse = rabbitmqalert.argparse_real

    def test_parse_calls_get_value_for_every_group_argument(self):
        logger = mock.MagicMock()

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + self.arguments_dict_to_list(self.construct_arguments())
        argparse_parser = rabbitmqalert.setup_arguments()

        argumentsparser.argument.Argument = mock.MagicMock()
        argumentsparser.apiclient.ApiClient.get_queues = mock.MagicMock()

        parser = argumentsparser.ArgumentsParser(logger)
        parser.validate = mock.MagicMock()
        parser.format_conditions = mock.MagicMock()

        parser.parse(argparse_parser)

        # count the number of arguments
        group_arguments_count = 0
        for group in argparse_parser._action_groups:
            for group_argument in group._group_actions:
                group_arguments_count += 1

        argumentsparser.argument.Argument.get_value.call_count == group_arguments_count

    def test_parse_returns_discovered_queues_when_argument_set(self):
        logger = mock.MagicMock()

        # edit the cli arguments to look like queues discovery was requested
        arguments = self.construct_arguments()
        arguments["--queues-discovery"] = True
        arguments_list = self.arguments_dict_to_list(arguments)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        argumentsparser.apiclient.ApiClient.get_queues = mock.MagicMock(return_value=["foo-queue", "bar-queue"])

        parser = argumentsparser.ArgumentsParser(logger)
        parser.validate = mock.MagicMock()
        parser.format_conditions = mock.MagicMock()

        parser.parse(argparse_parser)

        # create a copy of the arguments in the form they would look like after parsing them (behore calling validate)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = ["foo-queue", "bar-queue"]
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["queue_conditions"] = dict()
        arguments_dict["email_ssl"] = False

        argumentsparser.apiclient.ApiClient.get_queues.assert_called_once()
        parser.validate.assert_called_once_with(arguments_dict)

    def test_parse_returns_emails_split(self):
        logger = mock.MagicMock()

        # edit the cli arguments to look like multiple email address were given
        arguments = self.construct_arguments()
        arguments["--email-to"] = "foo-email-to,bar-email-to"
        arguments_list = self.arguments_dict_to_list(arguments)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        parser.validate = mock.MagicMock()
        parser.format_conditions = mock.MagicMock()

        parser.parse(argparse_parser)

        # create a copy of the arguments in the form they would look like after parsing them (behore calling validate)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = arguments_dict["server_queues"].split(",")
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["queue_conditions"] = dict()
        arguments_dict["server_queues_discovery"] = False
        arguments_dict["email_ssl"] = False

        parser.validate.assert_called_once_with(arguments_dict)

    def test_parse_skips_queue_conditions_when_non_standard_groups_do_not_exist(self):
        logger = mock.MagicMock()
        argumentsparser.argument.Argument.files_have_group = mock.MagicMock(return_value=False)

        arguments_list = self.arguments_dict_to_list(self.construct_arguments())

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        parser.validate = mock.MagicMock()
        parser.format_conditions = mock.MagicMock()

        parser.parse(argparse_parser)

        # create a copy of the arguments in the form they would look like after parsing them (behore calling validate)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = arguments_dict["server_queues"].split(",")
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["queue_conditions"] = dict()
        arguments_dict["server_queues_discovery"] = False
        arguments_dict["email_ssl"] = False

        # checks for non-standard group for queue specific conditions
        argumentsparser.argument.Argument.files_have_group.assert_called_once_with("Conditions:foo-queue")
        # validate called with empty queue_conditions
        parser.validate.assert_called_once_with(arguments_dict)

    def test_parse_constructs_queue_conditions_when_non_standard_groups_exist(self):
        logger = mock.MagicMock()

        argumentsparser.argument.Argument.files_have_group = mock.MagicMock(return_value=True)

        arguments_dict = self.construct_arguments()
        arguments_dict["--queues"] = "foo-queue,bar-queue"
        arguments_list = self.arguments_dict_to_list(arguments_dict)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        parser.validate = mock.MagicMock()
        parser.format_conditions = mock.MagicMock()

        parser.parse(argparse_parser)

        # create a copy of the arguments in the form they would look like after parsing them (behore calling validate)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = arguments_dict["server_queues"].split(",")
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["server_queues_discovery"] = False
        arguments_dict["email_ssl"] = False
        arguments_dict["queue_conditions"] = {
            "foo-queue": {
                "conditions_total_queue_size": 40,
                "conditions_ready_queue_size": 20,
                "conditions_queue_consumers_connected": 52,
                "conditions_unack_queue_size": 30
            },
            "bar-queue": {
                "conditions_total_queue_size": 40,
                "conditions_ready_queue_size": 20,
                "conditions_queue_consumers_connected": 52,
                "conditions_unack_queue_size": 30
            }
        }

        # checks for non-standard group for queue specific conditions
        argumentsparser.argument.Argument.files_have_group.assert_any_call("Conditions:foo-queue")
        argumentsparser.argument.Argument.files_have_group.assert_any_call("Conditions:bar-queue")
        # validate called with empty queue_conditions
        parser.validate.assert_called_once_with(arguments_dict)

    def test_parse_returns_merged_arguments_and_conditions(self):
        logger = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments_list = self.arguments_dict_to_list(arguments)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        result = parser.parse(argparse_parser)

        # create a copy of the arguments in the form they would look like after parsing them
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = arguments_dict["server_queues"].split(",")
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["server_queues_discovery"] = False
        arguments_dict["email_ssl"] = False
        arguments_dict["queue_conditions"] = dict()

        arguments_dict = dict(arguments_dict.items() + parser.format_conditions(arguments_dict).items())

        self.assertEquals(arguments_dict, result)

    def test_validate_exits_when_required_argument_is_missing(self):
        logger = mock.MagicMock()

        arguments = self.construct_arguments()
        del arguments["--host"]
        arguments_list = self.arguments_dict_to_list(arguments)

        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))

        with self.assertRaises(SystemExit) as ex:
            parser.validate(arguments_dict)

        self.assertEqual(ex.exception.code, 1)
        logger.error.assert_called_once_with("Required argument not defined: host")

    def test_validate_does_not_exit_when_all_required_arguments_exist(self):
        logger = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments_list = self.arguments_dict_to_list(arguments)

        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        parser = argumentsparser.ArgumentsParser(logger)
        arguments_dict = vars(argparse_parser.parse_args(arguments_list))

        parser.validate(arguments_dict)

        logger.error.assert_not_called()

    def test_format_conditions_returns_generic_and_queue_conditions(self):
        logger = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments_list = self.arguments_dict_to_list(arguments)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = ["foo-queue"]
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["queue_conditions"] = dict()

        parser = argumentsparser.ArgumentsParser(logger)
        results = parser.format_conditions(arguments_dict)

        self.assertTrue("conditions" in results)
        self.assertTrue("generic_conditions" in results)
        # generic conditions
        self.assertEquals(arguments_dict["conditions_consumers_connected"], results["generic_conditions"]["conditions_consumers_connected"])
        self.assertEquals(arguments_dict["conditions_open_connections"], results["generic_conditions"]["conditions_open_connections"])
        self.assertEquals(arguments_dict["conditions_nodes_running"], results["generic_conditions"]["conditions_nodes_running"])
        self.assertEquals(arguments_dict["conditions_node_memory_used"], results["generic_conditions"]["conditions_node_memory_used"])
        # queue conditions
        self.assertEquals(arguments_dict["conditions_ready_queue_size"], results["conditions"]["foo-queue"]["conditions_ready_queue_size"])
        self.assertEquals(arguments_dict["conditions_unack_queue_size"], results["conditions"]["foo-queue"]["conditions_unack_queue_size"])
        self.assertEquals(arguments_dict["conditions_total_queue_size"], results["conditions"]["foo-queue"]["conditions_total_queue_size"])
        self.assertEquals(arguments_dict["conditions_queue_consumers_connected"], results["conditions"]["foo-queue"]["conditions_queue_consumers_connected"])

    def test_format_conditions_returns_queue_conditions_when_exist(self):
        logger = mock.MagicMock()

        arguments = self.construct_arguments()
        arguments_list = self.arguments_dict_to_list(arguments)

        # setup the argparse argument parser with fake cli arguments
        rabbitmqalert.argparse._sys.argv = ['rabbitmqalert.py'] + arguments_list
        argparse_parser = rabbitmqalert.setup_arguments()

        arguments_dict = vars(argparse_parser.parse_args(arguments_list))
        arguments_dict["server_queues"] = ["foo-queue", "bar-queue"]
        arguments_dict["email_to"] = arguments_dict["email_to"].split(",")
        arguments_dict["help"] = None
        arguments_dict["queue_conditions"] = {
            "foo-queue": {
                "conditions_total_queue_size": 40,
                "conditions_ready_queue_size": 20,
                "conditions_queue_consumers_connected": 52,
                "conditions_unack_queue_size": 30
            },
            "bar-queue": {
                "conditions_total_queue_size": 40,
                "conditions_ready_queue_size": 20,
                "conditions_queue_consumers_connected": 52,
                "conditions_unack_queue_size": 30
            }
        }

        parser = argumentsparser.ArgumentsParser(logger)
        results = parser.format_conditions(arguments_dict)

        self.assertTrue("conditions" in results)
        self.assertTrue("generic_conditions" in results)
        # generic conditions
        self.assertEquals(arguments_dict["conditions_consumers_connected"], results["generic_conditions"]["conditions_consumers_connected"])
        self.assertEquals(arguments_dict["conditions_open_connections"], results["generic_conditions"]["conditions_open_connections"])
        self.assertEquals(arguments_dict["conditions_nodes_running"], results["generic_conditions"]["conditions_nodes_running"])
        self.assertEquals(arguments_dict["conditions_node_memory_used"], results["generic_conditions"]["conditions_node_memory_used"])
        # queue conditions
        self.assertTrue(arguments_dict["conditions_ready_queue_size"], results["conditions"]["foo-queue"]["conditions_ready_queue_size"])
        self.assertEquals(arguments_dict["conditions_unack_queue_size"], results["conditions"]["foo-queue"]["conditions_unack_queue_size"])
        self.assertEquals(arguments_dict["conditions_total_queue_size"], results["conditions"]["foo-queue"]["conditions_total_queue_size"])
        self.assertEquals(arguments_dict["conditions_queue_consumers_connected"], results["conditions"]["foo-queue"]["conditions_queue_consumers_connected"])
        self.assertTrue(arguments_dict["conditions_ready_queue_size"], results["conditions"]["bar-queue"]["conditions_ready_queue_size"])
        self.assertEquals(arguments_dict["conditions_unack_queue_size"], results["conditions"]["bar-queue"]["conditions_unack_queue_size"])
        self.assertEquals(arguments_dict["conditions_total_queue_size"], results["conditions"]["bar-queue"]["conditions_total_queue_size"])
        self.assertEquals(arguments_dict["conditions_queue_consumers_connected"], results["conditions"]["bar-queue"]["conditions_queue_consumers_connected"])

    @staticmethod
    def construct_arguments():
        return {
            "--config-file": None,
            "--scheme": "foo-scheme",
            "--host": "foo-host",
            "--port": "foo-port",
            "--host-alias": "bar-host",
            "--username": "foo-username",
            "--password": "foo-password",
            "--vhost": "foo-vhost",
            "--queues": "foo-queue",
            "--queues-discovery": False,
            "--check-rate": "10",
            "--ready-queue-size": "20",
            "--unacknowledged-queue-size": "30",
            "--total-queue-size": "40",
            "--queue-consumers-connected": "52",
            "--consumers-connected": "50",
            "--open-connections": "51",
            "--nodes-running": "60",
            "--node-memory-used": "70",
            "--email-to": "foo-email-to",
            "--email-from": "foo-email-from",
            "--email-subject": "foo-email-subject",
            "--email-server": "foo-email-server",
            "--email-password": "foo-email-password",
            "--email-ssl": False,
            "--slack-url": "foo-slack-url",
            "--slack-channel": "foo-slack-channel",
            "--slack-username": "foo-slack-username",
            "--telegram-bot-id": "foo-telegram-bot-id",
            "--telegram-channel": "foo-telegram-channel"
        }

    @staticmethod
    def arguments_dict_to_list(dict):
        result = []

        for key, value in dict.iteritems():
            if value not in [False, None]:
                result.append(key)
                # arguments of store_true or store_false action must not have a value
                result.append(value) if type(value) is not bool else None

        return result


if __name__ == "__main__":
    unittest.main()
