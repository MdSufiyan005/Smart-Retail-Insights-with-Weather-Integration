import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self, host, database, user, password):
        self.connection_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }
        # Create SQLAlchemy engine
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    
    def connect(self):
        """Establish database connection"""
        return psycopg2.connect(**self.connection_params)
    
    def insert_weather_data(self, weather_data):
        """Insert weather data into database"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO weather_data 
                (city, timestamp, temperature, humidity, pressure, 
                 wind_speed, weather_condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(insert_query, weather_data)
                conn.commit()
    
    def batch_insert_weather_data(self, weather_data_list):
        """Insert multiple weather data records in batch"""
        with self.connect() as conn:
            with conn.cursor() as cur:
                insert_query = """
                INSERT INTO weather_data 
                (city, timestamp, temperature, humidity, pressure, 
                 wind_speed, weather_condition)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cur.executemany(insert_query, weather_data_list)
                conn.commit()
    
    def get_weather_data(self, city, days=30):
        """Retrieve weather data for visualization"""
        query = """
        SELECT * FROM weather_data 
        WHERE city = %(city)s 
        AND timestamp >= CURRENT_DATE - INTERVAL '%(days)s days'
        ORDER BY timestamp
        """
        return pd.read_sql_query(query, self.engine, params={'city': city, 'days': days})
    
    def delete_city_weather_data(self, city):
        """Delete all weather data for a city (for testing/demo purposes)."""
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM weather_data WHERE city = %s", (city,))
                conn.commit()

def parse_weather_api_response(api_response):
    """Extracts and orders weather data for DB insertion."""
    return (
        api_response['name'],  # city
        pd.to_datetime(api_response['dt'], unit='s'),  # timestamp
        api_response['main']['temp'],  # temperature
        api_response['main']['humidity'],  # humidity
        api_response['main']['pressure'],  # pressure
        api_response['wind']['speed'],  # wind_speed
        api_response['weather'][0]['main'],  # weather_condition
    )