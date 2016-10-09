#!/bin/bash

docker run -d --net host -v /home/linker/cassandra-runtime:/var/lib/cassandra --name cassandra2 cassandra:2.2.5

sleep 2
echo "run cassandra container success!\nThe dir '/home/linker/cassandra-runtime' is used to store cassandra data."
