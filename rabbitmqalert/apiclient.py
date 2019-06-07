import urllib2
import json


class ApiClient:

    def __init__(self, log, arguments):
        self.log = log
        self.arguments = arguments

    def get_queue(self):
        uri = "/api/queues/%s/%s" % (self.arguments["server_vhost"], self.arguments["server_queue"])
        data = self.send_request(uri)

        return data

    def get_queues(self):
        uri = "/api/queues?page=1&page_size=300"
        data = self.send_request(uri)
        if data is None:
            self.log.error("No queues discovered (request failed).")
            return []

        queues = []
        for queue in data.get("items"):
            queues.append(queue.get("name"))

        if queues:
            self.log.info("Queues discovered: {0}".format(", ".join(queues)))
        else:
            self.log.error("No queues discovered.")

        return queues

    def get_connections(self):
        uri = "/api/connections"
        data = self.send_request(uri)

        return data

    def get_consumers(self):
        uri = "/api/consumers"
        data = self.send_request(uri)

        return data

    def get_nodes(self):
        uri = "/api/nodes"
        data = self.send_request(uri)

        return data

    def send_request(self, uri):
        url = "%s://%s:%s%s" % (self.arguments["server_scheme"], self.arguments["server_host"], self.arguments["server_port"], uri)

        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, self.arguments["server_username"], self.arguments["server_password"])
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)

        try:
            request = opener.open(url)
            response = request.read()
            request.close()

            return json.loads(response)
        except (urllib2.HTTPError, urllib2.URLError):
            self.log.error("Error while consuming the API endpoint \"{0}\"".format(url))
            return None
