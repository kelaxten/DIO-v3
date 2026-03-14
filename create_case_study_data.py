#!/usr/bin/env python3
"""
Create sample FY2024 DOD spending data for case study

Based on known DOD procurement and O&M patterns from:
- DOD Comptroller Green Book FY2024
- Congressional Budget Office defense spending analysis
- Prior USAspending.gov data patterns

This sample represents major DOD spending categories for methodological demonstration.
"""

import json
import sys
sys.path.insert(0, 'backend')

from pathlib import Path

def create_sample_dod_data():
    """
    Create realistic FY2024 DOD spending sample across major categories.

    Based on FY2024 DOD budget of ~$850B total:
    - Procurement: ~$170B (20%)
    - O&M: ~$320B (38%)
    - RDT&E: ~$145B (17%)
    - Personnel: ~$185B (22%) - excluded (no direct environmental multipliers)
    - Other: ~$30B (3%)

    Sample focuses on procurement and O&M with measurable environmental impacts.
    """

    # Sample represents ~$100B of FY2024 DOD spending
    # Focused on procurement and operations with environmental footprint

    sample_spending = {
        # AIRCRAFT AND AEROSPACE (~$35B)
        "336411": {
            "name": "Aircraft Manufacturing",
            "naics": "336411",
            "amount": 25_000_000_000,  # F-35, F/A-18, KC-46, etc.
            "description": "Combat aircraft, tankers, transport aircraft procurement"
        },
        "336412": {
            "name": "Aircraft Engine and Engine Parts Manufacturing",
            "naics": "336412",
            "amount": 5_000_000_000,
            "description": "Jet engines, propulsion systems"
        },
        "336413": {
            "name": "Other Aircraft Parts and Auxiliary Equipment Manufacturing",
            "naics": "336413",
            "amount": 5_000_000_000,
            "description": "Avionics, weapons systems, aircraft components"
        },

        # SHIPS AND SUBMARINES (~$25B)
        "336611": {
            "name": "Ship Building and Repairing",
            "naics": "336611",
            "amount": 22_000_000_000,  # Columbia-class, DDG-51, Virginia-class
            "description": "Naval vessels, submarines, carriers"
        },
        "333618": {
            "name": "Other Engine Equipment Manufacturing",
            "naics": "333618",
            "amount": 3_000_000_000,
            "description": "Marine propulsion systems"
        },

        # GROUND VEHICLES AND WEAPONS (~$15B)
        "336120": {
            "name": "Heavy Duty Truck Manufacturing",
            "naics": "336120",
            "amount": 4_000_000_000,  # JLTV, tactical trucks
            "description": "Military tactical vehicles"
        },
        "332994": {
            "name": "Small Arms, Ordnance, and Ordnance Accessories Manufacturing",
            "naics": "332994",
            "amount": 8_000_000_000,  # Ammunition, missiles, ordnance
            "description": "Weapons systems, ammunition"
        },
        "336992": {
            "name": "Military Armored Vehicle, Tank, and Tank Component Manufacturing",
            "naics": "336992",
            "amount": 3_000_000_000,  # Armored vehicles
            "description": "Tanks, armored personnel carriers"
        },

        # COMMUNICATIONS AND ELECTRONICS (~$12B)
        "334220": {
            "name": "Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing",
            "naics": "334220",
            "amount": 6_000_000_000,  # Communications systems
            "description": "Military communications equipment"
        },
        "334511": {
            "name": "Search, Detection, and Navigation Instruments Manufacturing",
            "naics": "334511",
            "amount": 6_000_000_000,  # Radar, sonar, guidance systems
            "description": "Radar, navigation systems, sensors"
        },

        # PETROLEUM AND FUEL (~$8B)
        "324110": {
            "name": "Petroleum Refineries",
            "naics": "324110",
            "amount": 8_000_000_000,  # Fuel for operations
            "description": "Jet fuel, diesel, military fuel operations"
        },

        # CONSTRUCTION AND FACILITIES (~$5B)
        "237990": {
            "name": "Other Heavy and Civil Engineering Construction",
            "naics": "237990",
            "amount": 3_000_000_000,  # Base construction, facilities
            "description": "Military base construction and infrastructure"
        },
        "236220": {
            "name": "Commercial and Institutional Building Construction",
            "naics": "236220",
            "amount": 2_000_000_000,
            "description": "Military facilities, barracks, office buildings"
        }
    }

    # Calculate totals
    total_amount = sum(item["amount"] for item in sample_spending.values())

    print("="*80)
    print("  FY2024 DOD SPENDING SAMPLE - CASE STUDY DATASET")
    print("="*80 + "\n")

    print(f"Sample represents: ${total_amount:,}")
    print(f"Categories: {len(sample_spending)} NAICS codes\n")

    print("Major categories:")
    categories = {
        "Aircraft & Aerospace": sum(v["amount"] for k, v in sample_spending.items() if k.startswith("3364")),
        "Ships & Marine": sum(v["amount"] for k, v in sample_spending.items() if k in ["336611", "333618"]),
        "Ground Vehicles & Weapons": sum(v["amount"] for k, v in sample_spending.items() if k in ["336120", "332994", "336992"]),
        "Communications & Electronics": sum(v["amount"] for k, v in sample_spending.items() if k.startswith("3345") or k == "334220"),
        "Petroleum & Fuel": 8_000_000_000,
        "Construction & Facilities": 5_000_000_000
    }

    for cat, amt in categories.items():
        pct = (amt / total_amount) * 100
        print(f"  {cat}: ${amt:,} ({pct:.1f}%)")

    # Save to file
    output_dir = Path("case_study_data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "dod_fy2024_sample.json"

    with open(output_file, 'w') as f:
        json.dump({
            "metadata": {
                "fiscal_year": 2024,
                "agency": "Department of Defense",
                "description": "Sample of FY2024 DOD spending for environmental impact case study",
                "total_amount": total_amount,
                "num_categories": len(sample_spending),
                "data_source": "Based on DOD Green Book FY2024 and procurement patterns",
                "note": "Sample data for methodological demonstration"
            },
            "spending_by_naics": sample_spending
        }, f, indent=2)

    print(f"\n✓ Saved sample data to {output_file}\n")

    return sample_spending, total_amount

if __name__ == '__main__':
    create_sample_dod_data()
