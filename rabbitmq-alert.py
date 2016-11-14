#! /usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import urllib2
import json
import time
import smtplib


def setup_options():
    arguments = OptionParser()
    arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string", default="localhost")
    arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string", default="55672")
    arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string", default="rabbitmq")
    arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string", default="rabbitmq")
    arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string", default="celery")
    arguments.add_option("--queues", dest="queues", help="List of comma-separated queue names to inspect", type="string", default="celery")

    arguments.add_option("--ready-queue-size", dest="ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--unacknowledged-queue-size", dest="unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--total-queue-size", dest="total_queue_size", help="Size of the Total messages on the queue to alert as warning", type="int", default=0)

    arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds.", type="int", default=60)
    arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")
    arguments.add_option("--email-from", dest="email_from", help="The sender email address", type="string")
    arguments.add_option("--email-server", dest="email_server", help="The hostname or IP address of the mail server", type="string", default="localhost")

    return arguments.parse_args()[0]


def send_notification(options, param, current_value):
    msgText = "%s - %s:\n\"%s\" > %s" % (options.host, options.queue, param, str(current_value))

    server = smtplib.SMTP(options.email_server, 25)

    recipients = options.email_to.split(",")
    server.sendmail(options.email_from, recipients, msgText)

    server.quit()


def run_notification_sender(options):
    url = "http://%s:%s/api/queues/%s/%s" % (options.host, options.port, options.vhost, options.queue)

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, options.username, options.password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)

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
            send_notification(options, 'messages_ready', ready_size)

        if unack_size and messages_unacknowledged > unack_size:
            send_notification(options, 'messages_unacknowledged', unack_size)

        if total_size and messages > total_size:
            send_notification(options, 'messages', total_size)

    except urllib2.HTTPError, e:
        print "Error code %s hitting %s" % (e.code, url)
        exit(1)


if __name__ ==  '__main__':
    options = setup_options()

    queues_list = options.queues.split(',')
    while True:
        for queue in queues_list:
            options.queue = queue
            run_notification_sender(options)

        time.sleep(options.check_rate)
