# Google Sheets API Setup Guide

This guide will walk you through setting up Google Sheets API access for FleetMind.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a Project" at the top, then "New Project"
3. Name your project (e.g., "FleetMind")
4. Click "Create"

## Step 2: Enable Google Sheets API

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and click "Enable"
4. Also enable "Google Drive API" (required for full access)

## Step 3: Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the details:
   - Service account name: `fleetmind-service`
   - Service account ID: (auto-generated)
   - Description: "Service account for FleetMind app"
4. Click "Create and Continue"
5. For roles, select "Editor" (or you can skip this step)
6. Click "Done"

## Step 4: Create and Download Service Account Key

1. In the Credentials page, find your newly created service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Select "JSON" format
6. Click "Create"
7. The JSON key file will download automatically
8. **Important**: Keep this file secure - it provides access to your Google Sheets

## Step 5: Setup Service Account File

1. Rename the downloaded JSON file to `service_account.json`
2. Move it to your FleetMind project root directory
3. Make sure `service_account.json` is in your `.gitignore` (it already is)

## Step 6: Create Google Spreadsheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new blank spreadsheet
3. Name it "FleetMind Data" (or any name you prefer)
4. Copy the spreadsheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - The SPREADSHEET_ID is the long string between `/d/` and `/edit`

## Step 7: Share Spreadsheet with Service Account

1. In your Google Spreadsheet, click "Share" button
2. Paste the service account email address (found in your `service_account.json` as `client_email`)
   - Format: `fleetmind-service@your-project-id.iam.gserviceaccount.com`
3. Select "Editor" access
4. Uncheck "Notify people" (service accounts don't receive emails)
5. Click "Share"

## Step 8: Configure FleetMind

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file:
   ```
   SPREADSHEET_ID=your_spreadsheet_id_from_step_6
   SHEET_NAME=Main_Log
   SERVICE_ACCOUNT_FILE=service_account.json
   ```

## Step 9: Verify Setup

Run the FleetMind app:
```bash
streamlit run app.py
```

If everything is configured correctly:
- The app should start without errors
- You should be able to access the Ping and Smart Gas tabs
- When you log a trip, a new "Main_Log" sheet should be created automatically in your spreadsheet

## Troubleshooting

### Error: "Service account file not found"
- Verify `service_account.json` is in the project root
- Check the path in your `.env` file

### Error: "Spreadsheet not found" or "Permission denied"
- Verify you copied the correct SPREADSHEET_ID
- Make sure you shared the spreadsheet with your service account email
- Check that the service account has "Editor" permissions

### Error: "API not enabled"
- Make sure both Google Sheets API and Google Drive API are enabled in your Google Cloud Console

### Error: "Quota exceeded"
- Google Sheets API has usage limits
- For personal use, the free tier should be sufficient
- Check your API usage in Google Cloud Console

## Security Best Practices

1. **Never commit `service_account.json` to git**
   - It's already in `.gitignore`
   - This file provides full access to your sheets

2. **Limit service account permissions**
   - Only share the specific spreadsheet(s) you need
   - Don't give the service account access to your entire Google Drive

3. **Rotate keys periodically**
   - Delete old keys and create new ones every few months
   - Update your `service_account.json` file accordingly

4. **Use environment variables**
   - Never hardcode credentials in your code
   - Use `.env` file for configuration (already set up)

## Additional Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [gspread Library Documentation](https://docs.gspread.org/)
- [Google Cloud Service Accounts](https://cloud.google.com/iam/docs/service-accounts)
