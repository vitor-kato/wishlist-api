#!/bin/bash

COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 \
    docker-compose -f \
    docker-compose.yml -f \
    docker-compose.prod.yml ${*:-up}
