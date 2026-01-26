# Open DIO - Defense Environmental Impact Calculator

**Calculate the environmental footprint of U.S. defense spending**

Open DIO is an open-source tool that estimates greenhouse gas emissions and other environmental impacts from military expenditures using Environmentally-Extended Input-Output (EEIO) analysis.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

Every dollar spent on defense has environmental consequences that ripple through the entire supply chain. Open DIO makes these hidden impacts visible by combining:

- **Economic input-output analysis** - Traces spending through 396 interconnected economic sectors
- **Environmental satellite data** - Links economic activity to GHG emissions, energy use, water consumption, and land use
- **Supply chain modeling** - Captures both direct impacts and indirect effects from suppliers, suppliers' suppliers, and beyond

### Example

> **$80 billion** spent on aircraft manufacturing generates approximately **10 million metric tons of CO2e** - equivalent to the annual emissions of **2.2 million passenger vehicles**.

---

## Features

- **396 economic sectors** covering the entire U.S. economy
- **109 defense-relevant sectors** organized into 15 categories (aircraft, ships, vehicles, weapons, electronics, IT, construction, etc.)
- **4 environmental impact categories**: GHG emissions, energy use, water consumption, land use
- **Full supply chain accounting** using Leontief inverse methodology
- **Modern web interface** for interactive calculations
- **REST API** for programmatic access
- **Transparent methodology** with documented data sources

---

## Data Sources

| Data | Source | Version | Year |
|------|--------|---------|------|
| GHG Emission Factors | Cornerstone Supply Chain Factors | v1.4.0 | 2024 USD |
| Economic Structure | BEA Input-Output Tables | Detail | 2017 NAICS |
| GWP Values | IPCC AR6 | GWP-100 | 2021 |

**Cornerstone Data Initiative**: Following EPA's transition away from USEEIO maintenance, the [Cornerstone Sustainability Data Initiative](https://cornerstonedata.org) (a collaboration between Watershed, Stanford, and ERG) now maintains and updates these datasets.

---

## Quick Start

### Web Application

```bash
# Clone the repository
git clone https://github.com/kelaxten/DIO-v3.git
cd DIO-v3

# Install frontend dependencies
cd open-dio-web/frontend
npm install

# Start development server
npm run dev

# Open http://localhost:5173
```

### Python (Direct Calculation)

```python
import json

# Load multipliers
with open('backend/app/data/multipliers.json') as f:
    data = json.load(f)

# Calculate impact for $1 billion in aircraft manufacturing
sector = '336411'  # Aircraft Manufacturing
spending = 1_000_000_000  # $1 billion

ghg_per_1000 = data['sectors'][sector]['GHG']  # kg CO2e per $1000
total_ghg = (spending / 1000) * ghg_per_1000

print(f"GHG Emissions: {total_ghg:,.0f} kg CO2e")
print(f"             = {total_ghg / 1000:,.0f} metric tons CO2e")
```

---

## Project Structure

```
DIO-v3/
├── open-dio-web/           # Web application
│   └── frontend/           # React frontend
│       └── public/data/    # Sector and multiplier JSON files
├── backend/                # Python API backend
│   └── app/data/           # Data files
│       ├── multipliers.json    # Environmental multipliers (396 sectors)
│       └── sectors.json        # Sector definitions and categories
├── DIO-updated/            # Original DIO model files
│   └── data/               # EPA DIO v2.0 source matrices
├── METHODOLOGY.md          # Full methodology documentation
├── 02_PRODUCT_BACKLOG.md   # Product roadmap
└── 03_TECHNICAL_SPEC.md    # Technical specifications
```

---

## Defense Sector Categories

Open DIO identifies **109 defense-relevant sectors** across 15 categories:

| Category | Sectors | Examples |
|----------|---------|----------|
| Electronics & Sensors | 23 | Navigation systems, radar, semiconductors |
| Metals & Fabrication | 19 | Steel mills, aluminum, metal products |
| Ground Vehicles & Armor | 11 | Tanks, military trucks, components |
| Energy & Fuel | 9 | Power generation, petroleum refineries |
| IT & Software | 8 | Computer systems, cybersecurity |
| Construction | 7 | Military bases, infrastructure |
| Chemicals | 6 | Industrial chemicals, propellants |
| Aircraft & Aerospace | 5 | Aircraft, missiles, space vehicles |
| Engineering & R&D | 5 | Engineering services, research |
| Transportation & Logistics | 5 | Air, sea, ground transport |
| Textiles & Equipment | 3 | Uniforms, protective gear |
| Food Services | 3 | Military food service |
| Ships & Marine | 2 | Ship building, boats |
| Weapons & Ammunition | 2 | Ammunition, explosives |
| Support Services | 1 | Facilities management |

---

## Methodology

Open DIO uses **Environmentally-Extended Input-Output (EEIO)** analysis:

```
Total Impact = Multiplier × Spending

Where: Multiplier = B × L
       B = Direct environmental intensity (emissions per $)
       L = Leontief inverse matrix (captures supply chain)
```

This approach captures:
- **Direct impacts**: Emissions from the sector itself
- **Indirect impacts**: Emissions from the entire supply chain (steel for aircraft, electricity for factories, fuel for transport, etc.)

For full methodology details, see [METHODOLOGY.md](METHODOLOGY.md).

---

## Sample Multipliers

| Sector | GHG (kg CO2e/$1000) |
|--------|---------------------|
| Aircraft Manufacturing | 126 |
| Ship Building | 183 |
| Military Armored Vehicles | 442 |
| Guided Missiles | 132 |
| Computer Systems Design | 90 |
| Engineering Services | 137 |
| Petroleum Refineries | 414 |
| Iron & Steel Mills | 1,006 |
| Electric Power Generation | 1,100 |

---

## API Usage

```bash
# Get list of sectors
curl http://localhost:8000/api/v1/sectors/

# Calculate impacts
curl -X POST http://localhost:8000/api/v1/calculate/ \
  -H "Content-Type: application/json" \
  -d '{"sectors": [{"code": "336411", "amount": 1000000000}]}'
```

---

## Contributing

Contributions are welcome! Areas where help is needed:

- **Data validation**: Compare outputs against published estimates
- **Sector mapping**: Improve defense sector identification
- **Frontend features**: Visualizations, comparisons, exports
- **Documentation**: Tutorials, examples, use cases

Please see [02_PRODUCT_BACKLOG.md](02_PRODUCT_BACKLOG.md) for the full roadmap.

---

## Related Projects & References

- [Cornerstone Data Initiative](https://cornerstonedata.org) - Maintains USEEIO and supply chain factors
- [USEEIO](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-technical-content) - EPA's original model
- [Costs of War Project](https://watson.brown.edu/costsofwar/) - Brown University research on military impacts
- [EPA DIO v2.0](https://catalog.data.gov/dataset/dio-v2-0) - Defense Input-Output model

---

## Citation

If you use Open DIO in your research, please cite:

```bibtex
@software{opendio2026,
  title = {Open DIO: Defense Environmental Impact Calculator},
  author = {Open DIO Contributors},
  year = {2026},
  url = {https://github.com/kelaxten/DIO-v3}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **Cornerstone Data Initiative** for maintaining supply chain emission factors
- **EPA** for the original DIO and USEEIO models
- **Dr. Wesley Ingwersen** and the USEEIO team for foundational methodology
- **Costs of War Project** at Brown University for research context

---

*Open DIO aims to make the environmental costs of military spending transparent and accessible to researchers, journalists, policymakers, and the public.*
