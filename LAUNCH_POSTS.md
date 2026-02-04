# Open DIO Launch Announcements

## Twitter/X Post (280 characters)

🚀 Launching Open DIO: Calculate the environmental impact of military spending

✅ 396 economic sectors
✅ GHG, energy, water, land impacts
✅ Based on EPA's Input-Output model
✅ Open source & transparent

Try it: [YOUR_GITHUB_PAGES_URL]
Repo: https://github.com/kelaxten/DIO-v3

#climate #defense #opensource

---

## Hacker News Post

**Title**: Open DIO – Environmental Impact Calculator for Defense Spending

**URL**: [YOUR_GITHUB_PAGES_URL]

**Text**:

I built Open DIO to make military environmental impact analysis accessible to everyone.

The tool uses the Defense Input-Output (DIO) model from the EPA to calculate the full supply chain environmental impacts of defense spending:
- GHG emissions (CO2 equivalent)
- Energy consumption
- Water use
- Land occupation

**Features:**
- Calculate impacts for any of 396 economic sectors
- Upload CSV files for bulk analysis
- Export full results as CSV
- Contextual comparisons (e.g., "equivalent to X million cars")
- Bar chart visualizations
- Glossary of environmental terms

**Data sources:**
- GHG: Cornerstone Supply Chain Factors v1.4.0 (real supply chain data, not estimates)
- Energy: EIA MECS 2018 with IO literature-based multipliers
- Water/Land: EPA USEEIO v2.0
- Economic structure: BEA Input-Output Tables 2017

**Example:** The F-35 program (~$80B/year) produces approximately 10 million metric tons of CO2e when you account for aircraft manufacturing, materials, electronics, etc.

The methodology is fully documented and all code is open source. Next step is analyzing the full FY2024 defense budget (~$850B) using USAspending.gov data.

Built with Python (FastAPI) + React. Backend deployed on Render, frontend on GitHub Pages. Total cost: $0-7/month.

Would love feedback from the HN community!

---

## Reddit Post (r/climate, r/dataisbeautiful, r/opensource)

**Title**: [OC] I built an open-source tool to calculate the environmental impact of military spending

**Text**:

I've been working on **Open DIO**, a web tool that calculates the environmental footprint of defense spending using official EPA and EIA government data.

**What it does:**
Calculate the full supply chain environmental impacts (GHG, energy, water, land) for any defense spending scenario. For example, plug in the F-35 program budget and see:
- 10+ million metric tons of CO2e
- Equivalent to 2.2 million cars driven for a year
- Breakdown by sector (aircraft manufacturing, metals, electronics, etc.)

**Why this matters:**
Military emissions are often excluded from climate reporting and policy discussions. This tool makes the data accessible to researchers, journalists, and the public.

**Data quality:**
- Uses peer-reviewed supply chain emission factors (Cornerstone v1.4.0)
- Energy multipliers based on EIA government data + Input-Output economics literature
- All sources documented, methodology transparent
- Uncertainty ranges clearly stated (±25-50% depending on category)

**Features:**
- Search 396 economic sectors
- Upload CSV for bulk analysis
- Export results as CSV
- Interactive visualizations
- Glossary for technical terms
- Mobile-responsive

**Tech stack:**
- Backend: Python + FastAPI + NumPy
- Frontend: React + TypeScript
- Deployed: Render (backend) + GitHub Pages (frontend)
- Cost: ~$0/month

**Try it:** [YOUR_GITHUB_PAGES_URL]
**Source:** https://github.com/kelaxten/DIO-v3

Next up: Analyzing the full FY2024 US defense budget (~$850 billion) using USAspending.gov contract data.

Happy to answer questions about the methodology, data sources, or implementation!

---

## LinkedIn Post

🚀 Excited to launch Open DIO - an open-source environmental impact calculator for defense spending

After months of development, I'm releasing a tool that makes military environmental impact analysis accessible to researchers, journalists, and policymakers.

**What makes this unique:**
✅ Based on EPA's Defense Input-Output model
✅ Real supply chain data (not estimates)
✅ Full transparency - all code and methodology documented
✅ Free and open source

**Key features:**
• Calculate GHG, energy, water, and land impacts
• 396 economic sectors from BEA Input-Output tables
• CSV upload/export for researchers
• Interactive visualizations
• Mobile-friendly interface

**Data sources:**
• Cornerstone Supply Chain Factors v1.4.0
• EIA Manufacturing Energy Consumption Survey
• EPA USEEIO model
• BEA Input-Output Tables 2017

The tool is live at [YOUR_GITHUB_PAGES_URL] and all code is on GitHub.

Next phase: Full analysis of the FY2024 defense budget using USAspending.gov data to show exactly where $850+ billion in spending creates environmental impacts.

#sustainability #climateaction #opensource #defense #dataanalysis

---

## Email Template (for journalists/researchers)

**Subject:** New tool for calculating military environmental impacts

Hi [Name],

I wanted to share a tool I've built that might be useful for your work on [climate/defense/policy]:

**Open DIO** - an environmental impact calculator for military spending
[YOUR_GITHUB_PAGES_URL]

It calculates the full supply chain footprint (GHG, energy, water, land) of defense spending using official EPA and EIA data.

**Example use cases:**
- Calculate emissions from specific weapons programs
- Compare environmental efficiency of different procurement options
- Analyze budget proposals for environmental impact
- Research military contribution to national emissions

**Data quality:**
- Based on peer-reviewed supply chain factors (Cornerstone Initiative)
- Energy data from EIA government surveys
- Full methodology documentation
- All sources cited

**Key finding from initial analysis:**
The F-35 program alone (~$80B/year) generates over 10 million metric tons of CO2e annually when accounting for manufacturing supply chains.

I'm currently working on a comprehensive analysis of the FY2024 defense budget (~$850B total) and would be happy to share preliminary findings if you're interested.

The tool is completely free and open source. Let me know if you'd like to discuss or if you have any questions about the methodology.

Best,
[Your name]

---

## Notes for Deployment

**GitHub Pages URL will be:**
`https://kelaxten.github.io/DIO-v3/`

**Update all launch posts with actual URL after deployment confirms**

**Timing:**
- Post to HN: 9-10 AM ET (best engagement)
- Post to Reddit: 10 AM - 2 PM ET
- Twitter: Multiple times through the day
- LinkedIn: Morning business hours

**Monitor:**
- GitHub stars
- Website analytics (if installed)
- Social media engagement
- Inbound emails/questions

**Be ready to respond to:**
- Methodology questions
- Data source verification requests
- Feature requests
- Bug reports
- Media inquiries

---

*Created: 2026-01-29*
*Status: Ready to post once deployment confirms*
