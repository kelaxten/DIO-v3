"""
Response schemas for Open DIO API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ImpactResult(BaseModel):
    """Single impact category result"""
    category: str
    value: float
    unit: str
    description: str


class SectorImpacts(BaseModel):
    """Impacts from a single sector"""
    name: str
    spending: float
    impacts: List[ImpactResult]


class CalculationResponse(BaseModel):
    """Response with calculated impacts"""
    total_spending: float
    impacts: List[ImpactResult]
    sector_breakdown: Dict[str, SectorImpacts]
    model_version: str = "DIO v2.0"


class SectorInfo(BaseModel):
    """Information about a sector"""
    code: str
    name: str
    is_defense_relevant: bool = False


class SectorsResponse(BaseModel):
    """List of available sectors"""
    sectors: List[SectorInfo]
    total: int


class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    version: str
    model: str
