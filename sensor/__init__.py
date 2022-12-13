from dotenv import load_dotenv
from sensor.logger import logging

logging.info("Loading environment variable from .env file")
print(f"Loading environment variable from .env file")

load_dotenv()