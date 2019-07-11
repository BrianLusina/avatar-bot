#!/usr/bin/env bash

docker build $DOCKER_USERNAME/avatar-bot
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push $DOCKER_USERNAME/avatar-bot