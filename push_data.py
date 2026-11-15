import os
import sys
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np

from pymongo import MongoClient
import certifi ### Provides a set of root certiticates which help to make secure HTTP requests

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URI")
ca = certifi.where()


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def  insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return f"{len(self.records)} records inserted"
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    file_path = "Network_Data\\phisingData.csv"
    database = "networkDB"
    collection = "networkData"
    networkObj = NetworkDataExtract()
    records = networkObj.csv_to_json_convertor(file_path=file_path)
    response = networkObj.insert_data_to_mongodb(records=records, database=database, collection=collection)
    print(response)
