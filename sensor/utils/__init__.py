import pandas as pd
from sensor.config import client
from sensor.logger import logging
from  sensor.exception import SensorException

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database: {database_name} and collection:{collection_name}")
        df=pd.DataFrame(list(client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df.drop("_id",axis=1)
        return df
    except Exception as e:
        logging.debug(str(e))
        raise SensorException(e, sys)
if __name__ == '__main__':
    try:
        get_collection_as_dataframe(database_name="aps", collection_name="sensor")
    except Exception as e:
        print(e)
    