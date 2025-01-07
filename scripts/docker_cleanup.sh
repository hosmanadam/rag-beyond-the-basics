#!/bin/bash

export IMAGE="rag-beyond-the-basics-chainlit-gui"
docker rm -f $(docker ps -a -q --filter "ancestor=$IMAGE") || echo "No containers are using $IMAGE"
docker rmi -f $IMAGE
