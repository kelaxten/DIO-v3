# Open DIO Project
## Product Backlog

---

## Vision Statement

**Enable anyone to understand the environmental cost of military spending** by providing an accessible, transparent tool that transforms defense budget data into actionable environmental impact assessments.

---

## User Personas

### 1. Maya - Investigative Journalist
- **Background**: Environmental reporter at major news outlet
- **Goals**: Quick, credible estimates for deadline-driven stories; compelling comparisons
- **Pain Points**: Complex data, lack of accessible tools, time pressure
- **Quote**: "I need numbers I can defend and comparisons readers understand"

### 2. Dr. Chen - Academic Researcher  
- **Background**: Environmental policy professor studying military emissions
- **Goals**: Methodology transparency, raw data access, integration with research tools
- **Pain Points**: Black-box models, inconsistent data sources
- **Quote**: "I need to understand exactly how these numbers are calculated"

### 3. Alex - Climate Advocate
- **Background**: Works for environmental NGO, non-technical background
- **Goals**: Clear visuals, shareable content, educational context
- **Pain Points**: Complex terminology, hard to communicate scale
- **Quote**: "I want to show people what their tax dollars mean for the climate"

### 4. Sam - Congressional Staffer
- **Background**: Works on defense appropriations committee
- **Goals**: Budget-level analysis, comparison across programs, policy options
- **Pain Points**: Lack of environmental data in budget discussions
- **Quote**: "We need to factor environmental costs into acquisition decisions"

---

## Epics Overview

| Epic | Description | Priority | Estimated Effort |
|------|-------------|----------|------------------|
| **E0** | **Update DIO to Latest USEEIO (Cornerstone)** | **Must Have - First** | **Medium** |
| E1 | Core Calculation Engine | Must Have | Large |
| E2 | Data Input & Classification | Must Have | Large |
| E3 | Results Dashboard | Must Have | Medium |
| E4 | Comparison & Context | Should Have | Medium |
| E5 | Export & Sharing | Should Have | Small |
| E6 | API & Integration | Could Have | Medium |
| E7 | Educational Content | Could Have | Small |
| E8 | Advanced Analysis | Won't Have (MVP) | Large |

---

## Epic 0: Update DIO to Latest USEEIO (Cornerstone)

**Goal**: Modernize the Defense Input-Output model by rebuilding it on the current USEEIO framework maintained by the Cornerstone Initiative, contributing improvements back to the open source community.

### Background

The existing DIO v2.0 was built on `useeior v1.2.1`, which is now significantly outdated. In August 2025, the **Cornerstone Sustainability Data Initiative** (a collaboration between Watershed, Stanford Sustainable Solutions Lab, and ERG) took over maintenance of USEEIO after EPA stopped supporting it. Dr. Wesley Ingwersen, the original USEEIO architect, now leads Cornerstone as Technical Director.

Updating DIO to the latest USEEIO framework:
- Ensures access to latest environmental data (2023 reference year vs. older data)
- Aligns with the broader sustainability data community
- Enables future compatibility as USEEIO merges with CEDA
- Creates opportunity to contribute defense extensions back to Cornerstone

### User Stories

#### E0.1 - Community Engagement
**As a** project maintainer  
**I want to** establish relationship with Cornerstone team  
**So that** our work aligns with the broader USEEIO ecosystem  

**Acceptance Criteria**:
- [ ] Introduce project to Cornerstone community via GitHub discussions
- [ ] Clarify licensing and contribution expectations
- [ ] Identify potential collaboration opportunities
- [ ] Document any Cornerstone roadmap items relevant to defense analysis

---

#### E0.2 - USEEIO Version Assessment
**As a** developer  
**I want to** understand differences between useeior v1.2.1 and current version  
**So that** I can plan the DIO migration  

