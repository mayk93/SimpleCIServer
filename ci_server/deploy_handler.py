import os
import json
import socket

# Git
import git

# Logging
import logging
logging.basicConfig(level=logging.INFO)


def get_other_data(repo_data):
    if repo_data is None:
        return {
            "updated_at": "unknown",
            "size": "unknown"
        }
    return {
        "updated_at": repo_data.get("updated_at", "unknown"),
        "size": repo_data.get("size", "unknown")
    }


class DeployHandler(object):
    def __init__(self, **kwargs):
        with open(kwargs.get("deploy_config_path", "/home/deploy/ci_server/deploy_config.json")) as source:
            self.deploy_config = json.loads(source.read())

        deploy_data = kwargs.get("deploy_data")

        self.repository_name = deploy_data.get("repository", {}).get("name") if deploy_data else None
        self.branch = deploy_data.get("ref", "").split("/")[::-1][0] if deploy_data else None
        self.ref = deploy_data.get("ref") if deploy_data else None
        self.time = deploy_data.get("head_commit", {}).get("timestamp") if deploy_data else None
        self.pusher = deploy_data.get("pusher") if deploy_data else None

        self.repository_path = os.path.join(
            self.deploy_config["repo_path"], self.repository_name
        ) if self.repository_name else None

        self.other_data = None

    def load_deploy_data(self, deploy_data):
        self.repository_name = deploy_data.get("repository", {}).get("name")
        self.branch = deploy_data.get("ref", "").split("/")[::-1][0]
        self.ref = deploy_data.get("ref")
        self.pusher = deploy_data.get("pusher")

        self.repository_path = os.path.join(self.deploy_config["repo_path"], self.repository_name)

        self.other_data = get_other_data(deploy_data.get("repository"))

    def handle_update(self):
        logging.info("Now updating for repo with data:")
        logging.info("Name: %s" % self.repository_name)
        logging.info("Found in: %s" % self.repository_path)

        if None in []:  # ToDo: Here, check to make sure there is no None in the required data.
            logging.info("Found None in the required data.")
            return None

        git.remote.Remote(self.repository_name, 'origin').pull(self.ref)

    def email(self):
        message = '''
        A new deploy has occurred!

        -> Repository: %s
        -> Updating branch: %s
        -> Time of update: %s
        -> Pushed by: %s
        -> Sent from: %s
        '''.strip() % (
            self.repository_name,
            self.branch,
            self.other_data["updated_at"],
            self.pusher,

            socket.gethostname()
        )

        for email in self.deploy_config["email_to"]:
            print("Sending this email to %s" % email)
            print("\n-----\n%s\n-----\n" % message)