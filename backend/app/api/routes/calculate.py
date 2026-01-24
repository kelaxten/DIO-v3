"""
Calculate endpoint - main calculation route
"""

from fastapi import APIRouter, HTTPException
from app.api.schemas.request import CalculationRequest
from app.api.schemas.response import CalculationResponse
from app.core.calculator import get_calculator

router = APIRouter()


@router.post(
    "/",
    response_model=CalculationResponse,
    summary="Calculate environmental impacts",
    description="""
Calculate environmental impacts from defense spending.

Provide sector codes and dollar amounts. Returns environmental
impacts including GHG emissions, energy use, water consumption, and land use.

Example:
```json
{
  "sectors": [
    {"code": "336411", "amount": 80000000000},
    {"code": "336611", "amount": 13000000000}
  ]
}
```
"""
)
async def calculate_impacts(request: CalculationRequest):
    """
    Calculate environmental impacts from defense spending

    Args:
        request: Calculation request with sector spending

    Returns:
        Detailed impact results with sector breakdown
    """
    calculator = get_calculator()

    # Build sector spending dict
    sector_spending = {
        sector.code: sector.amount
        for sector in request.sectors
    }

    try:
        result = calculator.calculate(
            sector_spending=sector_spending,
            impact_categories=request.impact_categories
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Calculation failed: {str(e)}"
        )
