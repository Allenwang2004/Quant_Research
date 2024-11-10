import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

import logging
from pymongo import MongoClient, errors
from datetime import datetime
class MongoHandler:
    def __init__(self, db, collection_name, logger):
        self.collection = db[collection_name]
        self.logger = logger

    def get_latest_date_for_symbol(self, symbol, product_type, frequency):
        try:
            latest_entry = self.collection.find_one(
                {"symbol": symbol, "product_type": product_type, "frequency": frequency},
                sort=[("datetime", -1)]
            )
            if latest_entry:
                return latest_entry["datetime"]
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving latest date for {symbol}: {e}")
            return None

    def insert_data(self, data):
        try:
            self.collection.insert_many(data, ordered=False)
            self.logger.info(f"Inserted {len(data)} records into the collection")
        except errors.BulkWriteError as e:
            self.logger.error(f"Bulk write error: {e.details}")

    def write_if_needed(self, data, last_update_date):
        filtered_data = []
        for record in data:
            data_dt = record["datetime"]
            if last_update_date is None or last_update_date < data_dt:
                # filtered_data.append(record)
                print('Simualating add')
                print(record)