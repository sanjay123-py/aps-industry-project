from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils import get_collection_as_dataframe
from sensor.entity import config_entity
import os, sys

if __name__ == '__main__':
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()
          data_ingestion_config=config_entity.DataIngestionConfig(training_pipeline_config)
          print(data_ingestion_config.to_dict())
     except Exception as e:
          print(e)
     
          