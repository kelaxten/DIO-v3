/**
 * Open DIO API Client
 *
 * Communicates with the Python FastAPI backend
 */

import type { SectorInput, CalculationResult, Sector } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface CalculateRequest {
  sectors: Array<{ code: string; amount: number }>;
  impact_categories: string[];
}

export interface CalculateResponse {
  total_spending: number;
  impacts: Array<{
    category: string;
    value: number;
    unit: string;
    description: string;
  }>;
  sector_breakdown: {
    [code: string]: {
      name: string;
      spending: number;
      impacts: Array<{
        category: string;
        value: number;
        unit: string;
        description: string;
      }>;
    };
  };
  model_version: string;
}

export interface SectorsResponse {
  sectors: Array<{
    code: string;
    name: string;
    is_defense_relevant: boolean;
  }>;
  total: number;
}

class DIOApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get list of available sectors
   */
  async getSectors(defenseOnly: boolean = false, query?: string): Promise<Sector[]> {
    const params = new URLSearchParams();
    if (defenseOnly) params.append('defense_only', 'true');
    if (query) params.append('query', query);

    const url = `${this.baseUrl}/api/v1/sectors/?${params.toString()}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Failed to fetch sectors: ${response.statusText}`);
    }

    const data: SectorsResponse = await response.json();
    return data.sectors.map(s => ({
      code: s.code,
      name: s.name,
      isDefenseRelevant: s.is_defense_relevant
    }));
  }

  /**
   * Calculate environmental impacts
   */
  async calculate(inputs: SectorInput[]): Promise<CalculationResult> {
    const request: CalculateRequest = {
      sectors: inputs.map(input => ({
        code: input.sectorCode,
        amount: input.amount
      })),
      impact_categories: ['GHG', 'Energy', 'Water', 'Land']
    };

    const url = `${this.baseUrl}/api/v1/calculate/`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Calculation failed: ${error}`);
    }

    const data: CalculateResponse = await response.json();

    // Transform to frontend format
    const impactMap: { [key: string]: number } = {};
    data.impacts.forEach(impact => {
      // Extract short name from category
      if (impact.category.includes('Greenhouse Gas')) {
        impactMap.GHG = impact.value;
      } else if (impact.category.includes('Energy')) {
        impactMap.Energy = impact.value;
      } else if (impact.category.includes('Water')) {
        impactMap.Water = impact.value;
      } else if (impact.category.includes('Land')) {
        impactMap.Land = impact.value;
      }
    });

    const sectorBreakdown: { [code: string]: any } = {};
    Object.entries(data.sector_breakdown).forEach(([code, sector]) => {
      const sectorImpacts: { [key: string]: number } = {};
      sector.impacts.forEach(impact => {
        if (impact.category.includes('Greenhouse Gas')) {
          sectorImpacts.GHG = impact.value;
        } else if (impact.category.includes('Energy')) {
          sectorImpacts.Energy = impact.value;
        } else if (impact.category.includes('Water')) {
          sectorImpacts.Water = impact.value;
        } else if (impact.category.includes('Land')) {
          sectorImpacts.Land = impact.value;
        }
      });

      sectorBreakdown[code] = {
        name: sector.name,
        spending: sector.spending,
        impacts: sectorImpacts
      };
    });

    return {
      totalSpending: data.total_spending,
      impacts: impactMap,
      sectorBreakdown
    };
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; version: string; model: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }
}

export const apiClient = new DIOApiClient();
