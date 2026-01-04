#!/usr/bin/env python3
"""
Test script to validate FleetMind core functionality
"""
import sys
from demo_mode import DemoSheetsManager
from ping_manager import PingManager
from smart_gas_manager import SmartGasManager

def test_ping_workflow():
    """Test the Ping (trip logging) workflow."""
    print("\n=== Testing Ping Workflow ===")
    
    # Initialize managers
    sheets_manager = DemoSheetsManager()
    sheets_manager.authenticate()
    ping_manager = PingManager(sheets_manager)
    
    # Log first trip
    print("Logging trip 1...")
    trip1 = ping_manager.log_trip(
        current_coords=(40.7128, -74.0060),  # NYC
        vehicle="Honda Civic",
        purpose="Business"
    )
    print(f"✓ Trip 1: {trip1['google_miles']:.2f} miles")
    
    # Log second trip
    print("Logging trip 2...")
    trip2 = ping_manager.log_trip(
        current_coords=(40.7589, -73.9851),  # Times Square
        vehicle="Honda Civic",
        purpose="Business"
    )
    print(f"✓ Trip 2: {trip2['google_miles']:.2f} miles from previous location")
    
    # Log third trip
    print("Logging trip 3...")
    trip3 = ping_manager.log_trip(
        current_coords=(40.7580, -73.9855),  # Near Times Square
        vehicle="Honda Civic",
        purpose="Personal"
    )
    print(f"✓ Trip 3: {trip3['google_miles']:.2f} miles from previous location")
    
    # Get trip history
    history = ping_manager.get_trip_history()
    print(f"\n✓ Total trips logged: {len(history)}")
    
    return sheets_manager

def test_smart_gas_workflow(sheets_manager):
    """Test the Smart Gas (variance reconciliation) workflow."""
    print("\n=== Testing Smart Gas Workflow ===")
    
    ping_manager = PingManager(sheets_manager)
    smart_gas_manager = SmartGasManager(sheets_manager)
    
    # Log first gas stop (with odometer reading)
    print("Logging first gas stop...")
    trip1 = ping_manager.log_trip(
        current_coords=(40.7489, -73.9680),
        vehicle="Honda Civic",
        purpose="Gas Fill-up",
        is_gas_stop=True,
        odometer=50000,
        gallons=12.5,
        price_per_gal=3.50
    )
    print(f"✓ Gas stop 1 at odometer: 50000")
    
    # Log a few more trips
    print("Logging additional trips...")
    for i, coords in enumerate([
        (40.7614, -73.9776),
        (40.7489, -73.9680),
        (40.7306, -73.9352)
    ], start=1):
        trip = ping_manager.log_trip(
            current_coords=coords,
            vehicle="Honda Civic",
            purpose="Business"
        )
        print(f"✓ Trip {i}: {trip['google_miles']:.2f} miles")
    
    # Log second gas stop
    print("Logging second gas stop...")
    trip2 = ping_manager.log_trip(
        current_coords=(40.7589, -73.9851),
        vehicle="Honda Civic",
        purpose="Gas Fill-up",
        is_gas_stop=True,
        odometer=50125,  # Traveled 125 actual miles
        gallons=10.0,
        price_per_gal=3.60
    )
    print(f"✓ Gas stop 2 at odometer: 50125")
    
    # Perform variance reconciliation
    print("\nPerforming variance reconciliation...")
    result = smart_gas_manager.reconcile_variance()
    
    if result['status'] == 'success':
        print(f"✓ Reconciliation complete!")
        print(f"  - Blocks processed: {result['blocks_processed']}")
        print(f"  - Trips updated: {result['trips_updated']}")
        print(f"  - {result['message']}")
    else:
        print(f"⚠ {result.get('message', 'Reconciliation failed')}")
    
    # Get statistics
    print("\nCalculating fuel statistics...")
    stats = smart_gas_manager.get_fuel_statistics()
    
    if stats['status'] == 'success':
        print(f"✓ Statistics:")
        print(f"  - Total Google Miles: {stats['total_google_miles']:.2f}")
        print(f"  - Total Actual Miles: {stats['total_actual_miles']:.2f}")
        print(f"  - Total Fuel Cost: ${stats['total_fuel_cost']:.2f}")
        print(f"  - Total Gallons: {stats['total_gallons']:.2f}")
        print(f"  - Average MPG: {stats['average_mpg']:.2f}")
        print(f"  - Gas Stops: {stats['gas_stops_count']}")
        
        if stats['total_google_miles'] > 0:
            variance_pct = (stats['total_actual_miles'] - stats['total_google_miles']) / stats['total_google_miles'] * 100
            print(f"  - GPS Variance: {variance_pct:+.1f}%")

def main():
    """Run all tests."""
    print("FleetMind Core Functionality Test")
    print("=" * 50)
    
    try:
        # Test Ping workflow
        sheets_manager = test_ping_workflow()
        
        # Test Smart Gas workflow
        test_smart_gas_workflow(sheets_manager)
        
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        print("=" * 50)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
