#!/usr/bin/env bash

BRANCH=${CODEBUILD_WEBHOOK_TRIGGER:7}  #Remove branch/

if [[ "${BRANCH}" == 'master' ]]; then
  DOCKER_TAG="${IMAGE_REPO_NAME}:master"
else
  DOCKER_TAG="${IMAGE_REPO_NAME}:dev-${BRANCH}"
fi

echo "$DOCKER_TAG"

docker build -t "${DOCKER_TAG}" .
docker tag "${DOCKER_TAG}" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}"
docker tag "${DOCKER_TAG}" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}-${CODEBUILD_BUILD_NUMBER}"
docker run "${DOCKER_TAG}" python -m 'scripts.build_assets'
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}"
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${DOCKER_TAG}-${CODEBUILD_BUILD_NUMBER}"

if [[ "${BRANCH}" == 'master' ]]; then
  docker tag "${DOCKER_TAG}" "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${IMAGE_REPO_NAME}"
  docker push "${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${IMAGE_REPO_NAME}"
fi
