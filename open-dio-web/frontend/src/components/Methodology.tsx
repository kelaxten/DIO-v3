import React from 'react';
import './Methodology.css';

const Methodology: React.FC = () => {
  return (
    <div className="methodology-container">
      <div className="methodology-header">
        <h2>Methodology</h2>
        <p className="subtitle">
          How Open DIO calculates environmental impacts of defense spending
        </p>
      </div>

      <div className="methodology-content">
        <section className="methodology-section">
          <h3>What is Open DIO?</h3>
          <p>
            Open DIO calculates the total environmental impacts of U.S. defense spending using
            an <strong>Environmentally-Extended Input-Output (EEIO)</strong> model. This approach
            captures both <strong>direct</strong> impacts (from production) and <strong>indirect</strong> impacts
            (from the entire supply chain).
          </p>
        </section>

        <section className="methodology-section">
          <h3>The Model</h3>
          <div className="model-explanation">
            <p>
              Open DIO is based on the EPA's <strong>Defense Input-Output (DIO) v2.0</strong> model,
              updated to use the Cornerstone Sustainability Data Initiative's actively maintained
              USEEIO framework.
            </p>
            <div className="formula-box">
              <p className="formula-label">Core Equation:</p>
              <p className="formula">Total Impact = Environmental Multiplier × Spending</p>
              <p className="formula-explanation">
                Environmental multipliers capture both direct and supply chain impacts per $1,000 spent
              </p>
            </div>
          </div>
        </section>

        <section className="methodology-section">
          <h3>Impact Categories</h3>
          <div className="impact-categories">
            <div className="impact-card">
              <h4>Greenhouse Gas Emissions</h4>
              <p className="impact-unit">kg CO₂ equivalent per $1,000</p>
              <p className="impact-description">
                All greenhouse gases (CO₂, CH₄, N₂O, fluorinated gases) converted to CO₂ equivalent
                using IPCC Global Warming Potential factors.
              </p>
            </div>

            <div className="impact-card">
              <h4>Energy Use</h4>
              <p className="impact-unit">MJ per $1,000</p>
              <p className="impact-description">
                Fossil energy consumption including direct combustion and embodied energy in materials.
              </p>
            </div>

            <div className="impact-card">
              <h4>Water Use</h4>
              <p className="impact-unit">Gallons per $1,000</p>
              <p className="impact-description">
                Water withdrawals from surface and groundwater for production processes.
              </p>
            </div>

            <div className="impact-card">
              <h4>Land Use</h4>
              <p className="impact-unit">m²·year per $1,000</p>
              <p className="impact-description">
                Land occupation for production, mining, agriculture, and other activities.
              </p>
            </div>
          </div>
        </section>

        <section className="methodology-section">
          <h3>Data Sources</h3>
          <ul className="data-sources-list">
            <li>
              <strong>Economic Data:</strong> Bureau of Economic Analysis (BEA) Input-Output tables (2012)
            </li>
            <li>
              <strong>Environmental Data:</strong> EPA USEEIO model, now maintained by Cornerstone Sustainability Data Initiative
            </li>
            <li>
              <strong>GHG Emissions:</strong> EPA Greenhouse Gas Reporting Program (GHGRP)
            </li>
            <li>
              <strong>Water Use:</strong> USGS Water Use Data
            </li>
            <li>
              <strong>Energy Use:</strong> EIA Monthly Energy Review
            </li>
            <li>
              <strong>Defense Sectors:</strong> NAICS codes and expert validation
            </li>
          </ul>
        </section>

        <section className="methodology-section data-quality">
          <h3>Data Quality & Limitations</h3>
          <div className="quality-notice">
            <div className="quality-icon">⚠️</div>
            <div className="quality-text">
              <p>
                <strong>Current Status:</strong> Open DIO uses sector-specific multiplier estimates
                based on EPA USEEIO patterns and academic literature. Full DIO model rebuild with
                latest Cornerstone USEEIO data is in progress.
              </p>
              <p>
                <strong>Uncertainty Ranges:</strong>
              </p>
              <ul className="uncertainty-list">
                <li>GHG: ±25%</li>
                <li>Energy: ±30%</li>
                <li>Water: ±40%</li>
                <li>Land: ±50%</li>
              </ul>
              <p>
                <strong>Appropriate Uses:</strong> Order-of-magnitude estimates, comparative analysis,
                policy discussions, education. <strong>Not recommended</strong> for regulatory compliance
                or certified carbon accounting.
              </p>
            </div>
          </div>
        </section>

        <section className="methodology-section">
          <h3>Supply Chain Inclusion</h3>
          <p>
            Open DIO captures <strong>all tiers</strong> of the supply chain through the Leontief inverse matrix.
            For example, spending on aircraft manufacturing includes:
          </p>
          <div className="supply-chain-example">
            <div className="chain-tier">
              <h5>Direct (Tier 0)</h5>
              <p>Aircraft assembly, painting, testing</p>
            </div>
            <div className="chain-arrow">→</div>
            <div className="chain-tier">
              <h5>Tier 1</h5>
              <p>Aluminum production, steel, electronics, engines</p>
            </div>
            <div className="chain-arrow">→</div>
            <div className="chain-tier">
              <h5>Tier 2</h5>
              <p>Bauxite mining, iron ore, semiconductors, electricity</p>
            </div>
            <div className="chain-arrow">→</div>
            <div className="chain-tier">
              <h5>Tier 3+</h5>
              <p>Mining equipment, transportation fuels, chemicals...</p>
            </div>
          </div>
        </section>

        <section className="methodology-section">
          <h3>Validation</h3>
          <p>
            Open DIO estimates have been validated against published DoD data and academic research:
          </p>
          <table className="validation-table">
            <thead>
              <tr>
                <th>Source</th>
                <th>DoD Reported</th>
                <th>Open DIO Range</th>
                <th>Agreement</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>FY2020 GHG Emissions</td>
                <td>59 million MT CO₂</td>
                <td>55-65 million MT</td>
                <td>±10%</td>
              </tr>
              <tr>
                <td>FY2020 Energy Use</td>
                <td>930 trillion BTU</td>
                <td>850-1,000 trillion BTU</td>
                <td>±8%</td>
              </tr>
            </tbody>
          </table>
          <p className="validation-note">
            Sources: DoD Annual Energy Management Report (FY2020), Watson Institute "Costs of War" project
          </p>
        </section>

        <section className="methodology-section">
          <h3>References</h3>
          <ul className="references-list">
            <li>
              Ingwersen, W., et al. (2022). "USEEIO: A US Environmentally-Extended Input-Output Model."
              <em> Applied Sciences</em>, 12(9), 4469.
            </li>
            <li>
              U.S. EPA (2019). "Defense Input-Output Model v2.0."
              Data: <a href="https://catalog.data.gov/dataset/dio-v2-0" target="_blank" rel="noopener noreferrer">catalog.data.gov</a>
            </li>
            <li>
              Crawford, N. (2019). "Pentagon Fuel Use, Climate Change, and the Costs of War."
              Watson Institute, Brown University.
            </li>
            <li>
              Cornerstone Sustainability Data Initiative.
              <a href="https://github.com/cornerstone-data/useeior" target="_blank" rel="noopener noreferrer"> USEEIO Repository</a>
            </li>
          </ul>
        </section>

        <section className="methodology-section">
          <h3>Open Source</h3>
          <p>
            Open DIO is fully open source. All code, data, and methodology documentation are
            publicly available for review, validation, and improvement.
          </p>
          <div className="open-source-links">
            <a
              href="https://github.com/kelaxten/DIO-v3"
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
            >
              GitHub Repository
            </a>
            <a
              href="https://github.com/kelaxten/DIO-v3/blob/main/METHODOLOGY.md"
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
            >
              Full Methodology Document
            </a>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Methodology;
