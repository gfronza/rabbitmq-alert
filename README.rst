About RabbitMQ Alert
====================

Send notifications when predefined conditions are met.

Which conditions?
=================

-  Ready messages
-  Unacknowledged messages
-  Total queued messages
-  Number of connected consumers
-  Number of open connections
-  Number of nodes running
-  Memory used by each node in MBs

| My inspiration to create this notification sender is to monitor a set
  of Celery workers. Sometimes they stop working and monitoring
| the queue size seems to be an easy way to know when these situations
  happen. Additionally, automatically monitoring the queue sizes
| is a great way to scale up/down the number of workers.

What type of notifications?
===========================

Currently the following are supported:

-  E-mails
-  Slack messages
-  Telegram messages

Installation
============

Use the ``PIP`` command, which should already exist in your Linux installation:

::

    sudo pip install rabbitmq-alert

Usage
=====

Execute with the global configuration file
------------------------------------------
Copy the example configuration file to the default path of the global configuration file:

::

    sudo cp /etc/rabbitmq-alert/config.ini.example /etc/rabbitmq-alert/config.ini

| Edit it with you preferred settings. Then you are ready to execute ``rabbitmq-alert``
| using the global configuration file. Just execute:

::

    sudo rabbitmq-alert

Execute with options
--------------------

| You can execute ``rabbitmq-alert`` along using the provided options,
  but first take a look at ``--help`` to see whats available
| and the purpose of each option.

Example:

::

    sudo rabbitmq-alert \
        --host=my-server --port=55672 --username=guest --password=guest \
        --vhost=%2F --queue=my_queue1,my_queue2 --ready-queue-size=3 --check-rate=300 \
        --email-to=admin@example.com --email-from=admin@example.com \
        --email-subject="RabbitMQ alert at %s - %s" --email-server=localhost

Execute with a custom configuration file
----------------------------------------

| Alternatively, you can use a custom configuration file.
  For the required format, take a look
| at the ``/etc/rabbitmq-alert/config.ini.example`` file.

Then execute ``rabbitmq-alert`` with the configuration file option:

::

    sudo rabbitmq-alert -c my_config.ini

Execute as a daemon
-------------------

| A ``systemd`` script is created upon installation with ``PIP``.
| Use the following commands to reload the ``systemd`` configuration
| and start ``rabbitmq-alert`` as a daemon.

::

    sudo systemctl daemon-reload
    sudo systemctl start rabbitmq-alert

Different options per queue
---------------------------
| Except conditions for all queues, you can also define queue specific conditions
| in the configuration file, in case you want to have fine-tuned options for each queue.
| Just create a ``[Conditions]`` section for each queue. Example:

::

    [Conditions:my-queue]
    ...

    [Conditions:my-other-queue]
    ...

Note that queue names also have to be defined in the ``[Server]``
section of the configuration file:

::

    [Server]
    ...
    queues=my-queue,my-other-queue
    ...

Logging
-------

| You can find the logs of ``rabbitmq-alert`` to ``/var/log/rabbitmq-alert/``.
| Log files are rotated in a daily basis.

Execute in a container
----------------------

| There is a docker image for the project. First, you have to create a configuration file
| for ``rabbitmq-alert``, which will then be copied into the container. Then you can run
| ``rabbitmq-alert`` inside a container.

::

    docker run -d --name rabbitmq-alert -v config.ini:/etc/rabbitmq-alert/config.ini mylkoh/rabbitmq-alert:latest

For the configuration file, advise the ``config.ini.example`` that exists in the project's repository.

Contribute
==========

| The project ``rabbitmq-alert`` is written in ``python2``.
| Of course, you can contribute to the project. Take a look at the
  GitHub “Issues” page and pick an issue to implement / fix.
| Fork the project, develop and then create a pull request, in order for
  your code to be added to the project.

Prepare your environment
------------------------

To start, you have to install the dev dependencies which are some
required python packages:

::

    make deps-dev

Run the tests!
--------------

After writing your awesomeness, run the test suites to ensure that
everything is still fine:

::

    make test

Do add tests yourself for the code you contribute to ensure the quality
of the project.

Happy coding :-)

Build and publish a new container version
-----------------------------------------

To build a new image version of the project:

::

    docker build --no-cache -t mylkoh/rabbitmq-alert:1.2.2 -t mylkoh/rabbitmq-alert:latest .

Publish the image:

::

    docker push mylkoh/rabbitmq-alert

Testing the container
---------------------

Create a network that all containers will belong to:

::

    docker network create rabbitmq-alert


Run ``rabbitmq`` into a container:

::

    docker run -d --name some-rabbit --net rabbitmq-alert -p 8080:15672 rabbitmq:3-management

| You can then go to http://localhost:8080 in a browser to use the management plugin.
| The username and password are both ``guest``. Create a fake SMTP server:

::

    docker run -d --name fake-smtp --net rabbitmq-alert -p 25:25 munkyboy/fakesmtp

Now, run ``rabbitmq-alert`` using the same network:

::

    docker run -d --name rabbitmq-alert --net rabbitmq-alert -v config.ini:/etc/rabbitmq-alert/config.ini mylkoh/rabbitmq-alert:latest
