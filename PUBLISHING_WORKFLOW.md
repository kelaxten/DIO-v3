# Publishing DOD Budget Analysis to Website

Complete workflow for fetching, analyzing, and publishing the FY2024 DOD budget environmental impact analysis to the Open DIO website.

## Overview

This workflow produces a public-facing interactive dataset showing line-by-line environmental impacts for every sector of the DOD budget. Users can:

- Browse complete FY2024 DOD spending with environmental impacts
- Sort by emissions, spending, or impact intensity
- Filter by sector name or NAICS code
- Download full dataset as CSV or JSON
- Inspect calculations for validation

## Complete Workflow

### Step 1: Fetch Real DOD Budget Data

```bash
python3 fetch_full_dod_budget.py
```

**What it does:**
- Fetches FY2024 DOD spending from USAspending.gov API
- Aggregates by NAICS industry code
- Saves to `dod_budget_data/fy2024_dod_aggregated.json`

**Expected output:**
- ~$850 billion total spending
- 200-300 NAICS categories
- Takes 2-5 minutes

**If API fails:**
- Network may block USAspending.gov
- Try from different network or VPN
- Use sample data as fallback (already present)

### Step 2: Calculate Environmental Impacts

```bash
python3 analyze_full_dod_budget.py
```

**What it does:**
- Maps NAICS codes to BEA Input-Output sectors
- Calculates GHG, energy, water, and land impacts using DIO methodology
- Exports line-by-line CSV and summary

**Expected output:**
- `dod_budget_results/fy2024_dod_line_by_line.csv` - Full dataset
- `dod_budget_results/fy2024_dod_summary.csv` - Aggregated by sector
- `dod_budget_results/fy2024_dod_full_results.json` - Complete JSON

**Expected results (full budget):**
- ~150-200 million metric tons CO2e
- ~8-10 trillion MJ energy
- 100-150 BEA sectors mapped

### Step 3: Publish to Website

```bash
python3 publish_budget_data.py
```

**What it does:**
- Converts CSV to JSON format for web app
- Creates summary statistics
- Copies files to `open-dio-web/frontend/public/data/`
- Makes data available to React app

**Output files:**
- `fy2024_dod_budget_analysis.json` - Combined data for web app (loaded by React)
- `fy2024_dod_line_by_line.csv` - Downloadable full dataset
- `fy2024_dod_summary.csv` - Downloadable summary
- `fy2024_dod_full_results.json` - Downloadable complete results

### Step 4: Test Locally

```bash
cd open-dio-web/frontend
npm run dev
```

**What to check:**
1. Navigate to "Budget Analysis" tab
2. Verify data loads (should see summary cards)
3. Test sorting (click column headers)
4. Test filtering (search for "aircraft" or NAICS code)
5. Test downloads (CSV and JSON links)

**Expected behavior:**
- Table shows all sectors with calculated impacts
- Sort by clicking column headers
- Filter updates results in real-time
- Download links provide full datasets

### Step 5: Deploy to GitHub Pages

```bash
cd open-dio-web/frontend
npm run build
npm run deploy
```

**What it does:**
- Builds production React app
- Deploys to GitHub Pages
- Makes analysis publicly accessible

**Published URL:**
- `https://kelaxten.github.io/DIO-v3/` (or your configured domain)
- Budget Analysis tab will be live

## Data Format

### Web Data JSON (`fy2024_dod_budget_analysis.json`)

```json
{
  "metadata": {
    "fiscal_year": 2024,
    "agency": "Department of Defense",
    "methodology": "DIO v2.0 with EEIO life cycle assessment",
    "data_sources": { ... }
  },
  "summary": {
    "total_spending": 850000000000,
    "total_ghg": 150000000000,
    "total_energy": 8000000000000,
    "total_water": 500000000000,
    "total_land": 1000000000,
    "num_sectors": 150,
    "fiscal_year": 2024
  },
  "line_by_line": [
    {
      "NAICS_Code": "336411",
      "BEA_Sector_Code": "336411",
      "BEA_Sector_Name": "Aircraft Manufacturing",
      "Spending_USD": 25000000000,
      "Pct_of_Total": 2.94,
      "GHG_kg_CO2e": 3630000000,
      "Energy_MJ": 71250000000,
      "Water_gallons": 80000000000,
      "Land_m2_year": 312500000,
      "GHG_Intensity_kg_per_1000USD": 145.2,
      "Energy_Intensity_MJ_per_1000USD": 2850.0
    },
    // ... more sectors
  ]
}
```

### Line-by-Line CSV

