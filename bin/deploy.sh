#!/usr/bin/env bash

BRANCH=${CODEBUILD_WEBHOOK_TRIGGER:7}  #Remove branch/

if [[ "${BRANCH}" == 'master' ]]; then
  CLUSTER="prod"
elif [[ "${BRANCH}" == 'caching' ]]; then
  CLUSTER="staging"
else
  exit 0
fi

aws ecs update-service --cluster "${CLUSTER}" --service "hackerstash" --force-new-deployment
aws ecs wait services-stable --cluster "${CLUSTER}" --services "hackerstash"
