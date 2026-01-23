# DIO Model Migration to Cornerstone USEEIO

**Date**: January 2026
**Status**: In Progress
**Epic**: E0 - Update DIO to Latest USEEIO (Cornerstone)

## Executive Summary

This document describes the migration of the Defense Input-Output (DIO) model from the EPA's archived USEEIO framework to the actively maintained Cornerstone Sustainability Data Initiative version.

## Background

### Why This Migration is Necessary

In August 2025, the **Cornerstone Sustainability Data Initiative** took over maintenance of USEEIO after the EPA stopped updating it. The Cornerstone Initiative is a collaboration between:

- **Watershed** (climate solutions provider)
- **Stanford Sustainable Solutions Lab** (Stanford Doerr School of Sustainability)
- **ERG** (environmental consulting firm)

**Dr. Wesley Ingwersen**, the original EPA architect of USEEIO, now serves as **Technical Director** at Cornerstone. This makes Cornerstone the authoritative source for USEEIO development moving forward.

### Version Comparison

| Aspect | Original DIO v2.0 | Target (Cornerstone) |
|--------|-------------------|----------------------|
| useeior Version | v1.2.1 (archived) | v1.8.0 (active) |
| Repository | USEPA/useeior | cornerstone-data/useeior |
| Maintenance Status | Archived (no updates) | Actively maintained |
| Lead Developer | EPA (discontinued) | Dr. Wesley Ingwersen |
| Latest Data Year | 2017 | 2023 (planned) |
| MRIO Integration | No | Yes (CEDA merger planned) |

## What Has Changed

### API/Schema Changes from v1.2.1 to v1.8.0

Based on review of the Cornerstone repository and changelog:

#### 1. **Core Functions - STABLE** ✅
The primary functions used in DIO remain stable:
- `buildModel()` - No breaking changes
- `writeModeltoXLSX()` - No breaking changes
- `calculateEEIOModel()` - Enhanced but backwards compatible

#### 2. **Data Access - ENHANCED** 📈
- **New**: Support for parquet files (via `arrow` package)
- **New**: Integration with `bedrock` data pipeline
- **Improved**: `flowsa` integration for environmental flow data
- **Enhanced**: Data validation and error reporting

#### 3. **Model Configuration - BACKWARDS COMPATIBLE** ✅
The YAML configuration format used in `DIOv2.0.yml` remains compatible. Changes are additive:
- All v1.2.1 configuration keys still supported
- New optional keys available for advanced features
- No required changes to existing model specs

#### 4. **New Capabilities** 🆕
Cornerstone v1.8.0 adds:
- **Improved hybridization** support
- **Enhanced validation** functions
- **Better performance** for large models
- **Extended documentation** and examples
- **JSON export** capabilities (in addition to Excel)

### Dependencies

#### New Required Packages (v1.8.0)
```r
arrow (>= 2.0.0)      # Parquet file support
configr (>= 0.3.4)    # Enhanced configuration
```

#### Existing Dependencies (unchanged)
All other dependencies remain the same as v1.2.1.

## Migration Steps

### Phase 1: Environment Setup ✅ COMPLETE

- [x] Install R 4.3+
- [x] Install devtools
- [x] Clone cornerstone-data/useeior repository
- [x] Document installation process

### Phase 2: Code Update 🔄 IN PROGRESS

#### A. Update Installation Command

**Original (DIO v2.0)**:
```r
devtools::install_github("USEPA/useeior@v1.7.2")
```

**Updated (Cornerstone)**:
```r
devtools::install_github("cornerstone-data/useeior")
# Or for specific version:
devtools::install_github("cornerstone-data/useeior@v1.8.0")
```

#### B. Review DIO.Rmd

The existing `DIO.Rmd` file requires only **one line change**:

```diff
- devtools::install_github("USEPA/useeior@v1.7.2")
+ devtools::install_github("cornerstone-data/useeior@v1.8.0")
```

All other code remains compatible.

#### C. Update Model Specification (Optional)

The `DIOv2.0.yml` configuration works as-is, but consider:
- Updating data years to latest available (2023 when released)
- Adding new satellite accounts from Cornerstone's expanded dataset
- Leveraging new validation capabilities

### Phase 3: Data Update 🔄 PENDING

#### Current Data Sources
DIO v2.0 uses:
- BEA IO Tables: 2012
- GHG Emissions: 2016
- Water Use: 2015
- Employment: 2017
- TRI/Air Emissions: 2017

#### Cornerstone Updates Available
- BEA IO Tables: 2017 (2012 still supported)
- GHG Emissions: 2021 (via updated flowsa)
- Water Use: 2020 (via flowsa)
- Employment: 2022 (via flowsa)
- Air Emissions: 2020+ (via updated NEI/TRI)

