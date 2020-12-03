#! /usr/bin/python2
# -*- coding: utf-8 -*-

import argparse
import time

import apiclient
import argumentsparser
import conditionchecker
import logger
import notifier


def setup_arguments():
    parser = argparse.ArgumentParser()

    generic = parser.add_argument_group("Generic")
    generic.add_argument("-c", "--config-file", dest="config_file", help="Path of the configuration file", type=str)

    server = parser.add_argument_group("Server")
    server.add_argument("--scheme", dest="server_scheme", help="RabbitMQ API scheme", type=str)
    server.add_argument("--host", dest="server_host", help="RabbitMQ API address", type=str)
    server.add_argument("--port", dest="server_port", help="RabbitMQ API port", type=str)
    server.add_argument("--host-alias", dest="server_host_alias", help="RabbitMQ API host alias (for display only)", type=str)
    server.add_argument("--username", dest="server_username", help="RabbitMQ API username", type=str)
    server.add_argument("--password", dest="server_password", help="RabbitMQ API password", type=str)
    server.add_argument("--vhost", dest="server_vhost", help="Name of the vhost to inspect", type=str)
    server.add_argument("--queues", dest="server_queues", help="List of comma-separated queue names to inspect", type=str)
    server.add_argument("--queues-discovery", dest="server_queues_discovery", help="Discover queues", default=None, action="store_true")
    server.add_argument("--check-rate", dest="server_check_rate", help="Conditions check frequency, in seconds.", type=int)

    conditions = parser.add_argument_group("Conditions")
    conditions.add_argument("--ready-queue-size", dest="conditions_ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type=int)
    conditions.add_argument("--unacknowledged-queue-size", dest="conditions_unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type=int)
    conditions.add_argument("--total-queue-size", dest="conditions_total_queue_size", help="Size of the Total messages on the queue to alert as warning", type=int)
    conditions.add_argument("--queue-consumers-connected", dest="conditions_queue_consumers_connected", help="The number of consumers that should be connected to the queue", type=int)
    conditions.add_argument("--consumers-connected", dest="conditions_consumers_connected", help="The number of consumers that should be connected", type=int)
    conditions.add_argument("--open-connections", dest="conditions_open_connections", help="The number of open connections", type=int)
    conditions.add_argument("--nodes-running", dest="conditions_nodes_running", help="The number of nodes running", type=int)
    conditions.add_argument("--node-memory-used", dest="conditions_node_memory_used", help="Memory used by each node in MBs", type=int)

    email = parser.add_argument_group("Email")

    email.add_argument("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type=str)
    email.add_argument("--email-from", dest="email_from", help="The sender email address", type=str)
    email.add_argument("--email-login", dest="email_login", help="The sender email login", type=str)
    email.add_argument("--email-subject", dest="email_subject", help="The email subject", type=str)
    email.add_argument("--email-server", dest="email_server", help="The hostname or IP address of the mail server", type=str)
    email.add_argument("--email-password", dest="email_password", help="The password for the authentication on the mail server", type=str)
    email.add_argument("--email-ssl", dest="email_ssl", help="Use SSL to send email", default=None, action="store_true")

    slack = parser.add_argument_group("Slack")
    slack.add_argument("--slack-url", dest="slack_url", help="Slack hook URL", type=str)
    slack.add_argument("--slack-channel", dest="slack_channel", help="Slack channel to message to", type=str)
    slack.add_argument("--slack-username", dest="slack_username", help="Sender's Slack username", type=str)

    telegram = parser.add_argument_group("Telegram")
    telegram.add_argument("--telegram-bot-id", dest="telegram_bot_id", help="Telegram bot id", type=str)
    telegram.add_argument("--telegram-channel", dest="telegram_channel", help="Telegram channel", type=str)

    return parser


def main():
    log = logger.Logger().get_logger()
    log.info("Starting application...")

    arguments_parser = argumentsparser.ArgumentsParser(log)
    arguments = arguments_parser.parse(setup_arguments())

    client = apiclient.ApiClient(log, arguments)
    notifier_object = notifier.Notifier(log, arguments)
    condition_checker = conditionchecker.ConditionChecker(log, client, notifier_object)

    while True:
        for queue in arguments["server_queues"]:
            arguments["server_queue"] = queue
            queue_conditions = arguments["conditions"][queue]

            if queue_conditions["conditions_ready_queue_size"] is not None \
                    or queue_conditions["conditions_unack_queue_size"] is not None \
                    or queue_conditions["conditions_total_queue_size"] is not None \
                    or queue_conditions["conditions_queue_consumers_connected"] is not None:
                condition_checker.check_queue_conditions(arguments)

        generic_conditions = arguments["generic_conditions"]
        if generic_conditions["conditions_nodes_running"] is not None \
                or generic_conditions["conditions_node_memory_used"] is not None:
            condition_checker.check_node_conditions(arguments)
        if generic_conditions["conditions_open_connections"] is not None:
            condition_checker.check_connection_conditions(arguments)
        if generic_conditions["conditions_consumers_connected"] is not None:
            condition_checker.check_consumer_conditions(arguments)

        time.sleep(arguments["server_check_rate"])


if __name__ == "__main__":
    main()
