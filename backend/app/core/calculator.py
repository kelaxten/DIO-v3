"""
DIO Calculation Engine

Implements the Defense Input-Output model calculations
using impact multipliers.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ImpactMultipliers:
    """Environmental impact multipliers for a sector"""
    GHG: float  # kg CO2 eq per $1000
    Energy: float  # MJ per $1000
    Water: float  # gallons per $1000
    Land: float  # m2-year per $1000


class DIOCalculator:
    """
    Defense Input-Output calculation engine

    Calculates environmental impacts from defense spending using
    pre-computed impact multipliers.
    """

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize calculator with multiplier data"""
        if data_path is None:
            data_path = Path(__file__).parent.parent / "data"

        self.data_path = data_path
        self.multipliers: Dict[str, ImpactMultipliers] = {}
        self.sector_names: Dict[str, str] = {}
        self.units = {
            'GHG': 'kg CO2 eq',
            'Energy': 'MJ',
            'Water': 'gallons',
            'Land': 'm2-year'
        }

        self._load_multipliers()

    def _load_multipliers(self):
        """Load impact multipliers from JSON file"""
        # Use data_path if provided, otherwise fall back to demo data
        multipliers_file = self.data_path / "multipliers.json"

        if not multipliers_file.exists():
            # Fallback to open-dio-web demo data (for frontend dev)
            multipliers_file = Path("open-dio-web/data/multipliers.json")

        if not multipliers_file.exists():
            raise FileNotFoundError(f"Multipliers file not found: {multipliers_file}")

        with open(multipliers_file, 'r') as f:
            data = json.load(f)

        # Load multipliers
        for code, values in data.get('sectors', {}).items():
            self.multipliers[code] = ImpactMultipliers(
                GHG=values.get('GHG', 0),
                Energy=values.get('Energy', 0),
                Water=values.get('Water', 0),
                Land=values.get('Land', 0)
            )
            self.sector_names[code] = values.get('name', f'Sector {code}')

        # Update units if provided
        if 'units' in data:
            self.units.update(data['units'])

    def calculate(
        self,
        sector_spending: Dict[str, float],
        impact_categories: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate environmental impacts from sector spending

        Args:
            sector_spending: Dict mapping sector codes to dollar amounts
            impact_categories: Optional list of categories to calculate

        Returns:
            Dict with total impacts and sector breakdown
        """
        if impact_categories is None:
            impact_categories = ['GHG', 'Energy', 'Water', 'Land']

        # Calculate total spending
        total_spending = sum(sector_spending.values())

        # Calculate impacts for each sector
        sector_breakdown = {}
        total_impacts = {cat: 0.0 for cat in impact_categories}

        for sector_code, amount in sector_spending.items():
            if sector_code not in self.multipliers:
                # Skip unknown sectors or use default multipliers
                continue

            multipliers = self.multipliers[sector_code]

            # Convert spending to thousands of dollars
            spending_thousands = amount / 1000

            # Calculate impacts
            sector_impacts = {}
            for category in impact_categories:
                multiplier = getattr(multipliers, category, 0)
                impact = multiplier * spending_thousands
                sector_impacts[category] = impact
                total_impacts[category] += impact

            # Store sector breakdown
            sector_breakdown[sector_code] = {
                'name': self.sector_names.get(sector_code, f'Sector {sector_code}'),
                'spending': amount,
                'impacts': [
                    {
                        'category': self._get_category_name(cat),
                        'value': sector_impacts[cat],
                        'unit': self.units[cat],
                        'description': self._get_category_description(cat)
                    }
                    for cat in impact_categories
                ]
            }

        # Format total impacts
        impacts = [
            {
                'category': self._get_category_name(cat),
                'value': total_impacts[cat],
                'unit': self.units[cat],
                'description': self._get_category_description(cat)
            }
            for cat in impact_categories
        ]

        return {
            'total_spending': total_spending,
            'impacts': impacts,
            'sector_breakdown': sector_breakdown,
            'model_version': 'DIO v2.0'
        }

    def _get_category_name(self, code: str) -> str:
        """Get human-readable category name"""
        names = {
            'GHG': 'Greenhouse Gas Emissions',
            'Energy': 'Energy Use',
            'Water': 'Water Consumption',
            'Land': 'Land Use'
        }
        return names.get(code, code)

    def _get_category_description(self, code: str) -> str:
        """Get category description"""
        descriptions = {
            'GHG': 'Total CO2 equivalent emissions',
            'Energy': 'Total energy consumption',
            'Water': 'Total freshwater use',
            'Land': 'Total land occupation'
        }
        return descriptions.get(code, '')

    def get_available_sectors(self) -> List[Dict]:
        """Get list of all available sectors"""
        return [
            {
                'code': code,
                'name': name,
                'is_defense_relevant': self._is_defense_sector(name)
            }
            for code, name in sorted(self.sector_names.items())
        ]

    def _is_defense_sector(self, name: str) -> bool:
        """Check if sector is defense-relevant"""
        defense_keywords = [
            'aircraft', 'ship', 'missile', 'weapon', 'military', 'defense',
            'ordnance', 'armored', 'guided', 'aerospace', 'ammunition'
        ]
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in defense_keywords)


# Singleton instance
_calculator_instance = None


def get_calculator() -> DIOCalculator:
    """Get or create calculator singleton"""
    global _calculator_instance
    if _calculator_instance is None:
        _calculator_instance = DIOCalculator()
    return _calculator_instance
