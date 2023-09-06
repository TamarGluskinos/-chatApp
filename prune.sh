#!/bin/bash

read -p "This will prune all containers, images, volumes, and networks. Are you sure? (y/n): " confirm

if [ "$confirm" != "y" ]; then
  echo "Prune canceled."
  exit 1
fi

docker container prune -f

docker image prune -af

docker volume prune -f

docker network prune -f

echo "Pruning completed."
