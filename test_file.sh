#!bin/bash
DIR=`pwd`
FILE=$DIR/test

if [ ! -d "${FILE}" ]; then
    mkdir ${FILE}
fi
