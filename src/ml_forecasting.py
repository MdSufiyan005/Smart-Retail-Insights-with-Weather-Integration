import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import os
from datetime import datetime

class WeatherForecaster:
    def __init__(self, data):
        self.data = data
        self.model = None
        
    def prepare_features(self):
        """Prepare features for ML model with enhanced engineering"""
        df = self.data.copy()  # Work on a copy to preserve original data
        
        print(f"\nInitial data shape: {df.shape}")
        
        # Convert numeric columns
        numeric_columns = ['temperature', 'humidity', 'pressure', 'wind_speed']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Basic time features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Simple lag features
        df['temp_lag_1'] = df['temperature'].shift(1)
        df['temp_lag_2'] = df['temperature'].shift(2)
        
        # Basic rolling mean
        df['temp_rolling_mean'] = df['temperature'].rolling(window=3, min_periods=1).mean()
        
        # Drop NaN values
        essential_columns = ['temperature', 'temp_lag_1', 'temp_lag_2', 'temp_rolling_mean']
        df = df.dropna(subset=essential_columns)
        
        print(f"Final shape after preprocessing: {df.shape}")
        
        if len(df) < 8:  # Changed from 10 to 8
            raise ValueError(f"Not enough data after preparation. Got {len(df)} samples, need at least 8.")
            
        return df
    
    def train_model(self):
        """Train a simple linear regression model"""
        try:
            # Prepare features only once
            if not hasattr(self, 'prepared_data'):
                self.prepared_data = self.prepare_features()
            
            # Select basic features for linear regression
            features = ['hour', 'day_of_week', 'temp_lag_1', 'temp_lag_2', 'temp_rolling_mean']
            features = [f for f in features if f in self.prepared_data.columns]
            
            X = self.prepared_data[features]
            y = self.prepared_data['temperature']
            
            # Use a larger test set (30%) and shuffle data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, shuffle=True, random_state=42
            )
            
            # Train linear regression model
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                'r2': r2_score(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'coefficients': dict(zip(features, self.model.coef_)),
                'intercept': self.model.intercept_
            }
            
            # Print detailed metrics
            print("\nModel Performance:")
            print(f"R² Score: {metrics['r2']:.3f}")
            print(f"RMSE: {metrics['rmse']:.3f}°C")
            print(f"MAE: {metrics['mae']:.3f}°C")
            
            # Save model after successful training
            self.save_model()
            
            return metrics
            
        except Exception as e:
            print(f"\nError during model training: {str(e)}")
            return None
    
    def forecast(self, steps=7):
        """Generate weather forecast"""
        # Implementation for multi-step forecasting
        pass
    
    def save_model(self, model_dir='models'):
        """Save the trained model and its metadata"""
        if self.model is None:
            raise ValueError("No trained model available. Please train the model first.")
        
        # Create models directory if it doesn't exist
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        # Generate timestamp for the model filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = os.path.join(model_dir, f'weather_model_{timestamp}.joblib')
        
        # Save model and metadata without calling train_model again
        model_info = {
            'model': self.model,
            'features': list(self.data.columns),
            'training_date': timestamp
        }
        
        # Save to disk
        joblib.dump(model_info, model_path)
        print(f"\nModel saved successfully to: {model_path}")
        return model_path

    @classmethod
    def load_model(cls, model_path):
        """Load a saved model"""
        try:
            model_info = joblib.load(model_path)
            
            # Create instance and set attributes
            instance = cls(pd.DataFrame())  # Empty DataFrame as placeholder
            instance.model = model_info['model']
            print(f"\nModel loaded successfully from: {model_path}")
            print(f"Training date: {model_info['training_date']}")
            print(f"Model features: {', '.join(model_info['features'])}")
            return instance
            
        except Exception as e:
            print(f"\nError loading model: {str(e)}")
            return None