# Energy Multipliers for Open DIO

## Objective

Calculate energy consumption multipliers for all 396 economic sectors using government data sources to enable complete environmental impact analysis.

## Methodology

### 1. Data Sources (Government & Academic Only)

#### Primary: EIA (Energy Information Administration) - U.S. Department of Energy

**Manufacturing Energy Consumption Survey (MECS)**
- Source: https://www.eia.gov/consumption/manufacturing/
- Latest: 2018 MECS (2014 and 2010 also available)
- Coverage: Manufacturing sectors (NAICS 31-33)
- Metrics: Energy consumption by fuel type and sector
- Unit: Trillion BTU

**Commercial Buildings Energy Consumption Survey (CBECS)**
- Source: https://www.eia.gov/consumption/commercial/
- Latest: 2018 CBECS
- Coverage: Commercial buildings and services
- Metrics: Energy use by building type and activity

**Annual Energy Outlook (AEO)**
- Source: https://www.eia.gov/outlooks/aeo/
- Provides energy intensity estimates by sector

#### Secondary: BEA (Bureau of Economic Analysis)

**Gross Output by Industry**
- Source: https://apps.bea.gov/iTable/
- Provides economic output data ($) by NAICS sector
- Needed to calculate energy per dollar

#### Tertiary: EPA USEEIO Model Documentation

**Energy Satellite Table**
- From DIO v2.0 configuration
- Uses EIA Monthly Energy Review + Form EIA-923
- Data year: 2014 (can be updated with newer EIA data)

### 2. Calculation Approach

**Step 1: Direct Energy Intensity (B matrix)**

For each sector *i*:
```
Energy Intensity_i = Total Energy Use_i / Economic Output_i
```

Where:
- Total Energy Use from EIA MECS/CBECS (BTU or MJ)
- Economic Output from BEA (USD)
- Result: MJ per $1 of output

**Step 2: Supply Chain Multipliers (Leontief Inverse)**

Total energy multipliers including supply chain:
```
M_energy = B_energy × L
```

Where:
- B_energy = Direct energy intensity vector (from Step 1)
- L = Leontief inverse matrix (already have from DIO model)
- M_energy = Total energy multipliers (MJ per $1)

**Step 3: Convert to per-$1000 basis**
```
Multiplier = M_energy × 1000
```

Result: MJ per $1000 spending

### 3. Sector Mapping Strategy

**Manufacturing Sectors (NAICS 31-33): ~100 sectors**
- Use MECS direct sector matches
- High confidence data

**Commercial/Services (NAICS 42-81): ~150 sectors**
- Use CBECS by building/activity type
- Match sectors to building categories (e.g., warehouses, offices, retail)

**Primary Sectors (Agriculture, Mining): ~40 sectors**
- Use AEO energy intensity estimates
- Cross-reference with academic literature

**Other Sectors (Construction, Utilities, Transportation): ~100 sectors**
- Use published EIA/DOE energy intensity factors
- Well-documented in energy economics literature

### 4. Quality Control

**Validation Checks:**
1. Compare manufacturing sector values to published MECS benchmarks
2. Cross-check total U.S. energy use (sum of all sectors) with EIA total energy statistics
3. Ensure energy-intensive sectors (refineries, smelters) have high values
4. Ensure service sectors have low values

**Uncertainty Ranges:**
- Manufacturing (MECS data): ±20-25%
- Services (CBECS data): ±30-35%
- Estimated sectors: ±40-50%

### 5. Data Gaps & Estimates

For sectors without direct EIA data:

**Method A: Sector Similarity**
```
Energy_unknown = Energy_similar_sector × adjustment_factor
```

Example:
- "Guided Missile Manufacturing" lacks specific data
- Use "Aircraft Manufacturing" as proxy with 10% adjustment for complexity

**Method B: Input-Output Inference**
```
Energy_i = Σ(Energy_j × A_ji)
```

Where A_ji is the amount of sector j needed to produce $1 of sector i (from DIO A matrix)

**Method C: Literature Values**
- Carnegie Mellon EIO-LCA database
- EPA sector profiles
- Academic energy economics papers

