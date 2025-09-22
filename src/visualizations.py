import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class WeatherVisualizer:
    def __init__(self, data):
        self.data = data
    
    def temperature_trend(self):
        """Create temperature trend visualization"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.data['timestamp'],
            y=self.data['temperature'],
            mode='lines+markers',
            name='Temperature (°C)'
        ))
        fig.update_layout(title='Temperature Trend - Last 30 Days')
        return fig
    
    def weather_dashboard(self):
        """Create comprehensive weather dashboard"""
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=('sdf')
        )
        
        # Add temperature plot
        fig.add_trace(go.Scatter(x=self.data['timestamp'], 
                               y=self.data['temperature']), row=1, col=1)
        
      
        return fig