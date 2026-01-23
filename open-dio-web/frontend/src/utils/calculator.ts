/**
 * Open DIO Calculation Engine
 *
 * Calculates environmental impacts from defense spending using
 * Input-Output analysis with the DIO model multipliers.
 */

import type {
  SectorInput,
  CalculationResult,
  ImpactResult,
  MultiplierData,
} from '../types';

export class DIOCalculator {
  private multipliers: MultiplierData | null = null;

  async loadMultipliers(): Promise<void> {
    const response = await fetch('/data/multipliers.json');
    this.multipliers = await response.json();
  }

  /**
   * Calculate environmental impacts from sector spending
   *
   * @param inputs Array of sector spending inputs
   * @returns Detailed impact results
   */
  calculate(inputs: SectorInput[]): CalculationResult {
    if (!this.multipliers) {
      throw new Error('Multipliers not loaded. Call loadMultipliers() first.');
    }

    // Calculate total spending
    const totalSpending = inputs.reduce((sum, input) => sum + input.amount, 0);

    // Calculate impacts for each sector
    const sectorBreakdown: CalculationResult['sectorBreakdown'] = {};
    const totalImpacts = {
      GHG: 0,
      Energy: 0,
      Water: 0,
      Land: 0,
    };

    for (const input of inputs) {
      const sectorMultipliers = this.multipliers.sectors[input.sectorCode];

      if (!sectorMultipliers) {
        console.warn(`No multipliers found for sector: ${input.sectorCode}`);
        continue;
      }

      // Convert spending to thousands of dollars (multipliers are per $1000)
      const spendingInThousands = input.amount / 1000;

      // Calculate impacts for this sector
      const ghg = sectorMultipliers.GHG * spendingInThousands;
      const energy = sectorMultipliers.Energy * spendingInThousands;
      const water = sectorMultipliers.Water * spendingInThousands;
      const land = sectorMultipliers.Land * spendingInThousands;

      // Add to totals
      totalImpacts.GHG += ghg;
      totalImpacts.Energy += energy;
      totalImpacts.Water += water;
      totalImpacts.Land += land;

      // Store sector breakdown
      sectorBreakdown[input.sectorCode] = {
        name: input.sectorName,
        spending: input.amount,
        impacts: [
          {
            category: 'Greenhouse Gas Emissions',
            value: ghg,
            unit: this.multipliers.units.GHG,
            description: 'Climate change potential',
          },
          {
            category: 'Energy Use',
            value: energy,
            unit: this.multipliers.units.Energy,
            description: 'Total energy consumed',
          },
          {
            category: 'Water Consumption',
            value: water,
            unit: this.multipliers.units.Water,
            description: 'Freshwater withdrawals',
          },
          {
            category: 'Land Use',
            value: land,
            unit: this.multipliers.units.Land,
            description: 'Land occupation',
          },
        ],
      };
    }

    // Format total impacts
    const impacts: ImpactResult[] = [
      {
        category: 'Greenhouse Gas Emissions',
        value: totalImpacts.GHG,
        unit: this.multipliers.units.GHG,
        description: 'Total CO2 equivalent emissions',
      },
      {
        category: 'Energy Use',
        value: totalImpacts.Energy,
        unit: this.multipliers.units.Energy,
        description: 'Total energy consumption',
      },
      {
        category: 'Water Consumption',
        value: totalImpacts.Water,
        unit: this.multipliers.units.Water,
        description: 'Total freshwater use',
      },
      {
        category: 'Land Use',
        value: totalImpacts.Land,
        unit: this.multipliers.units.Land,
        description: 'Total land occupation',
      },
    ];

    return {
      totalSpending,
      impacts,
      sectorBreakdown,
    };
  }

  /**
   * Get human-readable comparison context for emissions
   */
  getComparisons(ghgKg: number): string[] {
    const comparisons: string[] = [];

    // Convert to metric tons
    const metricTons = ghgKg / 1000;

    // Cars (avg 4.6 MT CO2/year)
    const cars = Math.round(metricTons / 4.6);
    if (cars > 0) {
      comparisons.push(`Equivalent to ${cars.toLocaleString()} cars driven for one year`);
    }

    // Homes (avg 8 MT CO2/year)
    const homes = Math.round(metricTons / 8);
    if (homes > 0) {
      comparisons.push(`Equivalent to ${homes.toLocaleString()} homes' energy use for one year`);
    }

    // Flights NYC-LA (0.9 MT CO2/flight)
    const flights = Math.round(metricTons / 0.9);
    if (flights > 0) {
      comparisons.push(`Equivalent to ${flights.toLocaleString()} one-way flights from NYC to LA`);
    }

    return comparisons;
  }

  /**
   * Format large numbers for display
   */
  formatNumber(value: number): string {
    if (value >= 1_000_000_000) {
      return `${(value / 1_000_000_000).toFixed(2)}B`;
    } else if (value >= 1_000_000) {
      return `${(value / 1_000_000).toFixed(2)}M`;
    } else if (value >= 1_000) {
      return `${(value / 1_000).toFixed(2)}K`;
    } else {
      return value.toFixed(2);
    }
  }
}

// Singleton instance
export const calculator = new DIOCalculator();
