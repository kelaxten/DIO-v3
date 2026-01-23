# 🌍 Open DIO Web Application

**Live Demo**: https://kelaxten.github.io/DIO-v3/ *(pending GitHub Pages activation)*

A web-based calculator that makes military environmental impact analysis accessible to everyone. Calculate the environmental footprint of defense spending in real-time using the Defense Input-Output (DIO) model.

---

## ✨ What This Does

Enter defense spending by sector (aircraft, ships, missiles, etc.) and instantly see:

- **🌡️ Greenhouse Gas Emissions** (kg CO2 equivalent)
- **⚡ Energy Use** (MJ)
- **💧 Water Consumption** (gallons)
- **🌍 Land Use** (m²-year)

Plus contextual comparisons like "equivalent to X cars driven for one year" to help understand the scale.

---

## 🚀 Quick Start

### Try It Online (When Live)

1. Visit https://kelaxten.github.io/DIO-v3/
2. Select a defense sector from the dropdown
3. Enter spending amount in USD
4. Click "Calculate Impacts"
5. View results and comparisons

### Run Locally

```bash
cd open-dio-web/frontend
npm install
npm run dev
```

Visit http://localhost:5173

---

## 💡 Example Scenarios

Try these real-world examples:

| Program | Sector | Amount | Est. GHG Impact |
|---------|--------|--------|-----------------|
| F-35 Fighter Jets | Aircraft Manufacturing | $80,000,000,000 | ~11.6M metric tons CO2e |
| Aircraft Carrier | Ship Building | $13,000,000,000 | ~2.0M metric tons CO2e |
| Cybersecurity Contract | Computer Systems Design | $500,000,000 | ~19K metric tons CO2e |
| Base Construction | Heavy Construction | $1,000,000,000 | ~98K metric tons CO2e |

---

## 🏗️ Technical Architecture

### Frontend
- **React 18** with TypeScript
- **Vite** for fast builds
- **Client-side calculation engine** (no backend needed)
- **Responsive design** for mobile and desktop

### Data
- **10 defense sectors** with realistic multipliers
- **4 impact categories** based on DIO v2.0
- **JSON format** for easy integration

### Deployment
- **GitHub Actions** for automated deployment
- **GitHub Pages** for free hosting
- **CDN distribution** for fast global access

---

## 📊 How Calculations Work

The app uses **Input-Output analysis**:

```
Total Impact = Spending × Multiplier
```

For example, Aircraft Manufacturing:
- **GHG**: 145.2 kg CO2e per $1,000 spent
- **Energy**: 2,850 MJ per $1,000 spent
- **Water**: 3,200 gallons per $1,000 spent
- **Land**: 12.5 m²-year per $1,000 spent

**$80 billion F-35 program:**
- GHG = ($80B / $1,000) × 145.2 kg = 11.6 million metric tons CO2e
- That's equivalent to 2.5 million cars driven for one year!

Multipliers trace **direct + indirect** impacts through the entire supply chain.

---

## 🗂️ Project Structure

```
open-dio-web/
├── data/
│   ├── sectors.json           # Defense sector definitions
│   └── multipliers.json        # Impact factors per $1,000
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SectorForm.tsx        # Input interface
│   │   │   └── ResultsDashboard.tsx   # Results display
│   │   ├── utils/
│   │   │   └── calculator.ts          # DIO calculation engine
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript definitions
│   │   └── App.tsx                    # Main application
│   │
│   ├── public/data/              # Runtime data files
│   ├── vite.config.ts            # Build configuration
│   └── package.json
│
└── README.md                     # This file
```

---

## 🎨 Features

### Current
- ✅ 10 defense-relevant sectors
- ✅ 4 environmental impact categories
- ✅ Real-time client-side calculations
- ✅ Contextual comparisons (cars, homes, flights)
- ✅ Sector-by-sector impact breakdown
- ✅ Responsive mobile-friendly UI
- ✅ Example scenarios for quick testing

### Planned (Future)
- [ ] More sectors (all 389 from DIO v2.0)
- [ ] CSV upload for bulk calculations
- [ ] PDF report export
- [ ] Comparison between scenarios
- [ ] Historical analysis charts
- [ ] Backend API integration (Python/FastAPI)

---

## 📚 Data Sources

This application uses simplified multipliers derived from:

- **DIO v2.0**: EPA's Defense Input-Output Model
- **BEA IO Tables**: Bureau of Economic Analysis (2012)
- **EPA GHG Inventory**: Greenhouse gas emissions data
- **USGS Water Use**: Water consumption data
- **Costs of War**: Validation against published estimates

**Note**: Current multipliers are illustrative for demo purposes. Production version will use full DIO matrices.

---

## 🛠️ Development

### Build for Production

```bash
cd open-dio-web/frontend
npm run build
```

Output goes to `dist/` directory.

### GitHub Pages Deployment

Automated via GitHub Actions (`.github/workflows/deploy.yml`):

1. Push to `main` or `claude/update-dio-model-jcHg1` branch
2. GitHub Actions builds the app
3. Deploys to GitHub Pages automatically

**First-time setup**:
1. Go to repository Settings → Pages
2. Source: "GitHub Actions"
3. Wait ~2 minutes for deployment

### Local Development

```bash
cd open-dio-web/frontend
npm install
npm run dev
```

Hot reload enabled - changes appear instantly.

---

## 🧪 Testing Calculations

To verify calculations are working:

**Test 1: Aircraft Manufacturing**
- Sector: 336411 (Aircraft Manufacturing)
- Amount: $1,000,000 (1 million dollars)
- Expected GHG: 145,200 kg CO2e (145.2 metric tons)

**Test 2: Multiple Sectors**
- Aircraft: $1M + Ship Building: $1M
- Expected total GHG: 145,200 + 156,300 = 301,500 kg CO2e

**Test 3: Comparison Context**
- $1B Aircraft spending → ~145K metric tons CO2e
- Should show: "Equivalent to ~31,500 cars driven for one year"

---

## 🔒 Data Privacy

- **No data collection**: Everything runs in your browser
- **No backend calls**: Calculations are client-side only
- **No tracking**: No analytics or third-party scripts
- **Open source**: All code is public and auditable

---

## 📖 Methodology

This tool implements **Environmentally-Extended Input-Output (EEIO) analysis**:

1. **Direct Requirements**: Materials and energy directly used
2. **Indirect Requirements**: Impacts throughout supply chain
3. **Total Impact**: Sum of direct + all indirect effects

For detailed methodology, see:
- [DIO Documentation](../DIO-updated/README_CORNERSTONE.md)
- [USEEIO Technical Guide](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-technical-content)

---

## 🤝 Contributing

This is part of the **Open DIO** project to democratize military environmental impact analysis.

**Ways to contribute**:
- Report bugs via GitHub Issues
- Suggest new features
- Improve documentation
- Add more sectors or impact categories
- Share with researchers, journalists, activists

**Vision**: Make this data as accessible as a Google search.

---

## 📜 License

This project builds on public domain work from the U.S. EPA. See repository root for license details.

---

## 🙏 Acknowledgments

- **EPA**: Original DIO Model v2.0
- **Cornerstone Initiative**: Maintained USEEIO framework
- **Costs of War Project**: Validation data and inspiration
- **Dr. Wesley Ingwersen**: USEEIO architecture and guidance

---

## 📞 Contact

- **GitHub Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Repository**: https://github.com/kelaxten/DIO-v3

---

**Built with ❤️ for transparency and accountability**

*"The best disinfectant is sunlight" - Louis Brandeis*
