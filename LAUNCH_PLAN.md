# Open DIO Launch Plan - Two-Phase Strategy

**Status**: MVP is production-ready with all features complete
**Date**: 2026-01-29

---

## Phase 1: MVP Launch (This Week)

### What's Ready NOW

**Core Functionality** ✅
- Calculate environmental impacts (GHG, Energy, Water, Land) for 396 sectors
- Manual sector entry with searchable dropdown
- CSV bulk upload with validation
- CSV export for full data download
- Real-time calculations via deployed API

**Data Quality** ✅
- GHG: Cornerstone v1.4.0 (±25% uncertainty)
- Energy: IO literature-based multipliers (±25-35% uncertainty)
- Water/Land: EPA USEEIO v2.0 (±40-50% uncertainty)
- 109 defense-relevant sectors identified

**User Experience** ✅
- Glossary with 18 key terms
- Contextual comparisons (cars, homes, flights)
- Bar chart visualization (top 10 sectors)
- Responsive mobile design
- Comprehensive methodology documentation

**Infrastructure** ✅
- Backend API: https://open-dio-api.onrender.com (deployed)
- Frontend: Ready for GitHub Pages deployment
- API docs: Available at /docs endpoint

### Launch Checklist

**Technical** (1-2 hours)
- [ ] Merge `claude/add-visualizations-jcHg1` into main (via PR)
- [ ] Deploy frontend to GitHub Pages
- [ ] Test end-to-end (calculator → results → export)
- [ ] Verify API cold start is acceptable (30-50 sec)
- [ ] Optional: Upgrade Render to paid tier ($7/mo, eliminates cold starts)

**Content** (2-3 hours)
- [ ] Update README with launch announcement
- [ ] Add usage examples to README
- [ ] Create CHANGELOG.md documenting v1.0 features
- [ ] Add GitHub repo description and topics
- [ ] Set up GitHub Pages custom domain (optional)

**Announcement** (1-2 hours)
- [ ] Write launch tweet/social post
- [ ] Post to relevant subreddits (r/climate, r/dataisbeautiful, r/opensource)
- [ ] Submit to Hacker News
- [ ] Email climate/defense journalists (optional)

**Total Time to Launch**: ~4-7 hours

---

## Phase 2: USAspending Integration (2-3 Weeks)

### Week 1: Data Pipeline

**Build Integration** (15-20 hours)
- [ ] Set up USAspending.gov API access (researcher tier)
- [ ] Build `usaspending_fetcher.py` module
- [ ] Implement NAICS-to-DIO sector mapping
- [ ] Create automated pipeline script
- [ ] Run FY2024 analysis (validate against known totals)
- [ ] Store pre-computed results

**Expected Output**:
```
FY2024 Defense Budget Analysis
- Total spending: ~$850 billion
- GHG emissions: ~304 million tons CO2e
- Energy: ~6,000-8,000 PJ
- Top sectors: Aircraft ($78B), Petroleum ($45B), Ships ($32B)
```

### Week 2: Frontend Integration

**Budget Explorer UI** (10-15 hours)
- [ ] Create "Explore Budget" page
- [ ] Fiscal year selector (FY2020-2024)
- [ ] Summary dashboard with key metrics
- [ ] Branch breakdown (Army, Navy, Air Force, Marines, Space Force)
- [ ] Sector breakdown with filters
- [ ] Enhanced visualizations (treemap, time series)
- [ ] Export full budget analysis

**Features**:
- Pre-computed analyses for instant exploration
- No cold start delays (data is cached)
- Multiple views: by branch, by year, by sector
- Comparison across fiscal years

### Week 3: Analysis & Launch Article

**Deep Analysis** (8-10 hours)
- [ ] Analyze FY2024 results thoroughly
- [ ] Identify key findings and narratives
- [ ] Compare to prior years (trends)
- [ ] Calculate efficiency metrics (impact per dollar)
- [ ] Create compelling visualizations

