#! /bin/bash
docker run -d --net host --name cda -v `pwd`/data:/var/lib/cassandra \
    dockerq/container-cassandra
