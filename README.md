# Animated Rainfall Map Project

This project creates an animated map visualization showing monthly average rainfall data over the last 100 years using matplotlib.

## Features

- Animated scatter plot on world map
- Monthly rainfall data visualization
- Time-series animation over 100 years
- Color-coded precipitation levels

## Requirements

- Python 3.8+
- matplotlib
- numpy
- pandas
- cartopy (for map projections)
- geopandas (for geographic data)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Project Structure

```
├── data/
│   └── rainfall_data.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── map_animator.py
│   └── visualization.py
├── main.py
├── requirements.txt
└── README.md
```

## Data Format

The rainfall data should be in CSV format with columns:
- year: Year of measurement
- month: Month of measurement
- latitude: Geographic latitude
- longitude: Geographic longitude
- rainfall: Monthly rainfall amount (mm)
