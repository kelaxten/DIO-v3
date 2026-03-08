## Budget Analysis Troubleshooting Guide

### Current Status
✅ Data file exists: `open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json`
✅ Data is valid: 313 sectors, $387B total spending
✅ Added better error logging to component

### Test Steps

**1. Start the dev server:**
```bash
cd open-dio-web/frontend
npm run dev
```

**2. Open in browser:**
- Navigate to http://localhost:5173
- Click "Budget Analysis" tab
- Open browser console (F12 or Cmd+Option+I)

**3. Check console for these messages:**
```
Fetching budget data from /data/fy2024_dod_budget_analysis.json...
Budget data loaded: { lineCount: 313, totalSpending: 387134760488.84 }
```

### Common Issues & Fixes

**Issue 1: 404 Not Found**
- **Symptom**: Console shows "HTTP 404: Not Found"
- **Cause**: Dev server not finding file in public directory
- **Fix**: Make sure you're in `open-dio-web/frontend/` when running `npm run dev`

**Issue 2: CORS Error**
- **Symptom**: Console shows "CORS policy" error
- **Cause**: Fetching from wrong origin
- **Fix**: Access via `http://localhost:5173` not `file://`

**Issue 3: JSON Parse Error**
- **Symptom**: "Unexpected token" or JSON error
- **Cause**: Malformed JSON file
- **Fix**: Run `python3 -m json.tool < public/data/fy2024_dod_budget_analysis.json > /dev/null`

**Issue 4: Empty Array**
- **Symptom**: Console shows "lineCount: 0"
- **Cause**: Data file has wrong structure
- **Fix**: Re-run `python3 publish_budget_data.py` from project root

### Quick Verification

Run this from project root to verify data:
```bash
python3 << 'EOF'
import json
with open('open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json') as f:
    data = json.load(f)
    print(f"✓ Valid JSON")
    print(f"✓ {len(data.get('line_by_line', []))} rows")
    print(f"✓ ${data.get('summary', {}).get('total_spending', 0):,.0f} total")
EOF
```

Expected output:
```
✓ Valid JSON
✓ 313 rows
✓ $387,134,760,489 total
```

### What to Tell Me

After testing, let me know:
1. What you see in the browser console
2. Any error messages
3. Whether the data loads or shows "No Data Available"

This will help me pinpoint the exact issue!
