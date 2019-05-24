#! /usr/bin/python2
# -*- coding: utf-8 -*-

import urllib2
import json
import time
import smtplib

import apiclient
import logger
import optionsresolver


class RabbitMQAlert:

    def __init__(self, log, client):
        self.log = log
        self.client = client

    def check_queue_conditions(self, options):
        response = self.client.get_queue()
        if response is None:
            return

        messages_ready = response.get("messages_ready")
        messages_unacknowledged = response.get("messages_unacknowledged")
        messages = response.get("messages")
        consumers = response.get("consumers")

        queue = options["queue"]
        queue_conditions = options["conditions"][queue]
        ready_size = queue_conditions.get("ready_queue_size")
        unack_size = queue_conditions.get("unack_queue_size")
        total_size = queue_conditions.get("total_queue_size")
        consumers_connected_min = queue_conditions.get("queue_consumers_connected")

        if ready_size is not None and messages_ready > ready_size:
            self.send_notification(options, "%s: messages_ready = %d > %d" % (queue, messages_ready, ready_size))

        if unack_size is not None and messages_unacknowledged > unack_size:
            self.send_notification(options, "%s: messages_unacknowledged = %d > %d" % (queue, messages_unacknowledged, unack_size))

        if total_size is not None and messages > total_size:
            self.send_notification(options, "%s: messages = %d > %d" % (queue, messages, total_size))

        if consumers_connected_min is not None and consumers < consumers_connected_min:
            self.send_notification(options, "%s: consumers_connected = %d < %d" % (queue, consumers, consumers_connected_min))

    def check_consumer_conditions(self, options):
        response = self.client.get_consumers()
        if response is None:
            return

        consumers_connected = len(response)
        consumers_connected_min = options["generic_conditions"].get("consumers_connected")

        if consumers_connected is not None and consumers_connected < consumers_connected_min:
            self.send_notification(options, "consumers_connected = %d < %d" % (consumers_connected, consumers_connected_min))

    def check_connection_conditions(self, options):
        response = self.client.get_connections()
        if response is None:
            return

        open_connections = len(response)

        open_connections_min = options["generic_conditions"].get("open_connections")

        if open_connections is not None and open_connections < open_connections_min:
            self.send_notification(options, "open_connections = %d < %d" % (open_connections, open_connections_min))

    def check_node_conditions(self, options):
        response = self.client.get_nodes()
        if response is None:
            return

        nodes_running = len(response)

        conditions = options["generic_conditions"]
        nodes_run = conditions.get("nodes_running")
        node_memory = conditions.get("node_memory_used")

        if nodes_run is not None and nodes_running < nodes_run:
            self.send_notification(options, "nodes_running = %d < %d" % (nodes_running, nodes_run))

        for node in response:
            if node_memory is not None and node.get("mem_used") > (node_memory * pow(1024, 2)):
                self.send_notification(options, "Node %s - node_memory_used = %d > %d MBs" % (node.get("name"), node.get("mem_used"), node_memory))

    def send_notification(self, options, body):
        text = "%s - %s" % (options["host_alias"] or options["host"], body)

        if "email_to" in options and options["email_to"]:
            self.log.info("Sending email notification: \"{0}\"".format(body))

            server = smtplib.SMTP(options["email_server"], 25)

            if "email_ssl" in options and options["email_ssl"]:
                server = smtplib.SMTP_SSL(options["email_server"], 465)

            if "email_password" in options and options["email_password"]:
                server.login(options["email_from"], options["email_password"])

            recipients = options["email_to"]
            # add subject as header before message text
            subject_email = options["email_subject"] % (options["host_alias"] or options["host"], options["queue"])
            text_email = "Subject: %s\n\n%s" % (subject_email, text)
            server.sendmail(options["email_from"], recipients, text_email)

            server.quit()

        if "slack_url" in options and options["slack_url"] and "slack_channel" in options and options["slack_channel"] and "slack_username" in options and options["slack_username"]:
            self.log.info("Sending Slack notification: \"{0}\"".format(body))

            # escape double quotes from possibly breaking the slack message payload
            text_slack = text.replace("\"", "\\\"")
            slack_payload = '{"channel": "#%s", "username": "%s", "text": "%s"}' % (options["slack_channel"], options["slack_username"], text_slack)

            request = urllib2.Request(options["slack_url"], slack_payload)
            response = urllib2.urlopen(request)
            response.close()

        if "telegram_bot_id" in options and options["telegram_bot_id"] and "telegram_channel" in options and options["telegram_channel"]:
            self.log.info("Sending Telegram notification: \"{0}\"".format(body))

            text_telegram = "%s: %s" % (options["queue"], text)
            telegram_url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (options["telegram_bot_id"], options["telegram_channel"], text_telegram)

            request = urllib2.Request(telegram_url)
            response = urllib2.urlopen(request)
            response.close()


def main():
    log = logger.Logger().get_logger()
    log.info("Starting application...")

    opt_resolver = optionsresolver.OptionsResolver(log)
    options = opt_resolver.setup_options()

    client = apiclient.ApiClient(log, options)
    rabbitmq_alert = RabbitMQAlert(log, client)

    while True:
        for queue in options["queues"]:
            options["queue"] = queue
            queue_conditions = options["conditions"][queue]

            if "ready_queue_size" in queue_conditions \
                    or "unack_queue_size" in queue_conditions \
                    or "total_queue_size" in queue_conditions \
                    or "queue_consumers_connected" in queue_conditions:
                rabbitmq_alert.check_queue_conditions(options)

        # common checks for all queues
        generic_conditions = options["generic_conditions"]
        if "nodes_running" in generic_conditions or "node_memory_used" in generic_conditions:
            rabbitmq_alert.check_node_conditions(options)
        if "open_connections" in generic_conditions:
            rabbitmq_alert.check_connection_conditions(options)
        if "consumers_connected" in generic_conditions:
            rabbitmq_alert.check_consumer_conditions(options)

        time.sleep(options["check_rate"])


if __name__ == "__main__":
    main()
