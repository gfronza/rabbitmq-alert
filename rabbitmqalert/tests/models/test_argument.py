#! /usr/bin/python2
# -*- coding: utf8 -*-

import mock
import unittest

from . import models
from . import argumentsparser
from . import rabbitmqalert


class ArgumentTestCase(unittest.TestCase):

    def setUp(self):
        models.argument.ConfigParser_real = models.argument.ConfigParser
        models.argument.os_real = models.argument.os
        models.argument.Argument.load_defaults_real = models.argument.Argument.load_defaults
        models.argument.Argument.load_file_real = models.argument.Argument.load_file
        models.argument.Argument.get_type_real = models.argument.Argument.get_type
        models.argument.Argument.get_value_from_file_real = models.argument.Argument.get_value_from_file

    def tearDown(self):
        models.argument.ConfigParser = models.argument.ConfigParser_real
        models.argument.os = models.argument.os_real
        models.argument.Argument.load_defaults = models.argument.Argument.load_defaults_real
        models.argument.Argument.load_file = models.argument.Argument.load_file_real
        models.argument.Argument.get_type = models.argument.Argument.get_type_real
        models.argument.Argument.get_value_from_file = models.argument.Argument.get_value_from_file_real

    def test_init_loads_files(self):
        logger = mock.MagicMock()

        arguments = self.construct_argparse_parsed_arguments()

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        argument = models.argument.Argument(logger, arguments)

        models.argument.Argument.load_defaults.assert_called_once()
        models.argument.Argument.load_file.assert_called_once()

    def test_load_defaults_loads_file_when_file_exists(self):
        logger = mock.MagicMock()

        arguments = {}

        models.argument.ConfigParser.ConfigParser.read = mock.MagicMock()
        models.argument.os.path.isfile = mock.MagicMock(return_value=True)
        # copy method and mock original to avoid calling during initialization of Argument
        models.argument.Argument.load_defaults_real = models.argument.Argument.load_defaults
        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()

        argument = models.argument.Argument(logger, arguments)
        # now that initilization is done, replace mocked load_defaults() with the original
        argument.load_defaults = argument.load_defaults_real

        argument.load_defaults()

        models.argument.ConfigParser.ConfigParser.read.assert_called_once()
        logger.info.assert_called_once()

    def test_load_defaults_exits_when_file_does_not_exist(self):
        logger = mock.MagicMock()

        arguments = {}

        models.argument.ConfigParser.ConfigParser.read = mock.MagicMock()
        models.argument.os.path.isfile = mock.MagicMock(return_value=False)
        # copy method and mock original to avoid calling during initialization of Argument
        models.argument.Argument.load_defaults_real = models.argument.Argument.load_defaults
        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()

        argument = models.argument.Argument(logger, arguments)
        # now that initilization is done, replace mocked load_defaults() with the original
        argument.load_defaults = argument.load_defaults_real

        with self.assertRaises(SystemExit) as se:
            argument.load_defaults()

        self.assertEqual(se.exception.code, 1)
        models.argument.ConfigParser.ConfigParser.read.assert_not_called()
        logger.error.assert_called_once()

    def test_load_file_loads_file_when_config_file_argument_given_and_file_exists(self):
        logger = mock.MagicMock()

        arguments = self.construct_argparse_parsed_arguments()
        arguments["config_file"] = "foo.ini"

        models.argument.ConfigParser.ConfigParser.read = mock.MagicMock()
        models.argument.os.path.isfile = mock.MagicMock(return_value=True)
        # copy method and mock original to avoid calling during initialization of Argument
        models.argument.Argument.load_file_real = models.argument.Argument.load_file
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.load_defaults = mock.MagicMock()

        argument = models.argument.Argument(logger, arguments)
        # now that initilization is done, replace mocked load_defaults() with the original
        argument.load_file = argument.load_file_real

        argument.load_file()

        models.argument.ConfigParser.ConfigParser.read.assert_called_once_with(arguments["config_file"])
        logger.info.assert_called_once()

    def test_load_file_exits_when_config_file_argument_given_and_file_does_not_exist(self):
        logger = mock.MagicMock()

        arguments = self.construct_argparse_parsed_arguments()
        arguments["config_file"] = "foo.ini"

        models.argument.ConfigParser.ConfigParser.read = mock.MagicMock()
        models.argument.os.path.isfile = mock.MagicMock(return_value=False)
        # copy method and mock original to avoid calling during initialization of Argument
        models.argument.Argument.load_file_real = models.argument.Argument.load_file
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.load_defaults = mock.MagicMock()

        argument = models.argument.Argument(logger, arguments)
        # now that initilization is done, replace mocked load_file() with the original
        argument.load_file = argument.load_file_real

        with self.assertRaises(SystemExit) as se:
            argument.load_file()

        self.assertEqual(se.exception.code, 1)
        models.argument.ConfigParser.ConfigParser.read.assert_not_called()
        logger.error.assert_called_once()

    def test_load_file_loads_global_file_when_exists_and_no_config_file_argument_given(self):
        logger = mock.MagicMock()

        # no config_file argument given
        arguments = {"config_file": None}

        models.argument.ConfigParser.ConfigParser.read = mock.MagicMock()
        models.argument.os.path.isfile = mock.MagicMock(return_value=True)
        # copy method and mock original to avoid calling during initialization of Argument
        models.argument.Argument.load_file_real = models.argument.Argument.load_file
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.load_defaults = mock.MagicMock()

        argument = models.argument.Argument(logger, arguments)
        # now that initilization is done, replace mocked load_defaults() with the original
        argument.load_file = argument.load_file_real

        argument.load_file()

        models.argument.ConfigParser.ConfigParser.read.assert_called_once_with(models.argument.CONFIG_FILE_PATH)
        logger.info.assert_called_once_with("Using configuration file \"{0}\"".format(models.argument.CONFIG_FILE_PATH))

    def test_get_type_returns_bool_type(self):
        argument_element = mock.MagicMock()
        argument_element.type = None
        argument_element.const = True

        logger = mock.MagicMock()
        arguments = self.construct_argparse_parsed_arguments()
        argument = models.argument.Argument(logger, arguments)

        self.assertEquals(bool, argument.get_type(argument_element))

        argument_element.const = False
        self.assertEquals(bool, argument.get_type(argument_element))

    def test_get_type_returns_int_type(self):
        argument_element = mock.MagicMock()
        argument_element.type = int

        logger = mock.MagicMock()
        arguments = self.construct_argparse_parsed_arguments()
        argument = models.argument.Argument(logger, arguments)

        self.assertEquals(int, argument.get_type(argument_element))

    def test_get_type_returns_str_type(self):
        argument_element = mock.MagicMock()
        argument_element.type = str

        logger = mock.MagicMock()
        arguments = self.construct_argparse_parsed_arguments()
        argument = models.argument.Argument(logger, arguments)

        self.assertEquals(str, argument.get_type(argument_element))

    def test_files_have_group_returns_false_when_group_does_not_exist(self):
        logger = mock.MagicMock()

        defaults_content = mock.MagicMock()
        defaults_content.has_section = mock.MagicMock(return_value=False)
        config_file_content = mock.MagicMock()
        config_file_content.has_section = mock.MagicMock(return_value=False)

        models.argument.Argument.load_defaults = mock.MagicMock(return_value=defaults_content)
        models.argument.Argument.load_file = mock.MagicMock(return_value=config_file_content)
        models.argument.Argument.get_value_from_file = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        result = argument.files_have_group("foo")

        defaults_content.has_section.assert_called_once_with("foo")
        config_file_content.has_section.assert_called_once_with("foo")
        self.assertEquals(False, result)

    def test_files_have_group_returns_true_when_group_exists_on_config_file(self):
        logger = mock.MagicMock()

        defaults_content = mock.MagicMock()
        defaults_content.has_section = mock.MagicMock(return_value=False)
        config_file_content = mock.MagicMock()
        config_file_content.has_section = mock.MagicMock(return_value=True)

        models.argument.Argument.load_defaults = mock.MagicMock(return_value=defaults_content)
        models.argument.Argument.load_file = mock.MagicMock(return_value=config_file_content)
        models.argument.Argument.get_value_from_file = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        result = argument.files_have_group("foo")

        defaults_content.has_section.assert_not_called()
        config_file_content.has_section.assert_called_once_with("foo")
        self.assertEquals(True, result)

    def test_files_have_group_returns_true_when_group_exists_on_defaults_file(self):
        logger = mock.MagicMock()

        defaults_content = mock.MagicMock()
        defaults_content.has_section = mock.MagicMock(return_value=True)
        config_file_content = mock.MagicMock()
        config_file_content.has_section = mock.MagicMock(return_value=False)

        models.argument.Argument.load_defaults = mock.MagicMock(return_value=defaults_content)
        models.argument.Argument.load_file = mock.MagicMock(return_value=config_file_content)
        models.argument.Argument.get_value_from_file = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        result = argument.files_have_group("foo")

        defaults_content.has_section.assert_called_once_with("foo")
        config_file_content.has_section.assert_called_once_with("foo")
        self.assertEquals(True, result)

    def test_create_argument_object_returns_object(self):
        logger = mock.MagicMock()

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        argument_object = argument.create_argument_object("foo", int, None)

        self.assertIsInstance(argument_object, object)
        self.assertEquals(argument_object.dest, "foo")
        self.assertEquals(argument_object.type, int)
        self.assertEquals(argument_object.const, None)

    def test_get_value_from_file_returns_none_when_file_has_no_such_argument(self):
        logger = mock.MagicMock()

        file = mock.MagicMock()
        file.has_option = mock.MagicMock(return_value=False)

        argument_element = mock.MagicMock()
        argument_element.dest = "server_host"
        argument_element.type = str

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_type = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        value = argument.get_value_from_file(file, "foo-group", argument_element)

        self.assertEquals(None, value)
        file.has_option.assert_called_once()
        argument.get_type.assert_not_called()

    def test_get_value_from_file_gets_string_value(self):
        logger = mock.MagicMock()

        file = mock.MagicMock()
        file.has_option = mock.MagicMock(return_value=True)

        argument_element = mock.MagicMock()
        argument_element.dest = "server_host"
        argument_element.type = str

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_type = mock.MagicMock(return_value=str)

        argument = models.argument.Argument(logger, {})
        argument.get_value_from_file(file, "foo-group", argument_element)

        file.has_option.assert_called_once()
        argument.get_type.assert_called()
        file.get.assert_called_once()
        file.getint.assert_not_called()
        file.getboolean.assert_not_called()

    def test_get_value_from_file_gets_integer_value(self):
        logger = mock.MagicMock()

        file = mock.MagicMock()
        file.has_option = mock.MagicMock(return_value=True)

        argument_element = mock.MagicMock()
        argument_element.dest = "server_port"
        argument_element.type = int

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_type = mock.MagicMock(return_value=int)

        argument = models.argument.Argument(logger, {})
        argument.get_value_from_file(file, "foo-group", argument_element)

        file.has_option.assert_called_once()
        argument.get_type.assert_called()
        file.get.assert_not_called()
        file.getint.assert_called_once()
        file.getboolean.assert_not_called()

    def test_get_value_from_file_gets_boolean_value(self):
        logger = mock.MagicMock()

        file = mock.MagicMock()
        file.has_option = mock.MagicMock(return_value=True)

        argument_element = mock.MagicMock()
        argument_element.dest = "server_queues_discovery"
        argument_element.type = bool

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_type = mock.MagicMock(return_value=bool)

        argument = models.argument.Argument(logger, {})
        argument.get_value_from_file(file, "foo-group", argument_element)

        file.has_option.assert_called_once()
        argument.get_type.assert_called()
        file.get.assert_not_called()
        file.getint.assert_not_called()
        file.getboolean.assert_called_once()

    def test_get_value_returns_value_from_cli(self):
        logger = mock.MagicMock()

        argument_element = mock.MagicMock()
        argument_element.dest = "server_queues_discovery"
        argument_element.type = bool

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_value_from_file = mock.MagicMock()

        argument = models.argument.Argument(logger, self.construct_argparse_parsed_arguments())
        value = argument.get_value("server", argument_element)

        argument.get_value_from_file.assert_not_called()
        self.assertEquals(False, value)

    def test_get_value_returns_value_from_config_file_when_no_cli_argument_given(self):
        logger = mock.MagicMock()

        defaults_content = mock.MagicMock()
        config_file_content = mock.MagicMock()

        argument_element = mock.MagicMock()
        argument_element.dest = "server_queues_discovery"
        argument_element.type = bool

        models.argument.Argument.load_defaults = mock.MagicMock(return_value=defaults_content)
        models.argument.Argument.load_file = mock.MagicMock(return_value=config_file_content)
        models.argument.Argument.get_value_from_file = mock.MagicMock()

        argument = models.argument.Argument(logger, {})
        value = argument.get_value("server", argument_element)

        argument.get_value_from_file.assert_called_once_with(config_file_content, "server", argument_element)

    def test_get_value_returns_value_from_defaults_file_when_no_cli_argument_and_config_file_argument_does_not_exist(self):
        logger = mock.MagicMock()

        defaults_content = mock.MagicMock()
        config_file_content = mock.MagicMock()

        argument_element = mock.MagicMock()
        argument_element.dest = "server_queues_discovery"
        argument_element.type = bool

        models.argument.Argument.load_defaults = mock.MagicMock(return_value=defaults_content)
        models.argument.Argument.load_file = mock.MagicMock(return_value=config_file_content)
        models.argument.Argument.get_value_from_file = mock.MagicMock()
        models.argument.Argument.get_value_from_file.side_effect = [None, True]

        argument = models.argument.Argument(logger, {})
        value = argument.get_value("server", argument_element)

        argument.get_value_from_file.assert_any_call(config_file_content, "server", argument_element)
        argument.get_value_from_file.assert_any_call(defaults_content, "server", argument_element)

    def test_get_value_returns_none_when_group_not_found_in_config_file(self):
        logger = mock.MagicMock()

        file = mock.MagicMock()
        file.has_option = mock.MagicMock(return_value=False)

        argument_element = mock.MagicMock()
        argument_element.dest = "server_host"
        argument_element.type = str

        models.argument.Argument.load_defaults = mock.MagicMock()
        models.argument.Argument.load_file = mock.MagicMock()
        models.argument.Argument.get_type = mock.MagicMock()
        models.argument.Argument.get_value_from_file = mock.MagicMock(return_value=None)

        argument = models.argument.Argument(logger, {})
        value = argument.get_value("foo-group", argument_element)

        self.assertEquals(None, value)
        self.assertEquals(2, argument.get_value_from_file.call_count)

    @staticmethod
    def construct_argparse_parsed_arguments():
        return {
            "config_file": None,
            "server_scheme": "http",
            "server_host": "foo-host",
            "server_port": 1,
            "server_host_alias": "bar-host",
            "server_username": "user",
            "server_password": "pass",
            "server_vhost": "foo",
            "server_queue": "foo",
            "server_queues": ["foo"],
            "server_queues_discovery": False,
            "conditions_consumers_connected": 1,
            "conditions_open_connections": 1,
            "conditions_nodes_running": 1,
            "conditions_node_memory_used": 1,
            "conditions_ready_queue_size": 0,
            "conditions_unack_queue_size": 0,
            "conditions_total_queue_size": 0,
            "conditions_queue_consumers_connected": 0,
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


if __name__ == "__main__":
    unittest.main()
