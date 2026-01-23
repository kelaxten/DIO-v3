// Type definitions for Open DIO

export interface Sector {
  code: string;
  name: string;
  description: string;
  category: string;
  naics: string;
}

export interface ImpactMultipliers {
  GHG: number;      // kg CO2 eq per $1000
  Energy: number;   // MJ per $1000
  Water: number;    // gallons per $1000
  Land: number;     // m2-year per $1000
}

export interface SectorMultipliers {
  [sectorCode: string]: ImpactMultipliers & { name: string };
}

export interface MultiplierData {
  description: string;
  units: {
    GHG: string;
    Energy: string;
    Water: string;
    Land: string;
  };
  sectors: SectorMultipliers;
  metadata: {
    model: string;
    base_year: number;
    data_sources: string;
    validation: string;
    note: string;
  };
}

export interface SectorInput {
  sectorCode: string;
  sectorName: string;
  amount: number;  // dollars
}

export interface ImpactResult {
  category: string;
  value: number;
  unit: string;
  description: string;
}

export interface CalculationResult {
  totalSpending: number;
  impacts: ImpactResult[];
  sectorBreakdown: {
    [sectorCode: string]: {
      name: string;
      spending: number;
      impacts: ImpactResult[];
    };
  };
}
