# Open Defense Input-Output (DIO) Model
## Literature and Code Review

**Project Objective**: Build an open-source tool that enables journalists, researchers, and laypeople to assess the environmental impacts of military acquisitions, operations, and exercises by inputting budget documents or expenditure lists and receiving environmental impact assessments.

---

## 1. Executive Summary

The Defense Input-Output (DIO) model is a defense-specific extension of the EPA's USEEIO framework, designed to calculate life cycle environmental impacts of military spending. Currently maintained as a static Excel file with limited accessibility, there is significant opportunity to democratize access to this powerful analytical tool. This review examines the technical foundations, available data sources, and relevant research to inform development of an accessible, open-source implementation.

---

## 2. Core Technical Foundations

### 2.1 The Defense Input-Output (DIO) Model

**Source**: [EPA Data Catalog - DIO v2.0](https://catalog.data.gov/dataset/dio-v2-0)

**Key Characteristics**:
- Built using `useeior v1.2.1` (R package)
- Defense-specific extension of USEEIO models
- Incorporates data from BEA, TRI, US GHG Inventory
- Provides impact characterization factors for goods, services, activities
- Includes external cost factors (monetized environmental impacts)
- Available as Excel spreadsheet with multiple tabs following USEEIO Model format

**GitHub Repository**: [https://github.com/USEPA/DIO](https://github.com/USEPA/DIO)
- 55 commits, 2 contributors
- R-Markdown build process (`DIO.Rmd`)
- Data folder requires manual population (see `data/README.md`)
- Model folder contains configuration
- Documentation and working documents included
- **License**: Public domain (EPA-generated)

**Current Limitations**:
- Static Excel output requires manual analysis
- No user-friendly interface for non-technical users
- Defense-specific extensions have limited resolution
- No direct integration with budget/spending data sources

### 2.2 USEEIO Framework & Cornerstone Initiative

**Overview**: US Environmentally-Extended Input-Output models bridge economic input-output analysis with environmental impact assessment.

#### ⚠️ Critical Update: Cornerstone Initiative (August 2025)

In August 2025, the **Cornerstone Sustainability Data Initiative** was launched as a collaboration between:
- **Watershed** (climate solutions provider)
- **Stanford Sustainable Solutions Lab** (Stanford Doerr School of Sustainability)
- **ERG** (environmental consulting firm)

This followed the EPA's announcement that it would no longer update USEEIO. **Dr. Wesley Ingwersen**, the original EPA architect of USEEIO, was let go from EPA in July 2025 and now serves as **Technical Director** at Cornerstone.

**Cornerstone is now the primary maintainer of USEEIO** and is actively:
- Maintaining and updating USEEIO models
- Planning to merge USEEIO with CEDA (Comprehensive Environmental Data Archive) into a unified global MRIO model
- Expanding environmental indicators beyond GHG to include air quality, water use, waste generation
- Updating US state models with latest data
- Fostering community engagement among industrial ecologists and IO modelers

**GitHub**: [github.com/cornerstone-data](https://github.com/cornerstone-data)
**Website**: [cornerstonedata.org](https://cornerstonedata.org)

#### Key Repositories (Now Maintained by Cornerstone)

| Component | Description | Language | Repository |
|-----------|-------------|----------|------------|
| `useeior` | Core model building package | R | [cornerstone-data/useeior](https://github.com/cornerstone-data/useeior) |
| `flowsa` | Environmental/employment flow data | Python | [cornerstone-data/flowsa](https://github.com/cornerstone-data/flowsa) |
| `stateior` | State-level IO models | R | [cornerstone-data/stateior](https://github.com/cornerstone-data/stateior) |
| `bedrock` | Core data pipeline | Python | [cornerstone-data/bedrock](https://github.com/cornerstone-data/bedrock) |
| `supply-chain-factors` | GHG emission factors | R | [cornerstone-data/supply-chain-factors](https://github.com/cornerstone-data/supply-chain-factors) |

**Legacy EPA Repositories** (archived/limited updates):
- [USEPA/useeior](https://github.com/USEPA/useeior) - Original, now forked by Cornerstone
- [USEPA/USEEIO_API](https://github.com/USEPA/USEEIO_API) - Go-based API server

**USEEIO Model Versions**:
- Current: v2.5 (2025) - available via Cornerstone
- DIO based on: USEEIO framework (useeior v1.2.1) - **significantly outdated**
- 389 industry sectors with environmental data on land, water, energy, minerals, air pollution, nutrients, toxics

**Key Academic Citation**:
> Li, M., Ingwersen, W.W., Young, B., Vendries, J. and Birney, C., 2022. useeior: An Open-Source R Package for Building and Using US Environmentally-Extended Input–Output Models. *Applied Sciences*, 12(9), p.4469.

#### Implications for Open DIO Project

**The DIO v2.0 model is now significantly outdated**, having been built on useeior v1.2.1 while Cornerstone maintains v1.7.1+ with ongoing development. A key contribution of this project should be:

1. **Update DIO to latest USEEIO** - Rebuild DIO using current Cornerstone-maintained useeior
2. **Engage with Cornerstone community** - Coordinate with Dr. Ingwersen's team to ensure alignment
3. **Contribute defense-specific extensions** - Potentially contribute DIO enhancements back to Cornerstone ecosystem
4. **Future-proof architecture** - Build on Cornerstone's `bedrock` pipeline for sustainability

### 2.3 Mathematical Foundation

**Leontief Inverse (Total Requirements Matrix)**:
The core calculation uses the Leontief inverse matrix `L = (I - A)^(-1)` where:
- `A` = Direct requirements matrix (inter-industry purchases per dollar of output)
- `L` = Total requirements matrix (direct + indirect requirements)
- Impact = L × demand vector × satellite accounts (environmental flows per dollar)

**Key Matrices in DIO/USEEIO**:
- `A`: Direct requirements matrix
- `L`: Total requirements matrix  
- `B`: Satellite accounts (environmental flows per $ output)
- `C`: Characterization factors (impacts per unit flow)
- `D`: Direct impact matrix
- `M`: Total impact multipliers

---

## 3. Data Sources and Integration Points

### 3.1 Defense Spending Data

**USAspending.gov**
- Comprehensive federal spending data (contracts, grants, loans)
- REST API available: [api.usaspending.gov](https://api.usaspending.gov)
- Bulk download available (CSV, PostgreSQL snapshots)
- Data available from FY2008 to present
- Includes NAICS codes for industry classification
- Includes PSC (Product Service Codes) for product/service classification

**Key Data Fields for Mapping**:
- NAICS codes (6-digit industry classification)
- PSC codes (Product Service Codes) 
- Award amounts (obligations)
- Agency/sub-agency identifiers
- Place of performance
- Recipient information

**API Capabilities**:
```
POST /api/v2/bulk_download/awards/
- Filter by agency (DOD: toptier_code = '097')
- Filter by date range
- Filter by award type
- Returns CSV zipfile
```

### 3.2 Industry Classification Mapping

**NAICS to BEA Sector Crosswalk**:
- USEEIO uses BEA sector codes (6-digit)
- DOD contracts tagged with NAICS codes
- Crosswalk available: NAICS → BEA Detail → BEA Summary
- 389 USEEIO sectors map from ~1,000 NAICS codes

**Defense-Specific NAICS Codes** (Top spending):
| NAICS | Description |
|-------|-------------|
| 336411 | Aircraft Manufacturing |
| 541330 | Engineering Services |
| 336414 | Guided Missile and Space Vehicle Manufacturing |
| 336611 | Ship Building and Repairing |
| 541512 | Computer Systems Design Services |
| 336413 | Other Aircraft Parts and Equipment |
| 237990 | Other Heavy Construction |

### 3.3 Environmental Data Sources (via USEEIO)

| Data Type | Source | Coverage |
|-----------|--------|----------|
| GHG Emissions | US GHG Inventory, EPA | National by sector |
| Toxic Releases | TRI (Toxics Release Inventory) | Facility-level |
| Water Use | USGS Water Use Data | State/County |
| Land Use | NLCD, USDA | National |
| Energy Use | EIA | National by sector |
| Employment | BLS QCEW | National by sector |

---

## 4. Academic Research and Prior Work

### 4.1 Costs of War Project (Brown University)

**Key Researcher**: Neta C. Crawford, University of Oxford (formerly Boston University)

**Seminal Work**: "Pentagon Fuel Use, Climate Change, and the Costs of War"
- Methodology for estimating US military emissions
- Data source: Department of Energy (since Pentagon withholds data from Congress)
- Found 1.2 billion metric tons CO2e emissions (2001-2017)
- 400+ million metric tons from war-related fuel consumption
- Military jets are largest fuel consumers

**Book**: Crawford, N.C. (2022). *The Pentagon, Climate Change, and War: Charting the Rise and Fall of U.S. Military Emissions*. MIT Press.

**Key Findings**:
- DOD is world's largest institutional consumer of fossil fuels
- DOD is single largest institutional GHG emitter globally
- Military emissions higher than many industrialized nations (Sweden, Portugal, Denmark)
- Estimated 59 million tons CO2 in 2017 alone
- If DOD were a country: 47th-55th largest emitter

### 4.2 Durham/Lancaster University Study (2019)

**Researchers**: Oliver Belcher, Benjamin Neimark, Patrick Bigger

**Key Findings**:
- US military is "one of the largest climate polluters in history"
- Consumes more liquid fuels than most countries
- Data retrieved via Freedom of Information Act requests
- Defense Logistics Agency fuel procurement data

### 4.3 Ryan Thombs Study (Penn State, 2025)

**Publication**: PLOS Climate (July 2025)

**Methodology**: 
- Analyzed publicly available DOD data 1975-2022
- Linked military spending to energy consumption and GHG emissions
- Found asymmetric effects: cuts reduce emissions more than increases raise them

### 4.4 DoD Internal Sustainability Analysis

**SERDP/ESTCP LCA Toolkit**: [serdp-estcp.mil/resources/toolkit](https://serdp-estcp.mil/resources/toolkit/b789a50d-2ffc-46b8-8ef7-8d704c35bcec/life-cycle-assessment-toolkit)

**DoD Sustainability Analysis Guidance**: 
- Located on DENIX (DoD Environment, Safety & Occupational Health Network)
- Combines LCA with Life Cycle Costing
- References DIO for impact characterization factors
- Supports Adaptive Acquisition Framework requirements

**SparkLC Tool**: Web-based sustainability analysis tool (developed by Noblis for SERDP/ESTCP)
- Not publicly accessible
- Designed for defense researchers

---

## 5. Technical Architecture Options

### 5.1 Backend Options

**Option A: Python-Native Implementation**
- Reimplement USEEIO calculations in Python
- Use NumPy/Pandas for matrix operations
- Advantages: Broad developer community, easy deployment
- Challenges: Must recreate R package functionality

**Option B: R Backend with Python/JS Frontend**
- Use `useeior` directly via `rpy2` bridge
- Advantages: Leverages existing EPA codebase
- Challenges: Added complexity, R dependency

**Option C: Pre-computed API Approach**
- Use USEEIO_API (Go) to serve pre-computed model results
- Build frontend that queries API
- Advantages: Leverages existing infrastructure
- Challenges: Less flexibility for custom calculations

### 5.2 Data Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Budget PDF → OCR → Line Item Extraction                    │
│  CSV Upload → Parse → Validate                              │
│  Manual Entry → Form → Validate                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Classification Layer                       │
├─────────────────────────────────────────────────────────────┤
│  Line Items → NAICS/PSC Codes → BEA Sectors                 │
│  Fuzzy matching for natural language descriptions           │
│  AI-assisted classification for ambiguous items             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Calculation Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Demand Vector ($ by sector) × DIO Multipliers              │
│  → Environmental Flows (emissions, water, land, etc.)       │
│  → Impact Potentials (GWP, acidification, etc.)             │
│  → External Costs (monetized damages)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Summary Dashboard (key metrics)                            │
│  Detailed Breakdowns (by category, sector, flow)            │
│  Comparisons (vs. countries, industries, baselines)         │
│  Exportable Reports (PDF, CSV)                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Key Technical Decisions

1. **Pre-compute vs. On-demand Calculation**
   - Pre-compute: Faster, simpler frontend
   - On-demand: More flexible, larger compute requirements

2. **Sector Resolution**
   - Summary (71 sectors): Simpler, faster
   - Detail (389 sectors): More precise, complex mapping

3. **Impact Categories to Include**
   - Essential: GHG emissions (CO2e), Energy use
   - Important: Water use, Land use, Criteria air pollutants
   - Advanced: Toxicity, Eutrophication, External costs

---

## 6. Comparable Tools and Interfaces

### 6.1 EPA SMM Prioritization Tools
- National and Organizational sustainability tools
- Uses USEEIO backend
- Web-based interface for procurement analysis

### 6.2 EIO-LCA (Carnegie Mellon)
- Classic economic input-output LCA tool
- Web interface for sector-based impact calculation
- Benchmark for user experience

### 6.3 OpenLCA
- Open-source LCA software
- Can import USEEIO models
- Desktop application (complex for non-experts)

---

## 7. Stakeholder Needs Assessment

### 7.1 Journalists
**Needs**:
- Quick, credible estimates for stories
- Comparisons that communicate scale (vs. countries, cities)
- Downloadable graphics/charts
- Clear methodology documentation for fact-checking

**Use Cases**:
- "What's the carbon footprint of the F-35 program?"
- "How do emissions from [military exercise] compare to [city]?"

### 7.2 Researchers
**Needs**:
- Detailed methodology transparency
- Raw data export
- Uncertainty/sensitivity analysis
- API access for integration with other tools

**Use Cases**:
- Academic studies on military environmental impact
- Policy analysis and recommendations

### 7.3 General Public/Advocates
**Needs**:
- Simple, intuitive interface
- Clear visualizations
- Shareable results
- Educational context

**Use Cases**:
- Understanding personal tax contribution to military emissions
- Advocacy and public awareness campaigns

---

## 8. Key Challenges and Mitigations

| Challenge | Description | Mitigation Strategy |
|-----------|-------------|---------------------|
| Data opacity | Pentagon restricts fuel/emissions data | Use DOE data, input-output estimates |
| Classification complexity | Mapping budget items to sectors | AI-assisted + manual review options |
| Model currency | DIO v2.0 uses older USEEIO version | Plan for periodic updates, document vintage |
| Uncertainty | All models have inherent uncertainty | Provide ranges, document assumptions |
| Validation | Difficult to validate against "ground truth" | Cross-check with Crawford/Costs of War estimates |
| Accessibility | IO models complex for non-experts | Layer of abstraction, educational content |

---

## 9. Recommended Next Steps

1. **Engage with Cornerstone Initiative** - Contact Dr. Wesley Ingwersen's team to discuss project alignment and potential collaboration
2. **Update DIO to latest USEEIO** - Rebuild DIO using Cornerstone's current useeior (v1.7.1+) as first open source contribution
3. **Download and analyze DIO v2.0 Excel file** to understand existing structure and required updates
4. **Prototype sector mapping** with sample DOD contracts from USAspending
5. **Define MVP scope** focusing on GHG emissions as primary output
6. **Design user interface** with journalist/public user stories
7. **Build calculation engine** (recommend Python for accessibility, potentially leveraging Cornerstone's `bedrock` pipeline)
8. **Create validation suite** comparing to published military emissions estimates

---

## 10. References

### Primary Sources
- EPA DIO v2.0: https://catalog.data.gov/dataset/dio-v2-0
- USEPA/DIO GitHub: https://github.com/USEPA/DIO
- **Cornerstone Initiative**: https://cornerstonedata.org
- **Cornerstone GitHub**: https://github.com/cornerstone-data
- Cornerstone useeior fork: https://github.com/cornerstone-data/useeior
- Legacy USEPA/useeior: https://github.com/USEPA/useeior
- USEPA/USEEIO Overview: https://github.com/USEPA/USEEIO
- USEEIO API: https://github.com/USEPA/USEEIO_API

### Cornerstone Initiative Coverage
- Watershed Blog: https://watershed.com/blog/cornerstone
- ESG Today (Aug 2025): "Watershed, Stanford Take Over Key Supply Chain Emissions Database After EPA Stops Updating it"
- Globe Newswire (Aug 2025): "Cornerstone Initiative Launches to Preserve and Expand Access to Foundational Sustainability Data"

### Academic Literature
- Li et al. (2022). useeior: An Open-Source R Package. *Applied Sciences*.
- Yang et al. (2017). USEEIO: A New and Transparent Model. *Journal of Cleaner Production*.
- Crawford (2022). *The Pentagon, Climate Change, and War*. MIT Press.
- Crawford (2019). Pentagon Fuel Use, Climate Change, and the Costs of War. Costs of War Project.

### Data Sources
- USAspending.gov: https://www.usaspending.gov
- USAspending API: https://api.usaspending.gov
- SERDP-ESTCP LCA Toolkit: https://serdp-estcp.mil/resources/toolkit
- EPA USEEIO Technical Content: https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-technical-content

---

*Document prepared: January 2026*
*For: Open DIO Project Planning*
