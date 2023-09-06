#!/bin/bash

docker rm -f $(docker ps -a -q)

# Deleting all images
docker rmi -f $(docker images -aq) .