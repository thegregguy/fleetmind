"""
Demo Mode for FleetMind
Simulates Google Sheets functionality without requiring actual credentials.
Useful for testing and demonstration purposes.
"""
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime


class DemoSheetsManager:
    """Demo manager that simulates Google Sheets operations in memory."""
    
    MAIN_LOG_HEADERS = [
        'Timestamp',
        'Vehicle',
        'Purpose',
        'Start GPS',
        'End GPS',
        'Start Addr',
        'End Addr',
        'Google Miles',
        'Actual Miles',
        'Gas Stop?',
        'Odometer',
        'Gallons',
        'Price/Gal',
        'Trip Fuel Cost ($)'
    ]
    
    def __init__(self):
        """Initialize demo manager with in-memory storage."""
        self.data = []
        self.authenticated = False
        
    def authenticate(self):
        """Simulate authentication."""
        self.authenticated = True
        print("Demo mode: Simulated authentication successful")
    
    def get_or_create_worksheet(self, sheet_name: str):
        """Simulate worksheet retrieval."""
        return self
    
    def append_trip_log(self, trip_data: Dict[str, Any], sheet_name: str = 'Main_Log'):
        """Append a trip log entry to in-memory storage."""
        row = [
            trip_data.get('timestamp', datetime.now().isoformat()),
            trip_data.get('vehicle', ''),
            trip_data.get('purpose', ''),
            trip_data.get('start_gps', ''),
            trip_data.get('end_gps', ''),
            trip_data.get('start_addr', ''),
            trip_data.get('end_addr', ''),
            trip_data.get('google_miles', 0),
            trip_data.get('actual_miles', ''),
            trip_data.get('gas_stop', False),
            trip_data.get('odometer', ''),
            trip_data.get('gallons', ''),
            trip_data.get('price_per_gal', ''),
            trip_data.get('trip_fuel_cost', '')
        ]
        
        self.data.append(dict(zip(self.MAIN_LOG_HEADERS, row)))
    
    def get_all_records(self, sheet_name: str = 'Main_Log') -> pd.DataFrame:
        """Get all records as a DataFrame."""
        return pd.DataFrame(self.data)
    
    def get_last_trip(self, sheet_name: str = 'Main_Log') -> Optional[Dict[str, Any]]:
        """Get the last trip entry."""
        if not self.data:
            return None
        return self.data[-1]
    
    def update_cell(self, row: int, col: int, value: Any, sheet_name: str = 'Main_Log'):
        """Update a specific cell (simulated)."""
        # row is 1-indexed and includes header, so data index is row-2
        data_idx = row - 2
        if 0 <= data_idx < len(self.data):
            col_name = self.MAIN_LOG_HEADERS[col - 1]
            self.data[data_idx][col_name] = value
    
    def batch_update_cells(self, updates: List[Dict[str, Any]], sheet_name: str = 'Main_Log'):
        """Batch update multiple cells."""
        for update in updates:
            self.update_cell(update['row'], update['col'], update['value'], sheet_name)
    
    def get_gas_stops(self, sheet_name: str = 'Main_Log') -> pd.DataFrame:
        """Get all gas stop entries."""
        df = self.get_all_records(sheet_name)
        if df.empty:
            return df
        
        gas_stops = df[df['Gas Stop?'] == True].copy()
        return gas_stops
    
    def clear_data(self):
        """Clear all stored data (demo mode utility)."""
        self.data = []
