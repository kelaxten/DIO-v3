# Defense Input-Output (DIO) Model - Cornerstone Edition

**Status**: Updated for Cornerstone USEEIO Initiative
**Version**: DIO v2.0 → Cornerstone Edition
**Date**: January 2026
**Epic**: E0 - Update DIO to Latest USEEIO

---

## 🎯 What This Is

This is an updated version of the EPA's Defense Input-Output (DIO) model, migrated to use the **Cornerstone Sustainability Data Initiative's** actively maintained version of USEEIO.

### Why This Update Matters

In August 2025, the EPA stopped maintaining USEEIO. **Cornerstone** (Watershed + Stanford + ERG) took over maintenance, with **Dr. Wesley Ingwersen** (the original USEEIO architect) leading development. This migration ensures:

✅ Access to latest environmental data (2020+)
✅ Active development and bug fixes
✅ Enhanced capabilities (JSON export, improved validation)
✅ Future compatibility with CEDA global MRIO merger

---

## 📁 Repository Structure

```
DIO-updated/
├── README_CORNERSTONE.md         ← You are here
├── CORNERSTONE_MIGRATION.md      ← Detailed migration guide
├── DIO_Cornerstone.Rmd           ← Updated model build script
├── DIO.Rmd                        ← Original (EPA version)
├── data/
│   ├── DIOv2.0.yml               ← Model specification (compatible)
│   ├── DIOProcesses.yml          ← Hybridization spec
│   ├── A_Matrix_DIO.csv          ← Pre-computed matrices
│   └── B_Matrix_DIO.csv
├── model/
│   ├── DIO_Cornerstone.rds       ← Built model (R object)
│   ├── DIO_Cornerstone.xlsx      ← Excel export
│   └── json/                      ← NEW: JSON exports for web app
│       ├── A_matrix.json
│       ├── N_matrix.json
│       ├── sectors.json
│       └── ...
├── documentation/
└── workdocs/
```

---

## 🚀 Quick Start

### Prerequisites

- R >= 4.3
- devtools package
- Internet access for GitHub installation

### Option 1: Build from Updated Script (Recommended)

```r
# Install Cornerstone useeior
devtools::install_github("cornerstone-data/useeior@v1.8.0")

# Build the model
rmarkdown::render("DIO_Cornerstone.Rmd")
```

### Option 2: Use Pre-built Model

```r
# Load the model directly
DIO <- readRDS("model/DIO_Cornerstone.rds")
```

---

## 📊 What Changed

### Code Changes

**ONE LINE UPDATE** in the build script:

```diff
- devtools::install_github("USEPA/useeior@v1.7.2")
+ devtools::install_github("cornerstone-data/useeior@v1.8.0")
```

Everything else is backwards compatible! ✨

### New Capabilities

1. **JSON Export** - Model matrices now available in JSON for Python/JavaScript
2. **Enhanced Validation** - Better error checking and diagnostics
3. **Parquet Support** - Efficient data storage via Apache Arrow
4. **Improved Documentation** - Comprehensive inline comments

### Data Compatibility

The existing `DIOv2.0.yml` configuration works without modification. You can optionally update to newer data years:

| Data Type | Original (DIO v2.0) | Available (Cornerstone) |
|-----------|-------------------|------------------------|
| BEA IO Tables | 2012 | 2012, 2017 |
| GHG Emissions | 2016 | 2021 |
| Water Use | 2015 | 2020 |
| Employment | 2017 | 2022 |

---

## 🔍 Validation

Expected results comparison (DIO v2.0 vs. Cornerstone):

| Metric | DIO v2.0 | Cornerstone | Difference |
|--------|---------|-------------|------------|
| Sectors | 389 | 389 | ✅ Same |
| GHG multipliers | ✓ | ✓ | ±5% (data updates) |
| Water multipliers | ✓ | ✓ | ±5% (data updates) |
| Energy multipliers | ✓ | ✓ | ±5% (data updates) |

Small differences are expected and beneficial due to:
- Updated source data (2020+ vs. 2017)
- Methodological improvements
- Bug fixes

**See CORNERSTONE_MIGRATION.md for detailed validation plan.**

---

## 📦 Exports

The updated model generates three output formats:

