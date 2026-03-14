#!/usr/bin/env python3
"""
Publish DOD budget analysis data to website

Converts analysis results to web-ready format and copies to public directory.
"""

import json
import csv
import shutil
from pathlib import Path
from typing import Dict, List

def load_line_by_line_csv(csv_file: Path) -> List[Dict]:
    """Load line-by-line CSV and convert to JSON"""
    data = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            data.append({
                'NAICS_Code': row['NAICS_Code'],
                'BEA_Sector_Code': row['BEA_Sector_Code'],
                'BEA_Sector_Name': row['BEA_Sector_Name'],
                'Spending_USD': float(row['Spending_USD']),
                'Pct_of_Total': float(row['Pct_of_Total']),
                'GHG_kg_CO2e': float(row['GHG_kg_CO2e']),
                'Energy_MJ': float(row['Energy_MJ']),
                'Water_gallons': float(row['Water_gallons']),
                'Land_m2_year': float(row['Land_m2_year']),
                'GHG_Intensity_kg_per_1000USD': float(row['GHG_Intensity_kg_per_1000USD']),
                'Energy_Intensity_MJ_per_1000USD': float(row['Energy_Intensity_MJ_per_1000USD'])
            })

    return data


def create_summary(data: List[Dict]) -> Dict:
    """Create summary statistics"""
    total_spending = sum(row['Spending_USD'] for row in data)
    total_ghg = sum(row['GHG_kg_CO2e'] for row in data)
    total_energy = sum(row['Energy_MJ'] for row in data)
    total_water = sum(row['Water_gallons'] for row in data)
    total_land = sum(row['Land_m2_year'] for row in data)

    return {
        'total_spending': total_spending,
        'total_ghg': total_ghg,
        'total_energy': total_energy,
        'total_water': total_water,
        'total_land': total_land,
        'num_sectors': len(data),
        'fiscal_year': 2024
    }


def publish_to_website():
    """Publish analysis data to website public directory"""

    print("="*80)
    print("  PUBLISHING FY2024 DOD BUDGET ANALYSIS TO WEBSITE")
    print("="*80 + "\n")

    # Input paths
    results_dir = Path("dod_budget_results")
    line_by_line_csv = results_dir / "fy2024_dod_line_by_line.csv"
    summary_csv = results_dir / "fy2024_dod_summary.csv"
    full_json = results_dir / "fy2024_dod_full_results.json"

    # Output paths
    public_dir = Path("open-dio-web/frontend/public/data")
    public_dir.mkdir(parents=True, exist_ok=True)

    if not line_by_line_csv.exists():
        print("❌ Error: Line-by-line CSV not found")
        print(f"   Expected: {line_by_line_csv}")
        print("\n   Please run analyze_full_dod_budget.py first")
        return False

    # Step 1: Load and convert line-by-line CSV to JSON
    print("[1/4] Loading line-by-line data...")
    line_data = load_line_by_line_csv(line_by_line_csv)
    print(f"  ✓ Loaded {len(line_data)} rows")

    # Step 2: Create summary
    print("\n[2/4] Creating summary statistics...")
    summary = create_summary(line_data)
    print(f"  ✓ Total spending: ${summary['total_spending']:,.0f}")
    print(f"  ✓ Total GHG: {summary['total_ghg']/1000:,.0f} metric tons CO2e")
    print(f"  ✓ Sectors: {summary['num_sectors']}")

    # Step 3: Create combined JSON for website
    print("\n[3/4] Creating web-ready JSON...")
    web_data = {
        'metadata': {
            'fiscal_year': 2024,
            'agency': 'Department of Defense',
            'description': 'Complete environmental impact analysis of FY2024 DOD spending',
            'methodology': 'DIO v2.0 with EEIO life cycle assessment',
            'data_sources': {
                'spending': 'USAspending.gov',
                'ghg': 'Cornerstone Supply Chain Factors v1.4.0',
                'energy': 'EIA MECS 2018',
                'water': 'EPA USEEIO v2.0',
                'land': 'EPA USEEIO v2.0'
            },
            'published_date': '2024-02-04'
        },
        'summary': summary,
        'line_by_line': line_data
    }

    # Save combined JSON
    web_json = public_dir / "fy2024_dod_budget_analysis.json"
    with open(web_json, 'w') as f:
        json.dump(web_data, f, indent=2)
    print(f"  ✓ Saved to {web_json}")

    # Step 4: Copy CSV and JSON files for download
    print("\n[4/4] Copying download files...")

    # Copy line-by-line CSV
    shutil.copy(line_by_line_csv, public_dir / "fy2024_dod_line_by_line.csv")
    print(f"  ✓ Copied {line_by_line_csv.name}")

    # Copy summary CSV
    if summary_csv.exists():
        shutil.copy(summary_csv, public_dir / "fy2024_dod_summary.csv")
        print(f"  ✓ Copied {summary_csv.name}")

    # Copy full JSON
    if full_json.exists():
        shutil.copy(full_json, public_dir / "fy2024_dod_full_results.json")
        print(f"  ✓ Copied {full_json.name}")

    # Print summary
    print("\n" + "="*80)
    print("  PUBLISHED FILES")
    print("="*80 + "\n")

    print("Web data (loaded by React app):")
    print(f"  {web_json}")
    print(f"  Size: {web_json.stat().st_size / 1024:.1f} KB")

    print("\nDownloadable files:")
    print(f"  {public_dir / 'fy2024_dod_line_by_line.csv'}")
    print(f"  {public_dir / 'fy2024_dod_summary.csv'}")
    print(f"  {public_dir / 'fy2024_dod_full_results.json'}")

    print("\n✓ Budget analysis data published successfully!")
    print("\nNext steps:")
    print("  1. Test locally: cd open-dio-web/frontend && npm run dev")
    print("  2. Navigate to 'Budget Analysis' tab")
    print("  3. Deploy to GitHub Pages when ready")
    print()

    return True


if __name__ == '__main__':
    try:
        success = publish_to_website()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
