#! /bin/bash
exited_containers=$(docker ps -a | grep Exited | wc -l)
if [[ ${exited_containers=} -eq 0 ]];then
    echo "no exited docker container."
else
    docker ps -a | grep Exited | awk '{print $1}' | xargs docker rm
fi
