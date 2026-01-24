"""
Request schemas for Open DIO API
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class SectorInput(BaseModel):
    """Single sector spending input"""
    code: str = Field(..., description="Sector code (BEA)")
    amount: float = Field(..., ge=0, description="Dollar amount")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "336411",
                    "amount": 1000000
                }
            ]
        }
    }


class CalculationRequest(BaseModel):
    """Request to calculate environmental impacts"""
    sectors: List[SectorInput] = Field(..., min_length=1)
    impact_categories: Optional[List[str]] = Field(
        None,
        description="Impact categories to calculate (default: all)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sectors": [
                        {"code": "336411", "amount": 80000000000},
                        {"code": "336611", "amount": 13000000000}
                    ]
                }
            ]
        }
    }
