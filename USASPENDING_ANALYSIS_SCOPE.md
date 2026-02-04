# USAspending.gov Defense Budget Analysis - Scope & Plan

**Goal**: Run comprehensive environmental impact analysis of US defense budget using actual contract data from USAspending.gov, creating both pre-computed analyses for users to explore AND a compelling paper/article for launch.

---

## Executive Summary

**Feasibility**: ✅ Highly feasible - USAspending.gov has free public API with all DOD contract data including NAICS codes

**Estimated Effort**: 15-20 hours development + 10-15 hours analysis/writing

**Estimated Costs**: $0-50/month (optional: upgraded hosting for better performance)

**Timeline**: 2-3 weeks to first publication-ready analysis

**Launch Story**: "The $850 Billion Question: Environmental Impact of US Defense Spending in FY2024"

---

## Part 1: Technical Implementation

### 1.1 USAspending.gov API Integration

**API Documentation**: https://api.usaspending.gov/

**What's Available**:
- All federal contracts, grants, loans, direct payments
- NAICS codes for each award
- Dollar amounts by fiscal year
- Agency/sub-agency breakdowns
- Detailed award descriptions
- Historical data back to 2008

**API Endpoints We Need**:

```python
# Endpoint 1: Search awards by agency
POST https://api.usaspending.gov/api/v2/search/spending_by_award/

# Example request for DOD FY2024
{
  "filters": {
    "agencies": [{"type": "funding", "tier": "toptier", "name": "Department of Defense"}],
    "time_period": [{"start_date": "2023-10-01", "end_date": "2024-09-30"}]
  },
  "fields": ["Award Amount", "NAICS Code", "Award Description"],
  "limit": 100000  # May need pagination
}

# Endpoint 2: Spending by category
POST https://api.usaspending.gov/api/v2/search/spending_by_category/naics/

# This aggregates by NAICS automatically - perfect for our use case!
```

**Implementation Steps**:
1. Create `usaspending_fetcher.py` module
2. Authenticate (no API key required for basic use, optional key for higher rate limits)
3. Fetch DOD awards by fiscal year
4. Aggregate by NAICS code
5. Map NAICS to DIO sectors using existing crosswalk
6. Run DIO calculation
7. Store results

**Rate Limits**:
- No authentication: 100 requests/hour
- With API key (free): 1,000 requests/hour
- With API key + IP whitelist (free for researchers): 10,000 requests/hour

**Data Volume Estimate**:
- FY2024 DOD contracts: ~100,000-150,000 individual awards
- After NAICS aggregation: ~300-400 sector totals (maps to our 396 sectors)
- Single API call can return aggregated data ✅

### 1.2 NAICS to DIO Sector Mapping

**What We Have**:
- DIO uses BEA 2017 sector codes (396 sectors)
- USAspending uses NAICS 2017 codes (6-digit)
- We have BEA-to-NAICS crosswalk data in cornerstone-useeior

**Mapping Logic**:
```python
def map_naics_to_dio_sector(naics_6digit: str) -> str:
    """
    Map 6-digit NAICS to DIO/BEA sector code

    Uses crosswalk from BEA:
    - Many NAICS codes map to single BEA sector
    - Some NAICS are split proportionally
    """
    # Load from cornerstone-useeior/inst/extdata/23_BEAtoUSEEIOtoNAICS_2017.csv
    # Return BEA sector code
```

**Challenges**:
- Some contracts have missing/invalid NAICS codes (~5-10%)
- Solution: Use award description + AI classification (E2.4 feature)
- For MVP: Flag as "Unclassified" and report separately

### 1.3 Data Processing Pipeline

```
┌─────────────────┐
│ USAspending API │
│ (DOD FY2024)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fetch & Filter  │  - Filter by DOD agencies
│                 │  - Aggregate by NAICS
│                 │  - ~150K awards → 396 sectors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Map NAICS→DIO   │  - Use BEA crosswalk
│                 │  - Handle unmapped codes
│                 │  - Proportional allocation
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ DIO Calculation │  - Run existing calculator
│                 │  - GHG, Energy, Water, Land
│                 │  - Sector breakdown
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Store Results   │  - PostgreSQL (detailed)
│                 │  - JSON cache (for frontend)
│                 │  - CSV export (for analysis)
└─────────────────┘
```

