#! /bin/bash
docker run --name postgres \
-e POSTGRES_PASSWORD=pass \
-e POSTGRES_USER=user \
-v `pwd`/data:/var/lib/postgresql/data \
-p 5432:5432 -d postgres:9.6-alpine
