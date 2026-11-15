from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## Configuration for data ingestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()
MONGO_URL = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_df(self):
        """
            Read data from MongoDB
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"])
            df.replace({"na":np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def export_data_to_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)  

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info(" Entered train test split of Data ingestion ")

            train_test_ratio = self.data_ingestion_config.train_test_split_ratio
            train_data, test_data = train_test_split(dataframe, test_size=train_test_ratio)

            logging.info(" Performed train test split on dataframe ")

            train_dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            test_dir_path = os.path.dirname(self.data_ingestion_config.testing_file_path)

            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)

            logging.info("Exporting train test files")

            train_data.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Exited the split data method of Data ingestion")

            return (train_data, test_data)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) 

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_df()
            dataframe = self.export_data_to_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)  