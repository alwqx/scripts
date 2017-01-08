#! /bin/bash
docker run -d --name owncloud \
-p 9090:80 \
--link postgres:postgres \
--restart always \
-v `pwd`/data:/var/www/html \
owncloud:9.1.3
