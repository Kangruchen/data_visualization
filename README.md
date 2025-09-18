# Hong Kong Rainfall Visualization Project

## Overview
This project creates an automated animated visualization of Hong Kong rainfall data from the Hong Kong Observatory. The system displays yearly bar charts showing monthly rainfall totals for each year from 1884-2025, with color-coded bars: Yellow (< 50mm), Blue shades (50-600mm), and Black (> 600mm). Simply run `python main.py` to start the animation.

## Features

- 📊 **Automated Animation**: Runs yearly bar chart animation automatically
- 🎨 **Color-Coded Rainfall**: Yellow (<50mm), Blue (50-600mm), Black (>600mm)
- 📈 **Complete Data Labels**: Every month displays precise rainfall values (including 0mm)
- 🗺️ **Unified Scale**: All years use same Y-axis (0-1400mm) for accurate comparison
- 📊 **Statistical Analysis**: Monthly totals, averages, and extremes
- ⚡ **Fast Processing**: Efficient pandas-based data handling
- 📈 **Historical Coverage**: 140+ years of rainfall data (1884-2025)

## Data Source
- **Provider**: Hong Kong Observatory (HKO)
- **Coverage**: 1884-2025 (140+ years)
- **File**: `daily_HKO_RF_ALL.csv` - Daily rainfall measurements
- **Location**: Hong Kong Observatory Headquarters

## Project Structure
```
data_visualization/
├── main.py                    # Main entry point - runs animation automatically
├── rainfall_visualizer.py     # Core visualization system
├── daily_HKO_RF_ALL.csv      # Hong Kong rainfall data
├── requirements.txt           # Python dependencies
└── README.md                 # This documentation
```

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Visualization
```bash
python main.py
```

This will automatically:
- Load Hong Kong Observatory daily rainfall data
- Calculate monthly rainfall totals
- Display animated yearly bar charts (1884-2025)
- Show rainfall statistics

## Visualization Features

### Color Mapping
- **Yellow**: < 50mm (Dry months)
- **Light Blue**: 50-200mm (Normal rainfall)
- **Medium Blue**: 200-400mm (Above average)
- **Dark Blue**: 400-600mm (High rainfall)
- **Black**: > 600mm (Extreme rainfall events)

### Animation Features
- **Automatic Play**: Animation starts automatically
- **Complete Coverage**: Shows all 135+ years of data (1884-2025)
- **Value Labels**: Every month displays exact rainfall amount (including 0mm)
- **Unified Scaling**: All years use the same Y-axis for comparison

## Data Statistics
- **Coverage**: 1884-2025 (49,000+ daily records)
- **Monthly Totals**: 1,600+ months of data
- **Rainfall Range**: 0mm to 1,346mm per month
- **Average**: ~188mm per month
- **Wettest Month**: June 2008 (1,346.1mm)
- **Driest Month**: December 1909 (0.0mm)

## Technical Details

### Dependencies
- `pandas>=2.0.0`: Data manipulation and analysis
- `matplotlib>=3.7.0`: Plotting and animation framework
- `seaborn>=0.12.0`: Enhanced color palettes
- `numpy>=1.24.0`: Numerical computations

### Data Processing
- Handles 49,000+ daily rainfall records from CSV
- Converts trace amounts to 0.01mm
- Manages missing data and data quality flags
- Calculates monthly totals and statistics

## License
This project visualizes publicly available data from Hong Kong Observatory.
Educational and research use.