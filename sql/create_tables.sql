-- Create database
CREATE DATABASE weather_retail_db;

-- Weather data table
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(5,2),
    humidity INTEGER,
    pressure DECIMAL(7,2),
    wind_speed DECIMAL(5,2),
    wind_direction INTEGER,
    weather_condition VARCHAR(50),
    visibility DECIMAL(5,2),
    uv_index DECIMAL(3,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for better query performance
CREATE INDEX idx_city_timestamp ON weather_data(city, timestamp);