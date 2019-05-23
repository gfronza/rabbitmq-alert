#! /usr/bin/python2
# -*- coding: utf-8 -*-

import urllib2
import json
import time
import smtplib

import logger
import optionsresolver


class RabbitMQAlert:

    def __init__(self, log):
        self.log = log

    def check_queue_conditions(self, options):
        queue = options["queue"]
        url = "%s://%s:%s/api/queues/%s/%s" % (options["scheme"], options["host"], options["port"], options["vhost"], options["queue"])
        data = self.send_request(url, options)
        if data is None:
            return

        messages_ready = data.get("messages_ready")
        messages_unacknowledged = data.get("messages_unacknowledged")
        messages = data.get("messages")
        consumers = data.get("consumers")

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
        url = "%s://%s:%s/api/consumers" % (options["scheme"], options["host"], options["port"])
        data = self.send_request(url, options)
        if data is None:
            return

        consumers_connected = len(data)
        consumers_connected_min = options["generic_conditions"].get("consumers_connected")

        if consumers_connected is not None and consumers_connected < consumers_connected_min:
            self.send_notification(options, "consumers_connected = %d < %d" % (consumers_connected, consumers_connected_min))

    def check_connection_conditions(self, options):
        url = "%s://%s:%s/api/connections" % (options["scheme"], options["host"], options["port"])
        data = self.send_request(url, options)
        if data is None:
            return

        open_connections = len(data)

        open_connections_min = options["generic_conditions"].get("open_connections")

        if open_connections is not None and open_connections < open_connections_min:
            self.send_notification(options, "open_connections = %d < %d" % (open_connections, open_connections_min))

    def check_node_conditions(self, options):
        url = "%s://%s:%s/api/nodes" % (options["scheme"], options["host"], options["port"])
        data = self.send_request(url, options)
        if data is None:
            return

        nodes_running = len(data)

        conditions = options["generic_conditions"]
        nodes_run = conditions.get("nodes_running")
        node_memory = conditions.get("node_memory_used")

        if nodes_run is not None and nodes_running < nodes_run:
            self.send_notification(options, "nodes_running = %d < %d" % (nodes_running, nodes_run))

        for node in data:
            if node_memory is not None and node.get("mem_used") > (node_memory * pow(1024, 2)):
                self.send_notification(options, "Node %s - node_memory_used = %d > %d MBs" % (node.get("name"), node.get("mem_used"), node_memory))

    def get_queues(self, options):
        url = "%s://%s:%s/api/queues?page=1&page_size=300" % (options["scheme"], options["host"], options["port"])
        data = self.send_request(url, options)
        if data is None:
            return []

        queues = []
        for queue in data.get("items"):
            queues.append(queue.get("name"))

        if queues:
            self.log.info("Queues discovered: {0}".format(", ".join(queues)))
        else:
            self.log.error("No queues discovered.")

        return queues

    def send_request(self, url, options):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, options["username"], options["password"])
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)

        try:
            request = opener.open(url)
            response = request.read()
            request.close()

            data = json.loads(response)
            return data
        except (urllib2.HTTPError, urllib2.URLError):
            self.log.error("Error while consuming the API endpoint \"{0}\"".format(url))
            return None

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

    rabbitmq_alert = RabbitMQAlert(log)

    opt_resolver = optionsresolver.OptionsResolver(log)
    options = opt_resolver.setup_options()

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
