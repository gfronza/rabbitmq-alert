#! /usr/bin/python2
# -*- coding: utf-8 -*-

import optparse
import ConfigParser
import os.path

CONFIG_FILE_PATH = "/etc/rabbitmq-alert/config.ini"


class OptionsResolver:
    def __init__(self, logger):
        self.log = logger

    def setup_options(self):
        arguments = optparse.OptionParser()
        arguments.add_option("-c", "--config-file", dest="config_file", help="Path of the configuration file", type="string")
        arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string")
        arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string")
        arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string")
        arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string")
        arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string")
        arguments.add_option("--queues", dest="queues", help="List of comma-separated queue names to inspect", type="string")
        arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds.", type="int")

        arguments.add_option("--ready-queue-size", dest="ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type="int")
        arguments.add_option("--unacknowledged-queue-size", dest="unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type="int")
        arguments.add_option("--total-queue-size", dest="total_queue_size", help="Size of the Total messages on the queue to alert as warning", type="int")
        arguments.add_option("--consumers-connected", dest="consumers_connected", help="The number of consumers that should be connected", type="int")
        arguments.add_option("--open-connections", dest="open_connections", help="The number of open connections", type="int")
        arguments.add_option("--nodes-running", dest="nodes_running", help="The number of nodes running", type="int")
        arguments.add_option("--node-memory-used", dest="node_memory_used", help="Memory used by each node in MBs", type="int")

        arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")
        arguments.add_option("--email-from", dest="email_from", help="The sender email address", type="string")
        arguments.add_option("--email-subject", dest="email_subject", help="The email subject", type="string")
        arguments.add_option("--email-server", dest="email_server", help="The hostname or IP address of the mail server", type="string")
        arguments.add_option("--email-password", dest="email_password", help="The password for the authentication on the mail server", type="string")
        arguments.add_option("--email-ssl", dest="email_ssl", help="Use SSL to send email", action="store_true", default=False)
        arguments.add_option("--slack-url", dest="slack_url", help="Slack hook URL", type="string")
        arguments.add_option("--slack-channel", dest="slack_channel", help="Slack channel to message to", type="string")
        arguments.add_option("--slack-username", dest="slack_username", help="Sender's Slack username", type="string")
        arguments.add_option("--telegram-bot-id", dest="telegram_bot_id", help="Telegram bot id", type="string")
        arguments.add_option("--telegram-channel", dest="telegram_channel", help="Telegram channel", type="string")

        cli_arguments = arguments.parse_args()[0]

        # set as defaults the cli argument values
        config_file_options = ConfigParser.ConfigParser(vars(cli_arguments))

        options = dict()
        if os.path.isfile(CONFIG_FILE_PATH) and not cli_arguments.config_file:
            config_file_options.read(CONFIG_FILE_PATH)
            self.log.info("Using configuration file \"{0}\"".format(CONFIG_FILE_PATH))
        elif cli_arguments.config_file:
            self.log.info("Using configuration file \"{0}\"".format(cli_arguments.config_file))
            if not os.path.isfile(cli_arguments.config_file):
                self.log.error("The provided configuration file \"{0}\" does not exist".format(cli_arguments.config_file))
                exit(1)

            config_file_options.read(cli_arguments.config_file)

        options["host"] = cli_arguments.host or config_file_options.get("Server", "host")
        options["port"] = cli_arguments.port or config_file_options.get("Server", "port")
        options["username"] = cli_arguments.username or config_file_options.get("Server", "username")
        options["password"] = cli_arguments.password or config_file_options.get("Server", "password")
        options["vhost"] = cli_arguments.vhost or config_file_options.get("Server", "vhost")
        options["check_rate"] = cli_arguments.check_rate or config_file_options.getfloat("Server", "check_rate")
        options["queues"] = cli_arguments.queues or config_file_options.get("Server", "queues")
        options["queues"] = options["queues"].split(",")

        options["email_to"] = cli_arguments.email_to or (config_file_options.get("Email", "to") if config_file_options.has_section("Email") else None)
        options["email_from"] = cli_arguments.email_from or (config_file_options.get("Email", "from") if config_file_options.has_section("Email") else None)
        options["email_subject"] = cli_arguments.email_subject or (config_file_options.get("Email", "subject") if config_file_options.has_section("Email") else None)
        options["email_server"] = cli_arguments.email_server or (config_file_options.get("Email", "host") if config_file_options.has_section("Email") else None)
        options["email_password"] = cli_arguments.email_password or (config_file_options.get("Email", "password") if config_file_options.has_section("Email") else None)
        options["slack_url"] = cli_arguments.slack_url or (config_file_options.get("Slack", "url") if config_file_options.has_section("Slack") else None)
        options["slack_channel"] = cli_arguments.slack_channel or (config_file_options.get("Slack", "channel") if config_file_options.has_section("Slack") else None)
        options["slack_username"] = cli_arguments.slack_username or (config_file_options.get("Slack", "username") if config_file_options.has_section("Slack") else None)
        options["telegram_bot_id"] = cli_arguments.telegram_bot_id or (config_file_options.get("Telegram", "bot_id") if config_file_options.has_section("Telegram") else None)
        options["telegram_channel"] = cli_arguments.telegram_channel or (config_file_options.get("Telegram", "channel") if config_file_options.has_section("Telegram") else None)
        options["email_to"] = options["email_to"].split(",") if not options["email_to"] is None else None

        if config_file_options.has_section("Email"):
            options["email_ssl"] = config_file_options.getboolean("Email", "ssl")
        else:
            options["email_ssl"] = cli_arguments.email_ssl

        # get queue specific condition values if any, else construct from the generic one
        conditions = OptionsResolver.construct_conditions(options, cli_arguments, config_file_options)
        options = dict(options.items() + conditions.items())

        return options

    @staticmethod
    def construct_conditions(options, cli_arguments, config_file_options):
        conditions = dict()

        # get the generic condition values from the "[Conditions]" section
        default_conditions = dict()
        try:
            default_conditions["ready_queue_size"] = cli_arguments.ready_queue_size or config_file_options.getint("Conditions", "ready_queue_size")
            default_conditions["unack_queue_size"] = cli_arguments.unack_queue_size or config_file_options.getint("Conditions", "unack_queue_size")
            default_conditions["total_queue_size"] = cli_arguments.total_queue_size or config_file_options.getint("Conditions", "total_queue_size")
            default_conditions["consumers_connected"] = cli_arguments.consumers_connected or config_file_options.getint("Conditions", "consumers_connected")
            default_conditions["open_connections"] = cli_arguments.open_connections or config_file_options.getint("Conditions", "open_connections")
            default_conditions["nodes_running"] = cli_arguments.nodes_running or config_file_options.getint("Conditions", "nodes_running")
            default_conditions["node_memory_used"] = cli_arguments.node_memory_used or config_file_options.getint("Conditions", "node_memory_used")
        except:
            pass

        # check if queue specific condition sections exist, if not use the generic conditions
        if "queues" in options:
            for queue in options["queues"]:
                queue_conditions_section_name = "Conditions:" + queue

                try:
                    queue_conditions = dict()
                    queue_conditions["ready_queue_size"] = cli_arguments.ready_queue_size or config_file_options.getint(queue_conditions_section_name, "ready_queue_size")
                    queue_conditions["unack_queue_size"] = cli_arguments.unack_queue_size or config_file_options.getint(queue_conditions_section_name, "unack_queue_size")
                    queue_conditions["total_queue_size"] = cli_arguments.total_queue_size or config_file_options.getint(queue_conditions_section_name, "total_queue_size")
                    queue_conditions["consumers_connected"] = cli_arguments.consumers_connected or config_file_options.getint(queue_conditions_section_name, "consumers_connected")
                    queue_conditions["open_connections"] = cli_arguments.open_connections or config_file_options.getint(queue_conditions_section_name, "open_connections")
                    queue_conditions["nodes_running"] = cli_arguments.nodes_running or config_file_options.getint(queue_conditions_section_name, "nodes_running")
                    queue_conditions["node_memory_used"] = cli_arguments.node_memory_used or config_file_options.getint(queue_conditions_section_name, "node_memory_used")
                    conditions[queue] = queue_conditions
                except:
                    conditions[queue] = default_conditions

        return {"conditions": conditions}
