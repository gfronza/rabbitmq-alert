#! /usr/bin/python2

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="rabbitmq-alert",
    version="1.0.3",
    long_description=readme(),
    packages=find_packages(exclude=["test*"]),
    description="Send notifications when predefined conditions are met",
    author="Germano Fronza, Kostas Milonas",
    author_email="germano.inf@gmail.com",
    url="https://github.com/gfronza/rabbitmq-alert",
    download_url="https://github.com/gfronza/rabbitmq-alert/tarball/1.0.2",
    keywords=["rabbitmq", "alert", "monitor"],
    classifiers=[]
)
