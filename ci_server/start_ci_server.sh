#!/usr/bin/env bash

touch /tmp/ci_server.pid

export PROD="true"

uwsgi --chmod-socket=666 --uwsgi-socket /home/deploy/other_config/ci_server/ci_server.sock --wsgi-file /home/deploy/other_data/SimpleCIServer/ci_server/ci_server.py --callable __hug_wsgi__ &

echo $! > /tmp/ci_server.pid