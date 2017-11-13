#!/usr/bin/env bash

touch /tmp/ci_server.pid

export PROD="true"

uwsgi --chmod-socket=666 --uwsgi-socket /home/deploy/server/backend.sock --wsgi-file PATH --callable __hug_wsgi__ &

echo $! > /tmp/ci_server.pid