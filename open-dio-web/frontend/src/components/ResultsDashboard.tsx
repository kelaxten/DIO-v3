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
  icon: string;
  color: string;
}

export function ResultsDashboard({ results }: Props) {
  // Get GHG value for comparisons
  const ghgValue = results.impacts.GHG || 0;
  const comparisons = getGHGComparisons(ghgValue);

  // Transform impacts object into array for rendering
  const impactsDisplay: ImpactDisplay[] = [
    {
      key: 'GHG',
      category: 'Greenhouse Gas Emissions',
      value: results.impacts.GHG || 0,
      unit: 'kg CO2 eq',
      description: 'Total CO2 equivalent emissions',
      icon: '🌡️',
      color: 'impact-ghg'
    },
    {
      key: 'Energy',
      category: 'Energy Use',
      value: results.impacts.Energy || 0,
      unit: 'MJ',
      description: 'Total energy consumption',
      icon: '⚡',
      color: 'impact-energy'
    },
    {
      key: 'Water',
      category: 'Water Consumption',
      value: results.impacts.Water || 0,
      unit: 'gallons',
      description: 'Total freshwater use',
      icon: '💧',
      color: 'impact-water'
    },
    {
      key: 'Land',
      category: 'Land Use',
      value: results.impacts.Land || 0,
      unit: 'm2-year',
      description: 'Total land occupation',
      icon: '🌍',
      color: 'impact-land'
    }
  ];

  return (
    <div className="results-dashboard">
      <h2>📈 Environmental Impact Results</h2>

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
          <div key={impact.key} className={`impact-card ${impact.color}`}>
            <div className="impact-header">
              <span className="impact-icon">{impact.icon}</span>
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
          <h3>🔍 Putting It In Context</h3>
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

      <div className="sector-breakdown-section">
        <h3>🏭 Breakdown by Sector</h3>
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
        <h4>📚 Methodology</h4>
        <p>
          These results are calculated using the <strong>Defense Input-Output (DIO) Model v2.0</strong>
          from the U.S. EPA. The model uses Environmentally-Extended Input-Output (EEIO) analysis
          to trace the direct and indirect environmental impacts throughout the supply chain.
        </p>
        <p>
          <strong>Data Sources:</strong> BEA Input-Output Tables (2012), EPA GHG Inventory,
          USGS Water Use Data
        </p>
      </div>
    </div>
  );
}
