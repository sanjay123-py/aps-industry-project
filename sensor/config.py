import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os, sys
@dataclass
class EnvironmentVariables:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")

env_variable = EnvironmentVariables()
client = pymongo.MongoClient(env_variable.mongo_db_url)