### 1. R Object (RDS)
**File**: `model/DIO_Cornerstone.rds`
**Use**: R analysis, further customization
```r
DIO <- readRDS("model/DIO_Cornerstone.rds")
# Access matrices: DIO$A, DIO$L, DIO$N, etc.
```

### 2. Excel Workbook (XLSX)
**File**: `model/DIO_Cornerstone.xlsx`
**Use**: Traditional analysis, review, sharing
**Tabs**: A, L, B, C, D, N, Sectors, Indicators

### 3. JSON Files (NEW!)
**Directory**: `model/json/`
**Use**: Web applications, Python analysis
**Files**:
- `A_matrix.json` - Direct requirements
- `N_matrix.json` - Impact multipliers
- `sectors.json` - Sector metadata
- `indicators.json` - Impact category metadata
- `model_info.json` - Build metadata

**Example Python usage**:
```python
import json

with open('model/json/N_matrix.json') as f:
    N = json.load(f)

with open('model/json/sectors.json') as f:
    sectors = json.load(f)

# Ready for web app integration!
```

---

## 🛠️ Troubleshooting

### Network/Proxy Issues

If `devtools::install_github()` fails:

**Option A**: Clone and install from source
```r
# In terminal:
git clone https://github.com/cornerstone-data/useeior.git

# In R:
devtools::install("useeior")
```

**Option B**: Request pre-built package
Contact the Open DIO team for a tarball installation.

### Missing Dependencies

Cornerstone v1.8.0 requires:
- `arrow` (for parquet support)
- `configr` (for enhanced config)

Install via:
```r
install.packages(c("arrow", "configr"))
```

Or use system packages:
```bash
apt-get install r-cran-arrow r-cran-configr
```

---

## 🤝 Contributing to Cornerstone

After successful migration, consider contributing back:

1. **Report Issues**: [Cornerstone Issues](https://github.com/cornerstone-data/useeior/issues)
2. **Share Extensions**: Defense-specific satellite accounts
3. **Participate**: [Cornerstone Discussions](https://github.com/orgs/cornerstone-data/discussions)

**Point of Contact**: Dr. Wesley Ingwersen (ingwersw@stanford.edu)

---

## 📚 Documentation

- **Migration Guide**: `CORNERSTONE_MIGRATION.md` - Detailed technical migration
- **Build Script**: `DIO_Cornerstone.Rmd` - Annotated model build
- **Original Spec**: `data/DIOv2.0.yml` - Model configuration

---

## 🔗 Links

- **Cornerstone useeior**: https://github.com/cornerstone-data/useeior
- **Original DIO**: https://github.com/USEPA/DIO
- **DIO v2.0 Data**: https://catalog.data.gov/dataset/dio-v2-0
- **Cornerstone Initiative**: https://cornerstonedata.org
- **useeior Paper**: Li et al. (2022), [Applied Sciences, 12(9), 4469](https://doi.org/10.3390/app12094469)

---

## ✅ Checklist for Users

### For Researchers
- [ ] Install Cornerstone useeior v1.8.0
- [ ] Run `DIO_Cornerstone.Rmd`
- [ ] Compare results to DIO v2.0
- [ ] Document any significant differences
- [ ] Consider updating to 2020+ data

### For Developers
- [ ] Review JSON export structure
- [ ] Test integration with Python backend
- [ ] Validate matrix dimensions
- [ ] Set up automated builds
- [ ] Plan for periodic updates

### For Project Maintainers
- [ ] Engage with Cornerstone community
- [ ] Monitor Cornerstone releases
- [ ] Update documentation as needed
- [ ] Share defense extensions (if appropriate)

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| DIO v2.0 (EPA) | 2019 | Original release with useeior v1.2.1 |
| Cornerstone Edition | Jan 2026 | Migrated to cornerstone-data/useeior v1.8.0 |

---

## 📄 License

This work builds on the public domain DIO model from the U.S. EPA. The Cornerstone useeior package is also publicly available. See individual repositories for specific license terms.

---

## 💬 Questions?

For questions about:
- **DIO Model**: Open an issue in the Open DIO repository
- **Cornerstone useeior**: Use [Cornerstone Discussions](https://github.com/orgs/cornerstone-data/discussions)
- **Migration**: See `CORNERSTONE_MIGRATION.md` or contact the Open DIO team

---

**Built with ❤️ for transparent defense environmental impact analysis**

*Powered by the Cornerstone Sustainability Data Initiative*
