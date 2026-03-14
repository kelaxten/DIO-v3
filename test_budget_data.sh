#!/bin/bash

echo "=========================================="
echo "Budget Analysis Data Verification"
echo "=========================================="
echo ""

# Check if data file exists
if [ -f "open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json" ]; then
    echo "✓ Data file exists"

    # Check file size
    SIZE=$(stat -f%z "open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json" 2>/dev/null || stat -c%s "open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json")
    echo "✓ File size: $SIZE bytes"

    # Validate JSON and show details
    python3 << 'EOF'
import json

try:
    with open('open-dio-web/frontend/public/data/fy2024_dod_budget_analysis.json') as f:
        data = json.load(f)

    print("✓ Valid JSON structure")
    print(f"✓ Sectors: {len(data.get('line_by_line', []))}")
    print(f"✓ Total spending: ${data.get('summary', {}).get('total_spending', 0):,.0f}")

    if len(data.get('line_by_line', [])) > 0:
        print("\n✓ Sample row:")
        sample = data['line_by_line'][0]
        print(f"  - {sample.get('BEA_Sector_Name')}")
        print(f"  - Spending: ${sample.get('Spending_USD', 0):,.0f}")
        print(f"  - GHG: {sample.get('GHG_kg_CO2e', 0):,.0f} kg CO2e")

    print("\n✓✓✓ Data file is ready!")
    print("\nNow test the frontend:")
    print("1. cd open-dio-web/frontend")
    print("2. npm run dev")
    print("3. Open http://localhost:5173")
    print("4. Click 'Budget Analysis' tab")
    print("5. Check browser console (F12) for fetch logs")

except Exception as e:
    print(f"✗ Error: {e}")
EOF

else
    echo "✗ Data file NOT found!"
    echo ""
    echo "Run this to create it:"
    echo "  python3 publish_budget_data.py"
fi

echo ""
echo "=========================================="
