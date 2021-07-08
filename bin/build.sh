#!/usr/bin/env bash

DOCKER_TAG="${IMAGE_REPO_NAME}:master"

docker build -t "${DOCKER_TAG}" .
docker tag "${DOCKER_TAG}" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}"
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}"
