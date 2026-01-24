"""
Extract DIO Model Data for Backend API

This script processes the DIO v2.0 CSV files and extracts:
1. Sector list (all BEA sectors)
2. Impact multipliers per sector
3. Sector metadata

Output: JSON files for the backend API
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict

# Paths
DIO_DATA_DIR = Path("DIO-updated/data")
OUTPUT_DIR = Path("backend/app/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading DIO model data...")

# Load A matrix (direct requirements)
print("  Loading A matrix...")
a_matrix = pd.read_csv(DIO_DATA_DIR / "A_Matrix_DIO.csv")
print(f"  A matrix: {len(a_matrix)} rows")

# Load B matrix (environmental satellite accounts)
print("  Loading B matrix...")
b_matrix = pd.read_csv(DIO_DATA_DIR / "B_Matrix_DIO.csv")
print(f"  B matrix: {len(b_matrix)} rows")

# Extract unique sectors from FlowID column (these are BEA sector codes)
print("\nExtracting sectors...")
sectors_a = set(a_matrix['FlowID'].unique())
print(f"  Sectors in A matrix: {len(sectors_a)}")

# Also get sector names
sector_info = {}
for _, row in a_matrix[['FlowID', 'Flow']].drop_duplicates().iterrows():
    sector_code = row['FlowID']
    sector_name = row['Flow']

    # Extract clean sector code and name
    # Format is usually: "SECTOR_CODE/US"
    if '/' in sector_code:
        code = sector_code.split('/')[0]
    else:
        code = sector_code

    # Extract name (format: "Name (code) - US")
    if '(' in sector_name:
        name = sector_name.split('(')[0].strip()
    else:
        name = sector_name

    sector_info[code] = {
        'code': code,
        'name': name,
        'full_code': sector_code
    }

print(f"  Extracted {len(sector_info)} unique sectors")

# Identify defense-relevant sectors
defense_keywords = [
    'aircraft', 'ship', 'missile', 'weapon', 'military', 'defense',
    'ordnance', 'armored', 'guided', 'aerospace', 'ammunition',
    'combat', 'naval', 'army', 'navy', 'air force'
]

defense_sectors = []
for code, info in sector_info.items():
    name_lower = info['name'].lower()
    if any(keyword in name_lower for keyword in defense_keywords):
        info['is_defense'] = True
        defense_sectors.append(code)
    else:
        info['is_defense'] = False

print(f"  Found {len(defense_sectors)} defense-relevant sectors")

# Save full sector list
print("\nSaving sector data...")
sectors_json = [
    {
        'code': code,
        'name': info['name'],
        'is_defense_relevant': info.get('is_defense', False)
    }
    for code, info in sorted(sector_info.items())
]

with open(OUTPUT_DIR / "sectors_full.json", 'w') as f:
    json.dump(sectors_json, f, indent=2)
print(f"  Saved {len(sectors_json)} sectors to sectors_full.json")

# Save defense sectors separately
defense_sectors_json = [s for s in sectors_json if s['is_defense_relevant']]
with open(OUTPUT_DIR / "sectors_defense.json", 'w') as f:
    json.dump(defense_sectors_json, f, indent=2)
print(f"  Saved {len(defense_sectors_json)} defense sectors to sectors_defense.json")

# For demo/testing, extract a sample of top sectors by total flows
print("\nCalculating sector impact factors...")

# Group environmental flows by sector
# B matrix has ProcessID (sectors) and Flow (environmental flows)
sector_flows = defaultdict(lambda: defaultdict(float))

for _, row in b_matrix.iterrows():
    process_id = row.get('ProcessID', '')
    flow = row.get('Flow', '')
    amount = row.get('Amount', 0)

    # Map process to sector (simplified - just track by sector code pattern)
    if '/' in process_id:
        sector = process_id.split('/')[0]
    else:
        sector = process_id

    # Categorize flow type
    flow_lower = flow.lower()
    if 'carbon' in flow_lower or 'co2' in flow_lower or 'methane' in flow_lower or 'greenhouse' in flow_lower:
        sector_flows[sector]['GHG'] += abs(amount)
    elif 'energy' in flow_lower or 'electricity' in flow_lower or 'fuel' in flow_lower:
        sector_flows[sector]['Energy'] += abs(amount)
    elif 'water' in flow_lower:
        sector_flows[sector]['Water'] += abs(amount)
    elif 'land' in flow_lower:
        sector_flows[sector]['Land'] += abs(amount)

print(f"  Calculated flows for {len(sector_flows)} sectors")

# Create simplified multipliers (total environmental flow per sector)
# Note: These are rough approximations for the demo
# Full implementation would calculate proper Leontief multipliers
multipliers = {}
for sector, flows in sector_flows.items():
    if sector in sector_info:
        multipliers[sector] = {
            'name': sector_info[sector]['name'],
            'GHG': flows.get('GHG', 0),
            'Energy': flows.get('Energy', 0),
            'Water': flows.get('Water', 0),
            'Land': flows.get('Land', 0)
        }

# Save multipliers
with open(OUTPUT_DIR / "multipliers_full.json", 'w') as f:
    json.dump({
        'description': 'DIO v2.0 environmental flow totals by sector',
        'note': 'These are simplified totals. Full model uses Leontief multipliers.',
        'units': {
            'GHG': 'kg CO2 eq',
            'Energy': 'MJ',
            'Water': 'gallons',
            'Land': 'm2-year'
        },
        'sectors': multipliers
    }, f, indent=2)

print(f"  Saved multipliers for {len(multipliers)} sectors")

# Create summary report
summary = {
    'model': 'DIO v2.0',
    'source': 'USEPA Defense Input-Output Model',
    'total_sectors': len(sector_info),
    'defense_sectors': len(defense_sectors),
    'sectors_with_multipliers': len(multipliers),
    'top_defense_sectors': defense_sectors[:20],
    'data_files': {
        'sectors_full': 'sectors_full.json',
        'sectors_defense': 'sectors_defense.json',
        'multipliers_full': 'multipliers_full.json'
    }
}

with open(OUTPUT_DIR / "model_info.json", 'w') as f:
    json.dump(summary, f, indent=2)

print("\n" + "="*60)
print("DATA EXTRACTION COMPLETE")
print("="*60)
print(f"Total sectors: {summary['total_sectors']}")
print(f"Defense sectors: {summary['defense_sectors']}")
print(f"Sectors with multipliers: {summary['sectors_with_multipliers']}")
print(f"\nOutput directory: {OUTPUT_DIR}")
print("="*60)
