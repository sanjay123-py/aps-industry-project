from sensor.logger import logging
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from scipy import stats
import pandas as pd 
import os, sys
import numpy as np
from typing import Optional
from sensor import utils
class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} *DataValidation* {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_anomaly = dict()
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
    def is_required_column_exists(self,base_df:pd.DataFrame,present_df:pd.DataFrame, report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = present_df.columns
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
            
            if missing_columns.__len__() > 0:
                self.validation_anomaly[report_key_name] = missing_columns
                return False
            return True
        except Exception as e:
            raise SensorException( e, sys )

    def drop_columns_with_high_missing_values(self, df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.threshold
            null_report = df.isna().sum()/df.shape[0]
            self.validation_anomaly[report_key_name] = list(null_report[null_report>threshold].index)
            drop_columns = null_report[null_report>threshold].index
            df.drop(drop_columns,axis=1,inplace=True)
            if( len(df.columns) == 0 ):
                return None
            return df
        except Exception as e:
            raise SensorException(error_message = e, error_detail = sys)
    
    def detect_data_drift(self,base_df:pd.DataFrame,present_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            for base_column in base_columns:
                base_data, current_data = base_df[base_column], present_df[base_column]
                
                same_distribution=stats.ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    drift_report[base_column]={
                        "P-value":float(same_distribution.pvalue),
                        "same_distribution":True
                    } 
                else:
                     drift_report[base_column]={
                        "P-value":float(same_distribution.pvalue),
                        "same_distribution":False
                    } 
            self.validation_anomaly[report_key_name] = drift_report
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info(f"Replace na value in base df")
            #base_df has na as null
            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_columns_with_high_missing_values(df=base_df,report_key_name="missing_values_within_base_dataset")

            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Drop null values colums from train df")
            train_df = self.drop_columns_with_high_missing_values(df=train_df,report_key_name="missing_values_within_train_dataset")
            logging.info(f"Drop null values colums from test df")
            test_df = self.drop_columns_with_high_missing_values(df=test_df,report_key_name="missing_values_within_test_dataset")

            exclude_columns = ["class"]
            base_df = utils.convert_columns_float(df=base_df, excluded_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, excluded_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, excluded_columns=exclude_columns)

            logging.info(f"Is all required columns present in train df")
            train_df_columns_status = self.is_required_column_exists(base_df=base_df, present_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.is_required_column_exists(base_df=base_df, present_df=test_df,report_key_name="missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.detect_data_drift(base_df=base_df, present_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.detect_data_drift(base_df=base_df, present_df=test_df,report_key_name="data_drift_within_test_dataset")

            #write the report
            logging.info("Write reprt in yaml file")
            utils.create_report_yaml(file_path=self.data_validation_config.report_file_path,
            data=self.validation_anomaly)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path,)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)