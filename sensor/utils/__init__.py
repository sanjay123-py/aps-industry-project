import pandas as pd
from sensor.config import client
from sensor.logger import logging
from  sensor.exception import SensorException
import yaml
import os, sys
import dill
import numpy as np

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database: {database_name} and collection:{collection_name}")
        df=pd.DataFrame(list(client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df.drop(["_id"],axis=1,inplace=True)
        return df
    except Exception as e:
        logging.debug(str(e))
        raise SensorException(e, sys)



def create_report_yaml(file_path:str,data:dict):
    try:
        filedir = os.path.dirname(file_path)
        os.makedirs(filedir,exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(data,f)
    except Exception as e:
        raise SensorException(e, sys)

def convert_columns_float(df:pd.DataFrame, excluded_columns:list)->pd.DataFrame:
    df_columns=df.columns
    for df_column in df_columns:
        if(df_column not in excluded_columns):
            df[df_column]=df[df_column].astype(float)
    return df

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise SensorException(e, sys)

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) 

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys)

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys)

if __name__ == '__main__':
    try:
        get_collection_as_dataframe(database_name="aps", collection_name="sensor")
    except Exception as e:
        print(e)