**Acceptance Criteria**:
- [ ] Document API/schema changes between useeior versions
- [ ] Identify deprecated functions used in DIO.Rmd
- [ ] Catalog new capabilities available in current useeior
- [ ] Assess compatibility of existing DIO data extensions

---

#### E0.3 - Rebuild DIO on Current useeior
**As a** developer  
**I want to** rebuild DIO using Cornerstone's useeior v1.7+  
**So that** the model uses current data and methods  

**Acceptance Criteria**:
- [ ] Fork DIO repository
- [ ] Update DIO.Rmd to use current useeior
- [ ] Regenerate DIO model with latest environmental data
- [ ] Validate outputs against v2.0 (document expected differences)
- [ ] Export as both Excel and JSON for programmatic access

**Technical Notes**:
- Use Cornerstone's `useeior` fork: https://github.com/cornerstone-data/useeior
- Consider using `flowsa` for updated environmental flow data
- Document any defense-specific satellite account requirements

---

#### E0.4 - Defense-Specific Extensions
**As a** domain expert  
**I want to** enhance defense-specific sector resolution  
**So that** military spending analysis is more accurate  

**Acceptance Criteria**:
- [ ] Review existing defense extensions in DIO data folder
- [ ] Identify gaps in defense sector coverage
- [ ] Research additional data sources for defense-specific flows
- [ ] Document enhancement opportunities for future work

**Potential Enhancements**:
- Military vehicle fuel consumption factors
- Weapons system manufacturing emissions
- Base operations environmental data
- Overseas operations adjustments

---

#### E0.5 - Contribute Back to Cornerstone
**As a** open source contributor  
**I want to** share our defense extensions with Cornerstone  
**So that** the broader community benefits  

**Acceptance Criteria**:
- [ ] Package defense extensions in Cornerstone-compatible format
- [ ] Submit PR or discussion to Cornerstone repos
- [ ] Document methodology for peer review
- [ ] Coordinate with Dr. Ingwersen's team on integration

---

## Epic 1: Core Calculation Engine

**Goal**: Implement the DIO/USEEIO calculation methodology in an accessible, maintainable codebase.

### User Stories

#### E1.1 - Basic Impact Calculation
**As a** user  
**I want to** input a dollar amount for a defense sector  
**So that** I can see the estimated environmental impacts  

**Acceptance Criteria**:
- [ ] User can select from list of defense-relevant sectors
- [ ] User can input dollar amount
- [ ] System returns GHG emissions (CO2e), energy use, water use
- [ ] Calculation completes in <2 seconds
- [ ] Results match DIO v2.0 Excel calculations (±1%)

**Technical Notes**:
- Implement Leontief inverse calculation
- Pre-load DIO multiplier matrices
- Python/NumPy recommended

---

#### E1.2 - Multi-Sector Calculation
**As a** researcher  
**I want to** input spending across multiple sectors simultaneously  
**So that** I can analyze complete budgets or programs  

**Acceptance Criteria**:
- [ ] User can input spending for 1-389 sectors
- [ ] System aggregates impacts across all sectors
- [ ] System shows breakdown by sector contribution
- [ ] Handles $0 to $1 trillion spending levels

---

#### E1.3 - Impact Category Selection
**As a** user  
**I want to** choose which environmental impacts to calculate  
**So that** I can focus on metrics relevant to my analysis  

**Acceptance Criteria**:
- [ ] User can select from available impact categories
- [ ] Default selection includes: GHG (CO2e), Energy, Water, Land
- [ ] Advanced categories available: Criteria pollutants, Toxicity, Eutrophication
- [ ] External costs (monetized) available as optional output

**Impact Categories (from DIO)**:
| Category | Unit | Priority |
|----------|------|----------|
| Global Warming Potential | kg CO2e | Essential |
| Energy Use | MJ | Essential |
| Water Consumption | m³ | Essential |
| Land Use | m² | Important |
| Acidification Potential | kg SO2e | Secondary |
| Eutrophication Potential | kg Ne | Secondary |
| Particulate Matter | kg PM2.5e | Secondary |
| Human Toxicity | CTUh | Advanced |
| Freshwater Ecotoxicity | CTUe | Advanced |
| External Costs | USD | Advanced |

