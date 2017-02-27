#! /bin/bash
# random post request to Mesos and Marathon cluster.

# set -o
# set -x

#declare args
host_url=
marathon_api_url=
instance=
sleep_time=
app_id=

app_json='{
  "id": "/random-job",
  "cmd": null,
  "cpus": 0.01,
  "mem": 32,
  "disk": 0,
  "instances": 0,
  "constraints": [],
  "container": {
    "type": "DOCKER",
    "volumes": [],
    "docker": {
      "image": "alexwhen/docker-2048",
      "network": "BRIDGE",
      "privileged": true,
      "parameters": [],
      "forcePullImage": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp",
          "name": null
        }
      ]
    }
  },
  "env": {},
  "labels": {},
  "healthChecks": []
}'

function abort() {
    printf "\nError: $1\n" && exit 1
}

log() {
  printf "%10s: %s\n" $1 $2
  echo
}

function init() {
    host_url=192.168.10.91:8080
    marathon_api_url=${host_url}/v2/apps
    app_id="random-job"
}

# refer http://stackoverflow.com/questions/24942875/change-json-file-by-bash-script
function configJson() {
    #s=`echo $app_json|jq '.instances'`
    app_json=`jq ".instances = $instance " <<<"$app_json"`
    #o=`echo $app_json|jq '.instances'`
    #echo $s
    #echo $o
}

function checkJQ() {
    if ! command -v $1 > /dev/null;then
        abort "you should install $1"
    fi
}

# refer http://unix.stackexchange.com/questions/140750/generate-random-numbers-in-specific-range
function random_number() {
    instance=$(shuf -i 1-30 -n 1)
    sleep_time=$(shuf -i 120-300 -n 1)
}

function update_job() {
    log update_job "${marathon_url}/${app_id}"
    curl -X "PUT" -H 'Content-Type: application/json' \
        -d "${app_json}" ${marathon_api_url}/${app_id}
    echo
}

function delete_job() {
    log delete_job "${marathon_api_url}/${app_id}"
    curl -X "DELETE" ${marathon_api_url}/${app_id}
    echo
}

function random_sleep() {
    log sleep $sleep_time"s"
    sleep $sleep_time
}

function main() {
    init
    checkJQ jq
    while true
    do
        random_number
        configJson
        update_job
        random_sleep

        delete_job
        random_number
        random_sleep
    done
}

echo "start random-jobs"
main

# refer http://stackoverflow.com/questions/19233529/run-bash-script-as-daemon
# to run as daemon