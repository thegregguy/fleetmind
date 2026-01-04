"""
Ping Workflow Module
Handles trip logging functionality for FleetMind.
"""
from typing import Tuple, Optional, Dict, Any
from datetime import datetime
from gps_utils import GPSUtils
from sheets_manager import GoogleSheetsManager


class PingManager:
    """Manager class for Ping (trip logging) operations."""
    
    def __init__(self, sheets_manager: GoogleSheetsManager):
        """
        Initialize Ping Manager.
        
        Args:
            sheets_manager: GoogleSheetsManager instance
        """
        self.sheets_manager = sheets_manager
        self.gps_utils = GPSUtils()
    
    def log_trip(self, 
                 current_coords: Tuple[float, float],
                 vehicle: str,
                 purpose: str,
                 is_gas_stop: bool = False,
                 odometer: Optional[float] = None,
                 gallons: Optional[float] = None,
                 price_per_gal: Optional[float] = None) -> Dict[str, Any]:
        """
        Log a new trip by capturing current GPS and calculating distance.
        
        Args:
            current_coords: Current GPS coordinates (lat, lon)
            vehicle: Vehicle identifier
            purpose: Trip purpose/status
            is_gas_stop: Whether this is a gas fill-up
            odometer: Odometer reading (for gas stops)
            gallons: Gallons purchased (for gas stops)
            price_per_gal: Price per gallon (for gas stops)
            
        Returns:
            Dictionary containing the logged trip data
        """
        # Get the last trip to determine start coordinates
        last_trip = self.sheets_manager.get_last_trip()
        
        if last_trip and last_trip.get('End GPS'):
            # Parse previous end coordinates as our start
            start_coords = self.gps_utils.parse_coords(last_trip['End GPS'])
            if start_coords:
                # Calculate distance
                google_miles = self.gps_utils.calculate_distance(
                    start_coords, current_coords
                )
            else:
                google_miles = 0
                start_coords = current_coords  # Fallback
        else:
            # First trip - no previous endpoint
            start_coords = current_coords
            google_miles = 0
        
        # Get addresses (reverse geocoding)
        start_addr = self.gps_utils.get_address(start_coords) or ""
        end_addr = self.gps_utils.get_address(current_coords) or ""
        
        # Prepare trip data
        trip_data = {
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle,
            'purpose': purpose,
            'start_gps': self.gps_utils.format_coords(start_coords),
            'end_gps': self.gps_utils.format_coords(current_coords),
            'start_addr': start_addr,
            'end_addr': end_addr,
            'google_miles': round(google_miles, 2),
            'actual_miles': '',  # Will be calculated during Smart Gas reconciliation
            'gas_stop': is_gas_stop,
            'odometer': odometer if is_gas_stop else '',
            'gallons': gallons if is_gas_stop else '',
            'price_per_gal': price_per_gal if is_gas_stop else '',
            'trip_fuel_cost': ''  # Will be calculated during Smart Gas reconciliation
        }
        
        # Append to Google Sheets
        self.sheets_manager.append_trip_log(trip_data)
        
        return trip_data
    
    def get_trip_history(self, limit: Optional[int] = None) -> list:
        """
        Get trip history from the sheet.
        
        Args:
            limit: Maximum number of trips to return (None for all)
            
        Returns:
            List of trip records
        """
        df = self.sheets_manager.get_all_records()
        
        if df.empty:
            return []
        
        if limit:
            df = df.tail(limit)
        
        return df.to_dict('records')
