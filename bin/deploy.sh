#!/usr/bin/env bash

aws ecs update-service --cluster hackerstash --service hackerstash --force-new-deployment
aws ecs wait services-stable --cluster hackerstash --services hackerstash
