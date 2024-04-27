#!/bin/bash
sudo docker compose down
sudo docker rmi -f $(sudo docker images -aq)
sudo docker buildx prune -f
sudo docker image prune -f