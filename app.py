"""
FleetMind - Mileage & Expense Tracker
Main Streamlit Application
"""
import streamlit as st
import os
from dotenv import load_dotenv
from typing import Tuple
from sheets_manager import GoogleSheetsManager
from demo_mode import DemoSheetsManager
from ping_manager import PingManager
from smart_gas_manager import SmartGasManager

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FleetMind - Mileage & Expense Tracker",
    page_icon="🚗",
    layout="wide"
)

# Initialize session state
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = None
if 'ping_manager' not in st.session_state:
    st.session_state.ping_manager = None
if 'smart_gas_manager' not in st.session_state:
    st.session_state.smart_gas_manager = None
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False


def initialize_managers():
    """Initialize manager instances with Google Sheets connection."""
    service_account_file = os.getenv('SERVICE_ACCOUNT_FILE', 'service_account.json')
    spreadsheet_id = os.getenv('SPREADSHEET_ID', '')
    
    # Check if demo mode should be used
    use_demo = os.getenv('DEMO_MODE', 'false').lower() == 'true'
    
    if use_demo or not spreadsheet_id or not os.path.exists(service_account_file):
        # Use demo mode
        st.info("ℹ️ Running in DEMO MODE (in-memory storage)")
        st.caption("To use Google Sheets, configure .env file and add service_account.json")
        
        sheets_manager = DemoSheetsManager()
        sheets_manager.authenticate()
        
        st.session_state.sheets_manager = sheets_manager
        st.session_state.ping_manager = PingManager(sheets_manager)
        st.session_state.smart_gas_manager = SmartGasManager(sheets_manager)
        st.session_state.demo_mode = True
        
        return True
    
    try:
        sheets_manager = GoogleSheetsManager(service_account_file, spreadsheet_id)
        sheets_manager.authenticate()
        
        st.session_state.sheets_manager = sheets_manager
        st.session_state.ping_manager = PingManager(sheets_manager)
        st.session_state.smart_gas_manager = SmartGasManager(sheets_manager)
        st.session_state.demo_mode = False
        
        st.success("✅ Connected to Google Sheets")
        
        return True
    except Exception as e:
        st.error(f"❌ Failed to initialize: {str(e)}")
        st.info("Tip: Try demo mode by setting DEMO_MODE=true in .env")
        return False


def get_current_location() -> Tuple[float, float]:
    """
    Get current GPS coordinates.
    In a production app, this would use actual GPS hardware.
    For demo purposes, using manual input.
    """
    # Note: In production, this could integrate with:
    # - Browser geolocation API via streamlit-javascript
    # - Mobile GPS via Streamlit mobile
    # - Hardware GPS device
    
    return None  # Placeholder for manual input


