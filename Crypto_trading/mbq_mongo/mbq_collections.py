import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

from mbq_mongo.mongo_connector import MongoConnector

mbq_mongoDB = MongoConnector().get_cloud_conn()

collection_open_interest_data = mbq_mongoDB['MARKET_DATA']['open_interest_data']
collection_monitor_binance_longside_OI = mbq_mongoDB['MONITOR_DATA']['binance_longside_OI']
collection_monitor_binance_longside_OI_5m = mbq_mongoDB['MONITOR_DATA']['binance_longside_OI_5m']
