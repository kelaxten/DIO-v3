#!/usr/bin/env python3
"""
Fetch complete FY2024 DOD spending from USAspending.gov API

This script downloads all DOD contract awards and obligations for FY2024,
aggregates by NAICS code, and prepares data for environmental impact analysis.
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class USAspendingFullFetcher:
    """Fetch complete DOD spending data from USAspending.gov"""

    BASE_URL = "https://api.usaspending.gov/api/v2"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'DIO-Environmental-Research/2.0'
        })

    def fetch_spending_by_agency(
        self,
        fiscal_year: int = 2024,
        agency_name: str = "Department of Defense",
        limit: int = 100
    ) -> Dict:
        """
        Fetch DOD spending aggregated by NAICS code

        This endpoint provides aggregated data which is much faster than
        fetching individual awards.
        """
        logger.info(f"Fetching {agency_name} spending for FY{fiscal_year}...")

        endpoint = f"{self.BASE_URL}/search/spending_by_category/naics"

        # FY2024 runs from Oct 1, 2023 to Sep 30, 2024
        start_date = f"{fiscal_year - 1}-10-01"
        end_date = f"{fiscal_year}-09-30"

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

        all_results = []
        page = 1

        while True:
            payload["page"] = page
            logger.info(f"  Fetching page {page}...")

            try:
                response = self.session.post(endpoint, json=payload, timeout=30)
                response.raise_for_status()

                data = response.json()
                results = data.get("results", [])

                if not results:
                    break

                all_results.extend(results)
                logger.info(f"    Got {len(results)} records (total: {len(all_results)})")

                # Check if there are more pages
                page_metadata = data.get("page_metadata", {})
                if page >= page_metadata.get("num_pages", 1):
                    break

                page += 1
                time.sleep(0.5)  # Rate limiting

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page {page}: {e}")
                break

        logger.info(f"✓ Fetched {len(all_results)} NAICS categories")
        return {
            "metadata": {
                "fiscal_year": fiscal_year,
                "agency": agency_name,
                "start_date": start_date,
                "end_date": end_date,
                "total_categories": len(all_results),
                "fetch_date": datetime.now().isoformat()
            },
            "results": all_results
        }

    def fetch_detailed_awards(
        self,
        fiscal_year: int = 2024,
        agency_name: str = "Department of Defense",
        limit: int = 1000
    ) -> List[Dict]:
        """
        Fetch detailed award-level data (slower but more granular)

        Use this for line-by-line inspection of contracts
        """
        logger.info(f"Fetching detailed awards for {agency_name} FY{fiscal_year}...")
        logger.warning("This will fetch up to 1000 awards per page - may take several minutes")

        endpoint = f"{self.BASE_URL}/search/spending_by_award"

        start_date = f"{fiscal_year - 1}-10-01"
        end_date = f"{fiscal_year}-09-30"

        payload = {
            "filters": {
                "time_period": [
                    {
                        "start_date": start_date,
                        "end_date": end_date,
                        "date_type": "action_date"
                    }
                ],
                "agencies": [
                    {
                        "type": "funding",
                        "tier": "toptier",
                        "name": agency_name
                    }
                ],
                "award_type_codes": ["A", "B", "C", "D"]  # Contracts only
            },
            "fields": [
                "Award ID",
                "Recipient Name",
                "Award Amount",
                "Total Outlays",
                "Description",
                "recipient_id",
                "Award Type",
                "awarding_agency",
                "funding_agency",
                "period_of_performance_start_date",
                "Award Base Action Date",
                "naics_code",
                "naics_description",
                "prime_award_transaction_place_of_performance_state_name"
            ],
            "limit": limit,
            "page": 1,
            "sort": "Award Amount",
            "order": "desc"
        }

        all_awards = []
        page = 1
        max_pages = 100  # Limit to prevent excessive API calls

        while page <= max_pages:
            payload["page"] = page
            logger.info(f"  Fetching page {page}/{max_pages}...")

            try:
                response = self.session.post(endpoint, json=payload, timeout=60)
                response.raise_for_status()

                data = response.json()
                results = data.get("results", [])

                if not results:
                    logger.info("  No more results")
                    break

                all_awards.extend(results)
                logger.info(f"    Got {len(results)} awards (total: {len(all_awards):,})")

                # Check if there are more pages
                page_metadata = data.get("page_metadata", {})
                total_pages = page_metadata.get("num_pages", 1)

                if page >= min(total_pages, max_pages):
                    logger.info(f"  Reached page limit ({min(total_pages, max_pages)} pages)")
                    break

                page += 1
                time.sleep(0.5)  # Rate limiting

            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching page {page}: {e}")
                if page == 1:
                    raise  # Fail if we can't get even the first page
                break

        logger.info(f"✓ Fetched {len(all_awards):,} detailed awards")
        return all_awards


def aggregate_by_naics(data: Dict) -> Dict[str, float]:
    """
    Aggregate spending by NAICS code from API results

    Returns dict mapping NAICS code -> total obligated amount
    """
    logger.info("Aggregating spending by NAICS code...")

    naics_spending = {}

    for item in data.get("results", []):
        naics = item.get("code", "").strip()
        amount = item.get("amount", 0)

        if naics and amount > 0:
            naics_spending[naics] = naics_spending.get(naics, 0) + amount

    # Sort by spending (descending)
    naics_spending = dict(sorted(
        naics_spending.items(),
        key=lambda x: x[1],
        reverse=True
    ))

    total = sum(naics_spending.values())
    logger.info(f"✓ Aggregated into {len(naics_spending)} NAICS codes")
    logger.info(f"  Total spending: ${total:,.2f}")

    return naics_spending


def save_data(data: Dict, output_dir: Path, filename: str):
    """Save fetched data to JSON file"""
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / filename

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"✓ Saved to {output_file}")


def main():
    """Main execution"""
    print("="*80)
    print("  FETCHING FULL FY2024 DOD BUDGET FROM USASPENDING.GOV")
    print("="*80 + "\n")

    fetcher = USAspendingFullFetcher()
    output_dir = Path("dod_budget_data")

    # Method 1: Aggregated spending by NAICS (fast, complete)
    print("\n[1/3] Fetching aggregated spending by NAICS code...")
    print("      This provides complete budget coverage efficiently\n")

    try:
        aggregated_data = fetcher.fetch_spending_by_agency(
            fiscal_year=2024,
            agency_name="Department of Defense",
            limit=500  # Should cover all NAICS codes
        )

        # Save raw data
        save_data(aggregated_data, output_dir, "fy2024_dod_by_naics.json")

        # Aggregate by NAICS
        naics_spending = aggregate_by_naics(aggregated_data)

        # Save aggregated spending
        aggregated_output = {
            "metadata": aggregated_data["metadata"],
            "spending_by_naics": naics_spending,
            "summary": {
                "total_spending": sum(naics_spending.values()),
                "num_naics_codes": len(naics_spending),
                "top_10_naics": list(naics_spending.items())[:10]
            }
        }
        save_data(aggregated_output, output_dir, "fy2024_dod_aggregated.json")

        # Print summary
        print("\n" + "="*80)
        print("  SUMMARY - FY2024 DOD SPENDING")
        print("="*80)
        total = aggregated_output["summary"]["total_spending"]
        print(f"\nTotal Spending: ${total:,.2f}")
        print(f"NAICS Categories: {len(naics_spending)}")
        print("\nTop 10 Sectors:")
        for i, (naics, amount) in enumerate(naics_spending.items()[:10], 1):
            pct = (amount / total) * 100
            print(f"  {i:2d}. {naics}: ${amount:>15,.2f} ({pct:5.2f}%)")

    except Exception as e:
        logger.error(f"Failed to fetch aggregated data: {e}")
        logger.info("You may need to run this script from a different network")
        print("\n⚠️  API fetch failed - this may be due to network restrictions")
        print("    The case study uses sample data instead")
        return False

    # Method 2: Detailed awards (optional - slower but has line items)
    print("\n\n[2/3] Fetching detailed award data (optional)...")
    print("      This provides line-by-line contract details for inspection\n")

    fetch_detailed = input("Fetch detailed awards? This may take 5-10 minutes (y/N): ").lower().strip()

    if fetch_detailed == 'y':
        try:
            detailed_awards = fetcher.fetch_detailed_awards(
                fiscal_year=2024,
                limit=1000  # 1000 per page
            )

            # Save detailed data
            detailed_output = {
                "metadata": {
                    "fiscal_year": 2024,
                    "agency": "Department of Defense",
                    "num_awards": len(detailed_awards),
                    "fetch_date": datetime.now().isoformat()
                },
                "awards": detailed_awards
            }
            save_data(detailed_output, output_dir, "fy2024_dod_detailed_awards.json")

        except Exception as e:
            logger.error(f"Failed to fetch detailed awards: {e}")
    else:
        print("  Skipped detailed awards fetch")

    print("\n\n[3/3] Data fetch complete!")
    print("\n" + "="*80)
    print("  OUTPUTS")
    print("="*80)
    print(f"\n  {output_dir}/fy2024_dod_by_naics.json")
    print(f"  {output_dir}/fy2024_dod_aggregated.json")
    print(f"  {output_dir}/fy2024_dod_detailed_awards.json (if fetched)")
    print("\nNext step: Run analyze_full_dod_budget.py to calculate environmental impacts")
    print()

    return True


if __name__ == '__main__':
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nFetch interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1)
