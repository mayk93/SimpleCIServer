# Server
import hug
from hug_middleware_cors import CORSMiddleware

# Python
import os
import sys
import json

# Logging
import logging
logging.basicConfig(level=logging.INFO)


api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=["*"]))

# Port: 4567


@hug.post('/deploy')
def deploy(*args, **kwargs):
    print("Deploy called")

    with open("/tmp/webhook.json", "w+") as dest:
        dest.write(json.dumps({
            "args": args,
            "kwargs": kwargs
        }))

    return {"ok": True}


