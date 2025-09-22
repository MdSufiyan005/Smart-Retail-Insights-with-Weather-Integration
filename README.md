# Weather Analysis and Forecasting Project

This project fetches historical weather data, stores it in a PostgreSQL database, visualizes weather patterns, and implements a simple ML model for temperature forecasting.

## Features

- 🌤️ Fetch weather data using Meteostat API
- 📊 Store data in PostgreSQL database
- 📈 Visualize weather trends
- 🤖 ML-based temperature forecasting
- 💾 Model persistence (save/load functionality)

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

### Environment Variables

Create a `.env` file in the project root:

```plaintext
DB_HOST=localhost
DB_NAME=weather_retail_db
DB_USER=your_username
DB_PASSWORD=your_password

```

### Database Setup

1. Create PostgreSQL database:

   ```sql
   CREATE DATABASE weather_retail_db;
   ```

2. Run the database initialization script:

   ```bash
   psql -U your_username -d weather_retail_db -f sql/create_tables.sql
   ```


## Usage

1. **Run the main script**:

   ```bash
   python main.py
   ```

2. **View weather data**:
   - Last 30 days of weather data will be fetched
   - Visualizations will be displayed
   - ML model performance metrics will be shown

## ML Model Details

- Uses Linear Regression for temperature forecasting
- Features:
  - Hour of day
  - Day of week
  - Temperature lag (1 and 2 days)
  - Rolling mean temperature
- Performance metrics:
  - R² Score
  - RMSE (°C)
  - MAE (°C)
