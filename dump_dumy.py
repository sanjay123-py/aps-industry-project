import pymongo
import pandas as pd
import json
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

#setting dataabase and collection name 
DATA_FILE_PATH='/config/workspace/aps_failure_training_set1.csv'
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"

if __name__=='__main__':
    df=pd.read_csv(DATA_FILE_PATH)
    print(df.shape)
    df.reset_index(drop=True,inplace=True)
    json_records=list(json.loads(df.T.to_json()).values())
    print(json_records[0])
    
    #insert data into the mongodb
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)
