#!/bin/bash

echo "Docker Containers:"
docker ps -a

echo "Docker Images:"
docker images

echo "Docker Volumes:"
docker volume ls

echo "Docker Networks:"
docker network ls
