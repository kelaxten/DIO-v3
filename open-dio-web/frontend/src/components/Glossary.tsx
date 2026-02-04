import './Glossary.css';

interface GlossaryEntry {
  term: string;
  definition: string;
  unit?: string;
}

const glossaryTerms: GlossaryEntry[] = [
  {
    term: 'CO2e (Carbon Dioxide Equivalent)',
    definition: 'A standard unit for measuring the climate impact of different greenhouse gases. It expresses the global warming potential of various gases (methane, nitrous oxide, etc.) in terms of the equivalent amount of CO2 that would have the same warming effect.',
    unit: 'kg CO2e or metric tons CO2e'
  },
  {
    term: 'GHG (Greenhouse Gas)',
    definition: 'Gases that trap heat in the atmosphere, contributing to climate change. Major GHGs include carbon dioxide (CO2), methane (CH4), and nitrous oxide (N2O).'
  },
  {
    term: 'MJ (Megajoule)',
    definition: 'A unit of energy equal to one million joules. Used to measure total energy consumption including electricity, fuel, and other energy sources.',
    unit: 'MJ'
  },
  {
    term: 'BEA Sector',
    definition: 'Economic sectors defined by the Bureau of Economic Analysis in their Input-Output tables. DIO uses 396 detailed sectors representing different industries and products in the US economy.'
  },
  {
    term: 'NAICS Code',
    definition: 'North American Industry Classification System - a standard for classifying business establishments. 6-digit codes like "336411" identify specific industries (e.g., Aircraft Manufacturing).'
  },
  {
    term: 'Input-Output Analysis',
    definition: 'An economic method that traces how dollars spent in one sector flow through the supply chain, affecting many other sectors. This allows us to calculate total (direct + indirect) environmental impacts.'
  },
  {
    term: 'EEIO (Environmentally-Extended Input-Output)',
    definition: 'Input-Output analysis that includes environmental impacts (GHG, energy, water, land) alongside economic flows. This is the methodology used by DIO.'
  },
  {
    term: 'Leontief Inverse',
    definition: 'A mathematical matrix that captures the total requirements (direct + indirect) across all sectors needed to produce one unit of final demand. Named after economist Wassily Leontief.'
  },
  {
    term: 'Supply Chain Emissions',
    definition: 'Indirect emissions from all upstream suppliers and processes. For example, aircraft manufacturing includes emissions from steel production, aluminum smelting, electronics manufacturing, etc.'
  },
  {
    term: 'Multiplier',
    definition: 'A factor that scales direct impacts to include supply chain effects. For example, a 1.75x multiplier means total impact is 1.75 times the direct impact.'
  },
  {
    term: 'Water Consumption',
    definition: 'Water withdrawn and not returned to the source (evaporated, incorporated into products, or consumed by humans/livestock). Different from water withdrawal.',
    unit: 'gallons or cubic meters'
  },
  {
    term: 'Land Use',
    definition: 'Land occupation over time, accounting for both the area and duration of use. Includes agricultural land, mining areas, infrastructure, etc.',
    unit: 'm²-year'
  },
  {
    term: 'Uncertainty Range',
    definition: 'The expected variation in results due to data limitations and modeling assumptions. Expressed as ±percentage (e.g., ±25% means results could vary by 25% up or down).'
  },
  {
    term: 'Scope 1, 2, 3 Emissions',
    definition: 'Scope 1: Direct emissions from owned sources. Scope 2: Indirect from purchased electricity. Scope 3: All other indirect emissions in the supply chain. DIO calculates total impact (equivalent to Scope 1+2+3).'
  },
  {
    term: 'AR6 GWP-100',
    definition: 'The 6th Assessment Report Global Warming Potential over 100 years - the latest IPCC methodology for converting different greenhouse gases to CO2 equivalents.'
  },
  {
    term: 'Cornerstone Supply Chain Factors',
    definition: 'Peer-reviewed environmental impact data maintained by the Cornerstone Sustainability Data Initiative, used for GHG calculations in Open DIO.'
  },
  {
    term: 'EIA (Energy Information Administration)',
    definition: 'US government agency providing official energy statistics. Source of manufacturing and commercial energy consumption data used in Open DIO.'
  },
  {
    term: 'USEEIO',
    definition: 'US Environmentally-Extended Input-Output model developed by the EPA. Provides the framework and some data used in DIO.'
  }
];

export default function Glossary() {
  return (
    <div className="glossary">
      <div className="glossary-header">
        <h2>Glossary of Terms</h2>
        <p className="glossary-intro">
          Understanding the terminology used in environmental impact analysis
        </p>
      </div>

      <div className="glossary-grid">
        {glossaryTerms.map((entry, index) => (
          <div key={index} className="glossary-entry">
            <h3 className="glossary-term">{entry.term}</h3>
            <p className="glossary-definition">{entry.definition}</p>
            {entry.unit && (
              <p className="glossary-unit">
                <strong>Unit:</strong> {entry.unit}
              </p>
            )}
          </div>
        ))}
      </div>

      <div className="glossary-footer">
        <h3>Additional Resources</h3>
        <ul>
          <li>
            <a href="https://www.epa.gov/climateleadership/ghg-emission-factors-hub" target="_blank" rel="noopener noreferrer">
              EPA GHG Emission Factors
            </a>
          </li>
          <li>
            <a href="https://www.eia.gov/energyexplained/" target="_blank" rel="noopener noreferrer">
              EIA Energy Explained
            </a>
          </li>
          <li>
            <a href="https://www.ipcc.ch/report/ar6/wg1/" target="_blank" rel="noopener noreferrer">
              IPCC Sixth Assessment Report
            </a>
          </li>
          <li>
            <a href="https://www.bea.gov/data/industries/input-output-accounts-data" target="_blank" rel="noopener noreferrer">
              BEA Input-Output Accounts
            </a>
          </li>
        </ul>
      </div>
    </div>
  );
}