---

#### E1.4 - Uncertainty Estimation
**As a** researcher  
**I want to** see confidence intervals on impact estimates  
**So that** I can appropriately qualify my findings  

**Acceptance Criteria**:
- [ ] System provides low/mid/high estimates
- [ ] Methodology for uncertainty clearly documented
- [ ] Visual representation of uncertainty range

---

## Epic 2: Data Input & Classification

**Goal**: Enable users to input spending data in various formats and automatically classify it to appropriate sectors.

### User Stories

#### E2.1 - Manual Sector Entry
**As a** user  
**I want to** manually select sectors and enter dollar amounts  
**So that** I can quickly analyze known budget items  

**Acceptance Criteria**:
- [ ] Searchable dropdown of all 389 DIO sectors
- [ ] Common defense sectors highlighted/prioritized
- [ ] Auto-complete on sector names
- [ ] Real-time validation of inputs

---

#### E2.2 - CSV/Excel Upload
**As a** researcher  
**I want to** upload a spreadsheet of budget items  
**So that** I can analyze large datasets efficiently  

**Acceptance Criteria**:
- [ ] Accept CSV and XLSX formats
- [ ] Support column mapping (amount, description, NAICS, etc.)
- [ ] Provide template download
- [ ] Handle files up to 10,000 rows
- [ ] Show upload progress and validation errors

**Template Columns**:
```
| description | amount_usd | naics_code | psc_code | notes |
```

---

#### E2.3 - NAICS Code Mapping
**As a** user  
**I want to** input NAICS codes instead of sector names  
**So that** I can use standard industry classifications from contract data  

**Acceptance Criteria**:
- [ ] Accept 2-6 digit NAICS codes
- [ ] Map NAICS to BEA sectors automatically
- [ ] Handle many-to-one mappings with proportional allocation
- [ ] Flag ambiguous mappings for user review

---

#### E2.4 - Natural Language Classification (AI-Assisted)
**As a** journalist  
**I want to** paste budget line item descriptions  
**So that** the system can automatically classify them  

**Acceptance Criteria**:
- [ ] Accept free-text descriptions (e.g., "F-35 aircraft procurement")
- [ ] AI suggests appropriate sector classification
- [ ] Confidence score displayed
- [ ] User can accept, modify, or reject suggestions
- [ ] System learns from user corrections (optional)

**Example Classifications**:
| Input Description | Suggested Sector | Confidence |
|-------------------|------------------|------------|
| "F-35 Lightning II aircraft" | Aircraft Manufacturing | 95% |
| "Base infrastructure repair" | Heavy Construction | 75% |
| "Cybersecurity services contract" | Computer Systems Design | 85% |

---

#### E2.5 - Budget Document Parser
**As a** journalist  
**I want to** upload a PDF budget document  
**So that** I can extract and analyze spending data automatically  

**Acceptance Criteria**:
- [ ] Accept PDF uploads (congressional budget docs, DOD reports)
- [ ] OCR for scanned documents
- [ ] Extract line items and amounts
- [ ] Present extracted data for review before calculation
- [ ] Handle common DOD budget formats

**Scope Note**: MVP may limit to structured PDFs; full document understanding is advanced feature.

---

#### E2.6 - USAspending.gov Integration
**As a** researcher  
**I want to** import contract data directly from USAspending  
**So that** I can analyze actual spending without manual data entry  

**Acceptance Criteria**:
- [ ] Search USAspending by agency, date range, NAICS
- [ ] Pre-filter to DOD agencies
- [ ] Import selected contracts with NAICS codes
- [ ] Aggregate by sector for calculation

---

## Epic 3: Results Dashboard

