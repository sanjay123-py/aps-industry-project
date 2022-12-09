from sensor.exception import SensorException
from sensor.logger import logging
import os, sys
def test_logger_and_exception():
     try:
          result=1/0

     except Exception as e:
          raise  SensorException(e, sys)
if __name__ == '__main__':
     try:
          test_logger_and_exception()

     except Exception as e:
          print(e)
     
          