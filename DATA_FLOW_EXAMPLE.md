# FleetMind Data Flow Example

This document illustrates how FleetMind tracks and reconciles trip data.

## Scenario: A Day of Gig Work

### Morning Shift (Gas Stop #1)
**Time**: 8:00 AM  
**Action**: Fill up gas  
**Odometer**: 50,000 miles  
**Gallons**: 12.5 gal  
**Price**: $3.50/gal  
**Location**: Home (40.7128, -74.0060)

---

### Trip 1: Home to Pickup
**Time**: 8:15 AM  
**GPS Distance**: 3.2 miles  
**Start**: Home (40.7128, -74.0060)  
**End**: Restaurant (40.7589, -73.9851)  
**Purpose**: Business  
**Actual Miles**: *Will be calculated after next gas stop*

---

### Trip 2: Pickup to Delivery
**Time**: 8:30 AM  
**GPS Distance**: 2.8 miles  
**Start**: Restaurant (40.7589, -73.9851)  
**End**: Customer (40.7489, -73.9680)  
**Purpose**: Business  
**Actual Miles**: *Will be calculated after next gas stop*

---

### Trip 3: Delivery to Next Pickup
**Time**: 9:00 AM  
**GPS Distance**: 1.5 miles  
**Start**: Customer (40.7489, -73.9680)  
**End**: Store (40.7614, -73.9776)  
**Purpose**: Business  
**Actual Miles**: *Will be calculated after next gas stop*

---

### Trip 4: Store to Customer
**Time**: 9:30 AM  
**GPS Distance**: 4.1 miles  
**Start**: Store (40.7614, -73.9776)  
**End**: Customer (40.7306, -73.9352)  
**Purpose**: Business  
**Actual Miles**: *Will be calculated after next gas stop*

---

### Evening (Gas Stop #2)
**Time**: 5:00 PM  
**Action**: Fill up gas  
**Odometer**: 50,125 miles  
**Gallons**: 10.0 gal  
**Price**: $3.60/gal  
**Location**: Gas Station (40.7589, -73.9851)

---

## Variance Calculation

### Step 1: Calculate Actual Miles
```
Actual Miles = Current Odometer - Previous Odometer
Actual Miles = 50,125 - 50,000 = 125 miles
```

### Step 2: Sum GPS Estimated Miles
```
Total GPS Miles = Gas Stop 1 + Trip 1 + Trip 2 + Trip 3 + Trip 4 + Gas Stop 2
Total GPS Miles = 0 + 3.2 + 2.8 + 1.5 + 4.1 + 1.4 = 13.0 miles
```

### Step 3: Calculate Variance Ratio
```
Variance Ratio = Actual Miles / Total GPS Miles
Variance Ratio = 125 / 13.0 ≈ 9.62
```
*Note: This high variance suggests GPS was not calculating correctly, 
perhaps tunnels, urban canyons, or incorrect test data. 
Real-world variance is typically 0.95 - 1.10*

### Step 4: Update Each Trip with Actual Miles
```
Trip 1 Actual Miles = 3.2 × 9.62 = 30.78 miles
Trip 2 Actual Miles = 2.8 × 9.62 = 26.94 miles
Trip 3 Actual Miles = 1.5 × 9.62 = 14.43 miles
Trip 4 Actual Miles = 4.1 × 9.62 = 39.44 miles
```

### Step 5: Calculate MPG for This Block
```
Total Gallons = 12.5 + 10.0 = 22.5 gallons
Block MPG = 125 miles / 22.5 gallons = 5.56 MPG
```

### Step 6: Calculate Fuel Cost Per Trip
Using last fill-up price ($3.60/gal):

```
Trip 1 Fuel Cost = (30.78 miles / 5.56 MPG) × $3.60 = $19.92
Trip 2 Fuel Cost = (26.94 miles / 5.56 MPG) × $3.60 = $17.43
Trip 3 Fuel Cost = (14.43 miles / 5.56 MPG) × $3.60 = $9.34
Trip 4 Fuel Cost = (39.44 miles / 5.56 MPG) × $3.60 = $25.53
```

---

## Final Google Sheet Data

| Timestamp | Vehicle | Purpose | GPS Miles | **Actual Miles** | Gas Stop? | Odometer | Gallons | Price/Gal | **Trip Fuel Cost** |
|-----------|---------|---------|-----------|------------------|-----------|----------|---------|-----------|-------------------|
| 8:00 AM | Civic | Gas Fill | 0.00 | 0.00 | TRUE | 50000 | 12.5 | 3.50 | $0.00 |
| 8:15 AM | Civic | Business | 3.20 | **30.78** | FALSE | - | - | - | **$19.92** |
| 8:30 AM | Civic | Business | 2.80 | **26.94** | FALSE | - | - | - | **$17.43** |
| 9:00 AM | Civic | Business | 1.50 | **14.43** | FALSE | - | - | - | **$9.34** |
| 9:30 AM | Civic | Business | 4.10 | **39.44** | FALSE | - | - | - | **$25.53** |
| 5:00 PM | Civic | Gas Fill | 1.40 | **13.46** | TRUE | 50125 | 10.0 | 3.60 | **$8.71** |

**Bold** = Values calculated by FleetMind's Smart Gas reconciliation

---

## Key Insights

### Accuracy
- GPS estimated: 13.0 miles
- Actual driven: 125 miles
- Variance: +862% (GPS significantly underestimated)

### Costs
- Total fuel cost: $80.93
- Cost per trip available for tax/business purposes
- Average cost per mile: $0.65

### Efficiency
- Average MPG: 5.56
- Can track efficiency changes over time
- Identify fuel-inefficient routes

---

## Realistic Example (Normal Variance)

In real-world usage, GPS is typically accurate within 5-10%:

### Realistic Scenario:
- GPS Total: 120 miles
- Actual Total: 125 miles  
- Variance: +4.17% (much more typical)
- Variance Ratio: 1.042

**Trip Updates**:
```
Trip 1: 3.2 GPS miles → 3.33 actual miles
Trip 2: 2.8 GPS miles → 2.92 actual miles
Trip 3: 1.5 GPS miles → 1.56 actual miles
Trip 4: 4.1 GPS miles → 4.27 actual miles
```

This small correction ensures accurate:
- Tax deductions
- Expense reimbursements
- Business accounting
- Performance tracking

---

## Why This Matters

### For Gig Workers
- **Accurate tax deductions**: Use actual miles, not estimates
- **Expense tracking**: Know real costs per trip
- **Profitability analysis**: Understand which trips are profitable
- **IRS compliance**: Have documented, reconciled mileage

### For Fleet Managers
- **Fuel budgeting**: Accurate fuel cost projections
- **Route optimization**: Identify inefficient routes
- **Vehicle performance**: Track MPG changes over time
- **Maintenance planning**: Use accurate mileage for service intervals

---

## Technical Notes

### GPS Accuracy Factors
GPS distance can be inaccurate due to:
- Urban canyons (tall buildings)
- Tunnels and bridges
- Signal loss
- Satellite geometry
- Device quality

### Odometer as Ground Truth
The odometer is used as the "ground truth" because:
- Legally calibrated by manufacturer
- Consistent measurement
- Not affected by GPS issues
- Accepted for tax purposes

### Variance Application
Variance is applied retroactively because:
- We don't know the error until we have odometer reading
- Past trips need accurate distances for tax purposes
- Batch correction is more efficient than continuous adjustment
- Maintains data consistency across trip blocks
