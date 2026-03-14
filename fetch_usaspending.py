#!/usr/bin/env python3
"""
USAspending.gov Data Fetcher

Fetches Department of Defense contract data from USAspending.gov API
for environmental impact analysis.

References:
- USAspending API: https://api.usaspending.gov/
- API Docs: https://github.com/fedspendingtransparency/usaspending-api/tree/master/usaspending_api/api_contracts/contracts
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class USAspendingFetcher:
    """Fetch and process DOD spending data from USAspending.gov"""

    BASE_URL = "https://api.usaspending.gov/api/v2"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })

    def fetch_spending_by_naics(
        self,
        fiscal_year: int,
        agency_name: str = "Department of Defense",
        limit: int = 100
    ) -> Dict:
        """
        Fetch spending aggregated by NAICS code for a given fiscal year.

        Args:
            fiscal_year: Fiscal year (e.g., 2024)
            agency_name: Federal agency name
            limit: Maximum results to return

        Returns:
            Dictionary with aggregated spending by NAICS code
        """

        # Fiscal year dates (Oct 1 - Sep 30)
        start_date = f"{fiscal_year - 1}-10-01"
        end_date = f"{fiscal_year}-09-30"

        endpoint = f"{self.BASE_URL}/search/spending_by_category/naics"

        payload = {
            "filters": {
                "time_period": [
                    {
                        "start_date": start_date,
                        "end_date": end_date
                    }
                ],
                "agencies": [
                    {
                        "type": "funding",
                        "tier": "toptier",
                        "name": agency_name
                    }
                ]
            },
            "category": "naics",
            "limit": limit,
            "page": 1
        }

        print(f"Fetching FY{fiscal_year} spending by NAICS...")
        print(f"  Agency: {agency_name}")
        print(f"  Date range: {start_date} to {end_date}")

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

            print(f"  ✓ Fetched {len(data.get('results', []))} NAICS categories")

            return data

        except requests.exceptions.RequestException as e:
            print(f"  ✗ API request failed: {e}")
            return {}

    def fetch_awards_sample(
        self,
        fiscal_year: int,
        agency_name: str = "Department of Defense",
        limit: int = 100
    ) -> Dict:
        """
        Fetch a sample of individual awards for detailed analysis.

        Args:
            fiscal_year: Fiscal year
            agency_name: Federal agency name
            limit: Number of awards to fetch

        Returns:
            Dictionary with award details
        """

        start_date = f"{fiscal_year - 1}-10-01"
        end_date = f"{fiscal_year}-09-30"

        endpoint = f"{self.BASE_URL}/search/spending_by_award"

        payload = {
            "filters": {
                "time_period": [
                    {
                        "start_date": start_date,
                        "end_date": end_date
                    }
                ],
                "agencies": [
                    {
                        "type": "funding",
                        "tier": "toptier",
                        "name": agency_name
                    }
                ]
            },
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "NAICS Code",
                "NAICS Description",
                "Award Type",
                "Awarding Agency",
                "Awarding Sub Agency"
            ],
            "limit": limit,
            "page": 1,
            "sort": "Award Amount",
            "order": "desc"
        }

        print(f"\nFetching top {limit} awards for FY{fiscal_year}...")

        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()

            awards = data.get('results', [])
            print(f"  ✓ Fetched {len(awards)} awards")

            if awards:
                total = sum(a.get('Award Amount', 0) for a in awards)
                print(f"  Total value: ${total:,.0f}")

            return data

        except requests.exceptions.RequestException as e:
            print(f"  ✗ API request failed: {e}")
            return {}

    def save_data(self, data: Dict, filename: str, output_dir: str = "usaspending_data"):
        """Save fetched data to JSON file"""

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        filepath = output_path / filename

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"  ✓ Saved to {filepath}")

        return filepath


def main():
    """Fetch sample DOD spending data for case study"""

    print("="*80)
    print("  USASPENDING.GOV DATA FETCH - DOD CASE STUDY")
    print("="*80 + "\n")

    fetcher = USAspendingFetcher()

    # Fetch FY2024 data (most recent complete fiscal year)
    fiscal_year = 2024

    # 1. Aggregate spending by NAICS
    print("[1/2] Fetching aggregated spending by NAICS code...")
    naics_data = fetcher.fetch_spending_by_naics(
        fiscal_year=fiscal_year,
        limit=100  # Top 100 NAICS codes
    )

    if naics_data:
        fetcher.save_data(
            naics_data,
            f"dod_fy{fiscal_year}_by_naics.json"
        )

    time.sleep(1)  # Rate limiting courtesy

    # 2. Sample of individual awards
    print("\n[2/2] Fetching sample of largest awards...")
    awards_data = fetcher.fetch_awards_sample(
        fiscal_year=fiscal_year,
        limit=50  # Top 50 largest contracts
    )

    if awards_data:
        fetcher.save_data(
            awards_data,
            f"dod_fy{fiscal_year}_top_awards.json"
        )

    print("\n" + "="*80)
    print("  DATA FETCH COMPLETE")
    print("="*80 + "\n")

    # Summary
    if naics_data and 'results' in naics_data:
        results = naics_data['results']
        total_spending = sum(r.get('amount', 0) for r in results)

        print(f"Summary for FY{fiscal_year}:")
        print(f"  NAICS categories: {len(results)}")
        print(f"  Total spending (top 100): ${total_spending:,.0f}")
        print(f"  Average per category: ${total_spending / len(results):,.0f}")

        print(f"\nTop 5 NAICS codes by spending:")
        for i, result in enumerate(results[:5], 1):
            code = result.get('code', 'N/A')
            name = result.get('name', 'Unknown')
            amount = result.get('amount', 0)
            print(f"  {i}. {code} - {name}: ${amount:,.0f}")

    print("\nNext steps:")
    print("  1. Map NAICS codes to DIO/BEA sectors")
    print("  2. Run environmental impact calculation")
    print("  3. Compare to Costs of War estimates")
    print("  4. Write up case study findings")


if __name__ == '__main__':
    main()
