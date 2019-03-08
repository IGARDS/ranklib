#!/bin/bash

cp /ranklib/deps/tool_conf.xml /galaxy-central/config/

cp /ranklib/deps/job_conf.xml /etc/galaxy/job_conf.xml
cp /ranklib/deps/job_conf.xml /galaxy-central/config/job_conf.xml

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

# Fix ssh keys
mkdir /root/.ssh
mkdir /home/galaxy/.ssh
cp -Rp /.ssh/id_rsa /home/galaxy/.ssh
cp -Rp /.ssh/id_rsa /root/.ssh
cp -Rp /.ssh/id_rsa.pub /home/galaxy/.ssh
cp -Rp /.ssh/id_rsa.pub /root/.ssh
cp -Rp /.ssh/authorized_keys /home/galaxy/.ssh
cp -Rp /.ssh/authorized_keys /root/.ssh

HOSTNAME=`grep shell_hostname /etc/galaxy/job_conf.xml | awk -F\> '{print $2}' | awk -F\< '{print $1}'`
ssh-keyscan $HOSTNAME >> /root/.ssh/known_hosts
ssh-keyscan $HOSTNAME >> /home/galaxy/.ssh/known_hosts

chown -R galaxy:galaxy /home/galaxy/.ssh
