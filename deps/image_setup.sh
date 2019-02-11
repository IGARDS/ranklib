#!/bin/bash

cp /deps/tool_conf.xml /galaxy-central/config/

apt-get update
apt-get install -y python3-pip
pip3 install pyrankability
