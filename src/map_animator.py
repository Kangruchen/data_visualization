"""
Map animation module for rainfall visualization.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
import numpy as np
from typing import List, Tuple, Optional
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class RainfallMapAnimator:
    """Creates animated map visualizations of rainfall data."""
    
    def __init__(self, data_loader, figsize: Tuple[int, int] = (12, 8)):
        """Initialize the animator with a data loader."""
        self.data_loader = data_loader
        self.figsize = figsize
        self.fig = None
        self.ax = None
        self.scatter = None
        self.colorbar = None
        
        # Animation parameters
        self.current_frame = 0
        self.total_frames = 0
        
        # Data range for consistent coloring
        self.vmin = 0
        self.vmax = 300  # mm of rainfall
        
    def setup_map(self):
        """Set up the base map with geographic features."""
        # Create figure and axis with map projection
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = plt.axes(projection=ccrs.PlateCarree())
        
        # Add map features
        self.ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        self.ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        self.ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.5)
        self.ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.3)
        
        # Set global extent
        self.ax.set_global()
        
        # Add gridlines
        self.ax.gridlines(draw_labels=True, alpha=0.3)
        
        # Set title
        self.ax.set_title('Monthly Average Rainfall Animation (1924-2023)', 
                         fontsize=14, fontweight='bold', pad=20)
        
        return self.fig, self.ax
    
    def create_animation(self, interval: int = 200, save_path: Optional[str] = None):
        """Create and run the rainfall animation."""
        # Load data and get date range
        self.data_loader.load_data()
        min_year, max_year = self.data_loader.get_date_range()
        
        # Calculate total frames (12 months × number of years)
        self.total_frames = (max_year - min_year + 1) * 12
        
        # Set up the map
        self.setup_map()
        
        # Create initial empty scatter plot
        self.scatter = self.ax.scatter([], [], c=[], s=[], 
                                     cmap='Blues', vmin=self.vmin, vmax=self.vmax,
                                     alpha=0.7, transform=ccrs.PlateCarree())
        
        # Add colorbar
        self.colorbar = plt.colorbar(self.scatter, ax=self.ax, orientation='horizontal',
                                   pad=0.05, shrink=0.8, aspect=30)
        self.colorbar.set_label('Monthly Rainfall (mm)', fontsize=12)
        
        # Create animation
        anim = animation.FuncAnimation(self.fig, self.animate_frame, frames=self.total_frames,
                                     interval=interval, blit=False, repeat=True)
        
        # Save animation if path provided
        if save_path:
            print(f"Saving animation to {save_path}...")
            anim.save(save_path, writer='pillow', fps=5)
            print("Animation saved successfully!")
        
        return anim
    
    def animate_frame(self, frame: int):
        """Animate a single frame of the rainfall data."""
        # Calculate year and month from frame number
        min_year, _ = self.data_loader.get_date_range()
        year = min_year + frame // 12
        month = (frame % 12) + 1
        
        # Get data for this time period
        frame_data = self.data_loader.get_data_for_period(year, month)
        
        if not frame_data.empty:
            # Extract coordinates and rainfall values
            lons = frame_data['longitude'].values
            lats = frame_data['latitude'].values
            rainfall = frame_data['rainfall'].values
            
            # Size points based on rainfall amount (minimum size for visibility)
            sizes = np.clip(rainfall * 2, 20, 200)
            
            # Update scatter plot
            self.scatter.set_offsets(np.column_stack([lons, lats]))
            self.scatter.set_array(rainfall)
            self.scatter.set_sizes(sizes)
            
            # Update title with current date
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.ax.set_title(f'Monthly Average Rainfall: {month_names[month-1]} {year}',
                            fontsize=14, fontweight='bold', pad=20)
        
        return [self.scatter]
    
    def show_static_frame(self, year: int, month: int):
        """Display a static frame for a specific year and month."""
        self.setup_map()
        
        # Get data for the specified time
        frame_data = self.data_loader.get_data_for_period(year, month)
        
        if not frame_data.empty:
            lons = frame_data['longitude'].values
            lats = frame_data['latitude'].values
            rainfall = frame_data['rainfall'].values
            sizes = np.clip(rainfall * 2, 20, 200)
            
            # Create scatter plot
            scatter = self.ax.scatter(lons, lats, c=rainfall, s=sizes,
                                    cmap='Blues', vmin=self.vmin, vmax=self.vmax,
                                    alpha=0.7, transform=ccrs.PlateCarree())
            
            # Add colorbar
            cbar = plt.colorbar(scatter, ax=self.ax, orientation='horizontal',
                              pad=0.05, shrink=0.8, aspect=30)
            cbar.set_label('Monthly Rainfall (mm)', fontsize=12)
            
            # Update title
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            self.ax.set_title(f'Monthly Average Rainfall: {month_names[month-1]} {year}',
                            fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        return self.fig
