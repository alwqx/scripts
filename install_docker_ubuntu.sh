#! /bin/bash

# usage: ./install_docker_ubuntu.sh
# after installed, remind to logout and religin

# install 
sudo apt update
sudo apt -yqq install apt-transport-https ca-certificates

sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

u_v=`lsb_release -cs`
echo "deb https://apt.dockerproject.org/repo ubuntu-${u_v} main" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install -yqq docker-engine
user_=`whoami`
sudo usermod -aG docker $user_