**Recommendation**: Start with existing 2012 data for validation, then update systematically.

### Phase 4: Rebuild & Validate 📋 PENDING

1. **Rebuild model** with Cornerstone useeior
2. **Validate outputs** against DIO v2.0
3. **Document differences** (expected due to:
   - Updated calculation algorithms
   - Improved data quality
   - Enhanced validation)
4. **Cross-check** key results with Costs of War estimates

### Phase 5: Export & Documentation 📦 PENDING

1. **Export to Excel** (existing format maintained)
2. **Export to JSON** (new capability for web application)
3. **Generate comparison report**
4. **Update all documentation**

## Technical Considerations

### Network/Installation Issues

In restricted network environments (like containers with proxies), GitHub package installation may fail. **Workarounds**:

1. **Clone and install from source**:
   ```r
   git clone https://github.com/cornerstone-data/useeior.git
   devtools::install("useeior")
   ```

2. **Pre-built package** (when available):
   ```r
   install.packages("useeior_1.8.0.tar.gz", repos = NULL, type = "source")
   ```

3. **Docker image** (recommended for production):
   ```dockerfile
   FROM rocker/tidyverse:latest
   RUN R -e "devtools::install_github('cornerstone-data/useeior')"
   ```

### Data Storage Location

Cornerstone uses a "Data Commons" approach:
- Environmental data stored in central repository
- Downloaded on-demand during model build
- Cached locally for subsequent builds
- Parquet format for efficiency

Ensure adequate disk space (~5GB for full USEEIO data).

## Expected Outcomes

### Immediate Benefits
1. **Community Support**: Active development and bug fixes
2. **Latest Data**: Access to 2020+ environmental data
3. **Enhanced Features**: Better validation, visualization, export
4. **Future-Proofing**: Alignment with CEDA merger roadmap

### Potential Differences in Results
Rebuilding DIO with Cornerstone may yield different results due to:
- **Methodological improvements** in impact characterization
- **Updated environmental data** (2020+ vs. 2017)
- **Enhanced sector resolution** in some categories
- **Bug fixes** in calculation algorithms

**This is expected and desirable** - document differences clearly.

## Engagement with Cornerstone Community

### Recommended Actions

1. **Introduce Project**: Post to [Cornerstone Discussions](https://github.com/orgs/cornerstone-data/discussions)
   - Describe Open DIO project goals
   - Share defense-specific use case
   - Request feedback on migration approach

2. **Report Issues**: Use Cornerstone issue tracker for bugs/questions
   - Be specific about DIO context
   - Provide reproducible examples
   - Share defense extensions (if appropriate)

3. **Contribute Back**: After successful migration
   - Share defense sector enhancements
   - Document military-specific satellite accounts
   - Contribute to examples/documentation

### Points of Contact

- **Dr. Wesley Ingwersen**: ingwersw@stanford.edu (Technical Director)
- **Cornerstone GitHub**: https://github.com/cornerstone-data
- **Discussions**: https://github.com/orgs/cornerstone-data/discussions

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Breaking API changes | Low | High | Comprehensive testing, maintain v2.0 parallel |
| Data incompatibility | Low | Medium | Validate sector mappings, document changes |
| Network access required | Medium | Low | Local caching, offline installation support |
| Community adoption pace | Low | Low | Cornerstone has strong institutional backing |
| Result divergence from published estimates | Medium | High | Thorough validation, clear documentation |

## Timeline

- **Week 1-2**: Environment setup, code review ✅
- **Week 3**: Model rebuild with Cornerstone useeior
- **Week 4**: Validation and comparison
- **Week 5**: Documentation and export
- **Week 6**: Community engagement and feedback

## Success Criteria

- [ ] DIO model builds successfully with Cornerstone useeior v1.8.0
- [ ] Results within ±10% of DIO v2.0 for key indicators (GHG, Energy, Water)
- [ ] Differences documented and explained
- [ ] Exported in both Excel and JSON formats
- [ ] Migration guide validated by independent user
- [ ] Cornerstone team notified and supportive

## Next Steps

1. Complete DIO.Rmd update with Cornerstone repository reference
2. Address dependency installation (arrow, configr)
3. Rebuild model and generate outputs
4. Create detailed comparison report
5. Engage with Cornerstone community

## References

- **Cornerstone Initiative Launch**: https://watershed.com/blog/cornerstone
- **cornerstone-data/useeior**: https://github.com/cornerstone-data/useeior
- **Original USEPA/DIO**: https://github.com/USEPA/DIO
- **DIO v2.0 Download**: https://catalog.data.gov/dataset/dio-v2-0
- **useeior Paper**: Li et al. (2022), Applied Sciences, 12(9), 4469

---

*Document Version: 1.0*
*Last Updated: January 23, 2026*
*Maintained by: Open DIO Project*
