#!/bin/bash

version=$1

if [[ -z version ]];then
    echo "missing parameters"
    exit 1
fi

rooms_dir="$(pwd)/src/rooms"
users_csv="$(pwd)/src/users.csv"

docker build -t chatapp:$version .

docker run  -p 5000:5000 -v "$rooms_dir:/src/rooms" -v "$users_csv:/src/users.csv" chatapp:$version