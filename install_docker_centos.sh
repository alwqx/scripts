#!/bin/bash
sudo yum update

sudo tee /etc/yum.repos.d/docker.repo <<- 'add_docker_repo'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
add_docker_repo

sudo yum install docker-engine-1.12.1-1.el7.centos
sudo usermod -aG docker linker
sudo service docker start
