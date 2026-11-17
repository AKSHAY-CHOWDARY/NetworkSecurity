from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestor = DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion initiated")
        data_ingestion_artifact = data_ingestor.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data Ingestion completed")
        logging.info("Data Validation initiated")
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)