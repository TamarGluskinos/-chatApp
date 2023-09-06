#!/bin/bash

version=$1
commit_hash=$2

if [[ -z $version || -z $commit_hash ]]; then
    echo "missing parameters"
    exit 1
fi

docker build -t chatapp:$version .

git tag $version $commit_hash

git push origin $version

