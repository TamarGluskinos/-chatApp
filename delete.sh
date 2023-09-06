#!/bin/bash

version=$1

if [[ -z version ]];then
    echo "missing parameters"
    exit 1
fi

docker rmi chatapp:$version



