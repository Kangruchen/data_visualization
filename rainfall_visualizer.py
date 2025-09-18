#!/usr/bin/env python3
"""
Hong Kong Rainfall Visualization System
Creates animated map visualization of monthly rainfall data from Hong Kong Observatory
Colors range from red (low rainfall) to blue (high rainfall)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import seaborn as sns
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

class HKRainfallVisualizer:
    """Hong Kong rainfall data visualizer with animated map"""
    
    def __init__(self, csv_file="daily_HKO_RF_ALL.csv"):
        """Initialize the visualizer with CSV data file"""
        self.csv_file = csv_file
        self.df = None
        self.monthly_data = None
        self.color_map = None
        self.fig = None
        self.ax = None
        

        
        print("Hong Kong Rainfall Visualizer initialized")
    
    def load_data(self):
        """Load and preprocess the rainfall data from CSV"""
        print("Loading rainfall data from CSV...")
        
        try:
            # Read CSV file, skipping header lines
            self.df = pd.read_csv(self.csv_file, skiprows=2)
            
            # Rename columns for easier handling
            self.df.columns = ['Year', 'Month', 'Day', 'Rainfall_mm', 'Quality']
            
            # Filter out non-numeric rows and convert data types
            self.df = self.df[self.df['Year'].astype(str).str.isdigit()]
            self.df['Year'] = self.df['Year'].astype(int)
            self.df['Month'] = self.df['Month'].astype(int)
            self.df['Day'] = self.df['Day'].astype(int)
            
            # Convert rainfall values, handling 'Trace' and missing values
            def parse_rainfall(val):
                if pd.isna(val) or val == '***':
                    return np.nan
                if val == 'Trace' or val == '微量':
                    return 0.01  # Trace amount
                try:
                    return float(val)
                except:
                    return np.nan
            
            self.df['Rainfall_mm'] = self.df['Rainfall_mm'].apply(parse_rainfall)
            
            # Create datetime column
            self.df['Date'] = pd.to_datetime(self.df[['Year', 'Month', 'Day']], errors='coerce')
            
            # Remove rows with invalid dates or missing rainfall data
            self.df = self.df.dropna(subset=['Date', 'Rainfall_mm'])
            
            print(f"Loaded {len(self.df):,} daily rainfall records")
            print(f"Date range: {self.df['Date'].min().date()} to {self.df['Date'].max().date()}")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def calculate_monthly_totals(self):
        """Calculate monthly rainfall totals"""
        print("Calculating monthly rainfall totals...")
        
        # Group by year and month, sum the rainfall
        self.monthly_data = self.df.groupby(['Year', 'Month']).agg({
            'Rainfall_mm': 'sum',
            'Date': 'first'
        }).reset_index()
        
        # Create year-month string for easier handling
        self.monthly_data['YearMonth'] = (
            self.monthly_data['Year'].astype(str) + '-' + 
            self.monthly_data['Month'].astype(str).str.zfill(2)
        )
        
        # Sort by date
        self.monthly_data = self.monthly_data.sort_values('Date').reset_index(drop=True)
        
        print(f"Calculated {len(self.monthly_data)} monthly totals")
        print(f"Rainfall range: {self.monthly_data['Rainfall_mm'].min():.1f}mm to {self.monthly_data['Rainfall_mm'].max():.1f}mm")
        
        return self.monthly_data
    
    def setup_color_mapping(self):
        """Set up color mapping from red (low) to blue (high) rainfall"""
        min_rain = self.monthly_data['Rainfall_mm'].min()
        max_rain = self.monthly_data['Rainfall_mm'].max()
        
        print(f"Setting up color mapping: {min_rain:.1f}mm (red) to {max_rain:.1f}mm (blue)")
        
        # Create custom colormap from red to blue
        colors = ['#8B0000', '#FF0000', '#FF4500', '#FFA500', '#FFFF00', 
                 '#ADFF2F', '#00FF00', '#00CED1', '#0000FF', '#000080']
        n_bins = 100
        self.color_map = sns.blend_palette(colors, n_colors=n_bins, as_cmap=True)
        
        # Normalize rainfall values to [0, 1] range
        self.monthly_data['Normalized_Rain'] = (
            (self.monthly_data['Rainfall_mm'] - min_rain) / (max_rain - min_rain)
        )
    

    
    def get_bar_color(self, rainfall_mm):
        """Get bar color based on rainfall amount"""
        if rainfall_mm < 50:
            return '#FFD700'  # Yellow for < 50mm
        elif rainfall_mm <= 600:
            # Different shades of blue for 50-600mm
            # Normalize within this range (0 to 1)
            normalized = (rainfall_mm - 50) / (600 - 50)
            # Light blue to dark blue gradient
            blues = ['#87CEEB', '#4682B4', '#1E90FF', '#0000FF', '#000080']
            idx = int(normalized * (len(blues) - 1))
            return blues[min(idx, len(blues) - 1)]
        else:
            return '#000000'  # Black for > 600mm
    
    def update_yearly_frame(self, year):
        """Update function for yearly bar chart animation"""
        self.ax.clear()
        
        # Clear any existing figure-level text to prevent overlap
        # Remove all texts that are not the main title
        for text in self.fig.texts[:]:
            if text != self.fig._suptitle:  # Keep the main title
                text.remove()
        
        # Get data for this year
        year_data = self.monthly_data[self.monthly_data['Year'] == year].copy()
        
        if len(year_data) == 0:
            return
        
        # Ensure we have 12 months, fill missing with 0
        months = list(range(1, 13))
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        rainfall_values = []
        colors = []
        
        for month in months:
            month_data = year_data[year_data['Month'] == month]
            if len(month_data) > 0:
                rainfall = month_data.iloc[0]['Rainfall_mm']
            else:
                rainfall = 0.0
            
            rainfall_values.append(rainfall)
            colors.append(self.get_bar_color(rainfall))
        
        # Create bar chart with smaller bar width for better spacing
        bars = self.ax.bar(month_names, rainfall_values, color=colors, 
                          edgecolor='white', linewidth=1.2, alpha=0.85, width=0.7)
        
        # Customize the chart
        self.ax.set_facecolor('#1a1a1a')
        self.ax.set_ylabel('Rainfall (mm)', fontsize=12, color='white', fontweight='bold')
        self.ax.set_xlabel('Month', fontsize=12, color='white', fontweight='bold')
        
        # Set unified y-axis limit for all years (0 to 1400mm to accommodate extreme values)
        self.ax.set_ylim(0, 1400)
        
        # Add title at the very top of the figure (outside plot area)
        main_title = f"Hong Kong Observatory Monthly Rainfall Statistics - {year}"
        self.fig.suptitle(main_title, fontsize=18, color='white', fontweight='bold', y=0.95)
        
        # Calculate statistics for display
        total_rainfall = sum(rainfall_values)
        avg_rainfall = total_rainfall / 12
        wettest_month_idx = rainfall_values.index(max(rainfall_values))
        wettest_month = month_names[wettest_month_idx]
        driest_month_idx = rainfall_values.index(min(rainfall_values))
        driest_month = month_names[driest_month_idx]
        
        # Add legend on left side and statistics on right side at same level
        self.add_side_by_side_info(total_rainfall, avg_rainfall, wettest_month, 
                                 max(rainfall_values), driest_month, min(rainfall_values))
        
        # Customize axes with smaller font for better fit
        self.ax.tick_params(colors='white', labelsize=10)
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        
        # Add value labels on ALL bars (including 0mm months)
        for bar, value in zip(bars, rainfall_values):
            height = bar.get_height()
            # For zero or very low values, position text slightly above x-axis
            if height < 30:
                label_y = 30
                label_color = 'white'
            else:
                label_y = height + 15
                label_color = 'white'
            
            self.ax.text(bar.get_x() + bar.get_width()/2., label_y,
                       f'{value:.0f}', ha='center', va='bottom', 
                       color=label_color, fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='black', 
                               edgecolor='none', alpha=0.7))
        

    
    def add_side_by_side_info(self, total_rainfall, avg_rainfall, wettest_month, 
                             max_value, driest_month, min_value):
        """Add legend on left and statistics on right outside chart area, below title"""
        from matplotlib.patches import Rectangle
        
        # Create legend elements
        legend_elements = [
            Rectangle((0, 0), 1, 1, facecolor='#FFD700', label='< 50mm'),
            Rectangle((0, 0), 1, 1, facecolor='#4682B4', label='50-600mm'),
            Rectangle((0, 0), 1, 1, facecolor='#000000', label='> 600mm')
        ]
        
        # Position legend towards center-left, outside chart area using figure coordinates
        legend = self.ax.legend(handles=legend_elements, loc='center left', 
                              frameon=True, fancybox=False, shadow=False,
                              facecolor='#2a2a2a', edgecolor='gray', 
                              labelcolor='white', fontsize=9, 
                              bbox_to_anchor=(0.15, 0.88), ncol=3,
                              columnspacing=1.0, handlelength=1.2, handletextpad=0.4,
                              bbox_transform=self.fig.transFigure)
        legend.get_frame().set_alpha(0.9)
        legend.get_frame().set_linewidth(1)
        
        # Add statistics on the right side using figure coordinates
        stats_text = f"Annual: {total_rainfall:.0f}mm | Avg: {avg_rainfall:.0f}mm | Peak: {wettest_month}({max_value:.0f}mm) | Low: {driest_month}({min_value:.0f}mm)"
        self.fig.text(0.93, 0.88, stats_text, ha='right', va='center', 
                     fontsize=9, color='lightgray', fontweight='bold')
    

    
    def create_yearly_bar_animation(self, start_year=1884, end_year=2025, interval=1500):
        """Create yearly bar chart animation"""
        print(f"Creating yearly bar chart animation for {start_year}-{end_year}...")
        
        # Get available years in the data
        available_years = sorted(self.monthly_data['Year'].unique())
        years_to_animate = [y for y in available_years if start_year <= y <= end_year]
        
        if len(years_to_animate) == 0:
            print(f"No data available for {start_year}-{end_year}")
            return None
        
        print(f"Animation will show {len(years_to_animate)} years of data")
        
        # Set up the plot for bar chart - more compact size
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Adjust layout to provide space for title at top and speed controls at bottom
        plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.18)
        
        # Store animation parameters for speed control
        self.years_to_animate = years_to_animate
        self.base_interval = interval
        self.current_speed = 1.0  # Default speed multiplier
        
        # Create animation
        def animate(frame):
            if frame < len(self.years_to_animate):
                year = self.years_to_animate[frame]
                self.update_yearly_frame(year)
        
        self.anim = FuncAnimation(self.fig, animate, frames=len(years_to_animate),
                                interval=interval, repeat=True, blit=False)
        
        # Add speed control buttons
        self.add_speed_controls()
        
        return self.anim
    
    def create_animation(self, start_year=1884, end_year=2025, interval=1500):
        """Create animated visualization - yearly bar charts"""
        return self.create_yearly_bar_animation(start_year, end_year, interval)
    

    
    def print_statistics(self):
        """Print basic statistics about the rainfall data"""
        if self.monthly_data is None:
            print("No monthly data available. Run calculate_monthly_totals() first.")
            return
        
        print("\n=== Hong Kong Rainfall Statistics ===")
        print(f"Total months of data: {len(self.monthly_data)}")
        print(f"Date range: {self.monthly_data['Date'].min().strftime('%Y-%m')} to {self.monthly_data['Date'].max().strftime('%Y-%m')}")
        print(f"Average monthly rainfall: {self.monthly_data['Rainfall_mm'].mean():.1f} mm")
        print(f"Minimum monthly rainfall: {self.monthly_data['Rainfall_mm'].min():.1f} mm")
        print(f"Maximum monthly rainfall: {self.monthly_data['Rainfall_mm'].max():.1f} mm")
        
        # Find wettest and driest months
        wettest = self.monthly_data.loc[self.monthly_data['Rainfall_mm'].idxmax()]
        driest = self.monthly_data.loc[self.monthly_data['Rainfall_mm'].idxmin()]
        
        print(f"Wettest month: {wettest['YearMonth']} ({wettest['Rainfall_mm']:.1f} mm)")
        print(f"Driest month: {driest['YearMonth']} ({driest['Rainfall_mm']:.1f} mm)")
    
    def add_speed_controls(self):
        """Add speed control buttons below the chart."""
        from matplotlib.widgets import Button
        
        # Create axes for buttons in the bottom space
        ax_1x = plt.axes([0.35, 0.05, 0.08, 0.04])  # [left, bottom, width, height]
        ax_2x = plt.axes([0.46, 0.05, 0.08, 0.04])
        ax_3x = plt.axes([0.57, 0.05, 0.08, 0.04])
        
        # Create buttons
        self.btn_1x = Button(ax_1x, '1x Speed')
        self.btn_2x = Button(ax_2x, '2x Speed') 
        self.btn_3x = Button(ax_3x, '3x Speed')
        
        # Connect button events
        self.btn_1x.on_clicked(lambda x: self.set_speed(1.0))
        self.btn_2x.on_clicked(lambda x: self.set_speed(2.0))
        self.btn_3x.on_clicked(lambda x: self.set_speed(3.0))
        
        # Highlight current speed button
        self.update_button_colors()
    
    def set_speed(self, speed):
        """Set animation speed."""
        self.current_speed = speed
        
        # Stop current animation
        self.anim.pause()
        
        # Create new animation with updated interval
        new_interval = int(self.base_interval / speed)
        
        def animate(frame):
            if frame < len(self.years_to_animate):
                year = self.years_to_animate[frame]
                self.update_yearly_frame(year)
        
        self.anim = FuncAnimation(self.fig, animate, frames=len(self.years_to_animate),
                                interval=new_interval, repeat=True, blit=False)
        
        # Update button colors
        self.update_button_colors()
        
        # Resume animation
        self.anim.resume()
    
    def update_button_colors(self):
        """Update button colors to highlight current speed."""
        # Reset all buttons to default color
        self.btn_1x.color = 'lightgray'
        self.btn_2x.color = 'lightgray'
        self.btn_3x.color = 'lightgray'
        
        # Highlight current speed button
        if self.current_speed == 1.0:
            self.btn_1x.color = 'lightgreen'
        elif self.current_speed == 2.0:
            self.btn_2x.color = 'lightgreen'
        elif self.current_speed == 3.0:
            self.btn_3x.color = 'lightgreen'
        
        # Redraw buttons
        self.btn_1x.ax.figure.canvas.draw()
        self.btn_2x.ax.figure.canvas.draw()
        self.btn_3x.ax.figure.canvas.draw()

def main():
    """Main function to run the bar chart animation"""
    print("=== Hong Kong Rainfall Visualization System ===")
    
    # Initialize visualizer
    visualizer = HKRainfallVisualizer()
    
    # Load and process data
    if not visualizer.load_data():
        print("Failed to load data. Please check the CSV file.")
        return
    
    visualizer.calculate_monthly_totals()
    visualizer.setup_color_mapping()
    
    # Print statistics
    visualizer.print_statistics()
    
    # Create and show animation directly
    print("\nStarting Hong Kong rainfall animation (1884-2025)...")
    print("🎮 SPEED CONTROLS: Use the buttons below the chart")
    print("   • 1x Speed: Normal speed (default)")
    print("   • 2x Speed: Double speed") 
    print("   • 3x Speed: Triple speed")
    print("Close the plot window to exit.")
    
    try:
        anim = visualizer.create_animation(1884, 2025, interval=1500)
        if anim:
            plt.show()
        else:
            print("Failed to create animation.")
            
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()