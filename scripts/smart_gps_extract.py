"""
Importable wrapper for smart-gps-extract.py

This module provides importable functions from the main script
for testing purposes.
"""

import sys
from pathlib import Path

# Import from the main script (with dashes)
# We'll use a workaround to import it
import importlib.util

script_path = Path(__file__).parent / 'smart-gps-extract.py'
spec = importlib.util.spec_from_file_location("smart_gps_extract_main", script_path)
if spec and spec.loader:
    smart_gps_extract_main = importlib.util.module_from_spec(spec)
    sys.modules["smart_gps_extract_main"] = smart_gps_extract_main
    spec.loader.exec_module(smart_gps_extract_main)
    
    # Re-export all functions and classes
    Colors = smart_gps_extract_main.Colors
    print_info = smart_gps_extract_main.print_info
    print_success = smart_gps_extract_main.print_success
    print_warning = smart_gps_extract_main.print_warning
    print_error = smart_gps_extract_main.print_error
    print_header = smart_gps_extract_main.print_header
    ask_continue = smart_gps_extract_main.ask_continue
    
    # Export main functions if they exist
    try:
        extract_gps_data = smart_gps_extract_main.extract_gps_data
        analyze_date_range = smart_gps_extract_main.analyze_date_range
        reverse_geocode_locations = smart_gps_extract_main.reverse_geocode_locations
        validate_coverage = smart_gps_extract_main.validate_coverage
        generate_gpx = smart_gps_extract_main.generate_gpx
        save_location_summary = smart_gps_extract_main.save_location_summary
    except AttributeError:
        # Functions might not be defined as top-level
        pass

else:
    raise ImportError("Could not load smart-gps-extract.py")

