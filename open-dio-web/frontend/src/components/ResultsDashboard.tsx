import type { CalculationResult } from '../types';
import { getGHGComparisons, formatNumber } from '../utils/comparisons';
import './ResultsDashboard.css';

interface Props {
  results: CalculationResult;
}

interface ImpactDisplay {
  key: string;
  category: string;
  value: number;
  unit: string;
  description: string;
}

interface SectorImpact {
  code: string;
  name: string;
  spending: number;
  ghg: number;
  energy: number;
  percentage: number;
}

export function ResultsDashboard({ results }: Props) {
  // Get GHG value for comparisons
  const ghgValue = results.impacts.GHG || 0;
  const comparisons = getGHGComparisons(ghgValue);

  // CSV Export Function
  const exportToCSV = () => {
    const rows: string[] = [];

    // Header
    rows.push('DIO Environmental Impact Analysis Results');
    rows.push(`Generated: ${new Date().toISOString()}`);
    rows.push(`Total Spending: $${results.totalSpending.toLocaleString()}`);
    rows.push('');

    // Summary
    rows.push('Impact Category,Value,Unit');
    rows.push(`Greenhouse Gas Emissions,${results.impacts.GHG},kg CO2 eq`);
    rows.push(`Energy Use,${results.impacts.Energy},MJ`);
    rows.push(`Water Consumption,${results.impacts.Water},gallons`);
    rows.push(`Land Use,${results.impacts.Land},m2-year`);
    rows.push('');

    // Sector Breakdown
    rows.push('Sector Breakdown');
    rows.push('Sector Code,Sector Name,Spending (USD),GHG (kg CO2 eq),Energy (MJ),Water (gallons),Land (m2-year)');

    Object.entries(results.sectorBreakdown).forEach(([code, data]) => {
      const ghg = data.impacts.GHG !== undefined ? data.impacts.GHG : 0;
      const energy = data.impacts.Energy !== undefined ? data.impacts.Energy : 0;
      const water = data.impacts.Water !== undefined ? data.impacts.Water : 0;
      const land = data.impacts.Land !== undefined ? data.impacts.Land : 0;

      rows.push(`${code},"${data.name}",${data.spending},${ghg},${energy},${water},${land}`);
    });

    rows.push('');
    rows.push('Data Source: Open DIO (Defense Input-Output Model v2.0)');
    rows.push('Methodology: BEA Input-Output Tables 2017, Cornerstone v1.4.0, EIA MECS 2018');
    rows.push('For more information: https://github.com/kelaxten/DIO-v3');

    const csvContent = rows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dio_results_${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  // Prepare sector data for visualization
  const sectorData: SectorImpact[] = Object.entries(results.sectorBreakdown)
    .map(([code, data]) => ({
      code,
      name: data.name,
      spending: data.spending,
      ghg: data.impacts.GHG || 0,
      energy: data.impacts.Energy || 0,
      percentage: (data.spending / results.totalSpending) * 100
    }))
    .sort((a, b) => b.spending - a.spending);

  // Top 10 sectors for visualization
  const topSectors = sectorData.slice(0, 10);
  const maxSpending = topSectors[0]?.spending || 1;

  // Transform impacts object into array for rendering
  const impactsDisplay: ImpactDisplay[] = [
    {
      key: 'GHG',
      category: 'Greenhouse Gas Emissions',
      value: results.impacts.GHG || 0,
      unit: 'kg CO2 eq',
      description: 'Total CO2 equivalent emissions'
    },
    {
      key: 'Energy',
      category: 'Energy Use',
      value: results.impacts.Energy || 0,
      unit: 'MJ',
      description: 'Total energy consumption'
    },
    {
      key: 'Water',
      category: 'Water Consumption',
      value: results.impacts.Water || 0,
      unit: 'gallons',
      description: 'Total freshwater use'
    },
    {
      key: 'Land',
      category: 'Land Use',
      value: results.impacts.Land || 0,
      unit: 'm2-year',
      description: 'Total land occupation'
    }
  ];

  return (
    <div className="results-dashboard">
      <div className="results-header">
        <h2>Environmental Impact Results</h2>
        <button onClick={exportToCSV} className="btn-export" title="Export results as CSV">
          📊 Export CSV
        </button>
      </div>

      <div className="data-quality-notice">
        <div className="notice-icon">⚠️</div>
        <div className="notice-content">
          <strong>Data Quality Notice:</strong> These estimates are based on sector-averaged environmental
          multipliers with uncertainty ranges of ±25-50% depending on impact category.
          Results are suitable for order-of-magnitude estimates and comparative analysis.
          See <strong>Methodology</strong> tab for details.
        </div>
      </div>

      <div className="results-summary">
        <div className="summary-card">
          <div className="summary-label">Total Spending Analyzed</div>
          <div className="summary-value">
            ${results.totalSpending.toLocaleString()}
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Sectors Analyzed</div>
          <div className="summary-value">
            {Object.keys(results.sectorBreakdown).length}
          </div>
        </div>
      </div>

      <div className="impacts-grid">
        {impactsDisplay.map((impact) => (
          <div key={impact.key} className="impact-card">
            <div className="impact-header">
              <h3>{impact.category}</h3>
            </div>
            <div className="impact-value">
              {formatNumber(impact.value)}
            </div>
            <div className="impact-unit">{impact.unit}</div>
            <div className="impact-description">{impact.description}</div>
          </div>
        ))}
      </div>

      {comparisons.length > 0 && (
        <div className="comparisons-section">
          <h3>Context</h3>
          <p className="comparisons-intro">
            To help understand the scale of these emissions:
          </p>
          <ul className="comparisons-list">
            {comparisons.map((comparison, index) => (
              <li key={index}>{comparison}</li>
            ))}
          </ul>
        </div>
      )}

      {topSectors.length > 0 && (
        <div className="visualization-section">
          <h3>Top Sectors by Spending</h3>
          <p className="chart-description">
            This chart shows the sectors with the highest spending amounts in your analysis.
          </p>
          <div className="bar-chart">
            {topSectors.map((sector) => (
              <div key={sector.code} className="bar-chart-row">
                <div className="bar-label">
                  <span className="bar-label-name" title={sector.name}>
                    {sector.name.length > 35 ? sector.name.substring(0, 35) + '...' : sector.name}
                  </span>
                  <span className="bar-label-value">
                    ${(sector.spending / 1e9).toFixed(1)}B
                  </span>
                </div>
                <div className="bar-container">
                  <div
                    className="bar-fill"
                    style={{ width: `${(sector.spending / maxSpending) * 100}%` }}
                    title={`${sector.percentage.toFixed(1)}% of total spending`}
                  >
                    <span className="bar-percentage">
                      {sector.percentage >= 5 ? `${sector.percentage.toFixed(1)}%` : ''}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          {sectorData.length > 10 && (
            <p className="chart-note">
              Showing top 10 of {sectorData.length} sectors. See full breakdown below.
            </p>
          )}
        </div>
      )}

      <div className="sector-breakdown-section">
        <h3>Breakdown by Sector</h3>
        <div className="sector-breakdown-list">
          {Object.entries(results.sectorBreakdown).map(([code, data]) => (
            <details key={code} className="sector-detail">
              <summary className="sector-summary">
                <span className="sector-name">{data.name}</span>
                <span className="sector-spending">
                  ${data.spending.toLocaleString()}
                </span>
              </summary>
              <div className="sector-impacts">
                {data.impacts.GHG !== undefined && (
                  <div className="sector-impact-row">
                    <span className="impact-label">GHG Emissions:</span>
                    <span className="impact-value-small">
                      {formatNumber(data.impacts.GHG)} kg CO2 eq
                    </span>
                  </div>
                )}
                {data.impacts.Energy !== undefined && (
                  <div className="sector-impact-row">
                    <span className="impact-label">Energy Use:</span>
                    <span className="impact-value-small">
                      {formatNumber(data.impacts.Energy)} MJ
                    </span>
                  </div>
                )}
                {data.impacts.Water !== undefined && (
                  <div className="sector-impact-row">
                    <span className="impact-label">Water Use:</span>
                    <span className="impact-value-small">
                      {formatNumber(data.impacts.Water)} gallons
                    </span>
                  </div>
                )}
                {data.impacts.Land !== undefined && (
                  <div className="sector-impact-row">
                    <span className="impact-label">Land Use:</span>
                    <span className="impact-value-small">
                      {formatNumber(data.impacts.Land)} m2-year
                    </span>
                  </div>
                )}
              </div>
            </details>
          ))}
        </div>
      </div>

      <div className="methodology-note">
        <h4>Methodology</h4>
        <p>
          These results are calculated using the <strong>Defense Input-Output (DIO) Model v2.0</strong>
          from the U.S. EPA. The model uses Environmentally-Extended Input-Output (EEIO) analysis
          to trace the direct and indirect environmental impacts throughout the supply chain.
        </p>
        <p>
          <strong>Data Sources:</strong> BEA Input-Output Tables (2017),
          Cornerstone Supply Chain Factors v1.4.0 (GHG),
          EIA Manufacturing Energy Consumption Survey 2018 (Energy),
          EPA USEEIO v2.0 (Water, Land)
        </p>
      </div>
    </div>
  );
}
