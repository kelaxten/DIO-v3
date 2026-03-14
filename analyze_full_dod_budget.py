#!/usr/bin/env python3
"""
Analyze full FY2024 DOD budget with line-by-line environmental impact calculations

Processes USAspending data, maps NAICS to BEA sectors, calculates environmental
impacts, and exports detailed CSV for inspection.
"""

import json
import csv
import sys
sys.path.insert(0, 'backend')

from pathlib import Path
from typing import Dict, List, Tuple, Optional
from app.core.calculator import DIOCalculator
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class NAICSMapper:
    """Maps NAICS codes to BEA Input-Output sectors"""

    def __init__(self, mapping_file: Path):
        with open(mapping_file, 'r') as f:
            data = json.load(f)

        self.mappings = data["mappings"]
        self.fallback_rules = data["fallback_rules"]

    def map_naics(self, naics: str) -> Optional[str]:
        """
        Map NAICS code to BEA sector code

        Returns:
            BEA sector code or None if no mapping found
        """
        # Clean NAICS code
        naics = str(naics).strip().replace('-', '')

        # Try exact match
        if naics in self.mappings:
            return self.mappings[naics]

        # Try 5-digit
        if len(naics) >= 5:
            naics_5 = naics[:5] + '0'
            if naics_5 in self.mappings:
                return self.mappings[naics_5]

        # Try 4-digit
        if len(naics) >= 4:
            naics_4 = naics[:4] + '00'
            if naics_4 in self.mappings:
                return self.mappings[naics_4]

        # Try 3-digit
        if len(naics) >= 3:
            naics_3 = naics[:3] + '000'
            if naics_3 in self.mappings:
                return self.mappings[naics_3]

        # No mapping found
        logger.debug(f"No BEA mapping found for NAICS {naics}")
        return None


