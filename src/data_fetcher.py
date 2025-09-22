import requests
from datetime import datetime, timedelta
from meteostat import Daily, Point
import pandas as pd

class WeatherDataFetcher:
    def __init__(self, api_key=None, db_manager=None):
        self.api_key = api_key  # Not needed for Meteostat
        self.db_manager = db_manager  # Add database manager

    def get_city_coordinates(self, city):
        # Hardcode or use a lookup for demonstration; you can expand this as needed
        city_coords = {
            "Mumbai": (19.0760, 72.8777),
            "Delhi": (28.6139, 77.2090),
            "Bangalore": (12.9716, 77.5946),
            # Add more cities as needed
        }
        return city_coords.get(city, (None, None))

    def fetch_historical_weather(self, city, days=30):
        """Fetch historical weather data for the last `days` days using Meteostat."""
        lat, lon = self.get_city_coordinates(city)
        if lat is None or lon is None:
            print(f"Could not get coordinates for {city}")
            return []
        end = datetime.utcnow()
        start = end - timedelta(days=days)
        location = Point(lat, lon)
        df = Daily(location, start, end).fetch()
        data = []
        for idx, row in df.iterrows():
            # Meteostat may have missing values; skip if temp is NaN
            if pd.isna(row['tavg']):
                continue
            record = {
                'name': city,
                'dt': int(idx.timestamp()),
                'main': {
                    'temp': row['tavg'],
                    'humidity': row['rhum'] if 'rhum' in row else None,
                    'pressure': row['pres'] if 'pres' in row else None
                },
                'wind': {'speed': row['wspd'] if 'wspd' in row else None},
                'weather': [{'main': 'N/A'}]  # Meteostat does not provide weather condition
            }
            data.append(record)
        return data

    def fetch_and_store_weather(self, city, days=30):
        """Fetch weather data and store it directly in the database"""
        weather_data = self.fetch_historical_weather(city, days)
        stored_count = 0
        
        for data in weather_data:
            try:
                # Parse the weather data
                parsed_data = parse_weather_api_response(data)
                # Store in database
                if self.db_manager:
                    self.db_manager.insert_weather_data(parsed_data)
                    stored_count += 1
            except Exception as e:
                print(f"Error storing data for {city}: {str(e)}")
        
        return f"Stored {stored_count} weather records for {city}"