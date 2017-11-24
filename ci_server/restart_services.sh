#!/usr/bin/env bash

echo "Restart services hook."
echo "Restart services hook." > /tmp/restart_services.txt

sudo service nginx stop
sudo serivice api_server stop

echo "Stopped server services."
echo "Stopped server services." >> /tmp/restart_services.txt

sleep 1

sudo serivice api_server start
sudo service nginx start

echo "Started server services."
echo "Started server services." >> /tmp/restart_services.txt