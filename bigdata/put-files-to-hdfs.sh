#!/bin/bash
base_dir=/sample_data
metrics=("cpu" "disk" "inventory.all" "log" "smart")
machines=("0c0e2dee9962b313e33a7d9740e161fa" "6f240a3c74ba9cba393a10260a8c05f8" "748d169f28c55c242b7fa61393d902d1" "7d183e93d67d71c123017b0c23a18de3" "c2ace5645bc2097dfcba3b74fe534cf0")
declare -a dirs

function generate_base_dirs(){
#    declare -a dir
    i=0
    for metric in "${metrics[@]}"
    do
        for machine in "${machines[@]}"
        do
#            echo $base_dir/$metric/$machine
            dirs[$i]=$base_dir/$metric/$machine
            i=`expr $i+1`
        done
    done
}

function put_files_hdfs(){
    for dir in "${dirs[@]}"
    do
        hdfs dfs -mkdir -p $dir
        hdfs dfs -put $dir/* $dir
    done
    echo "put all files to hdfs"
}

function list_dirs(){
    for dir in "${dirs[@]}"
    do
        echo $dir
    done
}

generate_base_dirs
put_files_hdfs