**Article Writing** (12-15 hours)
- [ ] Write 5,000-word investigative article
- [ ] Title: "The $850 Billion Question: Environmental Impact of US Defense Spending in FY2024"
- [ ] Structure: Executive summary, methodology, findings, context, implications
- [ ] Create charts and graphics
- [ ] Fact-check all numbers
- [ ] Edit and polish

**Publication Options**:
1. **Fast Track**: Self-publish on Medium/Substack + interactive web feature
2. **Partnership**: Submit to Quincy Institute or Costs of War Project
3. **Media**: Pitch to The Intercept, ProPublica, or investigative journalists
4. **Academic**: Post preprint to SSRN/arXiv

---

## Parallel Work Strategy

**You can work on both simultaneously:**

**Phase 1 (MVP Launch)**: Quick wins
- Launch basic tool this week
- Get initial users and feedback
- Establish credibility

**Phase 2 (USAspending)**: Build in parallel
- Work on integration while MVP is live
- Users can try self-service tool
- Big launch with FY2024 analysis in 2-3 weeks

**Benefits**:
- Early feedback on MVP
- Momentum from initial launch
- Bigger splash with pre-computed budget analysis
- Two launch moments instead of one

---

## Success Metrics

### MVP Launch (Month 1)
- [ ] 500+ unique visitors
- [ ] 100+ calculations performed
- [ ] 50+ CSV downloads
- [ ] 5+ GitHub stars
- [ ] Mentioned in 2+ articles/tweets

### USAspending Launch (Month 2)
- [ ] 5,000+ article views
- [ ] 10+ media citations
- [ ] 1,000+ budget explorer users
- [ ] Shared by climate/defense community
- [ ] Cited in policy discussions

### Long-term (6 months)
- [ ] 50,000+ total users
- [ ] 20+ media citations
- [ ] Tool used by 5+ organizations
- [ ] Academic paper published or under review
- [ ] Congressional testimony mention (stretch goal)

---

## Resource Requirements

**Time**:
- MVP Launch: 4-7 hours (this week)
- USAspending Integration: 40-55 hours (2-3 weeks)

**Cost**:
- Infrastructure: $0-7/month (optional Render upgrade)
- Domain: $0-12/year (optional)
- Total: **$0-84/year**

**All government data is free** ✅

---

## Risk Mitigation

**MVP Launch Risks**:
- Risk: Cold start delays annoy users
  - Mitigation: Add note explaining ~30 sec initial load; upgrade to paid ($7/mo)
- Risk: Limited initial users
  - Mitigation: Active promotion on social media, HN, Reddit

**USAspending Risks**:
- Risk: API rate limits
  - Mitigation: Request researcher tier (free, 10x higher limits)
- Risk: NAICS mapping errors
  - Mitigation: Validate against known totals, document unmapped sectors
- Risk: Results disputed
  - Mitigation: Full methodology transparency, cite all sources

---

## Next Immediate Actions

**Today/Tomorrow**:
1. ✅ Features complete (done!)
2. [ ] Create PR to merge visualizations
3. [ ] Deploy frontend to GitHub Pages
4. [ ] Test end-to-end
5. [ ] Write launch announcement

**This Week**:
1. [ ] Launch MVP (social media, HN, Reddit)
2. [ ] Monitor initial feedback
3. [ ] Start USAspending API setup

**Next Week**:
1. [ ] Build data pipeline
2. [ ] Run FY2024 analysis
3. [ ] Begin article outline

---

## Questions to Decide

1. **Hosting upgrade**: Pay $7/mo for Render to eliminate cold starts?
   - Recommendation: Yes, worth it for better UX

2. **Custom domain**: Get dio-calculator.org or similar?
   - Recommendation: Optional, can add later

3. **Article venue**: Self-publish or seek partnership?
   - Recommendation: Start with self-publish for speed, can republish with partner

4. **Author attribution**: Your name, organization, or anonymous?
   - Recommendation: Decide based on your goals

5. **Analytics**: Add privacy-respecting analytics (Plausible, Simple Analytics)?
   - Recommendation: Yes, helps measure success

---

**Status**: Ready to execute Phase 1 immediately!

All code is committed and ready. Just need to merge, deploy, and announce.
