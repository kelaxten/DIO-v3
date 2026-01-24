"""
Sectors endpoint - list available sectors
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.api.schemas.response import SectorsResponse, SectorInfo
from app.core.calculator import get_calculator

router = APIRouter()


@router.get(
    "/",
    response_model=SectorsResponse,
    summary="List available sectors",
    description="Get list of available defense sectors for calculation"
)
async def list_sectors(
    defense_only: bool = Query(False, description="Only defense-relevant sectors"),
    query: Optional[str] = Query(None, description="Search query for sector name")
):
    """
    List available sectors

    Args:
        defense_only: Filter to defense-relevant sectors only
        query: Search query to filter by sector name

    Returns:
        List of sectors with metadata
    """
    calculator = get_calculator()
    all_sectors = calculator.get_available_sectors()

    # Apply filters
    filtered_sectors = all_sectors

    if defense_only:
        filtered_sectors = [s for s in filtered_sectors if s['is_defense_relevant']]

    if query:
        query_lower = query.lower()
        filtered_sectors = [
            s for s in filtered_sectors
            if query_lower in s['name'].lower() or query_lower in s['code']
        ]

    # Convert to response format
    sector_infos = [SectorInfo(**s) for s in filtered_sectors]

    return SectorsResponse(
        sectors=sector_infos,
        total=len(sector_infos)
    )
