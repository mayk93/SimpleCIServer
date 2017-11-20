# Server
import hug
from hug_middleware_cors import CORSMiddleware

# Python
import os
from datetime import datetime

# Logging
import logging
logging.basicConfig(level=logging.INFO)

from deploy_handler import DeployHandler


api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=["https://github.com"]))

PROD = os.environ.get("PROD") == "true"
if PROD:
    deploy_handler = DeployHandler()
else:
    deploy_handler = DeployHandler(deploy_config_path="deploy_config.json")


@hug.post('/deploy')
def deploy(*args, **kwargs):
    logging.info("New deploy at %s" % datetime.now())

    deploy_handler.load_deploy_data(kwargs)
    deploy_handler.handle_update()
    deploy_handler.email()

    return {
        "ok": True
    }
