#!/usr/bin/env python3
"""
Quick end-to-end test of DIO calculator

Tests that the calculator can load data and perform calculations correctly.
"""

import sys
sys.path.insert(0, 'backend')

from app.core.calculator import DIOCalculator

def test_calculator():
    print("="*70)
    print("  DIO CALCULATOR END-TO-END TEST")
    print("="*70 + "\n")

    # Initialize calculator
    print("[1/4] Initializing calculator...")
    try:
        calc = DIOCalculator()
        print(f"  ✓ Calculator loaded with {len(calc.multipliers)} sectors\n")
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        return False

    # Test 1: F-35 Program
    print("[2/4] Test 1: F-35 Aircraft Program ($80B)")
    sector_spending = {
        '336411': 80_000_000_000  # Aircraft Manufacturing
    }

    try:
        result = calc.calculate(sector_spending)
        print(f"  Total Spending: ${result['total_spending']:,}")
        print(f"  Impacts:")
        for impact in result['impacts']:
            print(f"    {impact['category']}: {impact['value']:,.0f} {impact['unit']}")
        print("  ✓ F-35 calculation successful\n")
    except Exception as e:
        print(f"  ✗ Calculation failed: {e}\n")
        return False

    # Test 2: Multi-sector (F-35 + Ships)
    print("[3/4] Test 2: Multi-sector (F-35 + Aircraft Carrier)")
    sector_spending = {
        '336411': 80_000_000_000,  # Aircraft Manufacturing
        '336611': 13_000_000_000   # Ship Building
    }

    try:
        result = calc.calculate(sector_spending)
        print(f"  Total Spending: ${result['total_spending']:,}")
        print(f"  Sectors Analyzed: {len(result['sector_breakdown'])}")
        print(f"  Total GHG: {result['impacts'][0]['value']:,.0f} kg CO2 eq")

        # Calculate car equivalents
        ghg_tons = result['impacts'][0]['value'] / 1000
        cars = int(ghg_tons / 4.6)
        print(f"  Equivalent to: {cars:,} cars driven for one year")
        print("  ✓ Multi-sector calculation successful\n")
    except Exception as e:
        print(f"  ✗ Calculation failed: {e}\n")
        return False

    # Test 3: Verify energy multipliers
    print("[4/4] Test 3: Verify energy multipliers are loaded")
    aircraft_mult = calc.multipliers.get('336411')
    if aircraft_mult:
        print(f"  Aircraft Manufacturing (336411):")
        print(f"    GHG: {aircraft_mult.GHG} kg CO2e/$1000")
        print(f"    Energy: {aircraft_mult.Energy} MJ/$1000")
        print(f"    Water: {aircraft_mult.Water} gallons/$1000")
        print(f"    Land: {aircraft_mult.Land} m2-year/$1000")

        if aircraft_mult.Energy > 0:
            print("  ✓ Energy multipliers loaded correctly\n")
        else:
            print("  ✗ Energy multipliers are zero\n")
            return False
    else:
        print("  ✗ Aircraft sector not found\n")
        return False

    print("="*70)
    print("  ALL TESTS PASSED ✓")
    print("="*70 + "\n")

    print("Calculator is ready for production!")
    print("Backend API should return the same results.\n")

    return True

if __name__ == '__main__':
    success = test_calculator()
    sys.exit(0 if success else 1)
