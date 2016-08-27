#!/bin/bash
DATA_DIR=$1
STORE_DIR=$2
tar zcvf ${STORE_DIR}/ghost_content_data_`date "+%Y_%m_%d_%H_%M_%S"`.tar.gz ${DATA_DIR}
