#!/bin/bash

cp /ranklib/deps/tool_conf.xml /galaxy-central/config/

cp /ranklib/deps/galaxy.yml /etc/galaxy/galaxy.yml

apt-get update
apt-get install -y software-properties-common
add-apt-repository -y ppa:jonathonf/python-3.6
apt-get update
apt-get install -y python3.6
curl https://bootstrap.pypa.io/get-pip.py | sudo -H python3.6
apt-get install -y python3.6-dev
pip3.6 install pyrankability

ln -s /ranklib /export/galaxy-central/tools/