**Goal**: Present calculation results in clear, actionable visualizations.

### User Stories

#### E3.1 - Summary Metrics
**As a** user  
**I want to** see key environmental impacts at a glance  
**So that** I can quickly understand the magnitude  

**Acceptance Criteria**:
- [ ] Display top-line metrics: Total GHG, Energy, Water
- [ ] Large, readable numbers with appropriate units
- [ ] Color coding for magnitude (traffic light or gradient)
- [ ] Responsive design for mobile viewing

**Mock Summary**:
```
┌────────────────────────────────────────────────────────┐
│  Environmental Impact Summary                          │
│  Budget Analyzed: $50,000,000,000                     │
├────────────────────────────────────────────────────────┤
│  🌡️ Greenhouse Gas Emissions                          │
│     15.2 Million Metric Tons CO2e                     │
│     Equivalent to: 3.3 million cars for one year      │
├────────────────────────────────────────────────────────┤
│  ⚡ Energy Consumption                                 │
│     890 Petajoules                                    │
│     Equivalent to: 2% of US annual energy use         │
├────────────────────────────────────────────────────────┤
│  💧 Water Consumption                                  │
│     2.1 Billion Cubic Meters                          │
│     Equivalent to: Annual use of 4 million households │
└────────────────────────────────────────────────────────┘
```

---

#### E3.2 - Sector Breakdown Chart
**As a** researcher  
**I want to** see which sectors contribute most to impacts  
**So that** I can identify key drivers  

**Acceptance Criteria**:
- [ ] Treemap or bar chart showing sector contributions
- [ ] Sortable by spending amount or impact
- [ ] Drill-down to see sector details
- [ ] Show top 10 + "other" by default

---

#### E3.3 - Impact Category Comparison
**As a** user  
**I want to** compare across impact categories  
**So that** I can see the full environmental picture  

**Acceptance Criteria**:
- [ ] Radar chart or parallel coordinates showing all impacts
- [ ] Normalized view (% of maximum) for comparison
- [ ] Toggle between absolute and normalized views

---

#### E3.4 - Time Series View
**As a** researcher  
**I want to** analyze spending impacts over multiple years  
**So that** I can identify trends  

**Acceptance Criteria**:
- [ ] User can input or import multi-year data
- [ ] Line chart showing impacts over time
- [ ] Option to adjust for inflation
- [ ] Compare to baseline year

---

## Epic 4: Comparison & Context

**Goal**: Help users understand the scale and significance of calculated impacts.

### User Stories

#### E4.1 - Country Comparison
**As a** journalist  
**I want to** compare military emissions to country emissions  
**So that** I can communicate scale to readers  

**Acceptance Criteria**:
- [ ] Database of country GHG emissions (World Bank data)
- [ ] Auto-generate "equivalent to X country" comparisons
- [ ] Visual showing where on country ranking
- [ ] Citation for comparison data included

---

#### E4.2 - Everyday Equivalents
**As a** advocate  
**I want to** see impacts in everyday terms  
**So that** I can make data relatable  

**Acceptance Criteria**:
- [ ] Library of equivalents (cars, homes, flights, etc.)
- [ ] Auto-calculate for any result
- [ ] Customizable (user can add own equivalents)

**Equivalents Library**:
| Unit | Equivalent | Source |
|------|------------|--------|
| 1 ton CO2e | 2,500 miles driven (avg car) | EPA |
| 1 ton CO2e | 1,100 lbs coal burned | EIA |
| 1 ton CO2e | 0.22 homes' annual energy | EPA |
| 1 PJ energy | 277,778 MWh | - |
| 1 million m³ water | 400 Olympic pools | - |

---

#### E4.3 - Per-Capita Allocation
**As a** advocate  
**I want to** see my personal share of military emissions  
**So that** I can connect budget to individual impact  

