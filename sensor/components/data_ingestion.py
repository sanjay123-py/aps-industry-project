from sensor import utils
from sensor.entity import config_entity, artifact_entity
from sensor.exception import SensorException

class DataIngestion:
    
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(error_message=e, error_detail=sys)

    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame  = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name=self.data_ingestion_config.collection_name)

            df.replace(to_replace="na",value=np.NAN,inplace=True)

            #Save data in feature store
            logging.info("Create feature store folder if not available")
            #Create feature store folder if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)
            logging.info("Save df to feature store folder")
            #Save df to feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)
            
        except Exception as e:
            raise SensorException(e, sys)
