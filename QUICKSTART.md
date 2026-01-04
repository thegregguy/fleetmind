# FleetMind Quick Start Guide

This guide will get you up and running with FleetMind in under 5 minutes using demo mode.

## Option 1: Quick Start with Demo Mode (No Google Sheets Required)

Perfect for testing and evaluating FleetMind without any setup!

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Demo Mode
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set DEMO_MODE=true
echo "DEMO_MODE=true" > .env
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**Note**: In demo mode, all data is stored in memory and will be lost when you close the app.

## Option 2: Full Setup with Google Sheets

For production use with persistent data storage.

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Google Sheets API
Follow the detailed instructions in [SETUP_GUIDE.md](SETUP_GUIDE.md) to:
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a Service Account
4. Download credentials
5. Create and share a spreadsheet

### Step 3: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values:
# DEMO_MODE=false
# SPREADSHEET_ID=your_spreadsheet_id_here
# SHEET_NAME=Main_Log
# SERVICE_ACCOUNT_FILE=service_account.json
```

### Step 4: Add Service Account Credentials
Place your `service_account.json` file in the project root directory.

### Step 5: Run the Application
```bash
streamlit run app.py
```

## Using FleetMind

### Logging a Trip (Ping)

1. Open the **"Ping"** tab
2. Enter your vehicle name (e.g., "Honda Civic")
3. Select trip purpose (Business, Personal, Commute, Other)
4. Enter GPS coordinates (in production, these would be auto-captured)
5. Click **"Log Ping"**

The app will:
- Calculate distance from your last location
- Store the trip in your Google Sheet
- Display trip details

### Logging Gas Fill-ups (Smart Gas)

1. Open the **"Smart Gas"** tab
2. Fill in the gas fill-up form:
   - Vehicle name
   - Current odometer reading
   - Gallons purchased
   - Price per gallon
   - GPS coordinates
3. Click **"Log Gas Fill-up & Reconcile"**

The app will:
- Log the gas stop
- Calculate variance between GPS and actual miles
- Update ALL trips between gas stops retroactively
- Recalculate fuel costs per trip

### Viewing Statistics

In the **"Smart Gas"** tab:
- Click **"Calculate Statistics"** to see:
  - Total actual miles
  - Total fuel cost
  - Average MPG
  - GPS variance percentage
  - Number of gas stops

## Example Workflow

### Day 1: Start Tracking
1. Start your shift - **Ping** your location
2. Complete Trip 1 - **Ping** at destination
3. Complete Trip 2 - **Ping** at destination
4. Fill up gas (let's say odometer is at 50,000 miles) - Use **Smart Gas**
   - Odometer: 50000
   - Gallons: 12.5
   - Price: $3.50/gal

### Day 2: Continue Tracking
5. Complete Trip 3 - **Ping**
6. Complete Trip 4 - **Ping**
7. Complete Trip 5 - **Ping**
8. Fill up gas again (odometer now at 50,125 miles) - Use **Smart Gas**
   - Odometer: 50125
   - Gallons: 10.0
   - Price: $3.60/gal

**Magic Happens**: FleetMind automatically:
- Calculates actual miles: 50,125 - 50,000 = 125 miles
- Compares to GPS estimates (might be ~120 miles)
- Calculates variance ratio: 125 / 120 = 1.042
- Updates Trips 3-8 with corrected distances (multiply by 1.042)
- Calculates MPG: 125 miles / 22.5 gallons = 5.56 MPG
- Updates fuel cost for each trip based on actual miles

### Result
You now have accurate:
- ✅ Actual miles driven (not just GPS estimates)
- ✅ Fuel cost per trip
- ✅ Real MPG
- ✅ Variance tracking for tax purposes

## Troubleshooting

### "Demo mode active" message
- This is normal if you set `DEMO_MODE=true` in your .env file
- Your data will be stored in memory only
- To use Google Sheets, set `DEMO_MODE=false` and configure credentials

### "Service account file not found"
- Make sure `service_account.json` is in the project root
- Check the filename matches what's in your .env file

### "Spreadsheet not found"
- Verify you shared the spreadsheet with your service account email
- Check the SPREADSHEET_ID in your .env file

### Geocoding errors (in logs)
- These are normal if you don't have internet access
- The app will still work, just without reverse geocoded addresses
- Distance calculations use GPS coordinates directly

## Next Steps

- Read the full [README.md](README.md) for feature details
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for Google Sheets setup
- Run the test suite: `python test_fleetmind.py`
- Customize the vehicle types and trip purposes in `app.py`

## Tips

1. **Always log gas fill-ups**: This is when the magic happens! The variance calculation needs odometer readings.

2. **Be consistent**: Log every trip segment to get accurate data.

3. **Check statistics regularly**: Use the statistics feature to monitor your MPG and costs.

4. **Backup your data**: If using Google Sheets, your data is automatically backed up. In demo mode, remember to export before closing!

5. **Mobile usage**: For hands-free logging, consider:
   - Streamlit mobile app (when available)
   - Voice commands integration (future enhancement)
   - Bluetooth button integration (future enhancement)

## Support

Having issues? Check:
- [README.md](README.md) - Full documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- GitHub Issues - Report bugs or request features