class DODBudgetAnalyzer:
    """Analyze DOD budget with environmental impact calculations"""

    def __init__(self):
        # Load calculator with full 396-sector data
        backend_data_path = Path("backend/app/data")
        self.calculator = DIOCalculator(data_path=backend_data_path)
        logger.info(f"Loaded calculator with {len(self.calculator.multipliers)} sectors")

        # Load NAICS mapper
        self.mapper = NAICSMapper(Path("naics_to_bea_mapping.json"))
        logger.info("Loaded NAICS to BEA mapper")

        self.results = []

    def load_spending_data(self, data_file: Path) -> Dict[str, float]:
        """Load aggregated spending by NAICS from USAspending data"""
        logger.info(f"Loading spending data from {data_file}...")

        with open(data_file, 'r') as f:
            data = json.load(f)

        spending_by_naics = data.get("spending_by_naics", {})

        logger.info(f"✓ Loaded {len(spending_by_naics)} NAICS categories")
        total = sum(spending_by_naics.values())
        logger.info(f"  Total spending: ${total:,.2f}")

        return spending_by_naics

    def map_to_bea_sectors(self, naics_spending: Dict[str, float]) -> Dict[str, Dict]:
        """
        Map NAICS spending to BEA sectors

        Returns dict with BEA code -> {spending, naics_codes, naics_names}
        """
        logger.info("Mapping NAICS codes to BEA sectors...")

        bea_spending = {}
        unmapped_spending = 0
        unmapped_codes = []

        for naics, amount in naics_spending.items():
            bea_code = self.mapper.map_naics(naics)

            if bea_code:
                if bea_code not in bea_spending:
                    bea_spending[bea_code] = {
                        'spending': 0,
                        'naics_codes': [],
                        'naics_amounts': {}
                    }

                bea_spending[bea_code]['spending'] += amount
                bea_spending[bea_code]['naics_codes'].append(naics)
                bea_spending[bea_code]['naics_amounts'][naics] = amount
            else:
                unmapped_spending += amount
                unmapped_codes.append((naics, amount))

        logger.info(f"✓ Mapped to {len(bea_spending)} BEA sectors")

        if unmapped_spending > 0:
            pct = (unmapped_spending / sum(naics_spending.values())) * 100
            logger.warning(f"  Unmapped spending: ${unmapped_spending:,.2f} ({pct:.2f}%)")
            logger.warning(f"  Unmapped NAICS codes: {len(unmapped_codes)}")

            # Show top unmapped
            unmapped_codes.sort(key=lambda x: x[1], reverse=True)
            logger.warning("  Top 5 unmapped:")
            for naics, amt in unmapped_codes[:5]:
                logger.warning(f"    {naics}: ${amt:,.2f}")

        return bea_spending

    def calculate_impacts(self, bea_spending_detail: Dict[str, Dict]) -> Dict:
        """
        Calculate environmental impacts for all BEA sectors

        Returns detailed results with line-by-line calculations
        """
        logger.info("Calculating environmental impacts...")

        # Extract just spending amounts for calculator
        bea_spending = {code: detail['spending'] for code, detail in bea_spending_detail.items()}

        # Run DIO calculations
        results = self.calculator.calculate(bea_spending)

        # Enhance results with NAICS detail
        for bea_code, detail in bea_spending_detail.items():
            if bea_code in results['sector_breakdown']:
                results['sector_breakdown'][bea_code]['naics_codes'] = detail['naics_codes']
                results['sector_breakdown'][bea_code]['naics_amounts'] = detail['naics_amounts']

        logger.info("✓ Calculations complete")

        return results

    def export_line_by_line_csv(self, results: Dict, output_file: Path):
        """
        Export detailed line-by-line CSV with all calculations

        Each row shows:
        - NAICS code
        - BEA sector code and name
        - Spending amount
        - GHG emissions (kg CO2e)
        - Energy use (MJ)
        - Water consumption (gallons)
        - Land use (m²-year)
        - Percentage of total spending
        """
        logger.info(f"Exporting line-by-line results to {output_file}...")

        rows = []
        total_spending = results['total_spending']

        # Extract impact values
        for bea_code, sector_data in results['sector_breakdown'].items():
            sector_name = sector_data['name']
            bea_spending = sector_data['spending']

            # Get impacts
            impacts = {}
            for impact in sector_data['impacts']:
                category = impact['category']
                if 'Greenhouse Gas' in category:
                    impacts['GHG'] = impact['value']
                elif 'Energy' in category:
                    impacts['Energy'] = impact['value']
                elif 'Water' in category:
                    impacts['Water'] = impact['value']
                elif 'Land' in category:
                    impacts['Land'] = impact['value']

            # Get NAICS breakdown
            naics_codes = sector_data.get('naics_codes', [])
            naics_amounts = sector_data.get('naics_amounts', {})

            if naics_codes:
                # Create row for each NAICS code
                for naics in naics_codes:
                    naics_spending = naics_amounts.get(naics, 0)
                    pct_of_bea = (naics_spending / bea_spending) if bea_spending > 0 else 0

                    # Allocate impacts proportionally
                    row = {
                        'NAICS_Code': naics,
                        'BEA_Sector_Code': bea_code,
                        'BEA_Sector_Name': sector_name,
                        'Spending_USD': naics_spending,
                        'Pct_of_Total': (naics_spending / total_spending) * 100 if total_spending > 0 else 0,
                        'GHG_kg_CO2e': impacts.get('GHG', 0) * pct_of_bea,
                        'Energy_MJ': impacts.get('Energy', 0) * pct_of_bea,
                        'Water_gallons': impacts.get('Water', 0) * pct_of_bea,
                        'Land_m2_year': impacts.get('Land', 0) * pct_of_bea,
                        'GHG_Intensity_kg_per_1000USD': (impacts.get('GHG', 0) / (bea_spending / 1000)) if bea_spending > 0 else 0,
                        'Energy_Intensity_MJ_per_1000USD': (impacts.get('Energy', 0) / (bea_spending / 1000)) if bea_spending > 0 else 0
                    }
                    rows.append(row)
            else:
                # No NAICS detail, just BEA sector
                row = {
                    'NAICS_Code': '',
                    'BEA_Sector_Code': bea_code,
                    'BEA_Sector_Name': sector_name,
                    'Spending_USD': bea_spending,
                    'Pct_of_Total': (bea_spending / total_spending) * 100 if total_spending > 0 else 0,
                    'GHG_kg_CO2e': impacts.get('GHG', 0),
                    'Energy_MJ': impacts.get('Energy', 0),
                    'Water_gallons': impacts.get('Water', 0),
                    'Land_m2_year': impacts.get('Land', 0),
                    'GHG_Intensity_kg_per_1000USD': (impacts.get('GHG', 0) / (bea_spending / 1000)) if bea_spending > 0 else 0,
                    'Energy_Intensity_MJ_per_1000USD': (impacts.get('Energy', 0) / (bea_spending / 1000)) if bea_spending > 0 else 0
                }
                rows.append(row)

        # Sort by spending (descending)
        rows.sort(key=lambda x: x['Spending_USD'], reverse=True)

        # Write CSV
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', newline='') as f:
            fieldnames = [
                'NAICS_Code',
                'BEA_Sector_Code',
                'BEA_Sector_Name',
                'Spending_USD',
                'Pct_of_Total',
                'GHG_kg_CO2e',
                'Energy_MJ',
                'Water_gallons',
                'Land_m2_year',
                'GHG_Intensity_kg_per_1000USD',
                'Energy_Intensity_MJ_per_1000USD'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"✓ Exported {len(rows):,} rows to {output_file}")

    def export_summary_csv(self, results: Dict, output_file: Path):
        """Export summary CSV with BEA sector totals"""
        logger.info(f"Exporting summary to {output_file}...")

        rows = []
        total_spending = results['total_spending']

        for bea_code, sector_data in results['sector_breakdown'].items():
            sector_name = sector_data['name']
            spending = sector_data['spending']

            # Extract impacts
            impacts = {}
            for impact in sector_data['impacts']:
                category = impact['category']
                if 'Greenhouse Gas' in category:
                    impacts['GHG'] = impact['value']
                elif 'Energy' in category:
                    impacts['Energy'] = impact['value']
                elif 'Water' in category:
                    impacts['Water'] = impact['value']
                elif 'Land' in category:
                    impacts['Land'] = impact['value']

            row = {
                'BEA_Sector_Code': bea_code,
                'BEA_Sector_Name': sector_name,
                'Spending_USD': spending,
                'Pct_of_Total': (spending / total_spending) * 100 if total_spending > 0 else 0,
                'GHG_kg_CO2e': impacts.get('GHG', 0),
                'GHG_metric_tons_CO2e': impacts.get('GHG', 0) / 1000,
                'Energy_MJ': impacts.get('Energy', 0),
                'Water_gallons': impacts.get('Water', 0),
                'Land_m2_year': impacts.get('Land', 0),
                'GHG_Intensity_kg_per_1000USD': (impacts.get('GHG', 0) / (spending / 1000)) if spending > 0 else 0,
                'Num_NAICS_Codes': len(sector_data.get('naics_codes', []))
            }
            rows.append(row)

        # Sort by GHG emissions (descending)
        rows.sort(key=lambda x: x['GHG_kg_CO2e'], reverse=True)

        # Write CSV
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"✓ Exported {len(rows)} BEA sectors to {output_file}")


