#! /usr/bin/python2

from setuptools import setup, find_packages

setup(
    name="rabbitmq-alert",
    packages=find_packages(exclude=["test*"]),
    version="1.0.2",
    description="Send notifications when predefined conditions are met",
    author="Germano Fronza, Kostas Milonas",
    author_email="germano.inf@gmail.com",
    url="https://github.com/gfronza/rabbitmq-alert",
    download_url="https://github.com/gfronza/rabbitmq-alert/tarball/1.0.2",
    keywords=["rabbitmq", "alert", "monitor"],
    classifiers=[]
)
