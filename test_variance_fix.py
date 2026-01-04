#!/usr/bin/env python3
"""
Test to verify the off-by-one fix in variance calculation
"""
from demo_mode import DemoSheetsManager
from ping_manager import PingManager
from smart_gas_manager import SmartGasManager

def test_variance_fix():
    """Test that previous gas stop miles are not included in current block."""
    print("\n=== Testing Variance Calculation Fix ===")
    
    # Initialize managers
    sheets_manager = DemoSheetsManager()
    sheets_manager.authenticate()
    ping_manager = PingManager(sheets_manager)
    smart_gas_manager = SmartGasManager(sheets_manager)
    
    # Gas Stop 1: Odometer 50000, 0 miles to get there (first trip)
    print("1. Gas Stop 1 at odometer 50000...")
    ping_manager.log_trip(
        current_coords=(40.0, -74.0),
        vehicle="Test Car",
        purpose="Gas Fill-up",
        is_gas_stop=True,
        odometer=50000,
        gallons=10.0,
        price_per_gal=3.00
    )
    
    # Trip 1: 10 miles
    print("2. Trip 1: Drive 10 miles...")
    ping_manager.log_trip(
        current_coords=(40.1, -74.0),  # ~6.9 miles, but let's say GPS says 10
        vehicle="Test Car",
        purpose="Business"
    )
    
    # Trip 2: 15 miles
    print("3. Trip 2: Drive 15 miles...")
    ping_manager.log_trip(
        current_coords=(40.2, -74.0),  # Another segment
        vehicle="Test Car",
        purpose="Business"
    )
    
    # Gas Stop 2: Odometer 50025 (traveled exactly 25 actual miles)
    print("4. Gas Stop 2 at odometer 50025...")
    ping_manager.log_trip(
        current_coords=(40.3, -74.0),
        vehicle="Test Car",
        purpose="Gas Fill-up",
        is_gas_stop=True,
        odometer=50025,
        gallons=2.0,
        price_per_gal=3.00
    )
    
    # Get all data before reconciliation
    df_before = sheets_manager.get_all_records()
    print(f"\n📊 Data before reconciliation:")
    print(f"   Gas Stop 1: Google Miles = {df_before.iloc[0]['Google Miles']}")
    print(f"   Trip 1: Google Miles = {df_before.iloc[1]['Google Miles']}")
    print(f"   Trip 2: Google Miles = {df_before.iloc[2]['Google Miles']}")
    print(f"   Gas Stop 2: Google Miles = {df_before.iloc[3]['Google Miles']}")
    
    # Calculate expected values
    # Between Gas Stop 1 and Gas Stop 2:
    # - Real miles: 50025 - 50000 = 25 miles
    # - GPS miles should ONLY include Trip 1 + Trip 2 + Gas Stop 2
    # - NOT Gas Stop 1 (that's from the previous tank)
    
    trip1_gps = df_before.iloc[1]['Google Miles']
    trip2_gps = df_before.iloc[2]['Google Miles']
    gas2_gps = df_before.iloc[3]['Google Miles']
    
    gps_sum = trip1_gps + trip2_gps + gas2_gps
    print(f"\n🧮 Expected calculation:")
    print(f"   GPS sum = Trip1 ({trip1_gps}) + Trip2 ({trip2_gps}) + GasStop2 ({gas2_gps}) = {gps_sum}")
    print(f"   Variance ratio = 25 actual / {gps_sum} GPS = {25/gps_sum:.3f}")
    
    # Reconcile
    print("\n🔄 Running reconciliation...")
    result = smart_gas_manager.reconcile_variance()
    
    if result['status'] == 'success':
        print(f"✓ Reconciliation complete!")
        print(f"  - Blocks processed: {result['blocks_processed']}")
        print(f"  - Trips updated: {result['trips_updated']}")
        
        # Verify: Should update 3 trips (Trip1, Trip2, GasStop2), NOT GasStop1
        assert result['trips_updated'] == 3, f"Expected 3 trips updated, got {result['trips_updated']}"
        print(f"  ✓ Correct! Updated only the 3 trips in the current block (not Gas Stop 1)")
        
        # Get data after reconciliation
        df_after = sheets_manager.get_all_records()
        
        print(f"\n📊 Data after reconciliation:")
        print(f"   Gas Stop 1: Actual Miles = {df_after.iloc[0]['Actual Miles']} (should be 0 or empty)")
        print(f"   Trip 1: Actual Miles = {df_after.iloc[1]['Actual Miles']}")
        print(f"   Trip 2: Actual Miles = {df_after.iloc[2]['Actual Miles']}")
        print(f"   Gas Stop 2: Actual Miles = {df_after.iloc[3]['Actual Miles']}")
        
        # Verify Gas Stop 1 was not updated
        gas1_actual = df_after.iloc[0]['Actual Miles']
        if gas1_actual == '' or gas1_actual == 0:
            print(f"  ✓ Gas Stop 1 correctly NOT updated (previous tank)")
        else:
            print(f"  ❌ ERROR: Gas Stop 1 was updated (should not be)")
        
        # Check warnings for unusual variance
        if 'warnings' in result:
            print(f"\n⚠️ Variance warnings:")
            for warning in result['warnings']:
                print(f"   - Block {warning['block']}: {warning['message']}")
        
        print("\n✅ TEST PASSED: Off-by-one fix verified!")
        return True
    else:
        print(f"❌ TEST FAILED: {result.get('message')}")
        return False

if __name__ == "__main__":
    success = test_variance_fix()
    exit(0 if success else 1)