def print_summary(results: Dict):
    """Print executive summary of results"""
    print("\n" + "="*80)
    print("  FULL FY2024 DOD BUDGET ENVIRONMENTAL IMPACT ANALYSIS")
    print("="*80 + "\n")

    # Total impacts
    total_spending = results['total_spending']
    print(f"Total Spending: ${total_spending:,.2f}\n")

    print("Total Environmental Impacts:")
    for impact in results['impacts']:
        value = impact['value']
        unit = impact['unit']
        category = impact['category']

        # Convert to human-readable
        if 'Greenhouse Gas' in category:
            value_tons = value / 1000
            print(f"  {category}: {value_tons:,.0f} metric tons CO2e")
        elif 'Energy' in category:
            value_tj = value / 1e6  # Convert MJ to TJ
            print(f"  {category}: {value_tj:,.0f} TJ ({value:,.0f} MJ)")
        elif 'Water' in category:
            value_mgal = value / 1e6  # Convert to million gallons
            print(f"  {category}: {value_mgal:,.1f} million gallons")
        elif 'Land' in category:
            value_km2 = value / 1e6  # Convert m² to km²
            print(f"  {category}: {value_km2:,.1f} km²-year")

    # Top 10 sectors by GHG
    print("\n\nTop 10 Sectors by GHG Emissions:\n")

    sector_list = []
    for code, data in results['sector_breakdown'].items():
        ghg = next(imp['value'] for imp in data['impacts'] if 'Greenhouse Gas' in imp['category'])
        sector_list.append({
            'code': code,
            'name': data['name'],
            'spending': data['spending'],
            'ghg': ghg
        })

    sector_list.sort(key=lambda x: x['ghg'], reverse=True)

    for i, sector in enumerate(sector_list[:10], 1):
        pct = (sector['spending'] / total_spending) * 100
        ghg_tons = sector['ghg'] / 1000
        print(f"{i:2d}. {sector['name'][:60]}")
        print(f"    Spending: ${sector['spending']:>15,.0f} ({pct:5.2f}%)")
        print(f"    GHG:      {ghg_tons:>15,.0f} metric tons CO2e\n")

    print("="*80)


