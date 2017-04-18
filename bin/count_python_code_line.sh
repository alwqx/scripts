#!/bin/bash
if [ "$#" -eq 1 ]
then
  project_dir=$1
else
  project_dir=`pwd`
fi
tot=`find $project_dir -name "*.py" | xargs cat|wc -l`
remove_empty=`find $project_dir -name "*.py" | xargs cat|grep -v ^$|wc -l`
empty=$((tot - remove_empty))

echo "tot lines is: $tot"
echo "remove empty lines is: $remove_empty"
echo "empty lines is: $empty"
