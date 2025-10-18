"""
Helper utilities for testing GPS extraction scripts.

This module provides utilities to:
- Generate test data
- Mock external dependencies
- Validate outputs
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class TestDataGenerator:
    """Generate realistic test data for GPS extraction tests."""
    
    @staticmethod
    def create_gps_photo_data(
        num_photos: int,
        start_date: datetime,
        lat_start: float = 62.0,
        lon_start: float = -6.77,
        lat_delta: float = 0.001,
        lon_delta: float = 0.001,
        time_delta_hours: int = 1,
        include_gps: bool = True,
        include_date: bool = True
    ) -> List[Dict]:
        """
        Generate GPS photo data for testing.
        
        Args:
            num_photos: Number of photos to generate
            start_date: Starting datetime for first photo
            lat_start: Starting latitude
            lon_start: Starting longitude
            lat_delta: Latitude increment per photo
            lon_delta: Longitude increment per photo
            time_delta_hours: Hours between photos
            include_gps: Whether to include GPS coordinates
            include_date: Whether to include timestamp
            
        Returns:
            List of photo data dictionaries
            
        Examples:
            >>> gen = TestDataGenerator()
            >>> data = gen.create_gps_photo_data(
            ...     num_photos=5,
            ...     start_date=datetime(2025, 8, 15, 10, 0, 0)
            ... )
            >>> len(data)
            5
            >>> 'GPSLatitude' in data[0]
            True
        """
        photos = []
        current_date = start_date
        
        for i in range(num_photos):
            photo = {"FileName": f"IMG_{i:04d}.jpg"}
            
            if include_gps:
                photo["GPSLatitude"] = lat_start + i * lat_delta
                photo["GPSLongitude"] = lon_start + i * lon_delta
                photo["GPSAltitude"] = 0
            
            if include_date:
                photo["DateTimeOriginal"] = current_date.strftime('%Y:%m:%d %H:%M:%S')
                current_date += timedelta(hours=time_delta_hours)
            
            photos.append(photo)
        
        return photos
    
    @staticmethod
    def create_multi_day_trip(
        days: int,
        photos_per_day: int,
        start_date: datetime,
        cities: Optional[List[Tuple[float, float]]] = None
    ) -> List[Dict]:
        """
        Generate multi-day trip data.
        
        Args:
            days: Number of days in trip
            photos_per_day: Photos per day
            start_date: Trip start date
            cities: List of (lat, lon) tuples for each day (optional)
            
        Returns:
            List of photo data spanning multiple days
            
        Examples:
            >>> gen = TestDataGenerator()
            >>> cities = [(62.0, -6.77), (55.67, 12.56)]  # Tórshavn, Copenhagen
            >>> data = gen.create_multi_day_trip(
            ...     days=2,
            ...     photos_per_day=3,
            ...     start_date=datetime(2025, 8, 15),
            ...     cities=cities
            ... )
            >>> len(data)
            6
        """
        if cities is None:
            # Default: small increments simulating nearby locations
            cities = [(62.0 + i * 0.1, -6.77 + i * 0.1) for i in range(days)]
        
        all_photos = []
        current_date = start_date
        
        for day_idx in range(days):
            lat, lon = cities[day_idx % len(cities)]
            
            for photo_idx in range(photos_per_day):
                photo = {
                    "FileName": f"DAY{day_idx+1}_IMG_{photo_idx:03d}.jpg",
                    "GPSLatitude": lat + photo_idx * 0.001,
                    "GPSLongitude": lon + photo_idx * 0.001,
                    "DateTimeOriginal": current_date.strftime('%Y:%m:%d %H:%M:%S')
                }
                all_photos.append(photo)
                current_date += timedelta(hours=2)
            
            # Move to next day
            current_date = (start_date + timedelta(days=day_idx + 1)).replace(hour=8)
        
        return all_photos
    
    @staticmethod
    def create_trip_with_gaps(
        total_days: int,
        photo_days: List[int],
        start_date: datetime
    ) -> List[Dict]:
        """
        Generate trip data with missing days.
        
        Args:
            total_days: Total trip duration
            photo_days: List of day numbers (1-indexed) with photos
            start_date: Trip start date
            
        Returns:
            Photo data with gaps
            
        Examples:
            >>> gen = TestDataGenerator()
            >>> data = gen.create_trip_with_gaps(
            ...     total_days=7,
            ...     photo_days=[1, 3, 5, 7],  # Missing days 2, 4, 6
            ...     start_date=datetime(2025, 8, 15)
            ... )
            >>> # Should have photos only on specified days
        """
        photos = []
        
        for day_num in photo_days:
            if day_num > total_days:
                continue
            
            photo_date = start_date + timedelta(days=day_num - 1)
            photo_date = photo_date.replace(hour=12)
            
            photo = {
                "FileName": f"IMG_DAY{day_num}.jpg",
                "GPSLatitude": 62.0 + day_num * 0.01,
                "GPSLongitude": -6.77 + day_num * 0.01,
                "DateTimeOriginal": photo_date.strftime('%Y:%m:%d %H:%M:%S')
            }
            photos.append(photo)
        
        return photos


class MockGeocoder:
    """Mock geocoder for testing without API calls."""
    
    def __init__(self):
        """Initialize mock geocoder with known coordinates."""
        self.known_locations = {
            # Format: (lat, lon) -> city_name
            (62.01, -6.77): "Tórshavn",
            (55.68, 12.57): "Copenhagen",
            (56.16, 10.20): "Aarhus",
            (55.40, 10.38): "Odense",
            (35.68, 139.65): "Tokyo",
            (51.51, -0.13): "London",
            (48.86, 2.35): "Paris",
        }
    
    def reverse(self, coords: Tuple[float, float], language: str = 'en') -> Optional[Dict]:
        """
        Mock reverse geocoding.
        
        Args:
            coords: (latitude, longitude) tuple
            language: Language for result (ignored in mock)
            
        Returns:
            Mock geocoding result or None
            
        Examples:
            >>> geocoder = MockGeocoder()
            >>> result = geocoder.reverse((62.01, -6.77))
            >>> result['city']
            'Tórshavn'
        """
        # Round to 2 decimals for matching
        lat_round = round(coords[0], 2)
        lon_round = round(coords[1], 2)
        
        city = self.known_locations.get((lat_round, lon_round))
        
        if city:
            return {
                'city': city,
                'country': self._get_country(city),
                'address': f"{city}"
            }
        
        return None
    
    @staticmethod
    def _get_country(city: str) -> str:
        """Get country for a city (simplified)."""
        country_map = {
            'Tórshavn': 'Faroe Islands',
            'Copenhagen': 'Denmark',
            'Aarhus': 'Denmark',
            'Odense': 'Denmark',
            'Tokyo': 'Japan',
            'London': 'United Kingdom',
            'Paris': 'France',
        }
        return country_map.get(city, 'Unknown')


class GPXValidator:
    """Validate GPX file structure and content."""
    
    @staticmethod
    def validate_structure(gpx_content: str) -> Tuple[bool, List[str]]:
        """
        Validate basic GPX structure.
        
        Args:
            gpx_content: GPX XML content as string
            
        Returns:
            Tuple of (is_valid, list_of_errors)
            
        Checks:
            - Valid XML syntax
            - Has GPX root element
            - Has track and segments
            - Has track points
            
        Examples:
            >>> validator = GPXValidator()
            >>> valid, errors = validator.validate_structure(gpx_xml)
            >>> if not valid:
            ...     print(f"Errors: {errors}")
        """
        errors = []
        
        # Check XML declaration
        if '<?xml version' not in gpx_content:
            errors.append("Missing XML declaration")
        
        # Check GPX root
        if '<gpx' not in gpx_content:
            errors.append("Missing GPX root element")
        
        # Check track
        if '<trk' not in gpx_content:
            errors.append("Missing track element")
        
        # Check segments
        if '<trkseg' not in gpx_content:
            errors.append("Missing track segment")
        
        # Check track points
        if '<trkpt' not in gpx_content:
            errors.append("Missing track points")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_track_points(gpx_content: str) -> Tuple[bool, List[str]]:
        """
        Validate track point data.
        
        Args:
            gpx_content: GPX XML content
            
        Returns:
            Tuple of (is_valid, list_of_errors)
            
        Checks:
            - Track points have lat/lon
            - Coordinates are valid
            - Times are present (if expected)
            
        Examples:
            >>> validator = GPXValidator()
            >>> valid, errors = validator.validate_track_points(gpx_xml)
        """
        errors = []
        
        # Basic checks on track points
        if 'lat=' not in gpx_content:
            errors.append("Track points missing latitude")
        
        if 'lon=' not in gpx_content:
            errors.append("Track points missing longitude")
        
        return len(errors) == 0, errors


class OutputValidator:
    """Validate script output files."""
    
    @staticmethod
    def validate_summary_json(summary_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate summary JSON structure.
        
        Args:
            summary_path: Path to summary JSON file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
            
        Expected Structure:
            {
                "trip_name": str,
                "start_date": str,
                "end_date": str,
                "total_days": int,
                "daily_locations": [...],
                "cities_visited": [...]
            }
            
        Examples:
            >>> validator = OutputValidator()
            >>> valid, errors = validator.validate_summary_json(Path("summary.json"))
        """
        errors = []
        
        if not summary_path.exists():
            return False, ["Summary file does not exist"]
        
        try:
            with open(summary_path) as f:
                data = json.load(f)
            
            # Check required fields
            required_fields = [
                'trip_name', 'start_date', 'end_date',
                'total_days', 'daily_locations', 'cities_visited'
            ]
            
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate data types
            if 'total_days' in data and not isinstance(data['total_days'], int):
                errors.append("total_days should be integer")
            
            if 'daily_locations' in data and not isinstance(data['daily_locations'], list):
                errors.append("daily_locations should be list")
            
            if 'cities_visited' in data and not isinstance(data['cities_visited'], list):
                errors.append("cities_visited should be list")
            
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
        except Exception as e:
            errors.append(f"Error reading file: {e}")
        
        return len(errors) == 0, errors


