import React, { useState, useMemo } from 'react';
import './BudgetAnalysis.css';

interface BudgetDataRow {
  NAICS_Code: string;
  BEA_Sector_Code: string;
  BEA_Sector_Name: string;
  Spending_USD: number;
  Pct_of_Total: number;
  GHG_kg_CO2e: number;
  Energy_MJ: number;
  Water_gallons: number;
  Land_m2_year: number;
  GHG_Intensity_kg_per_1000USD: number;
  Energy_Intensity_MJ_per_1000USD: number;
}

interface BudgetSummary {
  total_spending: number;
  total_ghg: number;
  total_energy: number;
  total_water: number;
  total_land: number;
  num_sectors: number;
  fiscal_year: number;
}

const BudgetAnalysis: React.FC = () => {
  const [data, setData] = useState<BudgetDataRow[]>([]);
  const [summary, setSummary] = useState<BudgetSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [sortColumn, setSortColumn] = useState<keyof BudgetDataRow>('GHG_kg_CO2e');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [filterText, setFilterText] = useState('');
  const [selectedImpact, setSelectedImpact] = useState<'GHG' | 'Energy' | 'Water' | 'Land'>('GHG');

  // Load data on mount
  React.useEffect(() => {
    loadBudgetData();
  }, []);

  const loadBudgetData = async () => {
    try {
      // Try to load published dataset
      const response = await fetch('/data/fy2024_dod_budget_analysis.json');
      const jsonData = await response.json();

      setData(jsonData.line_by_line || []);
      setSummary(jsonData.summary || null);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load budget data:', error);
      setLoading(false);
    }
  };

  // Filter and sort data
  const filteredAndSortedData = useMemo(() => {
    let filtered = data;

    // Apply filter
    if (filterText) {
      const lowerFilter = filterText.toLowerCase();
      filtered = data.filter(row =>
        row.BEA_Sector_Name.toLowerCase().includes(lowerFilter) ||
        row.NAICS_Code.includes(filterText) ||
        row.BEA_Sector_Code.includes(filterText)
      );
    }

    // Apply sort
    const sorted = [...filtered].sort((a, b) => {
      const aVal = a[sortColumn];
      const bVal = b[sortColumn];

      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
      }

      return sortDirection === 'asc'
        ? String(aVal).localeCompare(String(bVal))
        : String(bVal).localeCompare(String(aVal));
    });

    return sorted;
  }, [data, filterText, sortColumn, sortDirection]);

  const handleSort = (column: keyof BudgetDataRow) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('desc');
    }
  };

  const formatNumber = (num: number, decimals: number = 0): string => {
    return num.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  const formatCurrency = (num: number): string => {
    if (num >= 1e9) {
      return `$${(num / 1e9).toFixed(2)}B`;
    } else if (num >= 1e6) {
      return `$${(num / 1e6).toFixed(2)}M`;
    }
    return `$${formatNumber(num, 0)}`;
  };

  const formatLargeNumber = (num: number, unit: string): string => {
    if (num >= 1e9) {
      return `${(num / 1e9).toFixed(2)}B ${unit}`;
    } else if (num >= 1e6) {
      return `${(num / 1e6).toFixed(2)}M ${unit}`;
    } else if (num >= 1e3) {
      return `${(num / 1e3).toFixed(2)}K ${unit}`;
    }
    return `${formatNumber(num, 0)} ${unit}`;
  };

  if (loading) {
    return (
      <div className="budget-analysis">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading FY2024 DOD Budget Analysis...</p>
        </div>
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="budget-analysis">
        <div className="error">
          <h2>No Data Available</h2>
          <p>The FY2024 DOD budget analysis dataset has not been published yet.</p>
          <p>Check back soon for the complete line-by-line environmental impact analysis.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="budget-analysis">
      <div className="budget-header">
        <h1>FY2024 DOD Budget Environmental Impact Analysis</h1>
        <p className="subtitle">
          Complete line-by-line environmental impact calculations for U.S. Department of Defense spending
        </p>
      </div>

      {summary && (
        <div className="budget-summary">
          <div className="summary-card">
            <div className="summary-label">Total Spending</div>
            <div className="summary-value">{formatCurrency(summary.total_spending)}</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">GHG Emissions</div>
            <div className="summary-value">{formatNumber(summary.total_ghg / 1000)} tons CO₂e</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Energy Use</div>
            <div className="summary-value">{formatLargeNumber(summary.total_energy, 'MJ')}</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Water Use</div>
            <div className="summary-value">{formatLargeNumber(summary.total_water, 'gal')}</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Sectors</div>
            <div className="summary-value">{summary.num_sectors}</div>
          </div>
        </div>
      )}

      <div className="budget-controls">
        <div className="control-group">
          <label htmlFor="filter">Filter by sector or code:</label>
          <input
            id="filter"
            type="text"
            placeholder="Search sectors, NAICS, or BEA codes..."
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="filter-input"
          />
        </div>

        <div className="control-group">
          <label htmlFor="impact-select">Highlight Impact:</label>
          <select
            id="impact-select"
            value={selectedImpact}
            onChange={(e) => setSelectedImpact(e.target.value as any)}
            className="impact-select"
          >
            <option value="GHG">GHG Emissions</option>
            <option value="Energy">Energy Use</option>
            <option value="Water">Water Consumption</option>
            <option value="Land">Land Use</option>
          </select>
        </div>

        <div className="results-count">
          Showing {formatNumber(filteredAndSortedData.length)} of {formatNumber(data.length)} sectors
        </div>
      </div>

      <div className="budget-table-container">
        <table className="budget-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('NAICS_Code')} className="sortable">
                NAICS Code {sortColumn === 'NAICS_Code' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('BEA_Sector_Name')} className="sortable">
                Sector Name {sortColumn === 'BEA_Sector_Name' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Spending_USD')} className="sortable number">
                Spending {sortColumn === 'Spending_USD' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Pct_of_Total')} className="sortable number">
                % of Total {sortColumn === 'Pct_of_Total' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('GHG_kg_CO2e')} className="sortable number">
                GHG (tons CO₂e) {sortColumn === 'GHG_kg_CO2e' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Energy_MJ')} className="sortable number">
                Energy (MJ) {sortColumn === 'Energy_MJ' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('Water_gallons')} className="sortable number">
                Water (gal) {sortColumn === 'Water_gallons' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th onClick={() => handleSort('GHG_Intensity_kg_per_1000USD')} className="sortable number">
                GHG Intensity {sortColumn === 'GHG_Intensity_kg_per_1000USD' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((row, idx) => (
              <tr key={idx}>
                <td className="naics-code">{row.NAICS_Code || '—'}</td>
                <td className="sector-name">{row.BEA_Sector_Name}</td>
                <td className="number">{formatCurrency(row.Spending_USD)}</td>
                <td className="number">{row.Pct_of_Total.toFixed(2)}%</td>
                <td className="number">{formatNumber(row.GHG_kg_CO2e / 1000)}</td>
                <td className="number">{formatLargeNumber(row.Energy_MJ, '')}</td>
                <td className="number">{formatLargeNumber(row.Water_gallons, '')}</td>
                <td className="number intensity">{row.GHG_Intensity_kg_per_1000USD.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="budget-footer">
        <div className="methodology-note">
          <h3>Methodology</h3>
          <p>
            This analysis uses the Defense Input-Output (DIO) methodology with environmentally-extended
            input-output life cycle assessment. Calculations include full supply chain impacts (Scope 1, 2, and 3 emissions).
          </p>
          <p>
            <strong>Data Sources:</strong> USAspending.gov (spending), Cornerstone v1.4.0 (GHG),
            EIA MECS 2018 (energy), EPA USEEIO v2.0 (water, land)
          </p>
          <p>
            <strong>GHG Intensity:</strong> kg CO₂e per $1,000 spending (includes supply chain)
          </p>
        </div>

        <div className="download-section">
          <h3>Download Data</h3>
          <a href="/data/fy2024_dod_line_by_line.csv" download className="download-link">
            📥 Download Full Dataset (CSV)
          </a>
          <a href="/data/fy2024_dod_summary.csv" download className="download-link">
            📥 Download Summary (CSV)
          </a>
          <a href="/data/fy2024_dod_full_results.json" download className="download-link">
            📥 Download Complete Results (JSON)
          </a>
        </div>
      </div>
    </div>
  );
};

export default BudgetAnalysis;
