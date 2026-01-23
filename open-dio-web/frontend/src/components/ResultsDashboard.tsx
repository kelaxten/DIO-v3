import type { CalculationResult } from '../types';
import type { DIOCalculator } from '../utils/calculator';
import './ResultsDashboard.css';

interface Props {
  results: CalculationResult;
  calculator: DIOCalculator;
}

export function ResultsDashboard({ results, calculator }: Props) {
  // Get GHG value for comparisons
  const ghgImpact = results.impacts.find((i) => i.category === 'Greenhouse Gas Emissions');
  const comparisons = ghgImpact ? calculator.getComparisons(ghgImpact.value) : [];

  const getImpactIcon = (category: string): string => {
    if (category.includes('Greenhouse')) return '🌡️';
    if (category.includes('Energy')) return '⚡';
    if (category.includes('Water')) return '💧';
    if (category.includes('Land')) return '🌍';
    return '📊';
  };

  const getImpactColor = (category: string): string => {
    if (category.includes('Greenhouse')) return 'impact-ghg';
    if (category.includes('Energy')) return 'impact-energy';
    if (category.includes('Water')) return 'impact-water';
    if (category.includes('Land')) return 'impact-land';
    return 'impact-default';
  };

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
        {results.impacts.map((impact, index) => (
          <div key={index} className={`impact-card ${getImpactColor(impact.category)}`}>
            <div className="impact-header">
              <span className="impact-icon">{getImpactIcon(impact.category)}</span>
              <h3>{impact.category}</h3>
            </div>
            <div className="impact-value">
              {calculator.formatNumber(impact.value)}
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
                {data.impacts.map((impact, idx) => (
                  <div key={idx} className="sector-impact-row">
                    <span className="impact-label">{impact.category}:</span>
                    <span className="impact-value-small">
                      {calculator.formatNumber(impact.value)} {impact.unit}
                    </span>
                  </div>
                ))}
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
