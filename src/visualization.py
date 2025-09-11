"""
Main visualization utilities and helper functions.
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple

def setup_matplotlib_style():
    """Set up matplotlib with a clean, professional style."""
    plt.style.use('default')
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 0.8,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'font.size': 11,
        'legend.fontsize': 10,
        'legend.frameon': True,
        'legend.fancybox': True,
        'legend.shadow': True,
        'grid.alpha': 0.3,
    })

def get_rainfall_colormap():
    """Return a custom colormap for rainfall visualization."""
    from matplotlib.colors import LinearSegmentedColormap
    
    # Define colors from dry to wet
    colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', 
              '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
    
    return LinearSegmentedColormap.from_list('rainfall', colors)

def create_legend_elements():
    """Create legend elements for rainfall levels."""
    import matplotlib.patches as mpatches
    
    legend_elements = [
        mpatches.Patch(color='#f7fbff', label='0-25 mm (Very Low)'),
        mpatches.Patch(color='#c6dbef', label='25-75 mm (Low)'),
        mpatches.Patch(color='#6baed6', label='75-150 mm (Moderate)'),
        mpatches.Patch(color='#2171b5', label='150-250 mm (High)'),
        mpatches.Patch(color='#08306b', label='250+ mm (Very High)'),
    ]
    
    return legend_elements

def validate_data_format(data) -> bool:
    """Validate that the data has the required columns."""
    required_columns = ['year', 'month', 'latitude', 'longitude', 'rainfall']
    
    if data is None or data.empty:
        print("Error: Data is empty or None")
        return False
    
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return False
    
    print("Data format validation passed")
    return True

def print_data_summary(data):
    """Print a summary of the rainfall data."""
    if data is None or data.empty:
        print("No data to summarize")
        return
    
    print("\n=== Data Summary ===")
    print(f"Total records: {len(data)}")
    print(f"Date range: {data['year'].min()}-{data['year'].max()}")
    print(f"Locations: {data.groupby(['latitude', 'longitude']).size().count()}")
    print(f"Rainfall range: {data['rainfall'].min():.1f} - {data['rainfall'].max():.1f} mm")
    print(f"Average rainfall: {data['rainfall'].mean():.1f} mm")
    
    if 'city' in data.columns:
        print(f"Cities: {', '.join(data['city'].unique())}")
    
    print("==================\n")
