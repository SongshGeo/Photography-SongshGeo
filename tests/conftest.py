"""
Pytest configuration and shared fixtures for photography workflow tests.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta


@pytest.fixture
def temp_dir():
    """
    Fixture: Create a temporary directory for test files.
    
    Yields:
        Path: Temporary directory path
        
    Cleanup:
        Removes the directory after test completion
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def gpx_dir(temp_dir):
    """
    Fixture: Create gpx directory in temp workspace.
    
    Args:
        temp_dir: Temporary directory fixture
        
    Returns:
        Path: gpx directory path
    """
    gpx_path = temp_dir / "gpx"
    gpx_path.mkdir()
    return gpx_path


@pytest.fixture
def sample_gps_data():
    """
    Fixture: Generate sample GPS data for testing.
    
    Returns:
        list: Sample GPS data with various scenarios
    """
    base_date = datetime(2025, 8, 15, 10, 0, 0)
    
    return [
        # Day 1: Tórshavn, Faroe Islands (3 photos)
        {
            "FileName": "IMG_001.jpg",
            "GPSLatitude": 62.0104,
            "GPSLongitude": -6.7719,
            "GPSAltitude": 0,
            "DateTimeOriginal": base_date.strftime('%Y:%m:%d %H:%M:%S')
        },
        {
            "FileName": "IMG_002.jpg",
            "GPSLatitude": 62.0105,
            "GPSLongitude": -6.7720,
            "DateTimeOriginal": (base_date + timedelta(hours=2)).strftime('%Y:%m:%d %H:%M:%S')
        },
        {
            "FileName": "IMG_003.jpg",
            "GPSLatitude": 62.0106,
            "GPSLongitude": -6.7718,
            "DateTimeOriginal": (base_date + timedelta(hours=5)).strftime('%Y:%m:%d %H:%M:%S')
        },
        # Day 2: Copenhagen, Denmark (2 photos)
        {
            "FileName": "IMG_004.jpg",
            "GPSLatitude": 55.6761,
            "GPSLongitude": 12.5683,
            "DateTimeOriginal": (base_date + timedelta(days=1, hours=1)).strftime('%Y:%m:%d %H:%M:%S')
        },
        {
            "FileName": "IMG_005.jpg",
            "GPSLatitude": 55.6762,
            "GPSLongitude": 12.5684,
            "DateTimeOriginal": (base_date + timedelta(days=1, hours=3)).strftime('%Y:%m:%d %H:%M:%S')
        },
        # Photo without GPS
        {
            "FileName": "IMG_006.jpg",
            "DateTimeOriginal": (base_date + timedelta(days=2)).strftime('%Y:%m:%d %H:%M:%S')
        },
        # Photo without date
        {
            "FileName": "IMG_007.jpg",
            "GPSLatitude": 55.6763,
            "GPSLongitude": 12.5685
        },
    ]


@pytest.fixture
def sample_gps_no_coords():
    """
    Fixture: GPS data with no coordinates (edge case).
    
    Returns:
        list: Photos without GPS coordinates
    """
    return [
        {"FileName": "IMG_001.jpg", "DateTimeOriginal": "2025:08:15 10:00:00"},
        {"FileName": "IMG_002.jpg", "DateTimeOriginal": "2025:08:15 12:00:00"},
    ]


@pytest.fixture
def sample_gps_single_day():
    """
    Fixture: GPS data from a single day.
    
    Returns:
        list: Photos all from one day
    """
    base_date = datetime(2025, 8, 15, 10, 0, 0)
    return [
        {
            "FileName": f"IMG_{i:03d}.jpg",
            "GPSLatitude": 62.0104 + i * 0.001,
            "GPSLongitude": -6.7719 + i * 0.001,
            "DateTimeOriginal": (base_date + timedelta(hours=i)).strftime('%Y:%m:%d %H:%M:%S')
        }
        for i in range(10)
    ]


@pytest.fixture
def sample_gps_multi_city_per_day():
    """
    Fixture: GPS data with multiple cities in one day.
    
    Returns:
        list: Photos from different cities on the same day
    """
    base_date = datetime(2025, 8, 15, 8, 0, 0)
    
    return [
        # Morning in Tórshavn
        {
            "FileName": "IMG_001.jpg",
            "GPSLatitude": 62.0104,
            "GPSLongitude": -6.7719,
            "DateTimeOriginal": base_date.strftime('%Y:%m:%d %H:%M:%S')
        },
        {
            "FileName": "IMG_002.jpg",
            "GPSLatitude": 62.0105,
            "GPSLongitude": -6.7720,
            "DateTimeOriginal": (base_date + timedelta(hours=1)).strftime('%Y:%m:%d %H:%M:%S')
        },
        # Afternoon in Vágar (50km away)
        {
            "FileName": "IMG_003.jpg",
            "GPSLatitude": 62.0644,
            "GPSLongitude": -7.2782,
            "DateTimeOriginal": (base_date + timedelta(hours=6)).strftime('%Y:%m:%d %H:%M:%S')
        },
        {
            "FileName": "IMG_004.jpg",
            "GPSLatitude": 62.0645,
            "GPSLongitude": -7.2783,
            "DateTimeOriginal": (base_date + timedelta(hours=8)).strftime('%Y:%m:%d %H:%M:%S')
        },
    ]


@pytest.fixture
def sample_gps_with_gaps():
    """
    Fixture: GPS data with date gaps.
    
    Returns:
        list: Photos with missing dates in between
    """
    return [
        # Day 1
        {
            "FileName": "IMG_001.jpg",
            "GPSLatitude": 62.0104,
            "GPSLongitude": -6.7719,
            "DateTimeOriginal": "2025:08:15 10:00:00"
        },
        # Day 5 (gap of 3 days)
        {
            "FileName": "IMG_002.jpg",
            "GPSLatitude": 55.6761,
            "GPSLongitude": 12.5683,
            "DateTimeOriginal": "2025:08:19 10:00:00"
        },
    ]


@pytest.fixture
def mock_exiftool_output(sample_gps_data):
    """
    Fixture: Mock exiftool JSON output.
    
    Args:
        sample_gps_data: Sample GPS data fixture
        
    Returns:
        str: JSON string mimicking exiftool output
    """
    return json.dumps(sample_gps_data, indent=2)

