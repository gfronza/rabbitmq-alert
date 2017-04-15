#! /usr/bin/python2

from distutils.core import setup

setup(
    name = "rabbitmq-alert",
    packages = ["rabbitmqalert"],
    version = "1.0",
    description = "Send notifications when predefined conditions are met",
    author = "Germano Fronza, Kostas Milonas",
    author_email = "germano.inf@gmail.com",
    url = "https://github.com/gfronza/rabbitmq-alert",
    download_url = "https://github.com/gfronza/rabbitmq-alert/tarball/1.0",
    keywords = ["rabbitmq", "alert", "monitor"],
    classifiers = []
)
