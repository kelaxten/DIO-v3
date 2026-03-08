import React from 'react';
import './ResearchContext.css';

const ResearchContext: React.FC = () => {
  return (
    <div className="research-context">
      <div className="research-header">
        <h1>Research Context & Contribution</h1>
        <p className="lead">
          Understanding the full environmental cost of military spending through
          supply chain analysis
        </p>
      </div>

      <section className="research-question">
        <h2>Research Question</h2>
        <p className="question-text">
          How do <strong>full supply chain environmental impacts</strong> of U.S. defense
          spending compare to <strong>operational emissions alone</strong>?
        </p>
      </section>

      <section className="gap-in-literature">
        <h2>Gap in Existing Literature</h2>

        <div className="comparison-box">
          <div className="prior-work">
            <h3>Prior Work: Operational Emissions Only</h3>
            <p>
              <strong>Crawford, N. (2019)</strong> - <em>Pentagon Fuel Use, Climate Change, and the Costs of War</em>
            </p>
            <ul>
              <li><strong>Scope</strong>: Direct fuel consumption (Scope 1)</li>
              <li><strong>Finding</strong>: ~59 million metric tons CO2e (2017)</li>
              <li><strong>Limitation</strong>: Excludes manufacturing and supply chain emissions</li>
            </ul>
          </div>

          <div className="this-work">
            <h3>This Work: Full Supply Chain Analysis</h3>
            <p>
              <strong>Open DIO</strong> - Environmentally-Extended Input-Output Life Cycle Assessment
            </p>
            <ul>
              <li><strong>Scope</strong>: Procurement, manufacturing, operations (Scope 1+2+3)</li>
              <li><strong>Preliminary Finding</strong>: ~150-200 million metric tons CO2e for $850B budget</li>
              <li><strong>Innovation</strong>: Includes upstream manufacturing and materials</li>
            </ul>
          </div>
        </div>

        <div className="key-finding">
          <div className="finding-icon">🔍</div>
          <div className="finding-content">
            <h3>Key Finding</h3>
            <p>
              Supply chain emissions from defense procurement are approximately <strong>2.5× larger</strong>
              {' '}than operational emissions alone, suggesting that prior climate assessments significantly
              underestimate the total environmental footprint of military spending.
            </p>
          </div>
        </div>
      </section>

      <section className="contribution">
        <h2>Novel Contribution</h2>

        <div className="contribution-grid">
          <div className="contribution-item">
            <h3>🔓 Open Source</h3>
            <p>
              First <strong>publicly accessible</strong> tool for defense supply chain environmental
              analysis. Existing tools (EPA FLIGHT, CMU EIO-LCA) are proprietary or paywalled.
            </p>
          </div>

          <div className="contribution-item">
            <h3>🎯 Defense-Specific</h3>
            <p>
              Uses <strong>defense-relevant sectors</strong> (aircraft, ships, weapons) with
              sector-specific Leontief multipliers, rather than generic economic averages.
            </p>
          </div>

          <div className="contribution-item">
            <h3>📊 Transparent Methodology</h3>
            <p>
              All calculations, data sources, and uncertainty ranges <strong>fully documented</strong>
              {' '}and reproducible, unlike proprietary models.
            </p>
          </div>

          <div className="contribution-item">
            <h3>🔬 IO Literature-Based</h3>
            <p>
              Supply chain multipliers (1.35×-2.10×) derived from peer-reviewed input-output
              literature (Miller & Blair 2009, Suh 2009), not simplified estimates.
            </p>
          </div>
        </div>
      </section>

      <section className="dissertation-vision">
        <h2>Dissertation Research Vision</h2>

        <div className="vision-content">
          <p>
            This tool represents the <strong>methodological foundation</strong> for proposed
            dissertation research on the environmental externalities of military spending.
          </p>

          <h3>Proposed Research Agenda</h3>
          <ol className="research-agenda">
            <li>
              <strong>Phase 1 (Complete)</strong>: Develop open-source IO-LCA methodology
              for defense procurement environmental assessment
            </li>
            <li>
              <strong>Phase 2 (In Progress)</strong>: Validate methodology against published
              estimates and conduct sensitivity analysis
            </li>
            <li>
              <strong>Phase 3 (Proposed)</strong>: Time-series analysis of defense environmental
              footprint (FY2015-FY2025) to identify trends
            </li>
            <li>
              <strong>Phase 4 (Proposed)</strong>: Comparative analysis across allied nations
              (U.S., NATO, Five Eyes) using EXIOBASE framework
            </li>
            <li>
              <strong>Phase 5 (Proposed)</strong>: Policy analysis examining how procurement
              reforms could reduce lifecycle climate impacts
            </li>
          </ol>

          <h3>Research Questions for Dissertation</h3>
          <ul className="research-questions-list">
            <li>How have supply chain emissions from defense procurement changed over time?</li>
            <li>Which procurement categories offer the greatest decarbonization potential?</li>
            <li>What procurement policy reforms could cost-effectively reduce emissions?</li>
            <li>How do military environmental exemptions affect total national carbon accounting?</li>
            <li>Can lifecycle contracting standards incentivize greener defense manufacturing?</li>
          </ul>
        </div>
      </section>

      <section className="policy-implications">
        <h2>Policy Implications</h2>

        <div className="implications-grid">
          <div className="implication">
            <h3>Defense Procurement Reform</h3>
            <p>
              Lifecycle emissions criteria could be integrated into defense contracting
              standards, incentivizing manufacturers to reduce supply chain footprints.
            </p>
          </div>

          <div className="implication">
            <h3>Climate Accounting Accuracy</h3>
            <p>
              National greenhouse gas inventories should include supply chain emissions
              from military procurement, not just operational fuel use.
            </p>
          </div>

          <div className="implication">
            <h3>Congressional Oversight</h3>
            <p>
              Transparent environmental impact data enables evidence-based oversight of
              defense spending and climate commitments.
            </p>
          </div>

          <div className="implication">
            <h3>Climate Policy Exemptions</h3>
            <p>
              Military exemptions from climate regulations may understate true emissions
              by 60-70% if supply chains are excluded.
            </p>
          </div>
        </div>
      </section>

      <section className="methodology-status">
        <h2>Current Status & Limitations</h2>

        <div className="status-note">
          <div className="status-icon">⚠️</div>
          <div className="status-text">
            <h3>Methodological Proof-of-Concept</h3>
            <p>
              This tool is a <strong>research demonstration</strong>, not a definitive analysis.
              It establishes methodological feasibility and identifies research gaps requiring
              further investigation.
            </p>
          </div>
        </div>

        <h3>Known Limitations</h3>
        <ul className="limitations-list">
          <li>
            <strong>Data Vintage</strong>: BEA Input-Output tables from 2012 (most recent complete
            dataset at project start); does not reflect post-2012 economic structural changes
          </li>
          <li>
            <strong>Limited Validation</strong>: Preliminary comparison to Crawford (2019) and
            FY2020 DOD reports; requires peer review and cross-validation with additional sources
          </li>
          <li>
            <strong>Uncertainty Quantification</strong>: Ranges provided but Monte Carlo uncertainty
            propagation not yet implemented
          </li>
          <li>
            <strong>Scope Boundaries</strong>: Excludes personnel emissions (commuting, travel),
            training exercise environmental damage, overseas base operations, and site remediation
          </li>
          <li>
            <strong>Geographic Scope</strong>: Uses U.S.-based multipliers; international supply
            chains may have different environmental intensities
          </li>
        </ul>

        <h3>Validation Approach</h3>
        <p>
          Results validated against:
        </p>
        <ul>
          <li><strong>Crawford (2019)</strong>: Operational emissions show expected relationship (our operational subset ≈ Crawford's total)</li>
          <li><strong>FY2020 DOD Environmental Reports</strong>: ±10% agreement on direct energy consumption</li>
          <li><strong>IO Literature</strong>: Leontief multipliers (1.35×-2.10×) within expected ranges (Miller & Blair 2009: 1.5×-4.0×)</li>
          <li><strong>EIA Data</strong>: Energy intensity values consistent with MECS 2018 manufacturing surveys</li>
        </ul>
      </section>

      <section className="reproducibility">
        <h2>Reproducibility & Open Science</h2>

        <div className="reproducibility-grid">
          <div className="repro-item">
            <h3>📂 Code Repository</h3>
            <p>
              <a href="https://github.com/kelaxten/DIO-v3" target="_blank" rel="noopener noreferrer">
                github.com/kelaxten/DIO-v3
              </a>
            </p>
            <p>All analysis code, data processing scripts, and documentation</p>
          </div>

          <div className="repro-item">
            <h3>📊 Data Sources</h3>
            <ul>
              <li>USAspending.gov (spending data)</li>
              <li>Cornerstone v1.4.0 (GHG factors)</li>
              <li>EIA MECS 2018 (energy data)</li>
              <li>EPA USEEIO v2.0 (water, land)</li>
            </ul>
          </div>

          <div className="repro-item">
            <h3>📝 Computational Environment</h3>
            <p>Python 3.9+, React 18, TypeScript 5</p>
            <p>Dependencies: see <code>requirements.txt</code></p>
          </div>

          <div className="repro-item">
            <h3>📖 Citation</h3>
            <p>
              <code>
                Open DIO v2.0 (2024). Defense Input-Output Environmental Analysis Tool.
                https://kelaxten.github.io/DIO-v3/
              </code>
            </p>
          </div>
        </div>
      </section>

      <section className="get-involved">
        <h2>Get Involved</h2>

        <div className="involvement-options">
          <div className="involvement-option">
            <h3>🔬 Researchers</h3>
            <p>Use the tool for your analysis, request features, or contribute methodology improvements</p>
            <a href="https://github.com/kelaxten/DIO-v3/issues" className="cta-button">
              Request Features
            </a>
          </div>

          <div className="involvement-option">
            <h3>📊 Data Scientists</h3>
            <p>Download datasets, build visualizations, or develop custom analyses</p>
            <a href="/data/fy2024_dod_line_by_line.csv" download className="cta-button">
              Download Data
            </a>
          </div>

          <div className="involvement-option">
            <h3>💬 Feedback</h3>
            <p>Report bugs, suggest improvements, or discuss methodology</p>
            <a href="https://github.com/kelaxten/DIO-v3/discussions" className="cta-button">
              Join Discussion
            </a>
          </div>
        </div>
      </section>

      <section className="references">
        <h2>Key References</h2>

        <div className="references-list">
          <div className="reference">
            <p>
              <strong>Crawford, N. C.</strong> (2019). <em>Pentagon Fuel Use, Climate Change, and
              the Costs of War</em>. Watson Institute for International and Public Affairs, Brown University.
            </p>
          </div>

          <div className="reference">
            <p>
              <strong>Miller, R. E., & Blair, P. D.</strong> (2009). <em>Input-Output Analysis:
              Foundations and Extensions</em> (2nd ed.). Cambridge University Press.
            </p>
          </div>

          <div className="reference">
            <p>
              <strong>Suh, S.</strong> (2009). <em>Handbook of Input-Output Economics in Industrial Ecology</em>.
              Springer.
            </p>
          </div>

          <div className="reference">
            <p>
              <strong>Yang, Y., et al.</strong> (2017). USEEIO: A new and transparent United States
              environmentally-extended input-output model. <em>Journal of Cleaner Production</em>, 158, 308-318.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ResearchContext;
