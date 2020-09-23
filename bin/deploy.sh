#!/usr/bin/env bash

BRANCH=${CODEBUILD_WEBHOOK_TRIGGER:7}  #Remove branch/

if [[ "${BRANCH}" == 'master' ]]; then
  SERVICE="hackerstash"
elif [[ "${BRANCH}" == 'add-stripe' ]]; then
  SERVICE="hackerstash-staging"
else
  exit 0
fi

aws ecs update-service --cluster hackerstash --service "${SERVICE}" --force-new-deployment
aws ecs wait services-stable --cluster hackerstash --services "${SERVICE}"
