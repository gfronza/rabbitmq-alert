#!/bin/bash
sudo apt-get update
sudo apt-get -y install python-virtualenv

deb http://www.rabbitmq.com/debian/ testing main

wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc

sudo apt-get -y install rabbitmq-server
rm -f rabbitmq-signing-key-public.asc