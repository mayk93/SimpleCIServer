#!/usr/bin/env bash

kill -9 $(cat /tmp/ci_server.pid)
rm /tmp/ci_server.pid