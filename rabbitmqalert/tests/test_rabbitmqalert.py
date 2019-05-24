#! /usr/bin/python2
# -*- coding: utf8 -*-

import mock
import unittest

from . import apiclient
from . import optionsresolver
from . import rabbitmqalert


class RabbitMQAlertTestCase(unittest.TestCase):

    def setUp(self):
        rabbitmqalert.logger_real = rabbitmqalert.logger
        rabbitmqalert.urllib2_real = rabbitmqalert.urllib2
        optionsresolver.OptionsResolver.setup_options_real = optionsresolver.OptionsResolver.setup_options

    def tearDown(self):
        rabbitmqalert.logger = rabbitmqalert.logger_real
        rabbitmqalert.urllib2 = rabbitmqalert.urllib2_real
        optionsresolver.OptionsResolver.setup_options = optionsresolver.OptionsResolver.setup_options_real

    def test_check_queue_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=self.construct_response_queue())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_ready(self):
        response = self.construct_response_queue()
        response["messages_ready"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages_unacknowledged(self):
        response = self.construct_response_queue()
        response["messages_unacknowledged"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_exceeding_messages(self):
        response = self.construct_response_queue()
        response["messages"] = 2

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_queue_conditions_sends_notification_when_beneath_consumers(self):
        response = self.construct_response_queue()
        response["consumers"] = 0
        options = self.construct_options()
        options["generic_conditions"]["queue_consumers_connected"] = 1
        options["conditions"]["foo"]["queue_consumers_connected"] = 1

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_queue = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_queue_conditions(options)

        rmqa.send_notification.assert_called_once()

    def test_check_consumer_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_not_sends_notification_when_exceeding_consumers_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=self.construct_response_consumers())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_consumer_conditions_sends_notification_when_beneath_consumers(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_consumers = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_consumer_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_connection_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_not_sends_notification_when_exceeding_connections_connected(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=self.construct_response_connections())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_connection_conditions_sends_notification_when_beneath_connections(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_connections = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_connection_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_exits_when_no_response_from_client(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=None)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_not_sends_notification_when_no_conditions_met(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=self.construct_response_nodes())

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_options())

        rmqa.send_notification.assert_not_called()

    def test_check_node_conditions_sends_notification_when_beneath_nodes_running(self):
        response = {}

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_check_node_conditions_sends_notification_when_exceeding_mem_used(self):
        response = self.construct_response_nodes()
        response[0]["mem_used"] = 2 * pow(1024, 2)

        logger = mock.MagicMock()
        client = mock.MagicMock()
        client.get_nodes = mock.MagicMock(return_value=response)

        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)
        rmqa.send_notification = mock.MagicMock()
        rmqa.check_node_conditions(self.construct_options())

        rmqa.send_notification.assert_called_once()

    def test_send_notification_does_not_send_email_when_email_to_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_not_called()

    def test_send_notification_sends_email_when_email_to_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(self.construct_options(), "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once()

    def test_send_notification_calls_login_when_email_password_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_password"] = "password"

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().login.assert_called_once()

    def test_send_notification_does_not_call_login_when_email_password_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(self.construct_options(), "")

        rabbitmqalert.smtplib.SMTP().login.assert_not_called()

    def test_send_notification_sends_email_with_ssl_when_email_ssl_is_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_ssl"] = True

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_called_once()

    def test_send_notification_does_not_send_email_with_ssl_when_email_ssl_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_ssl"] = False

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP_SSL().sendmail.assert_not_called()

    def test_send_notification_sends_to_slack_and_telegram_when_options_are_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.urllib2.urlopen.call_count = 2

    def test_send_notification_does_not_send_to_slack_when_any_option_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["slack_url"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # only telegram is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_does_not_send_to_telegram_when_any_option_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        # only slack is called
        rabbitmqalert.urllib2.urlopen.assert_called_once()

    def test_send_notification_uses_host_alias_when_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["host_alias"] = "bar-host"

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo bar-host foo\n\nbar-host - ")

    def test_send_notification_does_not_use_host_alias_when_not_set(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["host_alias"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        rabbitmqalert.smtplib.SMTP().sendmail.assert_called_once_with("bar@foobar.com", ["foo@foobar.com"], "Subject: foo foo-host foo\n\nfoo-host - ")

    def test_send_notification_logs_info_when_email_is_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["slack_url"] = None
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_email_not_sent(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_slack(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

    def test_send_notification_logs_info_when_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_called_once()

    def test_send_notification_does_not_log_info_when_not_sending_to_telegram(self):
        logger = mock.MagicMock()
        client = mock.MagicMock()
        rmqa = rabbitmqalert.RabbitMQAlert(logger, client)

        options = self.construct_options()
        options["email_to"] = None
        options["slack_url"] = None
        options["telegram_bot_id"] = None

        rabbitmqalert.smtplib = mock.MagicMock()
        rabbitmqalert.urllib2 = mock.MagicMock()
        rmqa.send_notification(options, "")

        logger.info.assert_not_called()

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

        options = self.construct_options()
        options["conditions"] = {
            "foo": {
                "ready_queue_size": 1
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["conditions"] = {
            "foo": {
                "unack_queue_size": 1
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["conditions"] = {
            "foo": {
                "total_queue_size": 1
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["conditions"] = {
            "foo": {
                "queue_consumers_connected": 1
            }
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["generic_conditions"] = {
            "nodes_running": 1
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["generic_conditions"] = {
            "node_memory_used": 1
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["generic_conditions"] = {
            "open_connections": 1
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

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

        options = self.construct_options()
        options["generic_conditions"] = {
            "consumers_connected": 1
        }
        optionsresolver.OptionsResolver.setup_options = mock.MagicMock(return_value=options)

        try:
            rabbitmqalert.main()
        except ValueError:
            pass

        rmqa.check_consumer_conditions.assert_called()

    @staticmethod
    def construct_options():
        options = {
            "scheme": "http",
            "host": "foo-host",
            "port": 1,
            "host_alias": "bar-host",
            "vhost": "foo",
            "queue": "foo",
            "queues": ["foo"],
            "queues_discovery": False,
            "check_rate": 1,
            "generic_conditions": {
                "ready_queue_size": 0,
                "unack_queue_size": 0,
                "total_queue_size": 0,
                "queue_consumers_connected": 0,
                "consumers_connected": 1,
                "open_connections": 1,
                "nodes_running": 1,
                "node_memory_used": 1
            },
            "conditions": {
                "foo": {
                    "ready_queue_size": 0,
                    "unack_queue_size": 0,
                    "total_queue_size": 0,
                    "queue_consumers_connected": 0,
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