**Acceptance Criteria**:
- [ ] Calculate per-taxpayer share of input spending
- [ ] Show corresponding per-taxpayer emissions
- [ ] Option to input personal tax contribution

---

#### E4.4 - Program Comparison
**As a** staffer  
**I want to** compare environmental impacts of different programs  
**So that** I can inform policy decisions  

**Acceptance Criteria**:
- [ ] Side-by-side comparison of multiple analyses
- [ ] Save analyses for later comparison
- [ ] Normalize by spending amount for efficiency comparison

---

#### E4.5 - Historical Context
**As a** researcher  
**I want to** compare current spending to historical baselines  
**So that** I can contextualize changes over time  

**Acceptance Criteria**:
- [ ] Pre-loaded historical military spending/emissions data
- [ ] Show current analysis relative to historical average
- [ ] Link to Costs of War project data

---

## Epic 5: Export & Sharing

**Goal**: Enable users to share and reuse analysis results.

### User Stories

#### E5.1 - Report Generation
**As a** journalist  
**I want to** generate a professional report  
**So that** I can include it in my story or share with editors  

**Acceptance Criteria**:
- [ ] Generate PDF report with methodology, inputs, results
- [ ] Include charts and visualizations
- [ ] Customizable header/footer (organization name)
- [ ] Include data sources and citations

---

#### E5.2 - Data Export
**As a** researcher  
**I want to** download raw calculation data  
**So that** I can perform additional analysis  

**Acceptance Criteria**:
- [ ] Export to CSV with full detail
- [ ] Include all impact categories calculated
- [ ] Include input mapping (description → sector)
- [ ] Include metadata (model version, date)

---

#### E5.3 - Shareable Link
**As a** user  
**I want to** share my analysis via URL  
**So that** others can view or verify my results  

**Acceptance Criteria**:
- [ ] Generate unique URL for saved analysis
- [ ] URL loads exact inputs and results
- [ ] Optional: password protection
- [ ] Links expire after configurable period (default: 1 year)

---

#### E5.4 - Social Media Cards
**As a** advocate  
**I want to** share key metrics on social media  
**So that** I can raise awareness  

**Acceptance Criteria**:
- [ ] Generate Open Graph / Twitter Card metadata
- [ ] Create shareable image with key metrics
- [ ] Pre-filled sharing text with citation

---

#### E5.5 - Embed Widget
**As a** journalist  
**I want to** embed an interactive chart in my article  
**So that** readers can explore the data  

**Acceptance Criteria**:
- [ ] Generate embeddable iframe code
- [ ] Responsive design
- [ ] Minimal branding, customizable colors

---

## Epic 6: API & Integration

**Goal**: Enable programmatic access for advanced users and integration with other tools.

### User Stories

#### E6.1 - REST API
**As a** developer  
**I want to** access calculations via API  
**So that** I can integrate with my own tools  

**Acceptance Criteria**:
- [ ] RESTful API with JSON responses
- [ ] Endpoints for: calculate, list-sectors, list-impacts
- [ ] API key authentication
- [ ] Rate limiting (100 requests/hour free tier)
- [ ] OpenAPI/Swagger documentation

**API Endpoints**:
```
POST /api/v1/calculate
  Body: { sectors: [{code: "336411", amount: 1000000}] }
  Returns: { impacts: {ghg: 1234, energy: 5678, ...} }

GET /api/v1/sectors
  Returns: [{code: "336411", name: "Aircraft Manufacturing", ...}]

GET /api/v1/impacts
  Returns: [{code: "GWP", name: "Global Warming Potential", unit: "kg CO2e"}]
```

---

#### E6.2 - Bulk Calculation
**As a** researcher  
**I want to** submit batch calculations  
**So that** I can analyze large datasets efficiently  

**Acceptance Criteria**:
- [ ] Endpoint accepts array of calculations
- [ ] Async processing for large batches
- [ ] Webhook notification on completion

---

