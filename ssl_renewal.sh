#!/bin/bash

COMPOSE="/usr/local/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

$DOCKER pull certbot/certbot
$COMPOSE restart app
$COMPOSE -f docker-compose.yml -f docker-compose.production.yml run certbot renew
$COMPOSE exec nginx nginx -s reload
$DOCKER system prune -af