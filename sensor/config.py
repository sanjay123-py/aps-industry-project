import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os, sys
@dataclass
class EnvironmentVariables:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

TARGET_COLUMN_MAPPING={
    'pos':1,
    'neg':0
}

env_variable = EnvironmentVariables()
client = pymongo.MongoClient(env_variable.mongo_db_url)
TARGET_COLUMN = 'class'