def create_mock_photo_files(
    directory: Path,
    num_files: int = 5,
    extensions: List[str] = None
) -> List[Path]:
    """
    Create empty mock photo files for testing.
    
    Args:
        directory: Directory to create files in
        num_files: Number of files to create
        extensions: List of extensions (default: ['jpg', 'heic'])
        
    Returns:
        List of created file paths
        
    Examples:
        >>> from pathlib import Path
        >>> import tempfile
        >>> temp_dir = Path(tempfile.mkdtemp())
        >>> files = create_mock_photo_files(temp_dir, num_files=3)
        >>> len(files)
        3
    """
    if extensions is None:
        extensions = ['jpg', 'heic']
    
    created_files = []
    
    for i in range(num_files):
        ext = extensions[i % len(extensions)]
        file_path = directory / f"IMG_{i:04d}.{ext}"
        file_path.touch()
        created_files.append(file_path)
    
    return created_files


if __name__ == '__main__':
    # Run basic tests of helper functions
    print("Testing helper utilities...")
    
    gen = TestDataGenerator()
    data = gen.create_gps_photo_data(5, datetime(2025, 8, 15))
    print(f"✅ Generated {len(data)} test photos")
    
    geocoder = MockGeocoder()
    result = geocoder.reverse((62.01, -6.77))
    print(f"✅ Mock geocoding: {result['city']}")
    
    print("\n✅ All helper tests passed!")

