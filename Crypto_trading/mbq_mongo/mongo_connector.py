import os, sys

import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

from pymongo import MongoClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')
DBCONFIG_FILE = os.path.join(CONFIG_DIR, 'db_config.json')

class Config(object):
    _instances = {}
    def __new__(cls, config_file_path):
        if config_file_path not in cls._instances:
            cls._instances[config_file_path] = super(Config, cls).__new__(cls)
            instance = cls._instances[config_file_path]
            instance.config_file_path = config_file_path
            instance.config = None
        return cls._instances[config_file_path]

    def load_config(self):
        if self.config is None:
            with open(self.config_file_path) as f:
                self.config = json.load(f)
        return self.config

class MongoConnector:
    """
    Singleton connector for managing MongoDB connections.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the MongoConnector class exists.

        Returns:
            MongoConnector: The singleton instance of the MongoConnector.
        """
        if not cls._instance:
            cls._instance = super(MongoConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the MongoDB connector with connection settings from the configuration.
        Ensures that it is only initialized once.
        """
        if not hasattr(self, '_initialized'):  # Avoid redundant initialization
            super().__init__()
            config = Config(DBCONFIG_FILE).load_config()
            cloud = config['mongo_connection']['cloud']
            try:
                self.cloud = MongoClient(cloud)
            except Exception as e:
                # Handle exceptions
                pass
            self._initialized = True

    def get_cloud_conn(self):
        """
        Returns the cloud MongoDB connection.

        Returns:
            AsyncIOMotorClient: The client instance for cloud MongoDB connection.
        """
        return self.cloud