#### E6.3 - Webhook Integration
**As a** developer  
**I want to** receive notifications when data updates  
**So that** my dashboards stay current  

**Acceptance Criteria**:
- [ ] Register webhook URLs
- [ ] Notifications for: model updates, saved analysis changes

---

## Epic 7: Educational Content

**Goal**: Help users understand the methodology and context.

### User Stories

#### E7.1 - Methodology Documentation
**As a** researcher  
**I want to** read detailed methodology documentation  
**So that** I can assess the validity of results  

**Acceptance Criteria**:
- [ ] Comprehensive methodology page
- [ ] Mathematical formulas with explanation
- [ ] Data sources listed with links
- [ ] Limitations and assumptions clearly stated

---

#### E7.2 - Glossary
**As a** non-expert user  
**I want to** look up unfamiliar terms  
**So that** I can understand the results  

**Acceptance Criteria**:
- [ ] Searchable glossary
- [ ] Terms linked throughout interface
- [ ] Includes: sectors, impact categories, units

---

#### E7.3 - Tutorial / Walkthrough
**As a** new user  
**I want to** complete a guided tutorial  
**So that** I can learn how to use the tool  

**Acceptance Criteria**:
- [ ] Interactive walkthrough on first visit
- [ ] Skip option for experienced users
- [ ] Re-accessible from help menu

---

#### E7.4 - Context Articles
**As a** user  
**I want to** read background on military emissions  
**So that** I can better interpret results  

**Acceptance Criteria**:
- [ ] Article: "Why Military Emissions Matter"
- [ ] Article: "How Input-Output Models Work"
- [ ] Article: "History of Military Environmental Impact"
- [ ] Links to external resources (Costs of War, etc.)

---

## Epic 8: Advanced Analysis (Future)

**Goal**: Provide sophisticated analysis capabilities for expert users.

### User Stories (Deferred from MVP)

#### E8.1 - Scenario Modeling
Compare "what-if" scenarios (e.g., 10% budget cut)

#### E8.2 - Supply Chain Decomposition
Show tier-by-tier supply chain impacts

#### E8.3 - Sensitivity Analysis
Identify which parameters most affect results

#### E8.4 - Regional Allocation
Map impacts to geographic regions

#### E8.5 - Real-Time Monitoring
Dashboard tracking ongoing military spending impacts

---

## MVP Definition

### Phase 0: Foundation Work (Pre-MVP)
- **E0.1-E0.3**: Cornerstone engagement, version assessment, rebuild DIO on current useeior

### Included in MVP (Version 1.0)
- **E0.3** (completed): Updated DIO model on current USEEIO
- **E1.1-E1.3**: Basic to multi-sector calculation, essential impact categories
- **E2.1-E2.3**: Manual entry, CSV upload, NAICS mapping
- **E3.1-E3.2**: Summary metrics, sector breakdown
- **E4.1-E4.2**: Country comparison, everyday equivalents
- **E5.1-E5.2**: Report generation, data export
- **E7.1-E7.2**: Methodology docs, glossary

### Post-MVP (Version 1.x)
- **E0.4-E0.5**: Enhanced defense extensions, Cornerstone contribution
- **E2.4-E2.6**: AI classification, document parsing, USAspending integration
- **E3.3-E3.4**: Full impact comparison, time series
- **E4.3-E4.5**: Per-capita, program comparison, historical context
- **E5.3-E5.5**: Shareable links, social cards, embeds
- **E6**: Full API
- **E7.3-E7.4**: Tutorials, context articles

### Future (Version 2.0+)
- **E1.4**: Uncertainty estimation
- **E8**: Advanced analysis features

---

## Technical Specifications

### Technology Stack (Recommended)

**Frontend**:
- React 18+ (familiar ecosystem, component library support)
- Tailwind CSS (rapid styling)
- Recharts or D3 (visualizations)
- React-Query (data fetching)

