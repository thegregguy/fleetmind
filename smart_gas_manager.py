"""
Smart Gas Workflow Module
Handles mileage and gas expense reconciliation with variance calculations.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from sheets_manager import GoogleSheetsManager


class SmartGasManager:
    """Manager class for Smart Gas (variance reconciliation) operations."""
    
    def __init__(self, sheets_manager: GoogleSheetsManager):
        """
        Initialize Smart Gas Manager.
        
        Args:
            sheets_manager: GoogleSheetsManager instance
        """
        self.sheets_manager = sheets_manager
    
    def log_gas_fillup(self,
                       current_coords: tuple,
                       vehicle: str,
                       odometer: float,
                       gallons: float,
                       price_per_gal: float,
                       purpose: str = "Gas Fill-up") -> Dict[str, Any]:
        """
        Log a gas fill-up and trigger variance reconciliation.
        
        Args:
            current_coords: Current GPS coordinates (lat, lon)
            vehicle: Vehicle identifier
            odometer: Current odometer reading
            gallons: Gallons purchased
            price_per_gal: Price per gallon
            purpose: Trip purpose (default: "Gas Fill-up")
            
        Returns:
            Dictionary with reconciliation results
        """
        from ping_manager import PingManager
        
        # First, log this as a ping with gas stop flag
        ping_manager = PingManager(self.sheets_manager)
        trip_data = ping_manager.log_trip(
            current_coords=current_coords,
            vehicle=vehicle,
            purpose=purpose,
            is_gas_stop=True,
            odometer=odometer,
            gallons=gallons,
            price_per_gal=price_per_gal
        )
        
        # Now perform variance reconciliation
        reconciliation_result = self.reconcile_variance()
        
        return {
            'trip_data': trip_data,
            'reconciliation': reconciliation_result
        }
    
    def reconcile_variance(self) -> Dict[str, Any]:
        """
        Perform retroactive variance calculation and update trips.
        
        Returns:
            Dictionary containing reconciliation results and statistics
        """
        # Get all records
        df = self.sheets_manager.get_all_records()
        
        if df.empty:
            return {'status': 'no_data', 'message': 'No trip data available'}
        
        # Find gas stops
        gas_stops = df[df['Gas Stop?'] == True].copy()
        
        if len(gas_stops) < 2:
            return {
                'status': 'insufficient_gas_stops',
                'message': 'Need at least 2 gas stops for variance calculation'
            }
        
        updates = []
        blocks_processed = 0
        
        # Process each pair of consecutive gas stops
        for i in range(len(gas_stops) - 1):
            prev_gas_idx = gas_stops.index[i]
            curr_gas_idx = gas_stops.index[i + 1]
            
            # Get odometer readings
            prev_odometer = float(gas_stops.iloc[i]['Odometer']) if gas_stops.iloc[i]['Odometer'] else None
            curr_odometer = float(gas_stops.iloc[i + 1]['Odometer']) if gas_stops.iloc[i + 1]['Odometer'] else None
            
            if prev_odometer is None or curr_odometer is None:
                continue
            
            # Calculate real miles from odometer
            real_miles = curr_odometer - prev_odometer
            
            # Get trips between these gas stops (inclusive of endpoints)
            trips_in_block = df.iloc[prev_gas_idx:curr_gas_idx + 1].copy()
            
            # Sum Google estimated miles
            google_miles_sum = trips_in_block['Google Miles'].apply(
                lambda x: float(x) if x and x != '' else 0
            ).sum()
            
            if google_miles_sum == 0:
                continue
            
            # Calculate variance ratio
            variance_ratio = real_miles / google_miles_sum
            
            # Calculate MPG for this block
            total_gallons = trips_in_block['Gallons'].apply(
                lambda x: float(x) if x and x != '' else 0
            ).sum()
            
            block_mpg = real_miles / total_gallons if total_gallons > 0 else 0
            
            # Get price per gallon (use the current gas stop's price)
            price_per_gal = float(gas_stops.iloc[i + 1]['Price/Gal']) if gas_stops.iloc[i + 1]['Price/Gal'] else 0
            
            # Update each trip in the block
            for idx in trips_in_block.index:
                google_miles = float(df.loc[idx, 'Google Miles']) if df.loc[idx, 'Google Miles'] else 0
                
                # Calculate actual miles
                actual_miles = google_miles * variance_ratio
                
                # Calculate fuel cost for this trip
                if block_mpg > 0 and price_per_gal > 0:
                    trip_fuel_cost = (actual_miles / block_mpg) * price_per_gal
                else:
                    trip_fuel_cost = 0
                
                # Prepare updates (row is 1-indexed, +2 for header and 0-indexing)
                row_num = idx + 2
                
                # Column indices (1-indexed)
                actual_miles_col = 9  # Column I
                trip_fuel_cost_col = 14  # Column N
                
                updates.append({
                    'row': row_num,
                    'col': actual_miles_col,
                    'value': round(actual_miles, 2)
                })
                
                updates.append({
                    'row': row_num,
                    'col': trip_fuel_cost_col,
                    'value': round(trip_fuel_cost, 2)
                })
            
            blocks_processed += 1
        
        # Perform batch update
        if updates:
            self.sheets_manager.batch_update_cells(updates)
        
        return {
            'status': 'success',
            'blocks_processed': blocks_processed,
            'trips_updated': len(updates) // 2,  # Each trip has 2 updates
            'message': f'Successfully reconciled {blocks_processed} block(s) and updated {len(updates) // 2} trip(s)'
        }
    
    def get_fuel_statistics(self) -> Dict[str, Any]:
        """
        Calculate fuel and mileage statistics.
        
        Returns:
            Dictionary with statistics
        """
        df = self.sheets_manager.get_all_records()
        
        if df.empty:
            return {'status': 'no_data'}
        
        # Calculate statistics
        total_google_miles = df['Google Miles'].apply(
            lambda x: float(x) if x and x != '' else 0
        ).sum()
        
        total_actual_miles = df['Actual Miles'].apply(
            lambda x: float(x) if x and x != '' else 0
        ).sum()
        
        total_fuel_cost = df['Trip Fuel Cost ($)'].apply(
            lambda x: float(x) if x and x != '' else 0
        ).sum()
        
        gas_stops = df[df['Gas Stop?'] == True]
        total_gallons = gas_stops['Gallons'].apply(
            lambda x: float(x) if x and x != '' else 0
        ).sum()
        
        return {
            'status': 'success',
            'total_google_miles': round(total_google_miles, 2),
            'total_actual_miles': round(total_actual_miles, 2),
            'total_fuel_cost': round(total_fuel_cost, 2),
            'total_gallons': round(total_gallons, 2),
            'average_mpg': round(total_actual_miles / total_gallons, 2) if total_gallons > 0 else 0,
            'gas_stops_count': len(gas_stops)
        }
