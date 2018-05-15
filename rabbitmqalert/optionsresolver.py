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
        arguments.add_option("--protocol", dest="protocol", help="RabbitMQ API protocol", type="string")
        arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string")
        arguments.add_option("--nickname", dest="nickname", help="RabbitMQ nickname", type="string")
        arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string")
        arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string")
        arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string")
        arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string")
        arguments.add_option("--queues", dest="queues", help="List of comma-separated queue names to inspect", type="string")
        arguments.add_option("--queues-check-rate", dest="queues_check_rate", help="Queues check frequency, in seconds", type="int")
        arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds", type="int")

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

        self.cli_arguments = arguments.parse_args()[0]

        # set as defaults the cli argument values
        self.config_file_options = ConfigParser.ConfigParser(vars(self.cli_arguments))

        options = dict()
        if os.path.isfile(CONFIG_FILE_PATH) and not self.cli_arguments.config_file:
            self.config_file_options.read(CONFIG_FILE_PATH)
            self.log.info("Using configuration file \"{0}\"".format(CONFIG_FILE_PATH))
        elif self.cli_arguments.config_file:
            self.log.info("Using configuration file \"{0}\"".format(self.cli_arguments.config_file))
            if not os.path.isfile(self.cli_arguments.config_file):
                self.log.error("The provided configuration file \"{0}\" does not exist".format(self.cli_arguments.config_file))
                exit(1)

            self.config_file_options.read(self.cli_arguments.config_file)

        if self.cli_arguments.config_file is None and not os.path.isfile(CONFIG_FILE_PATH):
            self.log.warn("No configuration file found: default file (%s) not found and not and no --config-file argument provided" % CONFIG_FILE_PATH)

        options["protocol"] = self.cli_arguments.protocol or self.config_file_options.get("Server", "protocol") or "http"
        options["host"] = self.cli_arguments.host or self.config_file_options.get("Server", "host")
        options["nickname"] = self.cli_arguments.nickname or self.config_file_options.get("Server", "nickname") or options["host"]
        options["port"] = self.cli_arguments.port or self.config_file_options.get("Server", "port")
        options["username"] = self.cli_arguments.username or self.config_file_options.get("Server", "username")
        options["password"] = self.cli_arguments.password or self.config_file_options.get("Server", "password")
        options["vhost"] = self.cli_arguments.vhost or self.config_file_options.get("Server", "vhost")
        options["check_rate"] = self.cli_arguments.check_rate or self.config_file_options.getfloat("Server", "check_rate")
        options["queues"] = self.cli_arguments.queues or self.config_file_options.get("Server", "queues")
        options["queues_check_rate"] = self.cli_arguments.queues_check_rate or self.config_file_options.getfloat("Server", "queues_check_rate")
        options["queues"] = options["queues"].split(",")

        options["email_to"] = self.cli_arguments.email_to or (self.config_file_options.get("Email", "to") if self.config_file_options.has_section("Email") else None)
        options["email_from"] = self.cli_arguments.email_from or (self.config_file_options.get("Email", "from") if self.config_file_options.has_section("Email") else None)
        options["email_subject"] = self.cli_arguments.email_subject or (self.config_file_options.get("Email", "subject") if self.config_file_options.has_section("Email") else None)
        options["email_server"] = self.cli_arguments.email_server or (self.config_file_options.get("Email", "host") if self.config_file_options.has_section("Email") else None)
        options["email_password"] = self.cli_arguments.email_password or (self.config_file_options.get("Email", "password") if self.config_file_options.has_section("Email") else None)
        options["slack_url"] = self.cli_arguments.slack_url or (self.config_file_options.get("Slack", "url") if self.config_file_options.has_section("Slack") else None)
        options["slack_channel"] = self.cli_arguments.slack_channel or (self.config_file_options.get("Slack", "channel") if self.config_file_options.has_section("Slack") else None)
        options["slack_username"] = self.cli_arguments.slack_username or (self.config_file_options.get("Slack", "username") if self.config_file_options.has_section("Slack") else None)
        options["telegram_bot_id"] = self.cli_arguments.telegram_bot_id or (self.config_file_options.get("Telegram", "bot_id") if self.config_file_options.has_section("Telegram") else None)
        options["telegram_channel"] = self.cli_arguments.telegram_channel or (self.config_file_options.get("Telegram", "channel") if self.config_file_options.has_section("Telegram") else None)
        options["email_to"] = options["email_to"].split(",") if not options["email_to"] is None else None

        if self.config_file_options.has_section("Email"):
            options["email_ssl"] = self.config_file_options.getboolean("Email", "ssl")
        else:
            options["email_ssl"] = self.cli_arguments.email_ssl

        return self.define_conditions(options, options["queues"])

    def define_conditions(self, options, queues):
        # get queue specific condition values if any, else construct from the generic one
        conditions = OptionsResolver.construct_conditions(queues, self.cli_arguments, self.config_file_options)
        options = dict(options.items() + conditions.items())
        return options


    @staticmethod 
    def construct_int_option(cli_arguments, config_file_options, conditions, section_key, key, default_conditions=None):
        try:
            conditions[key] = getattr(cli_arguments, key) or config_file_options.getint(section_key, key)
        except:
            if default_conditions is not None and key in default_conditions:
                conditions[key] = default_conditions[key]

    @staticmethod
    def construct_conditions(queues, cli_arguments, config_file_options):
        conditions = dict()

        # get the generic condition values from the "[Conditions]" section
        default_conditions = dict()
        for key in ("ready_queue_size", "unack_queue_size", "total_queue_size", "consumers_connected",
                    "queue_consumers_connected", "open_connections", "nodes_running", "node_memory_used"):
            OptionsResolver.construct_int_option(cli_arguments, config_file_options, default_conditions, "Conditions", key)

        # check if queue specific condition sections exist, if not use the generic conditions
        for queue in queues:
            queue_conditions_section_name = "Conditions:" + queue
            queue_conditions = dict()
            conditions[queue] = queue_conditions

            for key in ("ready_queue_size", "unack_queue_size", "total_queue_size", "queue_consumers_connected"):
                OptionsResolver.construct_int_option(cli_arguments, config_file_options, queue_conditions, queue_conditions_section_name, key, default_conditions)

        return {"conditions": conditions, "default_conditions": default_conditions}
