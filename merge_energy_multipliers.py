#!/usr/bin/env python3
"""
Merge energy multipliers into the main multipliers.json file.

This script:
1. Loads the existing multipliers.json (with GHG data from Cornerstone)
2. Loads the generated energy_multipliers.json (with EIA energy data)
3. Updates the Energy field for each sector
4. Saves the merged result back to multipliers.json
"""

import json
from pathlib import Path
from typing import Dict, Any

def load_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """Save JSON file with pretty formatting."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved: {filepath}")

def merge_energy_data() -> None:
    """Merge energy multipliers into main multipliers file."""

    # Paths
    multipliers_path = Path('backend/app/data/multipliers.json')
    energy_path = Path('backend/app/data/energy_multipliers_io.json')

    # Load data
    print("📂 Loading files...")
    multipliers = load_json(multipliers_path)
    energy_data = load_json(energy_path)

    print(f"   Main multipliers: {len(multipliers['sectors'])} sectors")
    print(f"   Energy data: {len(energy_data['sectors'])} sectors")

    # Track statistics
    updated = 0
    missing = 0
    mismatched_names = []

    # Update Energy field for each sector
    print("\n🔄 Merging energy data...")
    for sector_code, sector_data in multipliers['sectors'].items():
        if sector_code in energy_data['sectors']:
            energy_info = energy_data['sectors'][sector_code]

            # Update Energy field with total energy (includes supply chain)
            old_value = sector_data['Energy']
            new_value = energy_info['energy_total_mj_per_1000']
            sector_data['Energy'] = new_value
            updated += 1

            # Check for name mismatches (helpful for debugging)
            if sector_data['name'] != energy_info['name']:
                mismatched_names.append({
                    'code': sector_code,
                    'multipliers': sector_data['name'],
                    'energy': energy_info['name']
                })
        else:
            missing += 1
            print(f"   ⚠️  No energy data for sector {sector_code}: {sector_data['name']}")

    # Update metadata
    multipliers['last_updated'] = energy_data['calculation_date']
    multipliers['data_sources'] = {
        'GHG': 'Cornerstone Supply Chain Factors v1.4.0',
        'Energy': 'EIA MECS 2018, CBECS 2018, AEO 2023',
        'Water': 'EPA USEEIO v2.0',
        'Land': 'EPA USEEIO v2.0'
    }

    # Add note about energy methodology
    if 'notes' not in multipliers:
        multipliers['notes'] = []

    multipliers['notes'].append({
        'category': 'Energy',
        'description': 'Energy multipliers calculated from EIA government data with supply chain effects',
        'methodology': 'See ENERGY_METHODOLOGY.md for detailed calculation approach',
        'uncertainty': '±30-40% depending on sector data availability'
    })

    # Save merged data
    print(f"\n💾 Saving merged data...")
    save_json(multipliers_path, multipliers)

    # Report statistics
    print(f"\n📊 Merge Statistics:")
    print(f"   ✅ Updated: {updated} sectors")
    print(f"   ⚠️  Missing: {missing} sectors")

    if mismatched_names:
        print(f"\n⚠️  Found {len(mismatched_names)} name mismatches:")
        for item in mismatched_names[:5]:  # Show first 5
            print(f"   {item['code']}: '{item['multipliers']}' vs '{item['energy']}'")
        if len(mismatched_names) > 5:
            print(f"   ... and {len(mismatched_names) - 5} more")

    # Sample results
    print(f"\n🎯 Sample Energy Values (MJ/$1000):")
    sample_sectors = ['336411', '336414', '324110', '331110', '541300']
    for code in sample_sectors:
        if code in multipliers['sectors']:
            s = multipliers['sectors'][code]
            print(f"   {code}: {s['name']:<50} {s['Energy']:>10,.0f}")

    print(f"\n✅ ENERGY DATA INTEGRATION COMPLETE")
    print(f"   All {updated} sectors now have energy multipliers based on EIA government data.")

if __name__ == '__main__':
    merge_energy_data()
