import os
from configparser import RawConfigParser

HOME_DIR = os.path.expanduser('~')

CONFIG_FILE = os.path.join(HOME_DIR, ".dts", "config")
config = RawConfigParser()
config.read(CONFIG_FILE)

AWS_USER = config.get("aws", "AWS_USER")
SSH_KEY_PATH = config.get("main", "SSH_KEY_PATH")
