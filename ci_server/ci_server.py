# Server
import hug
from hug_middleware_cors import CORSMiddleware

# Python
from datetime import datetime

# Logging
import logging
logging.basicConfig(level=logging.INFO)


api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=["https://github.com"]))


@hug.post('/deploy')
def deploy(*args, **kwargs):
    print("New Deploy at %s" % datetime.now())
    try:
        print("Args:")
        print(args)
        print("Kwargs:")
        print(kwargs)
        print("\n---\n")
    except Exception as e:
        logging.exception(e)

    return {
        "ok": True
    }
