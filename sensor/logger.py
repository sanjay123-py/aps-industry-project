import logging
import os
from datetime import datetime

#each logging file should be save according to the timing
LOG_FILE_NAME=f"{datetime.now().strftime('%m%d%Y__%H:%M:%S')}.log"

#creating logging directory path
LOG_FILE_DIR=os.path.join(os.getcwd(),'logs')

#creating a directory if not exists for storing logging informations
os.makedirs(LOG_FILE_DIR,exist_ok=True)

#Creating a logging path
LOG_FILE_PATH=os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

#configure logging 
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)