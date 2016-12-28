#! /bin/bash

docker run -d -p 8888:8888 -v `pwd`:/home/jovyan/work --name jupyter \
    -e PASSWORD=pass --user root \
    adolphlwq/docker-jupyter:pyspark-notebook-1.6.0
