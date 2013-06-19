# -*- coding: utf-8 -*-
from optparse import OptionParser
import urllib2
import json
import time


def setup_options():
    arguments = OptionParser()
    arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string", default="localhost")
    arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string", default="55672")
    arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string", default="rabbitmq")
    arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string", default="rabbitmq")
    arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string", default="celery")
    arguments.add_option("--queue", dest="queue", help="Name of the queue to inspect", type="string", default="celery")

    arguments.add_option("--ready-queue-size", dest="ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--unacknowledged-queue-size", dest="unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--total-queue-size", dest="total_queue_size", help="Size of the Total messages on the queue to alert as warning", type="int", default=0)

    arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds.", type="int", default=60)
    arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")

    return arguments.parse_args()[0]


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


if __name__ == '__main__':
    run_notification_sender()
