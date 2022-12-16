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
            self.validation_anomaly = dict()
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
    def is_required_column_exists(self,base_df:pd.DataFrame,present_df:pd.DataFrame)->bool:
        try:
            base_columns = base_df.columns
            current_columns = present_df.columns
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
            
            if missing_columns.__len__() > 0:
                self.validation_anomaly['missing_columns'] = missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException( e, sys )

    def drop_columns_with_high_missing_values(self, df:pd.DataFrame, threshold:float = 0.3)->pd.DataFrame:
        try:
            threshold = self.data_validation_config.threshold
            null_report = df.isna().sum()/df.shape[0]
            self.validation_anomaly['droped_columns'] = list(null_report[null_report>threshold].index)
            drop_columns = null_report[null_report>threshold].index
            df.drop(drop_columns,axis=1,inplace=True)
            if( len(df.columns) == 0 ):
                return None
            return df
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
    
    def detect_data_drift(self,base_df:pd.Dataframe,present_df:pd.DataFrame):
        try:
            base_columns = base_df.columns
            for base_column in base_columns:
                base_data, current_data = base_df[base_column], present_df[base_column]
                
                same_distribution=stats.ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    pass 
                else:
                    pass

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:...