| Column | Description | Unit |
|--------|-------------|------|
| NAICS_Code | 6-digit industry code | - |
| BEA_Sector_Code | Input-Output sector code | - |
| BEA_Sector_Name | Sector name | - |
| Spending_USD | Dollar amount | USD |
| Pct_of_Total | Percent of total budget | % |
| GHG_kg_CO2e | Greenhouse gas emissions | kg CO2e |
| Energy_MJ | Energy consumption | MJ |
| Water_gallons | Water use | gallons |
| Land_m2_year | Land occupation | m²·year |
| GHG_Intensity_kg_per_1000USD | Emissions per $1000 | kg CO2e/$1000 |
| Energy_Intensity_MJ_per_1000USD | Energy per $1000 | MJ/$1000 |

## Website Features

### Budget Analysis Tab

**Summary Dashboard:**
- Total spending, GHG, energy, water, land
- Real-time calculated from dataset

**Interactive Table:**
- All sectors with impacts
- Sortable by any column (click header)
- Filterable by sector name or code
- Responsive design (mobile-friendly)

**Download Options:**
- Full dataset CSV (for Excel/analysis)
- Summary CSV (for reporting)
- Complete JSON (for developers)

**Methodology Section:**
- Data sources documented
- Calculation method explained
- Links to documentation

## Updating the Dataset

When new fiscal year data becomes available:

```bash
# 1. Update fiscal year in fetch script
# Edit fetch_full_dod_budget.py, change fiscal_year=2025

# 2. Fetch new data
python3 fetch_full_dod_budget.py

# 3. Analyze
python3 analyze_full_dod_budget.py

# 4. Publish
python3 publish_budget_data.py

# 5. Deploy
cd open-dio-web/frontend
npm run build
npm run deploy
```

The website will automatically load the updated data.

## Multiple Years

To publish multiple fiscal years:

```bash
# Fetch and analyze FY2023
python3 fetch_full_dod_budget.py --fiscal-year 2023
python3 analyze_full_dod_budget.py --input dod_budget_data/fy2023_dod_aggregated.json

# Publish as separate dataset
python3 publish_budget_data.py --year 2023

# Website can load different years
# Update BudgetAnalysis.tsx to add year selector
```

## Data Validation

Before publishing, verify:

1. **Total spending matches USAspending.gov:**
   ```bash
   # Check summary
   cat dod_budget_results/fy2024_dod_summary.csv | head -1
   ```

2. **GHG intensity is reasonable:**
   - Aircraft: 126-183 kg CO2e/$1000 ✓
   - Petroleum: 285-414 kg CO2e/$1000 ✓
   - Services: 50-100 kg CO2e/$1000 ✓

3. **No missing sectors:**
   - Check for unmapped NAICS codes
   - Review warning messages in analysis output

4. **Calculations validate against literature:**
   - Compare to Crawford (2019): Should be 2-3x higher (supply chain)
   - Energy multipliers: 1.35x-2.10x (IO literature range)

## Troubleshooting

### "No Data Available" on Website

**Check:**
```bash
ls -lh open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json
```

**If missing:**
```bash
python3 publish_budget_data.py
```

### Table Not Sorting

**Issue:** React state not updating

**Fix:** Clear browser cache, rebuild:
```bash
cd open-dio-web/frontend
rm -rf dist/
npm run build
```

### Large Dataset Performance

**If >500 rows:**
- Add pagination (50 rows per page)
- Add virtual scrolling
- Consider server-side filtering

**Update BudgetAnalysis.tsx:**
```typescript
const ROWS_PER_PAGE = 50;
// Add pagination state and logic
```

### Download Links 404

**Check:** Files copied to public directory
```bash
ls open-dio-web/frontend/public/data/
```

**Fix:** Re-run publish script
```bash
python3 publish_budget_data.py
```

## Security Considerations

**Public Data:**
- All data is public (USAspending.gov)
- No sensitive information
- Safe to publish on GitHub Pages

**Data Size:**
- Full dataset: ~5-10 MB
- Acceptable for GitHub Pages
- Consider CDN for >100 MB

**Rate Limiting:**
- API fetch includes delays
- Respects USAspending.gov limits
- No authentication required

## Citation

When users download the data, they should cite:

```
DIO v2.0 FY2024 DOD Budget Environmental Impact Analysis
Data: USAspending.gov | Methodology: EPA USEEIO + Cornerstone v1.4.0
Published: https://kelaxten.github.io/DIO-v3/
Code: https://github.com/kelaxten/DIO-v3
Date: 2024-02-04
```

## Support

**For issues:**
- Check FULL_BUDGET_ANALYSIS_README.md for methodology
- Review case_study_data/CASE_STUDY_REPORT.md for validation
- Open GitHub issue for bugs

**Contact:**
- GitHub: @kelaxten
- Issues: https://github.com/kelaxten/DIO-v3/issues

---

**Last Updated:** 2026-02-04
**Version:** 2.0
**Status:** Production Ready
