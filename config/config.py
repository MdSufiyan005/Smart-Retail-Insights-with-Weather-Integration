import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('WEATHER_API_KEY')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'weather_retail_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')  