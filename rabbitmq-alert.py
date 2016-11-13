#! /usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from ConfigParser import ConfigParser
import urllib2
import json
import time
import os.path


def setup_options():
    arguments = OptionParser()
    arguments.add_option("-c", "--config-file", dest="config_file", help="Path of the configuration file", type="string", default=None)
    arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string", default="localhost")
    arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string", default="55672")
    arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string", default="rabbitmq")
    arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string", default="rabbitmq")
    arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string", default="celery")
    arguments.add_option("--queue", dest="queue", help="Name of the queue to inspect", type="string", default="celery")
    arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds.", type="int", default=60)

    arguments.add_option("--ready-queue-size", dest="ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--unacknowledged-queue-size", dest="unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--total-queue-size", dest="total_queue_size", help="Size of the Total messages on the queue to alert as warning", type="int", default=0)

    arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")

    options = arguments.parse_args()[0]

    if not options.config_file is None and os.path.isfile(options.config_file):
        config = ConfigParser()
        config.read(options.config_file)

        options.host = get_config_file_option(config, "Server", "host")
        options.port = get_config_file_option(config, "Server", "port")
        options.username = get_config_file_option(config, "Server", "username")
        options.password = get_config_file_option(config, "Server", "password")
        options.vhost = get_config_file_option(config, "Server", "vhost")
        options.queue = get_config_file_option(config, "Server", "queue")
        options.check_rate = float(get_config_file_option(config, "Server", "check_rate"))
        options.ready_queue_size = get_config_file_option(config, "Conditions", "ready_queue_size")
        options.unack_queue_size = get_config_file_option(config, "Conditions", "unack_queue_size")
        options.total_queue_size = get_config_file_option(config, "Conditions", "total_queue_size")
        options.email_to = get_config_file_option(config, "Email", "to")

    return options


def send_notification(param, current_value):
    pass


def run_notification_sender():
    options = setup_options()

    url = "http://%s:%s/api/queues/%s/%s" % (options.host, options.port,
                                             options.vhost, options.queue)

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, options.username, options.password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)

    while True:
        try:
            request = opener.open(url)
            response = request.read()
            request.close()

            ready_size = options.ready_queue_size
            unack_size = options.unack_queue_size
            total_size = options.total_queue_size

            data = json.loads(response)
            messages_ready = data.get('messages_ready')
            messages_unacknowledged = data.get('messages_unacknowledged')
            messages = data.get('messages')

            if ready_size and messages_ready > ready_size:
                send_notification('messages_ready', ready_size)

            if unack_size and messages_unacknowledged > unack_size:
                send_notification('messages_unacknowledged', unack_size)

            if total_size and messages > total_size:
                send_notification('messages', total_size)

            time.sleep(options.check_rate)
        except urllib2.HTTPError, e:
            print "Error code %s hitting %s" % (e.code, url)
            exit(1)


def get_config_file_option(config, section, option):
    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)

    return None


if __name__ == '__main__':
    run_notification_sender()
