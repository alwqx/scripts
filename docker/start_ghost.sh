#!/bin/bash
docker run -d --name ghost-prod -p 2368:2368 \
    -v `pwd`/content:/opt/ghost/content ghost-prod
