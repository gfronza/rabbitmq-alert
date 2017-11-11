#! /usr/bin/python2

from setuptools import setup, find_packages
from os import path

# remember to push a new tag after changing this!
VERSION = "1.3.1"

DIST_CONFIG_PATH = "rabbitmqalert/config"

DATA_FILES = [
    ("/etc/rabbitmq-alert/", [DIST_CONFIG_PATH + "/config.ini.example"]),
    ("/var/log/rabbitmq-alert/", [])
]


def generate_readme():
    return open("README.rst").read()


def generate_data_files():
    if path.isdir("/etc/systemd/system/"):
        DATA_FILES.append(("/etc/systemd/system/", [DIST_CONFIG_PATH + "/service/rabbitmq-alert.service"]))
    if path.isdir("/etc/init.d/"):
        DATA_FILES.append(("/etc/init.d/", [DIST_CONFIG_PATH + "/service/rabbitmq-alert"]))

    return DATA_FILES

setup(
    name="rabbitmq-alert",
    version=VERSION,
    long_description=generate_readme(),
    packages=find_packages(exclude=["*tests*"]),
    description="Send notifications when predefined conditions are met",
    author="Germano Fronza, Kostas Milonas, velika12",
    author_email="germano.inf@gmail.com",
    url="https://github.com/gfronza/rabbitmq-alert",
    download_url="https://github.com/gfronza/rabbitmq-alert/tarball/"+VERSION,
    keywords=["rabbitmq", "alert", "monitor"],
    classifiers=[],
    entry_points={
        "console_scripts": [
            "rabbitmq-alert = rabbitmqalert:rabbitmqalert.main"
        ]
    },
    data_files=generate_data_files()
)
