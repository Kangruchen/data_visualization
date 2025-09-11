"""
Data loading and preprocessing module for rainfall data.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional

class RainfallDataLoader:
    """Handles loading and preprocessing of rainfall data."""
    
    def __init__(self, data_path: str):
        """Initialize the data loader with a data file path."""
        self.data_path = data_path
        self.data = None
    
    def load_data(self) -> pd.DataFrame:
        """Load rainfall data from CSV file."""
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.data)} records from {self.data_path}")
            return self.data
        except FileNotFoundError:
            print(f"Data file not found: {self.data_path}")
            return self.generate_sample_data()
    
    def generate_sample_data(self) -> pd.DataFrame:
        """Generate sample rainfall data for demonstration."""
        print("Generating sample rainfall data...")
        
        # Generate data for 100 years (1924-2023)
        years = range(1924, 2024)
        months = range(1, 13)
        
        # Sample locations (major cities worldwide)
        locations = [
            {'city': 'London', 'lat': 51.5074, 'lon': -0.1278},
            {'city': 'New York', 'lat': 40.7128, 'lon': -74.0060},
            {'city': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
            {'city': 'Sydney', 'lat': -33.8688, 'lon': 151.2093},
            {'city': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
            {'city': 'Cairo', 'lat': 30.0444, 'lon': 31.2357},
            {'city': 'São Paulo', 'lat': -23.5505, 'lon': -46.6333},
            {'city': 'Moscow', 'lat': 55.7558, 'lon': 37.6176},
        ]
        
        data = []
        for year in years:
            for month in months:
                for location in locations:
                    # Generate seasonal rainfall patterns
                    base_rainfall = self._get_seasonal_rainfall(month, location['lat'])
                    # Add some year-to-year variation
                    variation = np.random.normal(0, base_rainfall * 0.3)
                    rainfall = max(0, base_rainfall + variation)
                    
                    data.append({
                        'year': year,
                        'month': month,
                        'latitude': location['lat'],
                        'longitude': location['lon'],
                        'rainfall': rainfall,
                        'city': location['city']
                    })
        
        self.data = pd.DataFrame(data)
        return self.data
    
    def _get_seasonal_rainfall(self, month: int, latitude: float) -> float:
        """Generate realistic seasonal rainfall patterns based on latitude."""
        # Base patterns for different regions
        if latitude > 40:  # Northern temperate
            summer_months = [6, 7, 8]
            if month in summer_months:
                return np.random.uniform(60, 120)  # mm
            else:
                return np.random.uniform(30, 80)
        elif latitude > 0:  # Northern tropical/subtropical
            monsoon_months = [6, 7, 8, 9]
            if month in monsoon_months:
                return np.random.uniform(100, 300)
            else:
                return np.random.uniform(10, 60)
        else:  # Southern hemisphere
            # Reverse seasons
            summer_months = [12, 1, 2]
            if month in summer_months:
                return np.random.uniform(80, 150)
            else:
                return np.random.uniform(40, 90)
    
    def get_data_for_period(self, year: int, month: int) -> pd.DataFrame:
        """Get rainfall data for a specific year and month."""
        if self.data is None:
            self.load_data()
        
        return self.data[(self.data['year'] == year) & (self.data['month'] == month)]
    
    def get_date_range(self) -> Tuple[int, int]:
        """Get the date range of the dataset."""
        if self.data is None:
            self.load_data()
        
        min_year = self.data['year'].min()
        max_year = self.data['year'].max()
        return min_year, max_year
