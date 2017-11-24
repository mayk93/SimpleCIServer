#!/usr/bin/env bash

echo "Restart services hook."

sudo service nginx stop
sudo serivice api_server stop

echo "Stopped server services."

sleep 1

sudo serivice api_server start
sudo service nginx start

echo "Started server services."