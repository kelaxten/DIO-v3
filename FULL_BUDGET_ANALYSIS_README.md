# Full DOD Budget Analysis Pipeline

This pipeline fetches the complete FY2024 Department of Defense budget from USAspending.gov, maps spending to environmental impact sectors, calculates full supply chain impacts, and exports line-by-line results for inspection.

## Overview

The analysis pipeline consists of three main steps:

1. **Fetch** - Download FY2024 DOD spending data from USAspending.gov API
2. **Map** - Map NAICS industry codes to BEA Input-Output sectors
3. **Calculate** - Run DIO environmental impact calculations and export results

## Prerequisites

```bash
# Python 3.8+ required
pip install requests

# Ensure backend data is present
ls backend/app/data/multipliers.json
```

## Quick Start

### Step 1: Fetch USAspending Data

```bash
python3 fetch_full_dod_budget.py
```

This script:
- Fetches aggregated FY2024 DOD spending by NAICS code
- Optionally fetches detailed contract awards (slower)
- Saves data to `dod_budget_data/` directory

**Expected output:**
- `dod_budget_data/fy2024_dod_by_naics.json` - Raw API response
- `dod_budget_data/fy2024_dod_aggregated.json` - Spending totals by NAICS
- `dod_budget_data/fy2024_dod_detailed_awards.json` - Individual contracts (optional)

**Time:** 2-5 minutes for aggregated data, 10-30 minutes for detailed awards

### Step 2: Calculate Environmental Impacts

```bash
python3 analyze_full_dod_budget.py
```

This script:
- Loads fetched spending data
- Maps NAICS codes to BEA Input-Output sectors
- Calculates GHG, energy, water, and land impacts using DIO methodology
- Exports line-by-line CSV results

**Expected output:**
- `dod_budget_results/fy2024_dod_line_by_line.csv` - Detailed line-by-line calculations
- `dod_budget_results/fy2024_dod_summary.csv` - Summary by BEA sector
- `dod_budget_results/fy2024_dod_full_results.json` - Complete results (JSON)

**Time:** 1-2 minutes

### Step 3: Inspect Results

Open the CSV files in Excel, Google Sheets, or any spreadsheet tool:

```bash
# On Linux/Mac
xdg-open dod_budget_results/fy2024_dod_line_by_line.csv

# Or copy to your local machine
scp user@server:~/DIO-v3/dod_budget_results/*.csv .
```

## Output File Details

### Line-by-Line CSV (`fy2024_dod_line_by_line.csv`)

Contains one row per NAICS code with calculated environmental impacts:

| Column | Description | Unit |
|--------|-------------|------|
| NAICS_Code | 6-digit NAICS industry code | - |
| BEA_Sector_Code | Mapped BEA I-O sector | - |
| BEA_Sector_Name | Sector name | - |
| Spending_USD | Dollar amount | USD |
| Pct_of_Total | Percent of total DOD budget | % |
| GHG_kg_CO2e | Greenhouse gas emissions | kg CO2e |
| Energy_MJ | Energy consumption | MJ |
| Water_gallons | Water use | gallons |
| Land_m2_year | Land occupation | m²·year |
| GHG_Intensity_kg_per_1000USD | Emissions per $1000 | kg CO2e/$1000 |
| Energy_Intensity_MJ_per_1000USD | Energy per $1000 | MJ/$1000 |

**Example rows:**
```csv
NAICS_Code,BEA_Sector_Code,BEA_Sector_Name,Spending_USD,Pct_of_Total,GHG_kg_CO2e,...
336411,336411,Aircraft Manufacturing,25000000000,25.0,3150000000,...
336611,336611,Ship Building and Repairing,22000000000,22.0,4026000000,...
324110,324110,Petroleum Refineries,8000000000,8.0,3312000000,...
```

**Use cases:**
- Sort by GHG emissions to find highest-impact sectors
- Filter by sector type (e.g., all aerospace: NAICS 336xxx)
- Identify emissions intensity outliers
- Aggregate by higher-level categories

### Summary CSV (`fy2024_dod_summary.csv`)

Contains one row per BEA sector with aggregated totals:

| Column | Description |
|--------|-------------|
| BEA_Sector_Code | BEA I-O sector code |
| BEA_Sector_Name | Sector name |
| Spending_USD | Total spending in sector |
| Pct_of_Total | Percent of DOD budget |
| GHG_kg_CO2e | Total GHG emissions (kg) |
| GHG_metric_tons_CO2e | Total GHG emissions (metric tons) |
| Energy_MJ | Total energy use |
| Water_gallons | Total water consumption |
| Land_m2_year | Total land use |
| GHG_Intensity_kg_per_1000USD | Emissions intensity |
| Num_NAICS_Codes | Number of NAICS codes mapped to this sector |

**Use cases:**
- High-level sector comparison
- Portfolio analysis
- Pivot tables and charts
- Validation against literature

