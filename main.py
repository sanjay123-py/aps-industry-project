from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity
from sensor.components.data_ingestion import DataIngestion
import os
import sys

if __name__ == '__main__':
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config)
          print(data_ingestion_config.to_dict())

          #data ingestion
          data_ingestion = DataIngestion(data_ingestion_config)
          print(data_ingestion.initiate_data_ingestion())
     except Exception as e:
          print(e)
     
          