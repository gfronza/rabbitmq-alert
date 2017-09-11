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

For now you have to clone the repository:

::

    git clone https://github.com/gfronza/rabbitmq-alert.git

Usage
=====

Execute with options
--------------------

| You can execute ``rabbitmq-alert`` along using the provided options,
  but first take a look at ``--help`` to see whats available
| and the purpose of each option.

Example:

::

    ./rabbitmq-alert.py \
        --host=my-server --port=55672 --username=guest --password=guest \
        --vhost=%2F --queue=my_queue1,my_queue2 --ready-queue-size=3 --check-rate=300 \
        --email-to=admin@example.com --email-from=admin@example.com \
        --email-subject="RabbitMQ alert at %s - %s" --email-server=localhost

Execute with a configuration file
---------------------------------

| Alternatively, you can use a configuration file which is a lot
  cleaner. For the required format, take a look
| at the ``example.ini`` file contained in the project.

Then execute ``rabbitmq-alert`` with the configuration file option:

::

    ./rabbitmq-alert.py -c my_config.ini

| You can also define queue specific conditions in the configuration
  file, in case you want to have fine-tuned options for each queue.
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