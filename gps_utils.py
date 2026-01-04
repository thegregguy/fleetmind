"""
GPS Utilities Module
Handles GPS coordinate management and distance calculations for FleetMind.
"""
from typing import Tuple, Optional
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class GPSUtils:
    """Utility class for GPS-related operations."""
    
    def __init__(self):
        """Initialize GPS utilities with geocoder."""
        self.geocoder = Nominatim(user_agent="fleetmind_app")
    
    @staticmethod
    def calculate_distance(start_coords: Tuple[float, float], 
                          end_coords: Tuple[float, float]) -> float:
        """
        Calculate distance between two GPS coordinates in miles.
        
        Args:
            start_coords: Tuple of (latitude, longitude) for start point
            end_coords: Tuple of (latitude, longitude) for end point
            
        Returns:
            Distance in miles
        """
        return geodesic(start_coords, end_coords).miles
    
    def get_address(self, coords: Tuple[float, float]) -> Optional[str]:
        """
        Get human-readable address from GPS coordinates.
        
        Args:
            coords: Tuple of (latitude, longitude)
            
        Returns:
            Address string or None if geocoding fails
        """
        try:
            location = self.geocoder.reverse(coords, timeout=10)
            return location.address if location else None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding error: {e}")
            return None
    
    @staticmethod
    def format_coords(coords: Tuple[float, float]) -> str:
        """
        Format coordinates as a string for storage.
        
        Args:
            coords: Tuple of (latitude, longitude)
            
        Returns:
            Formatted string "lat,lon"
        """
        return f"{coords[0]:.6f},{coords[1]:.6f}"
    
    @staticmethod
    def parse_coords(coords_str: str) -> Optional[Tuple[float, float]]:
        """
        Parse coordinates from a string.
        
        Args:
            coords_str: String in format "lat,lon"
            
        Returns:
            Tuple of (latitude, longitude) or None if parsing fails
        """
        try:
            parts = coords_str.split(',')
            return (float(parts[0]), float(parts[1]))
        except (ValueError, IndexError):
            return None
