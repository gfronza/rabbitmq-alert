About RabbitMQ Alert
====================

Send notifications to the staff when predefined conditions are triggered.

(FYI, this is an work in progress)

What conditions?
================

* Ready Messages
* Unacknowledged Messages
* Total Queued Messages

My inspiration to create this notification sender is to monitor a set of Celery workers. Sometimes they stop working and monitoring the queue size seems to be an easy way to know when these situations happen. Additionally, automatically monitoring the queue sizes is a great way to scale up/down the number of workers.


TO DO
=====

* Provide other notification methods, like SMS and/or Jabber.
* Add other trigger conditions.