def ping_tab():
    """Render the Ping (Trip Logging) tab."""
    st.header("🚗 Ping - Log a Trip")
    
    st.write("Record your current location and log a trip.")
    
    with st.form("ping_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            vehicle = st.text_input("Vehicle", placeholder="e.g., Honda Civic")
            purpose = st.selectbox(
                "Purpose/Status",
                ["Business", "Personal", "Commute", "Other"]
            )
            
        with col2:
            # GPS coordinates input (in production, this would be automatic)
            latitude = st.number_input(
                "Latitude",
                format="%.6f",
                value=40.7128,
                help="In production, this would be automatically captured"
            )
            longitude = st.number_input(
                "Longitude",
                format="%.6f",
                value=-74.0060,
                help="In production, this would be automatically captured"
            )
        
        submitted = st.form_submit_button("📍 Log Ping", use_container_width=True)
        
        if submitted:
            if not vehicle:
                st.error("Please enter a vehicle name")
            else:
                try:
                    coords = (latitude, longitude)
                    trip_data = st.session_state.ping_manager.log_trip(
                        current_coords=coords,
                        vehicle=vehicle,
                        purpose=purpose
                    )
                    
                    st.success("✅ Trip logged successfully!")
                    
                    # Display trip details
                    st.subheader("Trip Details")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Distance", f"{trip_data['google_miles']:.2f} mi")
                    with col2:
                        st.metric("Vehicle", trip_data['vehicle'])
                    with col3:
                        st.metric("Purpose", trip_data['purpose'])
                    
                    with st.expander("View Full Details"):
                        st.json(trip_data)
                        
                except Exception as e:
                    st.error(f"❌ Error logging trip: {str(e)}")
    
    # Recent trips
    st.divider()
    st.subheader("Recent Trips")
    
    try:
        trips = st.session_state.ping_manager.get_trip_history(limit=10)
        if trips:
            import pandas as pd
            df = pd.DataFrame(trips)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No trips logged yet. Log your first trip above!")
    except Exception as e:
        st.error(f"Error loading trips: {str(e)}")


def smart_gas_tab():
    """Render the Smart Gas (Reconciliation) tab."""
    st.header("⛽ Smart Gas - Fuel & Mileage Reconciliation")
    
    st.write("Log gas fill-ups and automatically reconcile actual mileage vs GPS estimates.")
    
    # Gas Fill-up Form
    st.subheader("Log Gas Fill-up")
    
    with st.form("gas_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            vehicle = st.text_input("Vehicle", placeholder="e.g., Honda Civic")
            odometer = st.number_input(
                "Odometer Reading",
                min_value=0.0,
                format="%.1f",
                help="Current odometer reading in miles"
            )
            # GPS coordinates
            latitude = st.number_input(
                "Latitude",
                format="%.6f",
                value=40.7128,
                help="In production, this would be automatically captured"
            )
            
        with col2:
            gallons = st.number_input(
                "Gallons Purchased",
                min_value=0.0,
                format="%.3f"
            )
            price_per_gal = st.number_input(
                "Price per Gallon ($)",
                min_value=0.0,
                format="%.3f"
            )
            longitude = st.number_input(
                "Longitude",
                format="%.6f",
                value=-74.0060,
                help="In production, this would be automatically captured"
            )
        
        submitted = st.form_submit_button("⛽ Log Gas Fill-up & Reconcile", use_container_width=True)
        
        if submitted:
            if not vehicle or odometer <= 0 or gallons <= 0 or price_per_gal <= 0:
                st.error("Please fill in all required fields with valid values")
            else:
                try:
                    coords = (latitude, longitude)
                    result = st.session_state.smart_gas_manager.log_gas_fillup(
                        current_coords=coords,
                        vehicle=vehicle,
                        odometer=odometer,
                        gallons=gallons,
                        price_per_gal=price_per_gal
                    )
                    
                    st.success("✅ Gas fill-up logged and variance reconciled!")
                    
                    # Display reconciliation results
                    recon = result['reconciliation']
                    if recon['status'] == 'success':
                        st.subheader("Reconciliation Results")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Blocks Processed", recon['blocks_processed'])
                        with col2:
                            st.metric("Trips Updated", recon['trips_updated'])
                        
                        st.info(recon['message'])
                        
                        # Display variance warnings if any
                        if 'warnings' in recon and recon['warnings']:
                            st.warning("⚠️ Variance Warnings Detected")
                            for warning in recon['warnings']:
                                st.warning(
                                    f"**Block {warning['block']}**: Variance ratio {warning['variance_ratio']:.2f}x "
                                    f"({warning['real_miles']:.0f} actual miles vs {warning['gps_miles']:.0f} GPS miles). "
                                    f"{warning['message']}"
                                )
                    else:
                        st.warning(recon.get('message', 'Reconciliation pending'))
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Manual Reconciliation Button
    st.divider()
    st.subheader("Manual Reconciliation")
    st.write("Recalculate variance and update all trips based on existing gas stops.")
    
    if st.button("🔄 Run Variance Reconciliation", use_container_width=True):
        try:
            with st.spinner("Reconciling..."):
                result = st.session_state.smart_gas_manager.reconcile_variance()
                
            if result['status'] == 'success':
                st.success("✅ Reconciliation complete!")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Blocks Processed", result['blocks_processed'])
                with col2:
                    st.metric("Trips Updated", result['trips_updated'])
                
                # Display variance warnings if any
                if 'warnings' in result and result['warnings']:
                    st.warning("⚠️ Variance Warnings Detected")
                    for warning in result['warnings']:
                        st.warning(
                            f"**Block {warning['block']}**: Variance ratio {warning['variance_ratio']:.2f}x "
                            f"({warning['real_miles']:.0f} actual miles vs {warning['gps_miles']:.0f} GPS miles). "
                            f"{warning['message']}"
                        )
            else:
                st.warning(result.get('message', 'No data to reconcile'))
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    # Fuel Statistics
    st.divider()
    st.subheader("📊 Fuel Statistics")
    
    if st.button("📈 Calculate Statistics", use_container_width=True):
        try:
            stats = st.session_state.smart_gas_manager.get_fuel_statistics()
            
            if stats['status'] == 'success':
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Actual Miles", f"{stats['total_actual_miles']:.2f}")
                    st.metric("Total Fuel Cost", f"${stats['total_fuel_cost']:.2f}")
                with col2:
                    st.metric("Total Gallons", f"{stats['total_gallons']:.2f}")
                    st.metric("Gas Stops", stats['gas_stops_count'])
                with col3:
                    st.metric("Average MPG", f"{stats['average_mpg']:.2f}")
                    variance = (stats['total_actual_miles'] - stats['total_google_miles']) / stats['total_google_miles'] * 100 if stats['total_google_miles'] > 0 else 0
                    st.metric("GPS Variance", f"{variance:+.1f}%")
            else:
                st.info("No data available for statistics")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def main():
    """Main application entry point."""
    st.title("🚗 FleetMind")
    st.subheader("Mileage & Expense Tracker for Gig-Economy Drivers")
    
    # Initialize managers
    if st.session_state.sheets_manager is None:
        if not initialize_managers():
            st.stop()
    
    # Show demo mode warning
    if st.session_state.demo_mode:
        st.warning("⚠️ Demo Mode Active - Data is stored in memory only and will be lost when you close the app")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📍 Ping", "⛽ Smart Gas", "ℹ️ About"])
    
    with tab1:
        ping_tab()
    
    with tab2:
        smart_gas_tab()
    
    with tab3:
        st.header("About FleetMind")
        st.write("""
        FleetMind is a mileage and expense tracker designed for gig-economy drivers.
        
        **Features:**
        - **Ping**: Log trips with GPS coordinates and automatic distance calculation
        - **Smart Gas**: Reconcile actual mileage with GPS estimates using odometer readings
        - Automatic variance correction for improved accuracy
        - Fuel cost tracking per trip
        
        **How it Works:**
        1. **Log Trips**: Use the Ping feature to record each trip segment
        2. **Fill Up**: When you get gas, use Smart Gas to log odometer, gallons, and price
        3. **Automatic Reconciliation**: The system calculates variance between GPS and actual miles
        4. **Retroactive Updates**: All trips between gas stops are updated with accurate distances and fuel costs
        
        **Technical Details:**
        - Data stored in Google Sheets
        - GPS-based distance calculation using geopy
        - Variance ratio applied retroactively to trip blocks
        - Fuel cost calculated using: (Actual Miles / Block MPG) × Price per Gallon
        """)
        
        st.divider()
        st.caption("FleetMind - The Mileage & Expense Tracker for gig-economy drivers")


if __name__ == "__main__":
    main()