### 6. Implementation Plan

**Phase 1: High-Confidence Sectors (Week 1)**
- Extract manufacturing energy from MECS tables
- Match to NAICS codes
- Calculate direct intensities

**Phase 2: Commercial Sectors (Week 1-2)**
- Map NAICS to CBECS building types
- Calculate service sector intensities

**Phase 3: Remaining Sectors (Week 2)**
- Estimate using similarity method
- Apply IO inference where possible

**Phase 4: Supply Chain Integration (Week 2-3)**
- Apply Leontief inverse
- Calculate total multipliers
- Validate against benchmarks

**Phase 5: Documentation (Week 3)**
- Document all assumptions
- Cite all data sources
- Create methodology writeup

### 7. Expected Results

**Range of Energy Multipliers (MJ/$1000):**

| Sector Type | Range (MJ/$1000) | Examples |
|-------------|------------------|----------|
| Energy-Intensive Mfg | 15,000 - 50,000 | Aluminum smelting, petroleum refining |
| Standard Manufacturing | 5,000 - 15,000 | Aircraft, vehicles, machinery |
| Light Manufacturing | 2,000 - 5,000 | Electronics, pharmaceuticals |
| Services | 500 - 2,000 | Professional services, IT |
| Office-based | 200 - 500 | Finance, consulting |

**Comparison to Current GHG Multipliers:**

Energy and GHG should correlate:
```
Correlation coefficient: Expected r > 0.7
```

High GHG sectors (combustion-heavy) should also have high energy use.

### 8. Academic References

**Energy Input-Output Analysis:**
1. Miller & Blair (2009). "Input-Output Analysis: Foundations and Extensions." Cambridge University Press.
2. Bullard, C.W., & Herendeen, R.A. (1975). "The energy cost of goods and services." Energy Policy, 3(4), 268-278.
3. Carnegie Mellon EIO-LCA: http://www.eiolca.net/

**EIA Energy Intensity:**
4. EIA MECS Documentation: https://www.eia.gov/consumption/manufacturing/about.php
5. EIA Energy Intensity Indicators: https://www.eia.gov/totalenergy/data/monthly/

**USEEIO Energy Methods:**
6. Ingwersen et al. (2022). "USEEIO: A US Environmentally-Extended Input-Output Model." Applied Sciences.

### 9. Compliance with DIO/USEEIO Framework

**Consistent with DIO v2.0:**
- ✅ Uses same BEA IO structure (2012 Detail level)
- ✅ Same Leontief methodology
- ✅ Government data sources (EIA = DOE)
- ✅ Follows USEEIO satellite table approach

**Extension, not replacement:**
- DIO v2.0 has ENERGY satellite table defined
- Our implementation fills gap where Cornerstone v1.4.0 lacks energy data
- Uses same methodological framework

**Transparent & Reproducible:**
- All calculations documented
- Data sources cited
- Assumptions explicit
- Code open source

### 10. Next Steps

1. **Download EIA MECS 2018 tables** (public, no API key needed)
2. **Download BEA gross output data** (public)
3. **Create Python script** to calculate direct intensities
4. **Apply Leontief inverse** from existing DIO A matrix
5. **Validate** against published benchmarks
6. **Document** in ENERGY_METHODOLOGY.md
7. **Update** backend multipliers.json
8. **Deploy** to production

**Timeline: 2-3 weeks for complete, validated dataset**

---

## Decision: Proceed?

**Pros:**
- Fills critical gap (energy currently = 0)
- Uses only government sources (EIA, BEA)
- Methodologically sound (IO analysis)
- Consistent with DIO/USEEIO framework
- Fully transparent and reproducible

**Cons:**
- Requires data processing work (2-3 weeks)
- Some sectors require estimation
- Uncertainty ranges higher than GHG (±30-40% vs ±25%)

**Recommendation:** **PROCEED**

This approach is academically rigorous, uses only government sources, and follows established environmental IO methodology. The result will be a complete, validated energy multipliers dataset that complements the Cornerstone GHG data.
