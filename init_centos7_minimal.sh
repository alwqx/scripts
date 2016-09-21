#!/bin/bash

#
# This script aims to install nessary softwares after install centos 7 minimal
# refer http://computingforgeeks.com/top-things-to-do-after-fresh-installation-of-centos-7-x-minimal/
#

# for centos 6
#sudo rpm -iUvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm

#for centos 7
sudo yum install epel-release
sudo yum update
sudo yum install -y net-tools python-pip tmux
sudo pip install virtualenv

sudo sed -i 's/(^SELINUX=).*/SELINUX=disabled/' /etc/selinux/config
