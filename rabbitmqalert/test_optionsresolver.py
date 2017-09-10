#! /usr/bin/python2
# -*- coding: utf8 -*-

import unittest
import mock
import optionsresolver
import ConfigParser


class OptionsResolverTestCase(unittest.TestCase):
    def setUp(self):
        optionsresolver.os_real = optionsresolver.os
        optionsresolver.optparse.sys.argv[1:] = []

        # Stash the original function to reassign it later
        self.ConfigParser = optionsresolver.ConfigParser.ConfigParser

    def tearDown(self):
        optionsresolver.os = optionsresolver.os_real
        optionsresolver.optparse.sys.argv[1:] = []
        optionsresolver.ConfigParser.ConfigParser = self.ConfigParser

    def test_setup_options_returns_options_when_options_given_and_no_config_file(self):
        resolver = optionsresolver.OptionsResover()
        options = [
            "--host", "foo-host",
            "--port", "foo-port",
            "--username", "foo-username",
            "--password", "foo-password",
            "--vhost", "foo-vhost",
            "--queues", "foo-queue",
            "--check-rate", "10",
            "--ready-queue-size", "20",
            "--unacknowledged-queue-size", "30",
            "--total-queue-size", "40",
            "--consumers-connected", "50",
            "--open-connections", "51",
            "--nodes-running", "60",
            "--node-memory-used", "70",
            "--email-to", "foo-email-to",
            "--email-from", "foo-email-from",
            "--email-subject", "foo-email-subject",
            "--email-server", "foo-email-server",
            "--email-password", "foo-email-password",
            "--email-ssl", "",
            "--slack-url", "foo-slack-url",
            "--slack-channel", "foo-slack-channel",
            "--slack-username", "foo-slack-username",
            "--telegram-bot-id", "foo-telegram-bot-id",
            "--telegram-channel", "foo-telegram-channel"
        ]

        optionsresolver.optparse.sys.argv[1:] = options
        options_result = resolver.setup_options()

        self.assertEquals("foo-host", options_result["host"])
        self.assertEquals("foo-port", options_result["port"])
        self.assertEquals("foo-username", options_result["username"])
        self.assertEquals("foo-password", options_result["password"])
        self.assertEquals("foo-vhost", options_result["vhost"])
        self.assertEquals(["foo-queue"], options_result["queues"])
        self.assertEquals(10, options_result["check_rate"])
        self.assertEquals(20, options_result["conditions"]["foo-queue"]["ready_queue_size"])
        self.assertEquals(30, options_result["conditions"]["foo-queue"]["unack_queue_size"])
        self.assertEquals(40, options_result["conditions"]["foo-queue"]["total_queue_size"])
        self.assertEquals(50, options_result["conditions"]["foo-queue"]["consumers_connected"])
        self.assertEquals(51, options_result["conditions"]["foo-queue"]["open_connections"])
        self.assertEquals(60, options_result["conditions"]["foo-queue"]["nodes_running"])
        self.assertEquals(70, options_result["conditions"]["foo-queue"]["node_memory_used"])
        self.assertEquals(["foo-email-to"], options_result["email_to"])
        self.assertEquals("foo-email-from", options_result["email_from"])
        self.assertEquals("foo-email-subject", options_result["email_subject"])
        self.assertEquals("foo-email-server", options_result["email_server"])
        self.assertEquals("foo-email-password", options_result["email_password"])
        self.assertEquals(True, options_result["email_ssl"])
        self.assertEquals("foo-slack-url", options_result["slack_url"])
        self.assertEquals("foo-slack-channel", options_result["slack_channel"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-telegram-bot-id", options_result["telegram_bot_id"])
        self.assertEquals("foo-telegram-channel", options_result["telegram_channel"])

    def test_setup_options_without_ssl_return_options_when_options_without_ssl_given_and_no_config_file(self):
        resolver = optionsresolver.OptionsResover()
        options = [
            "--host", "foo-host",
            "--port", "foo-port",
            "--username", "foo-username",
            "--password", "foo-password",
            "--vhost", "foo-vhost",
            "--queues", "foo-queue",
            "--check-rate", "10",
            "--ready-queue-size", "20",
            "--unacknowledged-queue-size", "30",
            "--total-queue-size", "40",
            "--consumers-connected", "50",
            "--open-connections", "51",
            "--nodes-running", "60",
            "--node-memory-used", "70",
            "--email-to", "foo-email-to",
            "--email-from", "foo-email-from",
            "--email-subject", "foo-email-subject",
            "--email-server", "foo-email-server",
            "--email-password", "foo-email-password",
            "--slack-url", "foo-slack-url",
            "--slack-channel", "foo-slack-channel",
            "--slack-username", "foo-slack-username",
            "--telegram-bot-id", "foo-telegram-bot-id",
            "--telegram-channel", "foo-telegram-channel"
        ]

        optionsresolver.optparse.sys.argv[1:] = options
        options_result = resolver.setup_options()

        self.assertEquals("foo-host", options_result["host"])
        self.assertEquals("foo-port", options_result["port"])
        self.assertEquals("foo-username", options_result["username"])
        self.assertEquals("foo-password", options_result["password"])
        self.assertEquals("foo-vhost", options_result["vhost"])
        self.assertEquals(["foo-queue"], options_result["queues"])
        self.assertEquals(10, options_result["check_rate"])
        self.assertEquals(20, options_result["conditions"]["foo-queue"]["ready_queue_size"])
        self.assertEquals(30, options_result["conditions"]["foo-queue"]["unack_queue_size"])
        self.assertEquals(40, options_result["conditions"]["foo-queue"]["total_queue_size"])
        self.assertEquals(50, options_result["conditions"]["foo-queue"]["consumers_connected"])
        self.assertEquals(51, options_result["conditions"]["foo-queue"]["open_connections"])
        self.assertEquals(60, options_result["conditions"]["foo-queue"]["nodes_running"])
        self.assertEquals(70, options_result["conditions"]["foo-queue"]["node_memory_used"])
        self.assertEquals(["foo-email-to"], options_result["email_to"])
        self.assertEquals("foo-email-from", options_result["email_from"])
        self.assertEquals("foo-email-subject", options_result["email_subject"])
        self.assertEquals("foo-email-server", options_result["email_server"])
        self.assertEquals("foo-email-password", options_result["email_password"])
        self.assertEquals(False, options_result["email_ssl"])
        self.assertEquals("foo-slack-url", options_result["slack_url"])
        self.assertEquals("foo-slack-channel", options_result["slack_channel"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-telegram-bot-id", options_result["telegram_bot_id"])
        self.assertEquals("foo-telegram-channel", options_result["telegram_channel"])

    def test_setup_options_exits_with_error_when_config_file_not_found(self):
        resolver = optionsresolver.OptionsResover()
        options = ["--config", "foo.ini"]

        optionsresolver.os.path.isfile = mock.MagicMock(return_value=False)
        optionsresolver.optparse.sys.argv[1:] = options

        with self.assertRaises(SystemExit) as se:
            resolver.setup_options()

        self.assertEqual(se.exception.code, 1)

    def test_setup_options_returns_options_when_config_file_found(self):
        options = ["--config", "foo.ini"]

        config_file_options = self.construct_config_file_options_with_generic_conditions()
        parser = ConfigParser.ConfigParser()
        parser._sections = config_file_options

        optionsresolver.os.path.isfile = mock.MagicMock(return_value=True)
        optionsresolver.ConfigParser.ConfigParser = mock.MagicMock(return_value=parser)
        optionsresolver.optparse.sys.argv[1:] = options
        options_result = optionsresolver.OptionsResover.setup_options()

        self.assertEquals("foo-host", options_result["host"])
        self.assertEquals("foo-port", options_result["port"])
        self.assertEquals("foo-username", options_result["username"])
        self.assertEquals("foo-password", options_result["password"])
        self.assertEquals("foo-vhost", options_result["vhost"])
        self.assertEquals(["foo-queue"], options_result["queues"])
        self.assertEquals(10, options_result["check_rate"])
        self.assertEquals(20, options_result["conditions"]["foo-queue"]["ready_queue_size"])
        self.assertEquals(30, options_result["conditions"]["foo-queue"]["unack_queue_size"])
        self.assertEquals(40, options_result["conditions"]["foo-queue"]["total_queue_size"])
        self.assertEquals(50, options_result["conditions"]["foo-queue"]["consumers_connected"])
        self.assertEquals(51, options_result["conditions"]["foo-queue"]["open_connections"])
        self.assertEquals(60, options_result["conditions"]["foo-queue"]["nodes_running"])
        self.assertEquals(70, options_result["conditions"]["foo-queue"]["node_memory_used"])
        self.assertEquals(["foo-email-to"], options_result["email_to"])
        self.assertEquals("foo-email-from", options_result["email_from"])
        self.assertEquals("foo-email-subject", options_result["email_subject"])
        self.assertEquals("foo-email-host", options_result["email_server"])
        self.assertEquals("foo-email-password", options_result["email_password"])
        self.assertEquals(True, options_result["email_ssl"])
        self.assertEquals("foo-slack-url", options_result["slack_url"])
        self.assertEquals("foo-slack-channel", options_result["slack_channel"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-telegram-bot-id", options_result["telegram_bot_id"])
        self.assertEquals("foo-telegram-channel", options_result["telegram_channel"])

    def test_setup_options_overrides_config_file_option_when_option_given_from_cli(self):
        options = ["--config", "foo.ini", "--email-to", "foo-email-to-new"]

        config_file_options = self.construct_config_file_options_with_generic_conditions()
        parser = ConfigParser.ConfigParser()
        parser._sections = config_file_options

        optionsresolver.os.path.isfile = mock.MagicMock(return_value=True)
        optionsresolver.ConfigParser.ConfigParser = mock.MagicMock(return_value=parser)
        optionsresolver.optparse.sys.argv[1:] = options
        options_result = optionsresolver.OptionsResover.setup_options()

        self.assertEquals(["foo-email-to-new"], options_result["email_to"])

    def test_setup_options_returns_options_when_config_file_found_with_queue_specific_conditions(self):
        options = ["--config", "foo.ini"]

        config_file_options = self.construct_config_file_options_with_queue_specific_conditions()
        parser = ConfigParser.ConfigParser()
        parser._sections = config_file_options

        optionsresolver.os.path.isfile = mock.MagicMock(return_value=True)
        optionsresolver.ConfigParser.ConfigParser = mock.MagicMock(return_value=parser)
        optionsresolver.optparse.sys.argv[1:] = options
        options_result = optionsresolver.OptionsResover.setup_options()

        self.assertEquals("foo-host", options_result["host"])
        self.assertEquals("foo-port", options_result["port"])
        self.assertEquals("foo-username", options_result["username"])
        self.assertEquals("foo-password", options_result["password"])
        self.assertEquals("foo-vhost", options_result["vhost"])
        self.assertEquals(["foo-queue"], options_result["queues"])
        self.assertEquals(10, options_result["check_rate"])
        self.assertEquals(20, options_result["conditions"]["foo-queue"]["ready_queue_size"])
        self.assertEquals(30, options_result["conditions"]["foo-queue"]["unack_queue_size"])
        self.assertEquals(40, options_result["conditions"]["foo-queue"]["total_queue_size"])
        self.assertEquals(50, options_result["conditions"]["foo-queue"]["consumers_connected"])
        self.assertEquals(51, options_result["conditions"]["foo-queue"]["open_connections"])
        self.assertEquals(60, options_result["conditions"]["foo-queue"]["nodes_running"])
        self.assertEquals(70, options_result["conditions"]["foo-queue"]["node_memory_used"])
        self.assertEquals(["foo-email-to"], options_result["email_to"])
        self.assertEquals("foo-email-from", options_result["email_from"])
        self.assertEquals("foo-email-subject", options_result["email_subject"])
        self.assertEquals("foo-email-host", options_result["email_server"])
        self.assertEquals("foo-email-password", options_result["email_password"])
        self.assertEquals(True, options_result["email_ssl"])
        self.assertEquals("foo-slack-url", options_result["slack_url"])
        self.assertEquals("foo-slack-channel", options_result["slack_channel"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-telegram-bot-id", options_result["telegram_bot_id"])
        self.assertEquals("foo-telegram-channel", options_result["telegram_channel"])

    def test_setup_options_returns_options_when_config_file_found_with_multiple_queue_specific_conditions(self):
        options = ["--config", "foo.ini"]

        config_file_options = self.construct_config_file_options_with_multiple_queue_specific_conditions()
        parser = ConfigParser.ConfigParser()
        parser._sections = config_file_options

        optionsresolver.os.path.isfile = mock.MagicMock(return_value=True)
        optionsresolver.ConfigParser.ConfigParser = mock.MagicMock(return_value=parser)
        optionsresolver.optparse.sys.argv[1:] = options
        options_result = optionsresolver.OptionsResover.setup_options()

        self.assertEquals("foo-host", options_result["host"])
        self.assertEquals("foo-port", options_result["port"])
        self.assertEquals("foo-username", options_result["username"])
        self.assertEquals("foo-password", options_result["password"])
        self.assertEquals("foo-vhost", options_result["vhost"])
        self.assertEquals(["foo-queue", "bar-queue"], options_result["queues"])
        self.assertEquals(10, options_result["check_rate"])
        self.assertEquals(20, options_result["conditions"]["foo-queue"]["ready_queue_size"])
        self.assertEquals(30, options_result["conditions"]["foo-queue"]["unack_queue_size"])
        self.assertEquals(40, options_result["conditions"]["foo-queue"]["total_queue_size"])
        self.assertEquals(50, options_result["conditions"]["foo-queue"]["consumers_connected"])
        self.assertEquals(51, options_result["conditions"]["foo-queue"]["open_connections"])
        self.assertEquals(60, options_result["conditions"]["foo-queue"]["nodes_running"])
        self.assertEquals(70, options_result["conditions"]["foo-queue"]["node_memory_used"])
        self.assertEquals(30, options_result["conditions"]["bar-queue"]["ready_queue_size"])
        self.assertEquals(40, options_result["conditions"]["bar-queue"]["unack_queue_size"])
        self.assertEquals(50, options_result["conditions"]["bar-queue"]["total_queue_size"])
        self.assertEquals(60, options_result["conditions"]["bar-queue"]["consumers_connected"])
        self.assertEquals(61, options_result["conditions"]["bar-queue"]["open_connections"])
        self.assertEquals(70, options_result["conditions"]["bar-queue"]["nodes_running"])
        self.assertEquals(80, options_result["conditions"]["bar-queue"]["node_memory_used"])
        self.assertEquals(["foo-email-to"], options_result["email_to"])
        self.assertEquals("foo-email-from", options_result["email_from"])
        self.assertEquals("foo-email-subject", options_result["email_subject"])
        self.assertEquals("foo-email-host", options_result["email_server"])
        self.assertEquals("foo-email-password", options_result["email_password"])
        self.assertEquals(True, options_result["email_ssl"])
        self.assertEquals("foo-slack-url", options_result["slack_url"])
        self.assertEquals("foo-slack-channel", options_result["slack_channel"])
        self.assertEquals("foo-slack-username", options_result["slack_username"])
        self.assertEquals("foo-telegram-bot-id", options_result["telegram_bot_id"])
        self.assertEquals("foo-telegram-channel", options_result["telegram_channel"])

    @staticmethod
    def construct_config_file_options_with_generic_conditions():
        return {
            "Server": {
                "host": "foo-host",
                "port": "foo-port",
                "username": "foo-username",
                "password": "foo-password",
                "vhost": "foo-vhost",
                "queues": "foo-queue",
                "check_rate": "10"
            },
            "Conditions": {
                "ready_queue_size": "20",
                "unack_queue_size": "30",
                "total_queue_size": "40",
                "consumers_connected": "50",
                "open_connections": "51",
                "nodes_running": "60",
                "node_memory_used": "70"
            },
            "Email": {
                "to": "foo-email-to",
                "from": "foo-email-from",
                "subject": "foo-email-subject",
                "host": "foo-email-host",
                "password": "foo-email-password",
                "ssl": "True"
            },
            "Slack": {
                "url": "foo-slack-url",
                "channel": "foo-slack-channel",
                "username": "foo-slack-username"
            },
            "Telegram": {
                "bot_id": "foo-telegram-bot-id",
                "channel": "foo-telegram-channel"
            }
        }

    @staticmethod
    def construct_config_file_options_with_queue_specific_conditions():
        return {
            "Server": {
                "host": "foo-host",
                "port": "foo-port",
                "username": "foo-username",
                "password": "foo-password",
                "vhost": "foo-vhost",
                "queues": "foo-queue",
                "check_rate": "10"
            },
            "Conditions:foo-queue": {
                "ready_queue_size": "20",
                "unack_queue_size": "30",
                "total_queue_size": "40",
                "consumers_connected": "50",
                "open_connections": "51",
                "nodes_running": "60",
                "node_memory_used": "70"
            },
            "Email": {
                "to": "foo-email-to",
                "from": "foo-email-from",
                "subject": "foo-email-subject",
                "host": "foo-email-host",
                "password": "foo-email-password",
                "ssl": "True"
            },
            "Slack": {
                "url": "foo-slack-url",
                "channel": "foo-slack-channel",
                "username": "foo-slack-username"
            },
            "Telegram": {
                "bot_id": "foo-telegram-bot-id",
                "channel": "foo-telegram-channel"
            }
        }

    @staticmethod
    def construct_config_file_options_with_multiple_queue_specific_conditions():
        return {
            "Server": {
                "host": "foo-host",
                "port": "foo-port",
                "username": "foo-username",
                "password": "foo-password",
                "vhost": "foo-vhost",
                "queues": "foo-queue,bar-queue",
                "check_rate": "10"
            },
            "Conditions:foo-queue": {
                "ready_queue_size": "20",
                "unack_queue_size": "30",
                "total_queue_size": "40",
                "consumers_connected": "50",
                "open_connections": "51",
                "nodes_running": "60",
                "node_memory_used": "70"
            },
            "Conditions:bar-queue": {
                "ready_queue_size": "30",
                "unack_queue_size": "40",
                "total_queue_size": "50",
                "consumers_connected": "60",
                "open_connections": "61",
                "nodes_running": "70",
                "node_memory_used": "80"
            },
            "Email": {
                "to": "foo-email-to",
                "from": "foo-email-from",
                "subject": "foo-email-subject",
                "host": "foo-email-host",
                "password": "foo-email-password",
                "ssl": "True"
            },
            "Slack": {
                "url": "foo-slack-url",
                "channel": "foo-slack-channel",
                "username": "foo-slack-username"
            },
            "Telegram": {
                "bot_id": "foo-telegram-bot-id",
                "channel": "foo-telegram-channel"
            }
        }

if __name__ == "__main__":
    unittest.main()
