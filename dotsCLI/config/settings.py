import os
from configparser import RawConfigParser

HOME_DIR = os.path.expanduser("~")

CONFIG_FILE = os.path.join(HOME_DIR, ".dts", "config")
config = RawConfigParser()
config.read(CONFIG_FILE)

AWS_USER = config.get("aws", "AWS_USER")

SSH_DIRECTORY = config.get("main", "SSH_DIRECTORY")
PEM_KEY_PATH = config.get("main", "PEM_KEY_PATH")
FRONTEND_DIR_PATH = config.get("main", "FRONTEND_DIR_PATH")
FRONTEND_DIST_PATH = config.get("main", "FRONTEND_DIST_PATH")
