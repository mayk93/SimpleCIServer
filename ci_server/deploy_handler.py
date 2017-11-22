import os
import json
import socket

# Git
import git

# Logging
import logging
logging.basicConfig(level=logging.INFO)

from deploy_handler_utils import get_other_data, VALUE


class DeployHandler(object):
    def __init__(self, **kwargs):
        with open(kwargs.get("deploy_config_path", "/home/deploy/ci_server/deploy_config.json")) as source:
            self.deploy_config = json.loads(source.read())

        self.deploy_data = kwargs.get("deploy_data")

        self.repository_name = None
        self.repository_path = None
        self.repo = None

        self.branch = None
        self.ref = None
        self.time = None
        self.pusher = None
        self.other_data = None

        self.remote = None

        if self.deploy_data:
            self.load_deploy_data(self.deploy_data)
        else:
            logging.info("No deploy data supplied. You must call load_deploy_data explicitly.")

    def load_deploy_data(self, deploy_data):
        self.repository_name = deploy_data.get("repository", {}).get("name")
        self.repository_path = os.path.join(self.deploy_config["repo_path"], self.repository_name)
        self.repo = git.Repo(self.repository_path)

        self.branch = deploy_data.get("ref", "").split("/")[::-1][0]
        self.ref = deploy_data.get("ref")
        self.pusher = deploy_data.get("pusher")
        self.other_data = get_other_data(deploy_data.get("repository"))

        self.remote = self.repo.create_remote(self.branch, self.repo.remotes.origin.url)

    def handle_update(self):
        logging.info("Now updating for repo with data:")
        logging.info("Name: %s" % self.repository_name)
        logging.info("Found in: %s" % self.repository_path)

        if None in [attribute[VALUE] for attribute in self.__dict__.items() if attribute[:1] != '_']:
            logging.info("Found None in the required data.")
            return None

        self.remote.pull(self.branch)

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


import unittest


class TestDeployHandler(unittest.TestCase):
    def setUp(self):
        self.dh = DeployHandler(deploy_config_path="deploy_config_test.json")

        with open("test_data/example_hook_data_branch_local.json") as source:
            self.test_deploy_data = json.loads(source.read())

    def test_pull_to_deploy(self):
        self.dh.load_deploy_data(self.test_deploy_data)