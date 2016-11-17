#! /usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from ConfigParser import ConfigParser
import urllib2
import json
import time
import os.path
import smtplib

def setup_options():
    arguments = OptionParser()
    arguments.add_option("-c", "--config-file", dest="config_file", help="Path of the configuration file", type="string", default=None)
    arguments.add_option("--host", dest="host", help="RabbitMQ API address", type="string", default="localhost")
    arguments.add_option("--port", dest="port", help="RabbitMQ API port", type="string", default="55672")
    arguments.add_option("--username", dest="username", help="RabbitMQ API username", type="string", default="rabbitmq")
    arguments.add_option("--password", dest="password", help="RabbitMQ API password", type="string", default="rabbitmq")
    arguments.add_option("--vhost", dest="vhost", help="Name of the vhost to inspect", type="string", default="celery")
    arguments.add_option("--queues", dest="queues", help="List of comma-separated queue names to inspect", type="string", default="celery")
    arguments.add_option("--check-rate", dest="check_rate", help="Conditions check frequency, in seconds.", type="int", default=60)

    arguments.add_option("--ready-queue-size", dest="ready_queue_size", help="Size of Ready messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--unacknowledged-queue-size", dest="unack_queue_size", help="Size of the Unacknowledged messages on the queue to alert as warning", type="int", default=0)
    arguments.add_option("--total-queue-size", dest="total_queue_size", help="Size of the Total messages on the queue to alert as warning", type="int", default=0)

    arguments.add_option("--email-to", dest="email_to", help="List of comma-separated email addresses to send notification to", type="string")
    arguments.add_option("--email-from", dest="email_from", help="The sender email address", type="string")
    arguments.add_option("--email-subject", dest="email_subject", help="The email subject", type="string")
    arguments.add_option("--email-server", dest="email_server", help="The hostname or IP address of the mail server", type="string", default="localhost")
    arguments.add_option("--slack-url", dest="slack_url", help="Slack hook URL", type="string")
    arguments.add_option("--slack-channel", dest="slack_channel", help="Slack channel to message to", type="string")
    arguments.add_option("--slack-username", dest="slack_username", help="Sender's Slack username", type="string")

    options = arguments.parse_args()[0]

    if not options.config_file is None and os.path.isfile(options.config_file):
        # set as defaults the values or the defaults of OptionParser
        config = ConfigParser(vars(options))
        config.read(options.config_file)

        options.host = config.get("Server", "host")
        options.port = config.get("Server", "port")
        options.username = config.get("Server", "username")
        options.password = config.get("Server", "password")
        options.vhost = config.get("Server", "vhost")
        options.queues = config.get("Server", "queues")
        options.check_rate = float(config.get("Server", "check_rate"))
        options.ready_queue_size = int(config.get("Conditions", "ready_queue_size"))
        options.unack_queue_size = int(config.get("Conditions", "unack_queue_size"))
        options.total_queue_size = int(config.get("Conditions", "total_queue_size"))
        options.email_to = config.get("Email", "to")
        options.email_from = config.get("Email", "from")
        options.email_subject = config.get("Email", "subject")
        options.email_server = config.get("Email", "host")
        options.slack_url = config.get("Slack", "url")
        options.slack_channel = config.get("Slack", "channel")
        options.slack_username = config.get("Slack", "username")

    return options

def send_notification(options, param, current_value):
    text = "%s - %s:\n\"%s\" > %s" % (options.host, options.queue, param, str(current_value))
    
    if options.email_to:
        server = smtplib.SMTP(options.email_server, 25)

        recipients = options.email_to.split(",")
        # add subject as header before message text
        subject_email = options.email_subject % (options.host, options.queue)
        text_email = "Subject: %s\n\n%s" % (subject_email, text)
        server.sendmail(options.email_from, recipients, text_email)

        server.quit()

    if options.slack_url and options.slack_channel and options.slack_username:
        # escape double quotes from possibly breaking the slack message payload
        text_slack = text.replace("\"", "\\\"")
        slack_payload = '{"channel": "#%s", "username": "%s", "text": "%s"}' % (options.slack_channel, options.slack_username, text_slack)

        request = urllib2.Request(options.slack_url, slack_payload)
        response = urllib2.urlopen(request)
        response.close()

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