**Processing Time Estimate**:
- API fetch: 2-5 minutes (with aggregation endpoint)
- NAICS mapping: 10-30 seconds
- DIO calculation: <1 second (single multi-sector calculation)
- Total: <10 minutes for full FY analysis

### 1.4 Frontend Integration - Pre-Computed Analysis Explorer

**New Feature**: "Explore US Defense Budget Impact"

```
┌────────────────────────────────────────────────┐
│  🇺🇸 US Defense Budget Environmental Impact   │
│                                                │
│  Fiscal Year: [2024 ▼]                        │
│                                                │
│  Total Budget Analyzed: $849.8 Billion        │
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │ 🌡️ Greenhouse Gas Emissions             │ │
│  │    304 Million Metric Tons CO2e          │ │
│  │    Equivalent to: 66 million cars/year   │ │
│  │    Ranking: #6 globally (if a country)   │ │
│  └──────────────────────────────────────────┘ │
│                                                │
│  [View by Branch] [View by Sector] [Export]   │
│                                                │
│  Top Impact Sectors:                           │
│  ├─ Aircraft Manufacturing: $78.2B → 9.8M tons│
│  ├─ Petroleum Refineries: $45.1B → 13.2M tons │
│  ├─ Ship Building: $32.4B → 4.8M tons         │
│  └─ [See all 109 sectors]                     │
└────────────────────────────────────────────────┘
```

**Breakdown Views**:
1. **By Military Branch**: Army, Navy, Air Force, Marines, Space Force
2. **By Contract Type**: Procurement, R&D, Services, Construction
3. **By Major Program**: F-35, Columbia-class subs, etc.
4. **By Sector**: All 396 economic sectors
5. **Time Series**: FY2020-2024 trends

---

## Part 2: Analysis Scope

### 2.1 Fiscal Years to Analyze

**Priority 1 - MVP Launch**:
- **FY2024** (Oct 2023 - Sep 2024): Most recent complete year
  - Budget: ~$850 billion
  - Data available: ✅ Complete
  - Use for launch article

**Priority 2 - Context**:
- **FY2023**: Comparison baseline
- **FY2022**: Post-COVID normalization
- **FY2021**: COVID-affected year

**Priority 3 - Trends**:
- **FY2020-2024** (5-year trend): Show trajectory
- **FY2015-2024** (10-year trend): Longer context

### 2.2 Analysis Breakdowns

**Geographic**:
- By military branch (Army, Navy, Air Force, Marines, Space Force, DOD-wide)
- By command (NORTHCOM, CENTCOM, EUCOM, etc.)
- Domestic vs. overseas spending

**Programmatic**:
- By appropriation category:
  - Military Personnel: ~$180B
  - Operations & Maintenance: ~$300B
  - Procurement: ~$170B
  - R&D: ~$140B
  - Military Construction: ~$10B
  - Family Housing: ~$2B

**Major Weapons Systems**:
- F-35 Joint Strike Fighter (~$12B/year)
- Columbia-class submarines (~$6B/year)
- B-21 Raider bomber (~$3B/year)
- Ford-class carriers (~$2B/year)
- Etc.

**Sector Analysis**:
- Top 20 sectors by spending
- Top 20 sectors by GHG emissions
- Defense-relevant sectors (109 sectors)
- Efficiency analysis (impact per dollar)

### 2.3 Key Metrics to Calculate

**Total Impact**:
- GHG emissions (Mt CO2e)
- Energy consumption (PJ)
- Water use (billion gallons)
- Land use (km²-years)

**Comparisons**:
- Country equivalents (e.g., "Equal to Australia's annual emissions")
- Everyday equivalents (cars, homes, flights)
- As % of total US emissions (~13% based on literature)
- Per-dollar efficiency

