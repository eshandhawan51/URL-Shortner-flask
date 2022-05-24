#!/bin/bash
# A simple Bash script to run URL shortner 

echo starting redis-server 

docker restart redis-server

sleep 2s

echo redis service started 

echo Starting URL shortner service 

docker run --network=host  url-shortner-flask
