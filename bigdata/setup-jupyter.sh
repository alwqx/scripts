#!/bin/bash

docker run -d -p 8888:8888 -p 4040:4040 --privileged -e PASSWORD="bigdata" -e GRANT_SUDO=yes --name jupyter -v /home/linker/sample_data:/sample_data:rw -v /home/linker/jupyter-runtime:/home/jovyan/work:rw adolphlwq/docker-jupyter:pyspark-notebook-1.6.0

echo "setup jupyter success!"
