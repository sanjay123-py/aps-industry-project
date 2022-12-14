from sensor.logger import logging
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy import stats
import pandas as pd 
import os, sys
class DataValidation:
    def __init__(self,data_validation_congfig:DataValidationConfig):
        try:
            logging.info(f"{'>>'*20} *DataValidation* {'<<'*20}")
            self.data_validation_config = data_validation_congfig
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
    def id_required_column(self)->bool:...
    def drop_columns_with_high_missing_values(self, df:pd, threshold:float = 0.3)->pd.DataFrame:...

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:...