"""
Improve Defense Sector Identification

This script properly identifies and tags defense-relevant sectors
based on comprehensive NAICS codes and sector name keywords.
"""

import json
from pathlib import Path

OUTPUT_DIR = Path("backend/app/data")

# Load current sectors
with open(OUTPUT_DIR / "sectors_full.json") as f:
    sectors = json.load(f)

print("=" * 70)
print("  IMPROVING DEFENSE SECTOR IDENTIFICATION")
print("=" * 70)
print(f"\nTotal sectors: {len(sectors)}")

# Comprehensive list of defense-relevant NAICS codes
DEFENSE_NAICS = {
    # Aircraft and Aerospace
    '336411': 'Aircraft Manufacturing',
    '336412': 'Aircraft Engine and Engine Parts Manufacturing',
    '336413': 'Other Aircraft Parts and Auxiliary Equipment Manufacturing',
    '336414': 'Guided Missile and Space Vehicle Manufacturing',
    '336415': 'Guided Missile and Space Vehicle Propulsion Unit and Parts',
    '336419': 'Other Guided Missile and Space Vehicle Parts',
    '33641A': 'Aircraft and parts (aggregated)',
    '33641B': 'Guided missiles and parts (aggregated)',

    # Ships and Marine
    '336611': 'Ship Building and Repairing',
    '336612': 'Boat Building',
    '3366': 'Ship and boat building (aggregated)',

    # Military Vehicles
    '336992': 'Military Armored Vehicle, Tank, and Tank Component Manufacturing',
    '336120': 'Heavy Duty Truck Manufacturing',  # Used for military trucks

    # Weapons and Ammunition
    '332993': 'Ammunition (except Small Arms) Manufacturing',
    '332994': 'Small Arms Ammunition Manufacturing',
    '33299A': 'Ammunition, arms, ordnance and accessories (aggregated)',
    '332995': 'Other Ordnance and Accessories Manufacturing',

    # Tanks and Metal Products
    '332420': 'Metal Tank (Heavy Gauge) Manufacturing',

    # Electronics and Communications
    '334220': 'Radio and Television Broadcasting and Wireless Communications Equipment',
    '334290': 'Other Communications Equipment Manufacturing',
    '334511': 'Search, Detection, Navigation, Guidance, Aeronautical Systems',
    '334519': 'Other Measuring and Controlling Device Manufacturing',
    '334413': 'Semiconductor and Related Device Manufacturing',
    '334418': 'Printed Circuit Assembly Manufacturing',
    '334510': 'Electromedical and Electrotherapeutic Apparatus',

    # Engineering and R&D Services
    '541330': 'Engineering Services',
    '541380': 'Testing Laboratories',
    '541512': 'Computer Systems Design Services',
    '541513': 'Computer Facilities Management Services',
    '541519': 'Other Computer Related Services',
    '541690': 'Other Scientific and Technical Consulting Services',
    '541715': 'Research and Development in the Physical, Engineering, and Life Sciences',
    '541720': 'Research and Development in the Social Sciences and Humanities',

    # Construction
    '237310': 'Highway, Street, and Bridge Construction',
    '237990': 'Other Heavy and Civil Engineering Construction',
    '236220': 'Commercial and Institutional Building Construction',
    '238': 'Specialty Trade Contractors (aggregated)',

    # Management and Support Services
    '541611': 'Administrative Management and General Management Consulting Services',
    '541612': 'Human Resources Consulting Services',
    '541613': 'Marketing Consulting Services',
    '541614': 'Process, Physical Distribution, and Logistics Consulting Services',
    '541618': 'Other Management Consulting Services',
    '541610': 'Management Consulting Services (aggregated)',
    '561210': 'Facilities Support Services',
    '561499': 'All Other Business Support Services',
    '561110': 'Office Administrative Services',
    '561320': 'Temporary Help Services',
    '561330': 'Professional Employer Organizations',

    # Accommodation and Food Services (for military bases)
    '721': 'Accommodation (aggregated)',
    '721110': 'Hotels (except Casino Hotels) and Motels',
    '721120': 'Casino Hotels',
    '721191': 'Bed-and-Breakfast Inns',
    '721199': 'All Other Traveler Accommodation',
    '722': 'Food Services and Drinking Places (aggregated)',

    # Energy and Fuel
    '324110': 'Petroleum Refineries',  # Jet fuel, diesel
    '221100': 'Electric Power Generation',  # For military installations

    # Transportation
    '481000': 'Air Transportation',
    '482000': 'Rail Transportation',
    '483000': 'Water Transportation',
    '484000': 'Truck Transportation',

    # Information and Data Services
    '518210': 'Data Processing, Hosting, and Related Services',
    '541511': 'Custom Computer Programming Services',

    # Wholesale Trade (military equipment)
    '423': 'Merchant Wholesalers, Durable Goods (aggregated)',
}

