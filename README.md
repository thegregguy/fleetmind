# FleetMind 🚗

The Mileage & Expense Tracker for gig-economy drivers.

FleetMind is a Streamlit-based application that helps gig-economy drivers track mileage, reconcile GPS estimates with actual odometer readings, and calculate fuel costs per trip.

## Features

### 📍 Ping Workflow
- Log driving trips by capturing GPS coordinates
- Automatic distance calculation between trips
- Trip categorization (Business, Personal, Commute)
- Trip history and visualization

### ⛽ Smart Gas Workflow
- Log gas fill-ups with odometer readings
- Automatic variance reconciliation between GPS and actual miles
- Retroactive trip distance correction
- Per-trip fuel cost calculation
- Comprehensive fuel statistics and MPG tracking

## How It Works

### Variance Reconciliation Logic

1. **Real Miles Calculation**: `Real Miles = Current Odometer - Previous Odometer`
2. **Variance Ratio**: `Variance = Real Miles / Sum of Google Estimated Miles`
3. **Actual Miles per Trip**: `Actual Miles = Google Estimated Miles × Variance`
4. **Fuel Cost per Trip**: `Fuel Cost = (Trip Distance / Block MPG) × Price Per Gallon`

All trips between two gas stops are updated retroactively with accurate distances and fuel costs.

## Installation

### Prerequisites
- Python 3.8 or higher
- Google Cloud Service Account with Sheets API access
- Google Spreadsheet for data storage

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thegregguy/fleetmind.git
   cd fleetmind
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets API**
   
   a. Create a Google Cloud Project and enable the Google Sheets API
   
   b. Create a Service Account and download the JSON key file
   
   c. Save the JSON file as `service_account.json` in the project root
   
   d. Create a Google Spreadsheet and share it with the service account email

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```
   SPREADSHEET_ID=your_spreadsheet_id_here
   SHEET_NAME=Main_Log
   SERVICE_ACCOUNT_FILE=service_account.json
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Google Sheets Schema

The application uses a `Main_Log` sheet with the following columns:

| Column | Description |
|--------|-------------|
| Timestamp | ISO format timestamp of the trip |
| Vehicle | Vehicle identifier |
| Purpose | Trip purpose (Business, Personal, etc.) |
| Start GPS | Starting GPS coordinates (lat,lon) |
| End GPS | Ending GPS coordinates (lat,lon) |
| Start Addr | Human-readable start address |
| End Addr | Human-readable end address |
| Google Miles | GPS-calculated distance |
| Actual Miles | Variance-corrected distance |
| Gas Stop? | Boolean flag for gas fill-ups |
| Odometer | Odometer reading (gas stops only) |
| Gallons | Gallons purchased (gas stops only) |
| Price/Gal | Price per gallon (gas stops only) |
| Trip Fuel Cost ($) | Calculated fuel cost for trip |

## Usage

### Logging a Trip (Ping)

1. Navigate to the "Ping" tab
2. Enter your vehicle name
3. Select the trip purpose
4. Enter GPS coordinates (in production, these would be automatically captured)
5. Click "Log Ping"

### Logging a Gas Fill-up (Smart Gas)

1. Navigate to the "Smart Gas" tab
2. Fill in the gas fill-up form:
   - Vehicle name
   - Current odometer reading
   - Gallons purchased
   - Price per gallon
   - GPS coordinates
3. Click "Log Gas Fill-up & Reconcile"
4. The system will automatically:
   - Log the gas stop
   - Calculate variance between GPS and actual miles
   - Update all trips retroactively with corrected distances and fuel costs

### Viewing Statistics

In the "Smart Gas" tab, click "Calculate Statistics" to see:
- Total actual miles driven
- Total fuel cost
- Total gallons purchased
- Average MPG
- GPS variance percentage

## Future Enhancements

### Hardware Integration
- **Bluetooth Key Event Listener**: Add support for hands-free "Ping" using volume key presses
- **Automatic GPS Capture**: Integration with device GPS hardware
- **Mobile App**: Native mobile application for easier on-the-go logging

### Additional Features
- Export reports to PDF/Excel
- Multiple vehicle support with separate tracking
- Tax deduction calculations
- Integration with accounting software

## Development

### Project Structure
```
fleetmind/
├── app.py                  # Main Streamlit application
├── gps_utils.py           # GPS utilities and distance calculation
├── sheets_manager.py      # Google Sheets API integration
├── ping_manager.py        # Trip logging logic
├── smart_gas_manager.py   # Variance reconciliation logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
└── README.md             # This file
```

### Running Tests
```bash
# Tests can be added in the future
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.
