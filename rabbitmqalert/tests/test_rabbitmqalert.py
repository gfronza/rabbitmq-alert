#! /usr/bin/python2
# -*- coding: utf8 -*-

import argparse
import mock
import unittest

from . import apiclient
from . import argumentsparser
from . import rabbitmqalert


class RabbitMQAlertTestCase(unittest.TestCase):

    def setUp(self):
        rabbitmqalert.argumentsparser_real = rabbitmqalert.argumentsparser
        rabbitmqalert.logger_real = rabbitmqalert.logger
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2

    def tearDown(self):
        rabbitmqalert.argumentsparser = rabbitmqalert.argumentsparser_real
        rabbitmqalert.logger = rabbitmqalert.logger_real
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real

    def test_check_queue_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=self.construct_response_queue())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_ready(self):
        response = self.construct_response_queue()
        response["messages_ready"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_unacknowledged(self):
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages(self):
        response = self.construct_response_queue()
        response["messages"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_beneath_consumers(self):
        response = self.construct_response_queue()
        response["consumers"] = 0
        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_queue_consumers_connected"] = 1
        arguments["conditions"]["foo"]["conditions_queue_consumers_connected"] = 1

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(arguments)

        rmqa.send_notification.assert_called_once()

    def test_check_consumer_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_not_sends_notification_when_exceeding_consumers_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=self.construct_response_consumers())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_sends_notification_when_beneath_consumers(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_connection_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_not_sends_notification_when_exceeding_connections_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=self.construct_response_connections())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_sends_notification_when_beneath_connections(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=self.construct_response_nodes())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_arguments())

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_sends_notification_when_beneath_nodes_running(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_sends_notification_when_exceeding_mem_used(self):
        response = self.construct_response_nodes()
        response[0]["mem_used"] = 2 * pow(1024, 2)

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_arguments())

        rmqa.send_notification.assert_called_once()

    def test_send_notification_does_not_send_email_when_email_to_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_email_when_email_to_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(self.construct_arguments(), "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_calls_login_when_email_password_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_password"] = "password"

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP().login.assert_called_once()

    def test_send_notification_does_not_call_login_when_email_password_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(self.construct_arguments(), "")

        rabbitmqalert.smtplib.SMTP().login.assert_not_called()

    def test_send_notification_sends_email_with_ssl_when_email_ssl_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_ssl"] = True

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_called_once()

    def test_send_notification_does_not_send_email_with_ssl_when_email_ssl_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_ssl"] = False

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_and_telegram_when_arguments_are_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        self.assertEquals(2, rabbitmqalert.urllib2.urlopen.call_count)

    def test_send_notification_does_not_send_to_slack_when_any_argument_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["slack_url"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        # only telegram is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_does_not_send_to_telegram_when_any_argument_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        # only slack is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_uses_host_alias_when_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["server_host_alias"] = "bar-host"

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo bar-host foo\n\nbar-host - ")

    def test_send_notification_does_not_use_host_alias_when_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["server_host_alias"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo foo-host foo\n\nfoo-host - ")

    def test_send_notification_logs_info_when_email_is_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_email_not_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        arguments = self.construct_arguments()
        arguments["email_to"] = None
        arguments["slack_url"] = None
        arguments["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(arguments, "")

        logger.info.assert_not_called()

    def test_setup_arguments_returns_parser(self):
        parser = rabbitmqalert.setup_arguments()
        self.assertIsInstance(parser, argparse.ArgumentParser)

    def test_main_runs_check_queue_conditions_when_ready_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_ready_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_unack_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_unack_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_total_queue_size_in_queue_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_total_queue_size"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()

    def test_main_runs_check_queue_conditions_when_queue_consumers_connected_in_queue_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["conditions"]["foo"]["conditions_queue_consumers_connected"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_queue_conditions.assert_called()

    def test_main_runs_check_node_conditions_when_nodes_running_in_generic_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_nodes_running"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_node_conditions.assert_called()

    def test_main_runs_check_node_conditions_when_node_memory_used_in_generic_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_node_memory_used"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_node_conditions.assert_called()

    def test_main_runs_check_connection_conditions_when_open_connections_in_generic_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_open_connections"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_connection_conditions.assert_called()

    def test_main_runs_check_consumer_conditions_when_consumers_connected_in_generic_conditions(self):
        client = mock.MagicMock()
        rabbitmqalert.logger = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_queue_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_node_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_connection_conditions = mock.MagicMock()
        rabbitmqalert.RabbitMQAlert.check_consumer_conditions = mock.MagicMock()
        # throw exception to escape the "while True" loop
        rabbitmqalert.time.sleep = mock.MagicMock(side_effect=ValueError)
        rmqa = rabbitmqalert.RabbitMQAlert(rabbitmqalert.logger, client)

        arguments = self.construct_arguments()
        arguments["generic_conditions"]["conditions_consumers_connected"] = 1
        rabbitmqalert.argumentsparser = mock.MagicMock()
        rabbitmqalert.argumentsparser.ArgumentsParser(mock.MagicMock()).parse = mock.MagicMock(return_value=arguments)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_consumer_conditions.assert_called()

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