**Backend**:
- Python 3.10+ (FastAPI framework)
- NumPy/Pandas (matrix calculations)
- PostgreSQL (data storage)
- Redis (caching)

**Infrastructure**:
- Docker containers
- GitHub Actions (CI/CD)
- Vercel or Railway (hosting)
- S3-compatible storage (exports)

### Data Files Required

| File | Source | Format | Size |
|------|--------|--------|------|
| DIO v2.0 Model | EPA | XLSX | ~10 MB |
| NAICS-BEA Crosswalk | EPA/BEA | CSV | <1 MB |
| Country Emissions | World Bank | CSV | <5 MB |
| Equivalents Library | Various | JSON | <100 KB |

### Performance Requirements

| Metric | Target |
|--------|--------|
| Single calculation | <2 seconds |
| CSV upload (1000 rows) | <10 seconds |
| Page load | <3 seconds |
| Report generation | <30 seconds |

---

## Sprint Planning (Suggested)

### Sprint 0: Cornerstone Engagement & Assessment (2 weeks)
- Introduce project to Cornerstone community
- Assess useeior version differences
- Set up development environment with current useeior
- Plan DIO migration approach

### Sprint 1: DIO Model Update (2 weeks)
- Rebuild DIO on useeior v1.7+
- Validate outputs against DIO v2.0
- Document changes and improvements
- Export updated model in multiple formats

### Sprint 2-3: Calculation Engine & Basic UI (4 weeks)
- Implement core calculation engine in Python (E1.1-E1.2)
- Build basic sector selection UI (E2.1)
- Create minimal results display
- CSV upload functionality (E2.2)

### Sprint 4-5: Input & Output Features (4 weeks)
- NAICS mapping (E2.3)
- Summary dashboard (E3.1-E3.2)
- Basic report export (E5.1-E5.2)

### Sprint 6-7: Context & Polish (4 weeks)
- Country comparisons (E4.1)
- Everyday equivalents (E4.2)
- Methodology documentation (E7.1-E7.2)
- Testing and bug fixes
- MVP launch preparation

### Total MVP Timeline: ~16 weeks (including DIO update phase)

---

## Success Metrics

| Metric | Target (6 months post-launch) |
|--------|-------------------------------|
| Registered users | 500 |
| Calculations performed | 5,000 |
| Reports generated | 500 |
| Media citations | 10 |
| Academic citations | 2 |
| API integrations | 3 |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| DIO model accuracy questioned | Medium | High | Document methodology thoroughly; cross-validate with Costs of War estimates |
| User classification errors | High | Medium | Provide sector descriptions; AI-assistance in v1.1 |
| Political sensitivity | Medium | High | Clear nonpartisan framing; focus on data transparency |
| EPA stops maintaining DIO | Low | High | Archive current data; plan for community maintenance |
| Performance issues at scale | Low | Medium | Caching; async processing; CDN |

---

## Open Questions

1. **Cornerstone Relationship**: What level of formal partnership with Cornerstone is appropriate? Should we contribute DIO directly to their ecosystem or maintain as independent project?

2. **USEEIO-CEDA Merger**: Cornerstone plans to merge USEEIO and CEDA into unified global MRIO. Should we wait for this or build on current USEEIO? How do we future-proof?

3. **Hosting**: Should we pursue .gov or .org domain? Consider institutional partnerships (universities, nonprofits, Cornerstone?)

4. **Governance**: How will the project be maintained long-term? Open source community model vs. institutional ownership vs. Cornerstone integration

5. **Validation**: Should we seek endorsement from Cornerstone/Dr. Ingwersen or maintain independent status?

6. **Monetization**: If needed, what ethical revenue models? (Grants, institutional subscriptions, consulting)

7. **International**: Future expansion to other countries' military spending? (Requires different IO models - could leverage CEDA through Cornerstone)

---

*Document Version: 1.0*  
*Last Updated: January 2026*  
*Status: Ready for stakeholder review*