### Full Results JSON (`fy2024_dod_full_results.json`)

Complete structured results including:
- Total impacts across all categories
- Sector-by-sector breakdown
- NAICS to BEA mapping details
- Model version and metadata

**Use cases:**
- Programmatic access to results
- Integration with other tools
- Reproducibility verification
- Custom analysis scripts

## Expected Results (FY2024)

Based on the case study methodology:

| Metric | Expected Value |
|--------|----------------|
| Total DOD Spending | ~$850 billion |
| Total GHG Emissions | ~150-200 million metric tons CO2e |
| Total Energy Use | ~8-10 trillion MJ |
| NAICS Categories | 200-300 codes |
| BEA Sectors | 100-150 sectors |

**Comparison to prior work:**
- Crawford (2019): 59M tons CO2e (operational only)
- Our estimate: 2-3x higher (includes full supply chain)

## Methodology

### NAICS to BEA Mapping

The pipeline maps 6-digit NAICS codes to BEA Input-Output sectors using:

1. **Exact match** - Direct NAICS → BEA mapping
2. **5-digit aggregation** - Map to 5-digit NAICS level
3. **4-digit aggregation** - Map to 4-digit industry level
4. **3-digit aggregation** - Map to 3-digit subsector level

Defense-specific mappings:
- 336411 → Aircraft Manufacturing
- 336611 → Ship Building and Repairing
- 332994 → Small Arms and Ordnance
- 336992 → Military Armored Vehicles

### Environmental Calculations

Uses DIO v2.0 methodology:

**Impact = Spending × (Direct Intensity + Leontief × Indirect Intensity)**

Data sources:
- **GHG**: Cornerstone Supply Chain Factors v1.4.0 (AR6 GWP-100)
- **Energy**: EIA MECS 2018 + IO literature multipliers (1.35x-2.10x)
- **Water**: EPA USEEIO v2.0
- **Land**: EPA USEEIO v2.0

### Uncertainty

| Impact | Uncertainty |
|--------|-------------|
| GHG | ±25% |
| Energy | ±25-35% |
| Water | ±40% |
| Land | ±50% |

## Troubleshooting

### API Fetch Fails

**Error:** `ProxyError` or connection timeout

**Solution:** USAspending.gov API may be blocked by network firewalls. Try:
1. Run from different network (home internet vs corporate)
2. Use VPN
3. Contact USAspending support for API key
4. Use the case study sample data instead

### Missing Multipliers

**Error:** `FileNotFoundError: multipliers.json not found`

**Solution:** Ensure full 396-sector multipliers file exists:
```bash
ls -lh backend/app/data/multipliers.json
# Should be ~2800 lines, ~500KB
```

### Unmapped NAICS Codes

**Warning:** `Unmapped spending: $X billion`

**Explanation:** Some NAICS codes don't map cleanly to BEA sectors. This is normal for:
- New/emerging industries
- Government-specific codes
- Aggregated categories

**Impact:** Typically <5% of total spending. Document in analysis.

### Memory Issues

**Error:** `MemoryError` or system slowdown

**Solution:** Analysis requires ~2-4GB RAM. For large datasets:
- Process in chunks
- Use aggregated data instead of detailed awards
- Run on machine with more memory

## Validation

Compare results to published estimates:

1. **Crawford (2019) - Costs of War:**
   - 59M tons CO2e operational emissions
   - Our estimate should be 2-3x higher (includes supply chain)

2. **EPA FLIGHT Tool:**
   - Similar methodology but different scope
   - Good for cross-validation

3. **Academic literature:**
   - Nansai et al. (2021) - Military carbon footprint
   - Cottrell et al. (2019) - Defense sector emissions

## Citation

If using this analysis in research or publication:

```
DIO v2.0 Full Budget Analysis Pipeline (2026)
Data: USAspending.gov FY2024 DOD obligations
Methodology: EPA USEEIO + Cornerstone Supply Chain Factors v1.4.0
Code: https://github.com/kelaxten/DIO-v3
```

## Files in This Pipeline

| File | Purpose |
|------|---------|
| `fetch_full_dod_budget.py` | Download FY2024 DOD data from USAspending API |
| `analyze_full_dod_budget.py` | Calculate environmental impacts and export CSVs |
| `naics_to_bea_mapping.json` | NAICS → BEA sector crosswalk |
| `backend/app/data/multipliers.json` | Environmental multipliers (396 sectors) |
| `case_study_data/` | Sample data and journal article case study |

## Support

For issues with:
- **USAspending API**: https://api.usaspending.gov/docs/
- **DIO methodology**: See `case_study_data/CASE_STUDY_REPORT.md`
- **Code/bugs**: https://github.com/kelaxten/DIO-v3/issues

---

**Last Updated:** 2026-02-04
**Version:** 2.0
**License:** MIT
