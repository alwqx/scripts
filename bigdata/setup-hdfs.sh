#!/bin/bash
datanode_dir=$1
docker run -d --name hdfs --net host --privileged -e SSH_PORT=2221 -v $datanode_dir:/hdfsdata:rw dockerq/docker-hdfs 
