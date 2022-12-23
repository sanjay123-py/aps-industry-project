from sensor.logger import logging
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from sensor import utils
from scipy import stats
import pandas as pd 
import os, sys
import numpy as np
from typing import Optional
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import Pipeline
from sklearn.impute import SimpleInputer
from sklearn.preprocessing import RobustScaler
class DataTransformation:
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise SensorException(e, sys)
    @classmethod
    def get_data_transformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleInputer(strategy="constant",fill_value = 0)
            robust_scaler =  RobustScaler()
            pipeline = Pipeline(step=[
                ("imputer",simple_imputer),
                ("Robust_Scaler",robust_scaler)
            ])
            return pipeline
        except Exception as e:
            raise SensorException(e, sys)