**Trends**:
- Year-over-year change in emissions
- Change in energy intensity
- Correlation with budget changes

---

## Part 3: Launch Content Strategy

### 3.1 Academic Paper Option

**Title**: "Environmental Footprint of US Defense Spending: An Input-Output Analysis of FY2024"

**Structure**:
1. **Abstract** (250 words)
2. **Introduction** (1,500 words)
   - Military environmental impacts understudied
   - Existing research gaps
   - Our contribution: comprehensive IO analysis
3. **Methodology** (2,000 words)
   - DIO model overview
   - Data sources (USAspending, Cornerstone, EIA)
   - NAICS-to-sector mapping
   - Uncertainty analysis
4. **Results** (3,000 words)
   - Total impacts by category
   - Sector breakdown
   - Branch comparison
   - Major programs analysis
5. **Discussion** (2,000 words)
   - Comparison to prior estimates
   - Policy implications
   - Limitations
6. **Conclusion** (500 words)

**Target Journals**:
- *Environmental Science & Technology* (Impact Factor: 11.4)
- *Journal of Industrial Ecology* (IF: 5.9)
- *Environmental Research Letters* (IF: 6.7)
- *Ecological Economics* (IF: 6.6)

**Timeline**: 6-12 months (peer review)

### 3.2 Long-Form Article / Report Option (FASTER)

**Title**: "The $850 Billion Question: Environmental Impact of US Defense Spending in FY2024"

**Format**: ~5,000 word investigative article with interactive visualizations

**Structure**:
1. **Executive Summary** (500 words)
   - Key findings
   - Main policy implications
2. **Background** (800 words)
   - Why military emissions matter
   - Reporting exemptions
   - Scale of defense spending
3. **Methodology** (600 words)
   - How we calculated impacts
   - Data sources
   - Transparency & reproducibility
4. **Findings** (2,000 words)
   - Total emissions: 304M tons CO2e
   - Where it goes: sector breakdown
   - What's driving it: major programs
   - Trends over time
5. **Context** (800 words)
   - Comparison to countries
   - % of US total emissions
   - Per-capita allocation
6. **Implications** (800 words)
   - Climate policy gap
   - Acquisition reform opportunities
   - Transparency recommendations
7. **Conclusion** (500 words)

**Publication Venues**:
- **Quincy Institute** (defense policy think tank)
- **Costs of War Project** (Brown University)
- **The Intercept** / **ProPublica** (investigative journalism)
- **Medium** / **Substack** (self-published with wide distribution)
- **arXiv** (preprint for academic visibility)

**Timeline**: 2-4 weeks

### 3.3 Interactive Web Feature (RECOMMENDED FOR LAUNCH)

**"Explore the Environmental Cost of Defense Spending"**

**Components**:
1. **Landing Page**: Summary + key visualizations
2. **Interactive Explorer**: Filter by year/branch/sector
3. **Sector Deep Dive**: Click any sector to see details
4. **Methodology Page**: Full transparency
5. **Download Data**: CSV exports for researchers

**Visualizations**:
- Treemap: Sectors by spending size, colored by emissions intensity
- Sankey diagram: Money flow → Sectors → Environmental impacts
- Time series: Trends over 5 years
- Map: Geographic distribution (if data available)
- Comparison bar chart: Military vs. countries

**SEO & Distribution**:
- Title: "US Military Emissions: [X]M Tons CO2 from $850B Budget"
- Meta description optimized for search
- Social cards with key stats
- Submit to Hacker News, Reddit, etc.
- Press release to defense/climate journalists

---

## Part 4: Cost Analysis

### 4.1 Development Costs

| Item | Time | Cost (if outsourced @ $75/hr) |
|------|------|-------------------------------|
| USAspending API integration | 8 hours | $600 |
| NAICS mapping logic | 4 hours | $300 |
| Data processing pipeline | 6 hours | $450 |
| Frontend explorer UI | 12 hours | $900 |
| Visualizations | 8 hours | $600 |
| Testing & QA | 4 hours | $300 |
| **Total Development** | **42 hours** | **$3,150** |

