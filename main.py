#!/usr/bin/env python3
"""
Hong Kong Rainfall Visualization - Main Entry Point
Automatically plays animated yearly bar charts of Hong Kong Observatory rainfall data
"""

import sys
import os
import matplotlib.pyplot as plt
from rainfall_visualizer import HKRainfallVisualizer

def main():
    """Main function to run Hong Kong rainfall visualization"""
    print("=== Hong Kong Rainfall Visualization System ===")
    print("Loading Hong Kong Observatory daily rainfall data...")
    print("Creating animated yearly bar charts with color-coded rainfall")
    print("Colors: Yellow (< 50mm) → Blue (50-600mm) → Black (> 600mm)")
    print()
    
    # Check if CSV file exists
    csv_file = "daily_HKO_RF_ALL.csv"
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("Please ensure the Hong Kong Observatory rainfall data CSV is in the current directory.")
        return 1
    
    try:
        # Initialize and run visualization
        visualizer = HKRainfallVisualizer(csv_file)
        
        # Load and process data
        if not visualizer.load_data():
            print("Failed to load rainfall data from CSV file.")
            return 1
        
        visualizer.calculate_monthly_totals()
        visualizer.setup_color_mapping()
        
        # Show statistics
        visualizer.print_statistics()
        
        # Run animation directly
        print("\n" + "="*50)
        print("Starting Hong Kong rainfall animation (1884-2025)...")
        print("Animation will play automatically at medium speed")
        print("Close the plot window to exit")
        print("="*50)
        
        # Create and show animation
        anim = visualizer.create_animation(1884, 2025, interval=2000)
        
        if anim:
            print("📊 Color Legend: Yellow (<50mm) | Blue (50-600mm) | Black (>600mm)")
            print("🎬 Starting animation...")
            plt.show()
        else:
            print("Failed to create animation.")
            return 1
        
        print("Animation completed!")
        return 0
        
    except KeyboardInterrupt:
        print("\nAnimation stopped by user.")
        return 0
    except Exception as e:
        print(f"Error running animation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
