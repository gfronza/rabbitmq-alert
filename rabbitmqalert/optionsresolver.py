#! /usr/bin/python2
# -*- coding: utf-8 -*-

import optparse
import ConfigParser
import os.path


class OptionsResover:
    @staticmethod
    def setup_options():
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
        arguments.add_option("--nodes-running", dest="nodes_running", help="The number of nodes running", type="int")
        arguments.add_option("--node-memory-used", dest="node_memory_used", help="Memory used by each node in MBs", type="int")

        arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")
        arguments.add_option("--email-from", dest="email_from", help="The sender email address", type="string")
        arguments.add_option("--email-subject", dest="email_subject", help="The email subject", type="string")
        arguments.add_option("--email-server", dest="email_server", help="The hostname or IP address of the mail server", type="string")
        arguments.add_option("--slack-url", dest="slack_url", help="Slack hook URL", type="string")
        arguments.add_option("--slack-channel", dest="slack_channel", help="Slack channel to message to", type="string")
        arguments.add_option("--slack-username", dest="slack_username", help="Sender's Slack username", type="string")

        options = arguments.parse_args()[0]

        if options.config_file:
            if not os.path.isfile(options.config_file):
                print "The provided configuration file does not exist."
                exit(1)

            # set as defaults the values or the defaults of OptionParser
            config = ConfigParser.ConfigParser(vars(options))
            config.read(options.config_file)

            options.host = options.host or config.get("Server", "host")
            options.port = options.port or config.get("Server", "port")
            options.username = options.username or config.get("Server", "username")
            options.password = options.password or config.get("Server", "password")
            options.vhost = options.vhost or config.get("Server", "vhost")
            options.queues = options.queues or config.get("Server", "queues")
            options.check_rate = options.check_rate or config.getfloat("Server", "check_rate")
            options.ready_queue_size = options.ready_queue_size or config.getint("Conditions", "ready_queue_size")
            options.unack_queue_size = options.unack_queue_size or config.getint("Conditions", "unack_queue_size")
            options.total_queue_size = options.total_queue_size or config.getint("Conditions", "total_queue_size")
            options.consumers_connected = options.consumers_connected or config.getint("Conditions", "consumers_connected")
            options.nodes_running = options.nodes_running or config.getint("Conditions", "nodes_running")
            options.node_memory_used = options.node_memory_used or config.getint("Conditions", "node_memory_used")
            options.email_to = options.email_to or config.get("Email", "to")
            options.email_from = options.email_from or config.get("Email", "from")
            options.email_subject = options.email_subject or config.get("Email", "subject")
            options.email_server = options.email_server or config.get("Email", "host")
            options.slack_url = options.slack_url or config.get("Slack", "url")
            options.slack_channel = options.slack_channel or config.get("Slack", "channel")
            options.slack_username = options.slack_username or config.get("Slack", "username")

        return options