# Defense-related keywords for name matching
DEFENSE_KEYWORDS = [
    'aircraft', 'airplane', 'aviation', 'aerospace',
    'missile', 'rocket', 'space vehicle',
    'ship', 'vessel', 'boat', 'naval', 'marine', 'maritime',
    'ammunition', 'arms', 'ordnance', 'weapon', 'gun', 'firearm',
    'military', 'defense', 'armored', 'armor', 'tank',
    'radar', 'navigation', 'guidance', 'detection',
    'combat', 'tactical', 'strategic',
    'ballistic', 'munition'
]

# Secondary keywords (require additional context)
SECONDARY_KEYWORDS = [
    'engineering', 'research', 'development', 'consulting',
    'computer systems', 'technical', 'facilities support'
]

# Tag defense-relevant sectors
defense_count = 0
newly_tagged = []

for sector in sectors:
    code = sector['code']
    name = sector['name'].lower()
    was_defense = sector['is_defense_relevant']

    # Check by NAICS code (partial matching for aggregated codes)
    is_defense = False

    # Exact match
    if code in DEFENSE_NAICS:
        is_defense = True

    # Partial match (e.g., '33641A' matches '336411', '336412', etc.)
    for defense_code in DEFENSE_NAICS:
        if code.startswith(defense_code[:5]) or defense_code.startswith(code[:5]):
            if len(code) >= 5 and len(defense_code) >= 5:
                is_defense = True
                break

    # Check by primary keywords in name
    if not is_defense:
        for keyword in DEFENSE_KEYWORDS:
            if keyword in name:
                is_defense = True
                break

    # Check by secondary keywords (need specific industry context)
    if not is_defense:
        for keyword in SECONDARY_KEYWORDS:
            if keyword in name:
                # Only tag if it's in relevant industries
                if code.startswith('54'):  # Professional services
                    is_defense = True
                    break
                elif code.startswith('56'):  # Support services
                    is_defense = True
                    break

    # Update sector
    sector['is_defense_relevant'] = is_defense

    if is_defense:
        defense_count += 1
        if not was_defense:
            newly_tagged.append((code, sector['name']))

print(f"\n{'=' * 70}")
print(f"RESULTS")
print(f"{'=' * 70}\n")

print(f"Defense-relevant sectors: {defense_count} (was 1)")
print(f"Newly tagged: {len(newly_tagged)}")

if newly_tagged:
    print(f"\nNewly identified defense sectors:")
    for code, name in sorted(newly_tagged)[:30]:
        print(f"  {code:8s} {name}")
    if len(newly_tagged) > 30:
        print(f"  ... and {len(newly_tagged) - 30} more")

# Save updated sectors
with open(OUTPUT_DIR / "sectors_full.json", 'w') as f:
    json.dump(sectors, f, indent=2)
print(f"\n✓ Updated: {OUTPUT_DIR / 'sectors_full.json'}")

# Save defense sectors separately
defense_sectors = [s for s in sectors if s['is_defense_relevant']]
with open(OUTPUT_DIR / "sectors_defense.json", 'w') as f:
    json.dump(defense_sectors, f, indent=2)
print(f"✓ Updated: {OUTPUT_DIR / 'sectors_defense.json'}")

# Show categorized breakdown
print(f"\nDefense sectors by category:")

categories = {
    'Manufacturing - Aircraft/Aerospace': [s for s in defense_sectors if s['code'].startswith('3364')],
    'Manufacturing - Ships/Marine': [s for s in defense_sectors if s['code'].startswith('3366')],
    'Manufacturing - Weapons/Ammunition': [s for s in defense_sectors if '332' in s['code'] and 'ammun' in s['name'].lower()],
    'Manufacturing - Electronics': [s for s in defense_sectors if s['code'].startswith('3344') or s['code'].startswith('3345')],
    'Services - Engineering/R&D': [s for s in defense_sectors if s['code'].startswith('5413') or s['code'].startswith('5417')],
    'Services - IT/Computing': [s for s in defense_sectors if s['code'].startswith('5415')],
    'Services - Management/Support': [s for s in defense_sectors if s['code'].startswith('5416') or s['code'].startswith('561')],
    'Construction': [s for s in defense_sectors if s['code'].startswith('23')],
    'Other': [s for s in defense_sectors if not any(s['code'].startswith(p) for p in ['3364', '3366', '332', '334', '541', '561', '23'])]
}

for category, items in categories.items():
    if items:
        print(f"\n  {category}: {len(items)}")
        for item in items[:5]:
            print(f"    {item['code']:8s} {item['name'][:55]}")
        if len(items) > 5:
            print(f"    ... and {len(items) - 5} more")

print(f"\n{'=' * 70}")
print(f"✓ Defense sector identification improved!")
print(f"  {len(defense_sectors)} sectors now properly tagged")
print(f"{'=' * 70}\n")
