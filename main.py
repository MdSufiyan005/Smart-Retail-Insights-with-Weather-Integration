from src.data_fetcher import WeatherDataFetcher
from src.database import DatabaseManager, parse_weather_api_response
from src.visualizations import WeatherVisualizer
from src.ml_forecasting import WeatherForecaster
from config.config import Config
import pandas as pd
import os

def main():
    # Initialize components
    fetcher = WeatherDataFetcher(Config.API_KEY)
    db = DatabaseManager(Config.DB_HOST, Config.DB_NAME, 
                        Config.DB_USER, Config.DB_PASSWORD)
    
    city = "Mumbai"

    # Clear old data for the city
    db.delete_city_weather_data(city)

    # Fetch 30 days of historical weather data
    historical_weather = fetcher.fetch_historical_weather(city, days=30)
    if not historical_weather or len(historical_weather) == 0:
        print("Could not fetch historical weather data.")
        return

    # Insert each day's weather data into the database
    for day_data in historical_weather:
        try:
            db.insert_weather_data(parse_weather_api_response(day_data))
        except Exception as e:
            print(f"Error inserting data: {e}")

    # Get historical data for analysis
    historical_data = db.get_weather_data(city, days=30)
    
    # --- Feature engineering for ML ---
    df = historical_data.copy()
    
    # Convert all relevant columns to numeric
    numeric_columns = ['temperature', 'humidity', 'pressure', 'wind_speed', 
                      'wind_direction', 'visibility', 'uv_index']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp and create features
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Create time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['month'] = df['timestamp'].dt.month
    
    # Create lag features (using ffill() instead of deprecated fillna)
    df['temp_lag_1'] = df['temperature'].shift(1).ffill()
    df['temp_lag_2'] = df['temperature'].shift(2).ffill()
    
    # Add more features for better prediction
    df['temp_rolling_mean'] = df['temperature'].rolling(window=3, min_periods=1).mean()
    df['temp_rolling_std'] = df['temperature'].rolling(window=3, min_periods=1).std()
    
    # Drop any remaining NaN values
    df = df.dropna(subset=['temperature', 'temp_lag_1', 'temp_lag_2'])
    
    print(f"\nRows after feature engineering: {len(df)}")
    print("\nFinal feature set:")
    print(df.dtypes)
    
    if df.empty or len(df) < 5:
        print("Not enough data for ML forecasting. Please collect more weather data.")
        return

    # Create visualizations
    visualizer = WeatherVisualizer(df)
    dashboard = visualizer.weather_dashboard()
    dashboard.show()
    
    # Perform ML forecasting
    forecaster = WeatherForecaster(df)
    model_metrics = forecaster.train_model()
    
    if model_metrics:
        print(f"Model Performance: R² = {model_metrics['r2']:.3f}")
    else:
        print("Model training failed. Please check the errors above.")

    # Example usage in main.py
    # Train and save the model
    forecaster = WeatherForecaster(df)
    metrics = forecaster.train_model()  # This will automatically save the model
    
    # Load a saved model
    saved_model_path = "models/weather_model_20250922_123456.joblib"  # Use actual path
    loaded_forecaster = WeatherForecaster.load_model(saved_model_path)
    
    # Create ML forecaster
    forecaster = WeatherForecaster(historical_data)
    model_metrics = forecaster.train_model()
    
    if model_metrics:
        print("\nFinal Model Performance:")
        print(f"R² Score: {model_metrics['r2']:.3f}")
        print(f"RMSE: {model_metrics['rmse']:.3f}°C")
        print(f"MAE: {model_metrics['mae']:.3f}°C")
        
        # Load and verify the saved model
        latest_model = sorted(os.listdir('models'))[-1]
        model_path = os.path.join('models', latest_model)
        loaded_forecaster = WeatherForecaster.load_model(model_path)

if __name__ == "__main__":
    main()