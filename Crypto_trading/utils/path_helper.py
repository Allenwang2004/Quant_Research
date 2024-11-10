import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

import configparser
path_config = configparser.ConfigParser()
path_config.read(f'{PROJECT_ROOT}/config/path_config.ini')

PRICE_DATA_PATH = path_config['PATH']['Price_data']
OPEN_INTEREST_PATH = path_config['PATH']['OI_data']
PRICE_SAVE_PATH = path_config['PATH']['Price_save_data']
SIGNAL_PATH = path_config['PATH']['Signal_data']

os.makedirs(OPEN_INTEREST_PATH, exist_ok=True)
os.makedirs(PRICE_DATA_PATH, exist_ok=True)
os.makedirs(PRICE_SAVE_PATH, exist_ok=True)
os.makedirs(SIGNAL_PATH, exist_ok=True)