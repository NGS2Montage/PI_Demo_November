#!/bin/bash

sudo apt-get update
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
sudo apt-get install python-setuptools
sudo apt-get upgrade ssh

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo apt-get install python-dev
sudo apt install libicu-dev
sudo apt-get install libgrib-api-dev
sudo apt-get install python-virtualenv
sudo apt-get install fort77
sudo apt-get install sendmail
sudo apt-get install php
sudo apt-get install python-tk
sudo apt-get install git