**If you do it yourself**: $0 (just time)

### 4.2 Infrastructure Costs

| Service | Free Tier | Paid Tier | Recommended |
|---------|-----------|-----------|-------------|
| USAspending API | ✅ Free | ✅ Free (researcher tier) | Free |
| Backend (Render) | ✅ Free (cold starts) | $7/mo (no cold starts) | $7/mo |
| Database (Render PostgreSQL) | ✅ Free (1GB) | $7/mo (10GB) | Free for now |
| Frontend (GitHub Pages) | ✅ Free | - | Free |
| Domain (optional) | - | $12/year | Optional |
| CDN (Cloudflare) | ✅ Free | - | Free |

**Total Infrastructure**: **$0-7/month** (or $0-84/year)

### 4.3 Data Processing Costs

| Item | Cost |
|------|------|
| USAspending API access | $0 (free) |
| Compute (one-time analysis) | $0 (local/free tier) |
| Storage (5 years of results) | $0 (< 100MB) |
| **Total** | **$0** |

### 4.4 Content Creation Costs

| Item | Time | Cost (if outsourced @ $100/hr) |
|------|------|-------------------------------|
| Data analysis | 8 hours | $800 |
| Article writing | 12 hours | $1,200 |
| Fact-checking | 4 hours | $400 |
| Editing | 4 hours | $400 |
| Visual design | 6 hours | $600 |
| **Total Content** | **34 hours** | **$3,400** |

**If you write yourself**: $0 (just time)

---

## Part 5: Implementation Plan

### Phase 1: Data Integration (Week 1)
**Deliverable**: Automated DOD budget analysis from USAspending

- [ ] Set up USAspending API access (request researcher tier)
- [ ] Build `usaspending_fetcher.py` module
- [ ] Implement NAICS-to-DIO mapping using BEA crosswalk
- [ ] Test with FY2024 data
- [ ] Validate results against known defense budget totals
- [ ] Create automated pipeline script

**Output**: `analyze_dod_budget.py` script that produces full analysis

### Phase 2: Pre-Computed Analysis Storage (Week 1-2)
**Deliverable**: Stored analysis results for frontend

- [ ] Design database schema for storing analyses
- [ ] Run FY2024 analysis and store results
- [ ] Run FY2023, FY2022, FY2021 for comparison
- [ ] Create JSON API endpoints for frontend
- [ ] Add caching layer

**Output**: API endpoints for pre-computed analyses

### Phase 3: Frontend Explorer (Week 2)
**Deliverable**: Interactive budget explorer

- [ ] Create "Explore Budget" page
- [ ] Fiscal year selector
- [ ] Summary dashboard
- [ ] Branch breakdown view
- [ ] Sector breakdown view
- [ ] Export functionality

**Output**: User-facing budget explorer

### Phase 4: Analysis & Writing (Week 2-3)
**Deliverable**: Launch article/paper

- [ ] Deep analysis of FY2024 results
- [ ] Identify key findings and narratives
- [ ] Write article (5,000 words)
- [ ] Create visualizations
- [ ] Fact-check and edit
- [ ] Prepare for publication

**Output**: Publication-ready article

### Phase 5: Launch (Week 3-4)
**Deliverable**: Public release

- [ ] Publish article to selected venue
- [ ] Launch updated website with budget explorer
- [ ] Press release to relevant journalists
- [ ] Social media campaign
- [ ] Post to Hacker News, Reddit, etc.
- [ ] Monitor coverage and feedback

**Output**: Public launch with media coverage

---

## Part 6: Expected Findings (Preliminary Estimates)

Based on existing research (Crawford 2019, Belcher et al. 2020) and our data quality:

**FY2024 Defense Budget**: ~$850 billion

**Estimated Total Impacts**:
- **GHG Emissions**: 250-350 million metric tons CO2e
  - Equivalent to: 55-75 million cars
  - Ranking: #5-8 globally (if a country, between Japan and Germany)
  - % of US total: 4-6% of ~6,000 Mt US total

