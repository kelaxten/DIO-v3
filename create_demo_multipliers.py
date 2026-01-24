"""
Create demo multipliers for backend testing

This creates reasonable impact multipliers for the extracted sectors
based on typical values from the literature until we can properly
calculate them from the full DIO model.
"""

import json
from pathlib import Path

OUTPUT_DIR = Path("backend/app/data")

# Load the extracted sectors
with open(OUTPUT_DIR / "sectors_full.json") as f:
    sectors = json.load(f)

# Create multipliers based on typical defense sector values
# These are rough estimates per $1000 spending
# Source: Similar to EPA DIO model documentation

# Base multipliers (conservative estimates)
BASE_MULTIPLIERS = {
    'GHG': 150.0,      # kg CO2 eq per $1000
    'Energy': 2500.0,   # MJ per $1000
    'Water': 3000.0,    # gallons per $1000
    'Land': 10.0        # m2-year per $1000
}

# Sector-specific adjustments (multiplier factors)
SECTOR_ADJUSTMENTS = {
    # High energy/emissions industries
    '33299A': 1.8,  # Ammunition manufacturing
    '336411': 2.2,  # Aircraft manufacturing
    '336414': 2.0,  # Guided missile manufacturing
    '3366': 1.9,    # Ship building
    '336992': 1.7,  # Military armored vehicles

    # Medium industries
    '334511': 1.3,  # Navigation equipment
    '334413': 1.2,  # Semiconductors
    '541715': 0.6,  # R&D services (lower physical footprint)
    '334220': 1.1,  # Communications equipment
    '332993': 1.5,  # Ammunition components

    # Service industries (lower physical footprint)
    '541': 0.5,     # Professional services
    '561': 0.4,     # Administrative services
    '721': 0.3,     # Accommodation
}

# Create multipliers for all sectors
multipliers = {}
for sector in sectors:
    code = sector['code']

    # Get adjustment factor (default to 1.0 if not specified)
    adjustment = SECTOR_ADJUSTMENTS.get(code, 1.0)

    # Check if defense-relevant - give slight boost to typical defense sectors
    if sector['is_defense_relevant']:
        adjustment *= 1.1

    multipliers[code] = {
        'name': sector['name'],
        'GHG': round(BASE_MULTIPLIERS['GHG'] * adjustment, 2),
        'Energy': round(BASE_MULTIPLIERS['Energy'] * adjustment, 2),
        'Water': round(BASE_MULTIPLIERS['Water'] * adjustment, 2),
        'Land': round(BASE_MULTIPLIERS['Land'] * adjustment, 2)
    }

# Create output structure
output = {
    'description': 'DIO v2.0 environmental impact multipliers by sector',
    'note': 'Demo multipliers based on typical values. Full model uses calculated Leontief multipliers.',
    'units': {
        'GHG': 'kg CO2 eq per $1000 spending',
        'Energy': 'MJ per $1000 spending',
        'Water': 'gallons per $1000 spending',
        'Land': 'm2-year per $1000 spending'
    },
    'sectors': multipliers
}

# Save
with open(OUTPUT_DIR / "multipliers_full.json", 'w') as f:
    json.dump(output, f, indent=2)

print(f"Created multipliers for {len(multipliers)} sectors")
print(f"Saved to {OUTPUT_DIR / 'multipliers_full.json'}")

# Show sample
print("\nSample multipliers:")
for i, (code, mult) in enumerate(list(multipliers.items())[:5]):
    print(f"  {code} ({mult['name'][:50]}...):")
    print(f"    GHG: {mult['GHG']}, Energy: {mult['Energy']}, Water: {mult['Water']}, Land: {mult['Land']}")
