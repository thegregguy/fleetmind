"""
Google Sheets Integration Module
Handles all interactions with Google Sheets API for FleetMind.
"""
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


class GoogleSheetsManager:
    """Manager class for Google Sheets operations."""
    
    # Define the required scopes for Google Sheets API
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Column headers for Main_Log sheet
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
    
    def __init__(self, service_account_file: str, spreadsheet_id: str):
        """
        Initialize Google Sheets Manager.
        
        Args:
            service_account_file: Path to service account JSON file
            spreadsheet_id: ID of the Google Spreadsheet
        """
        self.service_account_file = service_account_file
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self.spreadsheet = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API."""
        if not os.path.exists(self.service_account_file):
            raise FileNotFoundError(
                f"Service account file not found: {self.service_account_file}"
            )
        
        creds = Credentials.from_service_account_file(
            self.service_account_file,
            scopes=self.SCOPES
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
    
    def get_or_create_worksheet(self, sheet_name: str) -> gspread.Worksheet:
        """
        Get existing worksheet or create new one.
        
        Args:
            sheet_name: Name of the worksheet
            
        Returns:
            Worksheet object
        """
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(
                title=sheet_name,
                rows=1000,
                cols=20
            )
            # Add headers if this is Main_Log
            if sheet_name == 'Main_Log':
                worksheet.append_row(self.MAIN_LOG_HEADERS)
        
        return worksheet
    
    def append_trip_log(self, trip_data: Dict[str, Any], sheet_name: str = 'Main_Log'):
        """
        Append a trip log entry to the Main_Log sheet.
        
        Args:
            trip_data: Dictionary containing trip information
            sheet_name: Name of the sheet to append to
        """
        worksheet = self.get_or_create_worksheet(sheet_name)
        
        # Prepare row data according to headers
        row = [
            trip_data.get('timestamp', datetime.now().isoformat()),
            trip_data.get('vehicle', ''),
            trip_data.get('purpose', ''),
            trip_data.get('start_gps', ''),
            trip_data.get('end_gps', ''),
            trip_data.get('start_addr', ''),
            trip_data.get('end_addr', ''),
            trip_data.get('google_miles', 0),
            trip_data.get('actual_miles', ''),  # Empty initially
            trip_data.get('gas_stop', False),
            trip_data.get('odometer', ''),
            trip_data.get('gallons', ''),
            trip_data.get('price_per_gal', ''),
            trip_data.get('trip_fuel_cost', '')  # Empty initially
        ]
        
        worksheet.append_row(row)
    
    def get_all_records(self, sheet_name: str = 'Main_Log') -> pd.DataFrame:
        """
        Get all records from a worksheet as a DataFrame.
        
        Args:
            sheet_name: Name of the worksheet
            
        Returns:
            DataFrame containing all records
        """
        worksheet = self.get_or_create_worksheet(sheet_name)
        records = worksheet.get_all_records()
        return pd.DataFrame(records)
    
    def get_last_trip(self, sheet_name: str = 'Main_Log') -> Optional[Dict[str, Any]]:
        """
        Get the last trip entry from the sheet.
        
        Args:
            sheet_name: Name of the worksheet
            
        Returns:
            Dictionary with last trip data or None
        """
        worksheet = self.get_or_create_worksheet(sheet_name)
        all_values = worksheet.get_all_values()
        
        if len(all_values) <= 1:  # Only headers or empty
            return None
        
        headers = all_values[0]
        last_row = all_values[-1]
        
        return dict(zip(headers, last_row))
    
    def update_cell(self, row: int, col: int, value: Any, 
                   sheet_name: str = 'Main_Log'):
        """
        Update a specific cell in the worksheet.
        
        Args:
            row: Row number (1-indexed)
            col: Column number (1-indexed)
            value: Value to set
            sheet_name: Name of the worksheet
        """
        worksheet = self.get_or_create_worksheet(sheet_name)
        worksheet.update_cell(row, col, value)
    
    def batch_update_cells(self, updates: List[Dict[str, Any]], 
                          sheet_name: str = 'Main_Log'):
        """
        Batch update multiple cells in the worksheet.
        
        Args:
            updates: List of dicts with 'row', 'col', 'value' keys
            sheet_name: Name of the worksheet
        """
        worksheet = self.get_or_create_worksheet(sheet_name)
        
        # Build cell list for batch update
        cell_list = []
        for update in updates:
            cell = worksheet.cell(update['row'], update['col'])
            cell.value = update['value']
            cell_list.append(cell)
        
        worksheet.update_cells(cell_list)
    
    def get_gas_stops(self, sheet_name: str = 'Main_Log') -> pd.DataFrame:
        """
        Get all gas stop entries from the sheet.
        
        Args:
            sheet_name: Name of the worksheet
            
        Returns:
            DataFrame containing only gas stop records
        """
        df = self.get_all_records(sheet_name)
        if df.empty:
            return df
        
        # Filter for gas stops
        gas_stops = df[df['Gas Stop?'] == True].copy()
        return gas_stops