- **Energy Consumption**: 6,000-8,000 PJ
  - Equivalent to: 1.6-2.1 trillion kWh
  - % of US total: ~5-7% of 100 quadrillion BTU US total

- **Water Use**: 1,500-2,500 billion gallons
  - Equivalent to: Annual use of 10-17 million households

**Top Contributing Sectors** (anticipated):
1. Aircraft Manufacturing (~$78B) → ~9.8M tons CO2e
2. Petroleum Refineries (~$45B) → ~13.2M tons CO2e
3. Ship Building (~$32B) → ~4.8M tons CO2e
4. Electronics Manufacturing (~$28B) → ~2.8M tons CO2e
5. Professional Services (~$65B) → ~6.5M tons CO2e

**By Military Branch** (rough estimate based on budget share):
- Air Force (29%): ~$246B → 70-100M tons CO2e
- Navy (28%): ~$238B → 65-95M tons CO2e
- Army (27%): ~$230B → 60-90M tons CO2e
- DOD-wide (16%): ~$136B → 35-50M tons CO2e

---

## Part 7: Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| NAICS codes missing/wrong | Medium | Medium | Use AI classification for unmapped; document % unmapped |
| API rate limiting | Low | Low | Request researcher tier; implement caching |
| Data size too large | Low | Medium | Use aggregation endpoints; paginate if needed |
| Results disputed | Medium | High | Full methodology transparency; cite sources; peer review |
| Political backlash | Medium | Medium | Nonpartisan framing; focus on data/transparency |
| Scooped by other org | Low | Medium | Move quickly; unique angle (sector-level detail) |

---

## Part 8: Success Metrics

**Launch Goals (First Month)**:
- [ ] 10,000+ article views
- [ ] 5+ media citations
- [ ] 1,000+ budget explorer users
- [ ] 100+ data downloads
- [ ] 1+ academic citation/reference

**Long-Term Goals (6 Months)**:
- [ ] 50,000+ total views
- [ ] 20+ media citations
- [ ] Cited in congressional testimony/report
- [ ] Academic paper published or under review
- [ ] Tool used by 5+ organizations

---

## Part 9: Recommended Approach

**For MVP Launch**, I recommend:

1. **Focus on FY2024 analysis** (most recent complete year)
2. **Build USAspending integration** (15-20 hours)
3. **Write 5,000-word article** with key findings (15-20 hours)
4. **Create interactive explorer** for website (10-15 hours)
5. **Publish as web feature** (fastest path to impact)

**Total effort**: ~40-55 hours
**Total cost**: $0-7/month (hosting)
**Timeline**: 2-3 weeks

**Launch with**:
- Article: "The $850 Billion Question: Environmental Impact of US Defense Spending"
- Interactive tool showing FY2024 breakdown
- Full data transparency & downloadable CSVs
- Press outreach to defense/climate journalists

**Follow-up with**:
- Academic paper submission (6-12 month timeline)
- Yearly updates (FY2025, FY2026, etc.)
- Expansion to other government spending

---

## Next Steps

**Immediate (This Session/Next)**:
1. Set up USAspending API access
2. Test fetching FY2024 DOD data
3. Validate NAICS mapping works
4. Run preliminary analysis

**This Week**:
1. Build automated pipeline
2. Run full FY2024 analysis
3. Start data analysis for article

**Next Week**:
1. Write article draft
2. Build frontend explorer
3. Create visualizations

**Week 3**:
1. Edit and finalize article
2. Launch preparation
3. Public release

---

**Questions for Decision**:

1. **Content format**: Academic paper (slow, prestigious) vs. Long-form article (fast, wide reach)?
2. **Scope**: FY2024 only vs. 5-year trends?
3. **Launch venue**: Self-publish vs. partner with organization (Quincy, Costs of War)?
4. **Author attribution**: Your name? Organizational affiliation? Anonymous?
5. **Licensing**: All data/code open source?

---

*Document Version: 1.0*
*Created: 2026-01-29*
