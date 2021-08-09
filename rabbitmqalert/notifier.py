import datetime
import smtplib

import requests
import urllib2


class Notifier:

    def __init__(self, logger, arguments):
        self.log = logger
        self.arguments = arguments

    def send_notification(self, body):
        text = "%s - %s" % (self.arguments["server_host_alias"] or self.arguments["server_host"], body)

        if self.arguments["email_to"]:
            self.log.info("Sending email notification: \"{0}\"".format(body))

            server = smtplib.SMTP(self.arguments["email_server"], 25)

            if self.arguments["email_ssl"]:
                server = smtplib.SMTP_SSL(self.arguments["email_server"], 465)

            if self.arguments["email_password"]:
                if self.arguments["email_login"]:
                    server.login(self.arguments["email_login"], self.arguments["email_password"])
                else:
                    server.login(self.arguments["email_from"], self.arguments["email_password"])

            email_from = self.arguments["email_from"]
            recipients = self.arguments["email_to"]
            # add subject as header before message text
            subject_email = self.arguments["email_subject"] % (self.arguments["server_host_alias"] or self.arguments["server_host"], self.arguments["server_queue"])
            text_email = "From: %s\nSubject: %s\n\n%s" % (email_from, subject_email, text)
            server.sendmail(email_from, recipients, text_email)
            server.quit()

        if self.arguments["slack_url"] and self.arguments["slack_channel"] and self.arguments["slack_username"]:
            self.log.info("Sending Slack notification: \"{0}\"".format(body))

            # escape double quotes from possibly breaking the slack message payload
            text_slack = text.replace("\"", "\\\"")
            slack_payload = '{"channel": "#%s", "username": "%s", "text": "%s"}' % (self.arguments["slack_channel"], self.arguments["slack_username"], text_slack)

            request = urllib2.Request(self.arguments["slack_url"], slack_payload)
            response = urllib2.urlopen(request)
            response.close()

        if self.arguments["telegram_bot_id"] and self.arguments["telegram_channel"]:
            self.log.info("Sending Telegram notification: \"{0}\"".format(body))

            text_telegram = "- <b>Time</b>: {0}\n" \
                            "- <b>Server</b>: {1}\n" \
                            "- <b>Queue</b>: {2}\n" \
                            "- <b>Message</b>: {3}\n".format(datetime.datetime.now(), self.arguments["server_host_alias"], self.arguments["server_queue"], body)
            data = {
                'chat_id': self.arguments["telegram_channel"],
                'text': text_telegram[0:4090],
                'parse_mode': 'HTML'
            }
            telegram_url = "https://api.telegram.org/bot%s/sendMessage" % (self.arguments["telegram_bot_id"])

            request = requests.post(telegram_url, data=data, allow_redirects=True)
            if request.status_code != 200:
                self.log.info("Sending Telegram notification: \"{0}\"".format(request.text))
