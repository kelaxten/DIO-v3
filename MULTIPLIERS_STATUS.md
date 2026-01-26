# Environmental Multipliers Status Report

## Current State

### What We're Using Now
The backend currently uses **estimated multipliers** based on typical values from environmental economics literature and EPA documentation. These are approximations, not actual DIO v2.0 model results.

**Current multipliers** (baseline per $1000 spending):
- GHG: 150 kg CO2 eq
- Energy: 2,500 MJ
- Water: 3,000 gallons
- Land: 10 m2-year

With sector-specific adjustment factors (e.g., aircraft manufacturing × 2.2, ammunition × 1.8).

### Why We're Not Using Real DIO Multipliers Yet

The DIO v2.0 model structure is complex:

1. **A Matrix** (45,716 rows) - Economic transactions between 246 BEA sectors
2. **B Matrix** (62,481 rows) - Environmental flows from 376 production processes
3. **Process-to-Sector Mapping** - Needed to aggregate process-level emissions to sectors

**The Challenge**: The B matrix contains emissions at the *process level* (e.g., "Natural gas combustion in large burners"), but we need multipliers at the *sector level* (e.g., "Aircraft Manufacturing - 336411").

## What Real DIO Multipliers Would Include

The complete DIO model calculates **total multipliers** as:

```
M = B * L
```

Where:
- **B** = Environmental flows per unit of production (from satellite tables)
- **L** = Leontief inverse matrix (I - A)^-1 (captures supply chain effects)
- **M** = Total environmental impact per dollar of final demand

This includes:
- **Direct effects**: Emissions from the sector itself
- **Indirect effects**: Emissions from the entire supply chain

For example, buying a $1M aircraft doesn't just cause emissions from aircraft manufacturing - it also causes emissions from:
- Steel production (for the aircraft frame)
- Electronics manufacturing (for avionics)
- Rubber production (for tires)
- Electricity generation (for the factory)
- Transportation (shipping components)
- And dozens more sectors in the supply chain

## Data Sources in DIO v2.0

According to the model specification (DIOv2.0.yml), the actual sources are:

| Category | Source | Year |
|----------|--------|------|
| **GHG** | EPA GHG Inventory | 2016 |
| **Water** | USGS Water Use Survey | 2015 |
| **Land** | USDA Major Land Uses + EIA surveys | 2012 |
| **Energy** | USEEIO v1.1 Energy tables | 2014 |
| **Air Emissions** | EPA NEI + TRI | 2017 |

## Available DIO Files

We have:
- ✅ `A_Matrix_DIO.csv` - Economic transactions (6.7 MB)
- ✅ `B_Matrix_DIO.csv` - Environmental flows (10 MB)
- ✅ `DIOv2.0.yml` - Model specification
- ❌ `DIO.rds` - Pre-built model (file corrupted, only 133 bytes)
- ❌ `N_Matrix` - Impact multipliers (not extracted yet)

## Path Forward: Three Options

### Option 1: Calculate from Raw Data (Most Accurate, Most Complex)
**Steps**:
1. Build A matrix in proper 246×246 form from CSV
2. Calculate Leontief inverse: L = (I - A)^-1
3. Create process-to-sector mapping from DIOProcesses.yml
4. Aggregate B matrix from process level to sector level
5. Calculate M = B * L
6. Extract multipliers for all 246 sectors

**Pros**: Most accurate, includes full supply chain effects
**Cons**: Complex, requires proper process-sector mapping, computational

**Estimated Effort**: 2-3 days of development + validation

### Option 2: Rebuild DIO Model in R (Accurate, Standard Method)
**Steps**:
1. Install R and useeior package from Cornerstone
2. Run `DIO_Cornerstone.Rmd` to build the model
3. Extract N matrix (total multipliers) from built model
4. Export to JSON for backend

**Pros**: Uses EPA's official methodology, well-documented
**Cons**: Requires R environment, model build takes ~30min, large dependencies

**Estimated Effort**: 1 day setup + build time

### Option 3: Use EPA Published Results (Quick, but Limited)
**Steps**:
1. Find published DIO v2.0 results/documentation from EPA
2. Extract sector-level multipliers from tables/appendices
3. Manual data entry for 246 sectors

**Pros**: Fast, uses peer-reviewed values
**Cons**: May not have all sectors, less flexible for updates

**Estimated Effort**: Few hours if data is available

## Recommended Approach

I recommend **Option 2** (Rebuild DIO Model in R) because:

1. **Official Method**: Uses EPA's standard tooling
2. **Complete**: Gets us all 246 sectors with validated multipliers
3. **Documented**: useeior package has extensive documentation
4. **Maintainable**: Can be re-run if data updates
5. **Verifiable**: Results can be compared against EPA publications

## Validation Strategy

Once we have real multipliers, we should validate by:

1. **Sanity Checks**:
   - GHG multipliers should be 200-1000 kg CO2/USD for manufacturing
   - Service sectors should be 50-200 kg CO2/USD
   - Energy-intensive sectors (refineries, metals) should be highest

2. **Comparison to Literature**:
   - Cross-check against EIO-LCA (Carnegie Mellon)
   - Compare to USEEIO sector averages
   - Check against published DIO documentation

3. **Example Calculations**:
   - Calculate impacts for known defense programs (F-35, etc.)
   - Compare to published estimates from:
     - Costs of War project (Brown University)
     - Neta Crawford's research
     - EPA's own DIO case studies

4. **Sector Relationships**:
   - Verify that aircraft > automobiles
   - Verify that manufacturing > services
   - Check that rankings make sense

## Impact on Current Application

### Current Accuracy
- **Orders of magnitude**: Likely correct (hundreds of kg CO2 per $1000)
- **Relative rankings**: Probably reasonable (manufacturing > services)
- **Absolute values**: Could be off by 2-5x for individual sectors
- **Supply chain effects**: Not fully captured (direct effects only)

### User Communication
We should add a disclaimer to the frontend:

> **Data Note**: Environmental impact estimates are currently based on literature averages and sector adjustments. Full DIO v2.0 model multipliers (including supply chain effects) are being integrated. Results should be considered preliminary estimates.

## Next Steps

1. **Immediate**: Add data quality disclaimer to frontend
2. **Short-term**: Rebuild DIO model in R to extract real multipliers
3. **Medium-term**: Implement proper validation against published results
4. **Long-term**: Set up automated pipeline to update with new EPA data

## Questions for Discussion

1. **Accuracy requirements**: What level of precision do you need for your use case?
2. **Timeline**: How soon do you need validated multipliers?
3. **Transparency**: Should we show users data quality indicators per sector?
4. **Features**: Would you like confidence intervals or uncertainty ranges?

---

**Status**: PRELIMINARY MULTIPLIERS IN USE
**Last Updated**: 2026-01-24
**Next Review**: After DIO model rebuild