def main():
    """Main execution"""
    print("="*80)
    print("  ANALYZING FULL FY2024 DOD BUDGET")
    print("  Environmental Impact Line-by-Line Calculation")
    print("="*80 + "\n")

    analyzer = DODBudgetAnalyzer()
    output_dir = Path("dod_budget_results")
    output_dir.mkdir(exist_ok=True)

    # Load spending data
    print("[1/5] Loading USAspending data...")
    data_file = Path("dod_budget_data/fy2024_dod_aggregated.json")

    if not data_file.exists():
        logger.error(f"Data file not found: {data_file}")
        logger.error("Please run fetch_full_dod_budget.py first")
        return False

    naics_spending = analyzer.load_spending_data(data_file)

    # Map to BEA sectors
    print("\n[2/5] Mapping NAICS codes to BEA sectors...")
    bea_spending_detail = analyzer.map_to_bea_sectors(naics_spending)

    # Calculate impacts
    print("\n[3/5] Calculating environmental impacts...")
    results = analyzer.calculate_impacts(bea_spending_detail)

    # Export line-by-line CSV
    print("\n[4/5] Exporting line-by-line results...")
    analyzer.export_line_by_line_csv(
        results,
        output_dir / "fy2024_dod_line_by_line.csv"
    )

    # Export summary CSV
    print("\n[5/5] Exporting summary...")
    analyzer.export_summary_csv(
        results,
        output_dir / "fy2024_dod_summary.csv"
    )

    # Save full JSON results
    with open(output_dir / "fy2024_dod_full_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"✓ Saved full results to {output_dir / 'fy2024_dod_full_results.json'}")

    # Print summary
    print_summary(results)

    print("\nOutputs:")
    print(f"  {output_dir}/fy2024_dod_line_by_line.csv - Detailed line-by-line results")
    print(f"  {output_dir}/fy2024_dod_summary.csv - Summary by BEA sector")
    print(f"  {output_dir}/fy2024_dod_full_results.json - Complete results (JSON)")
    print("\n✓ Analysis complete! Open CSV files in Excel/spreadsheet for inspection\n")

    return True


if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        exit(1)
