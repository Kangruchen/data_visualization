#!/usr/bin/env python3
"""
Animated Rainfall Map Visualization

This script creates an animated map showing monthly average rainfall data
over the last 100 years using matplotlib and cartopy.

Usage:
    python main.py              # Run with sample data
    python main.py --static     # Show static example
    python main.py --save       # Save animation as GIF
"""

import argparse
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import RainfallDataLoader
from src.map_animator import RainfallMapAnimator
from src.visualization import setup_matplotlib_style, print_data_summary

def main():
    """Main function to run the rainfall animation."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Animated Rainfall Map Visualization')
    parser.add_argument('--data', type=str, default='data/rainfall_data.csv',
                       help='Path to rainfall data CSV file')
    parser.add_argument('--static', action='store_true',
                       help='Show a static frame instead of animation')
    parser.add_argument('--save', type=str, default=None,
                       help='Save animation as GIF (provide filename)')
    parser.add_argument('--year', type=int, default=2020,
                       help='Year for static display (default: 2020)')
    parser.add_argument('--month', type=int, default=7,
                       help='Month for static display (default: 7)')
    parser.add_argument('--interval', type=int, default=200,
                       help='Animation interval in milliseconds (default: 200)')
    
    args = parser.parse_args()
    
    # Set up matplotlib style
    setup_matplotlib_style()
    
    print("🌧️  Animated Rainfall Map Visualization")
    print("=" * 50)
    
    # Initialize data loader
    print(f"Loading data from: {args.data}")
    data_loader = RainfallDataLoader(args.data)
    
    # Load and validate data
    data = data_loader.load_data()
    print_data_summary(data)
    
    # Initialize animator
    animator = RainfallMapAnimator(data_loader)
    
    try:
        if args.static:
            # Show static frame
            print(f"Displaying static frame for {args.month}/{args.year}")
            fig = animator.show_static_frame(args.year, args.month)
            import matplotlib.pyplot as plt
            plt.show()
            
        else:
            # Create animation
            print("Creating animation...")
            print("⏱️  This may take a moment to initialize...")
            
            save_path = args.save if args.save else None
            if save_path and not save_path.endswith('.gif'):
                save_path += '.gif'
            
            anim = animator.create_animation(
                interval=args.interval,
                save_path=save_path
            )
            
            if not save_path:
                print("🎬 Animation ready! Close the window to exit.")
                import matplotlib.pyplot as plt
                plt.show()
            else:
                print(f"✅ Animation saved to: {save_path}")
    
    except KeyboardInterrupt:
        print("\n⚠️  Animation interrupted by user")
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\nTo install required packages, run:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    print("\n✨ Thank you for using the Rainfall Map Visualizer!")
    return 0

if __name__ == '__main__':
    exit(main())
