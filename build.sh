#!/usr/bin/env bash
BRANCH=${1:7}
echo $BRANCH
echo $CODEBUILD_WEBHOOK_TRIGGER
#docker build -t $IMAGE_REPO_NAME .
#- docker tag $IMAGE_REPO_NAME ${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/$IMAGE_REPO_NAME
#- docker run $IMAGE_REPO_NAME python -m 'scripts.build_assets'
#- docker push ${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/$IMAGE_REPO_NAME