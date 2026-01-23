# Open DIO Project
## Technical Implementation Specification

---

## Important Context: Cornerstone Initiative

As of August 2025, the **Cornerstone Sustainability Data Initiative** has taken over maintenance of USEEIO from the EPA. The existing DIO v2.0 was built on `useeior v1.2.1`, which is now significantly outdated compared to Cornerstone's actively maintained version (v1.7.1+).

**Key Implications for This Project:**

1. **First Priority**: Update DIO to work with current USEEIO (Phase 0)
2. **Use Cornerstone Repos**: Work with `cornerstone-data/useeior` not `USEPA/useeior`
3. **Community Engagement**: Coordinate with Dr. Wesley Ingwersen (Cornerstone Technical Director, original USEEIO architect)
4. **Contribution Opportunity**: Defense-specific extensions could be contributed back to Cornerstone ecosystem

**Relevant Cornerstone Resources:**
- GitHub: https://github.com/cornerstone-data
- Website: https://cornerstonedata.org
- Discussions: https://github.com/orgs/cornerstone-data/discussions

---

## 1. Prototype Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (React)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Input Form │  │ File Upload │  │  Results    │  │   Export   │ │
│  │  Component  │  │  Component  │  │  Dashboard  │  │  Component │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP/JSON
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Backend API (FastAPI)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │ /calculate  │  │  /sectors   │  │  /compare   │  │  /export   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Calculation Engine (Python)                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  DIO Model Data (NumPy Arrays)                               │   │
│  │  ├── A_matrix (Direct Requirements)                          │   │
│  │  ├── L_matrix (Total Requirements / Leontief Inverse)        │   │
│  │  ├── B_matrix (Satellite Accounts)                           │   │
│  │  ├── C_matrix (Characterization Factors)                     │   │
│  │  └── sector_metadata                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  calculate_impacts(demand_vector) → impacts                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Directory Structure

```
open-dio/
├── README.md
├── LICENSE (MIT or Apache 2.0)
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings and configuration
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── calculate.py
│   │   │   │   ├── sectors.py
│   │   │   │   ├── compare.py
│   │   │   │   └── export.py
│   │   │   └── schemas/
│   │   │       ├── request.py
│   │   │       └── response.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── dio_model.py     # DIO calculation engine
│   │   │   ├── sector_mapper.py # NAICS to BEA mapping
│   │   │   └── comparisons.py   # Country/equivalent comparisons
│   │   └── data/
│   │       ├── __init__.py
│   │       ├── load_dio.py      # Load DIO Excel into memory
│   │       └── reference/
│   │           ├── naics_bea_crosswalk.csv
│   │           ├── country_emissions.csv
│   │           └── equivalents.json
│   └── tests/
│       ├── test_calculate.py
│       ├── test_sector_mapper.py
│       └── fixtures/
│           └── sample_inputs.json
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   │   └── client.ts        # API client
│   │   ├── components/
│   │   │   ├── SectorInput.tsx
│   │   │   ├── FileUpload.tsx
│   │   │   ├── ResultsDashboard.tsx
│   │   │   ├── SectorBreakdown.tsx
│   │   │   ├── ComparisonCards.tsx
│   │   │   └── ExportButton.tsx
│   │   ├── hooks/
│   │   │   └── useCalculation.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── utils/
│   │       └── formatters.ts
│   └── tests/
│       └── components/
│
├── data/
│   ├── README.md
│   └── DIOv2.0_w_metadata.xlsx  # Downloaded from EPA
│
└── docs/
    ├── methodology.md
    ├── api.md
    └── development.md
```

---

## 2. Backend Implementation

### 2.1 Dependencies (requirements.txt)

```
# Core
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0

# Data Processing
numpy>=1.26.0
pandas>=2.2.0
openpyxl>=3.1.0  # Excel reading

# Export
reportlab>=4.0.0  # PDF generation
xlsxwriter>=3.1.0

# Testing
pytest>=7.4.0
httpx>=0.26.0

# Dev
black>=24.1.0
ruff>=0.1.0
mypy>=1.8.0
```

### 2.2 Core Calculation Engine

```python
# backend/app/core/dio_model.py

import numpy as np
import pandas as pd
from pathlib import Path
from functools import lru_cache
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Sector:
    code: str
    name: str
    description: Optional[str] = None
    naics_codes: Optional[List[str]] = None

@dataclass
class ImpactCategory:
    code: str
    name: str
    unit: str
    description: Optional[str] = None

@dataclass
class CalculationResult:
    total_impacts: Dict[str, float]
    sector_contributions: Dict[str, Dict[str, float]]
    demand_vector: Dict[str, float]
    model_version: str

class DIOModel:
    """
    Defense Input-Output Model calculation engine.
    
    Implements the USEEIO calculation methodology:
    Total Requirements: L = (I - A)^(-1)
    Environmental Impacts: impacts = D * y where D = B * L
    """
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._load_model()
    
    def _load_model(self):
        """Load DIO model matrices from Excel file."""
        xlsx = pd.ExcelFile(self.data_path)
        
        # Load matrices - tab names from USEEIO Model format
        # A matrix: Direct requirements (industry x industry)
        self.A = pd.read_excel(xlsx, 'A', index_col=0).values
        
        # L matrix: Total requirements (Leontief inverse)
        self.L = pd.read_excel(xlsx, 'L', index_col=0).values
        
        # B matrix: Satellite accounts (flow x industry)
        # Environmental flows per dollar of output
        self.B = pd.read_excel(xlsx, 'B', index_col=0).values
        
        # C matrix: Characterization factors (impact x flow)
        self.C = pd.read_excel(xlsx, 'C', index_col=0).values
        
        # D matrix: Direct impact intensity = C * B
        # Or pre-computed in DIO
        self.D = pd.read_excel(xlsx, 'D', index_col=0).values
        
        # N matrix: Total impact multipliers = D * L
        # Impacts per dollar of final demand
        self.N = pd.read_excel(xlsx, 'N', index_col=0).values
        
        # Sector metadata
        self.sectors_df = pd.read_excel(xlsx, 'Sectors')
        self.sectors = {
            row['Code']: Sector(
                code=row['Code'],
                name=row['Name'],
                description=row.get('Description')
            )
            for _, row in self.sectors_df.iterrows()
        }
        self.sector_codes = list(self.sectors.keys())
        self.sector_index = {code: i for i, code in enumerate(self.sector_codes)}
        
        # Impact category metadata
        self.impacts_df = pd.read_excel(xlsx, 'Indicators')
        self.impact_categories = {
            row['Code']: ImpactCategory(
                code=row['Code'],
                name=row['Name'],
                unit=row['Unit'],
                description=row.get('Description')
            )
            for _, row in self.impacts_df.iterrows()
        }
        self.impact_codes = list(self.impact_categories.keys())
        
        # Model metadata
        self.model_version = "DIO v2.0"
        self.n_sectors = len(self.sector_codes)
        self.n_impacts = len(self.impact_codes)
    
    def calculate(
        self, 
        demand: Dict[str, float],
        impact_categories: Optional[List[str]] = None
    ) -> CalculationResult:
        """
        Calculate environmental impacts for given demand vector.
        
        Args:
            demand: Dict mapping sector codes to dollar amounts
            impact_categories: Optional list of impact codes to calculate
                              (defaults to all)
        
        Returns:
            CalculationResult with total impacts and sector breakdown
        """
        # Build demand vector
        y = np.zeros(self.n_sectors)
        for sector_code, amount in demand.items():
            if sector_code in self.sector_index:
                y[self.sector_index[sector_code]] = amount
            else:
                raise ValueError(f"Unknown sector code: {sector_code}")
        
        # Calculate total requirements
        # x = L * y (total output required from each sector)
        x = self.L @ y
        
        # Calculate environmental flows
        # flows = B * diag(x) (total flows from all production)
        flows = self.B @ np.diag(x) @ np.ones(self.n_sectors)
        
        # Calculate impacts
        # impacts = C * flows
        impacts = self.C @ flows
        
        # Alternative: Use pre-computed N matrix
        # impacts = N * y
        impacts_from_N = self.N @ y
        
        # Build results
        total_impacts = {}
        impact_idx = {code: i for i, code in enumerate(self.impact_codes)}
        
        selected_impacts = impact_categories or self.impact_codes
        for code in selected_impacts:
            if code in impact_idx:
                total_impacts[code] = float(impacts_from_N[impact_idx[code]])
        
        # Calculate sector contributions
        sector_contributions = self._calculate_contributions(y, selected_impacts)
        
        return CalculationResult(
            total_impacts=total_impacts,
            sector_contributions=sector_contributions,
            demand_vector=demand,
            model_version=self.model_version
        )
    
    def _calculate_contributions(
        self, 
        y: np.ndarray,
        impact_categories: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """Calculate each sector's contribution to total impacts."""
        contributions = {}
        
        for code in impact_categories:
            impact_idx = self.impact_codes.index(code)
            # Get the row of N matrix for this impact
            n_row = self.N[impact_idx, :]
            # Contribution = multiplier * demand
            sector_impacts = n_row * y
            
            contributions[code] = {
                self.sector_codes[i]: float(sector_impacts[i])
                for i in range(self.n_sectors)
                if sector_impacts[i] > 0
            }
        
        return contributions
    
    def get_sector(self, code: str) -> Optional[Sector]:
        return self.sectors.get(code)
    
    def search_sectors(self, query: str) -> List[Sector]:
        """Search sectors by name or code."""
        query_lower = query.lower()
        return [
            sector for sector in self.sectors.values()
            if query_lower in sector.name.lower() or query_lower in sector.code.lower()
        ]
    
    def get_defense_sectors(self) -> List[Sector]:
        """Return sectors most relevant to defense spending."""
        defense_codes = [
            '336411',  # Aircraft Manufacturing
            '336414',  # Guided Missile Manufacturing
            '336413',  # Other Aircraft Parts
            '336611',  # Ship Building
            '336992',  # Military Armored Vehicle
            '541330',  # Engineering Services
            '541512',  # Computer Systems Design
            '541715',  # R&D Physical Sciences
            '237990',  # Heavy Construction
            '324110',  # Petroleum Refineries
        ]
        return [self.sectors[c] for c in defense_codes if c in self.sectors]


@lru_cache(maxsize=1)
def get_dio_model() -> DIOModel:
    """Singleton factory for DIO model."""
    data_path = Path(__file__).parent.parent / 'data' / 'DIOv2.0_w_metadata.xlsx'
    return DIOModel(data_path)
```

### 2.3 API Routes

```python
# backend/app/api/routes/calculate.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from app.core.dio_model import get_dio_model, CalculationResult

router = APIRouter(prefix="/calculate", tags=["calculate"])

class SectorInput(BaseModel):
    code: str = Field(..., description="Sector code (BEA or NAICS)")
    amount: float = Field(..., ge=0, description="Dollar amount")

class CalculationRequest(BaseModel):
    sectors: List[SectorInput] = Field(..., min_length=1)
    impact_categories: Optional[List[str]] = Field(
        None, 
        description="Impact categories to calculate (default: all)"
    )

class ImpactResult(BaseModel):
    code: str
    name: str
    value: float
    unit: str

class CalculationResponse(BaseModel):
    total_spending: float
    impacts: List[ImpactResult]
    sector_breakdown: Dict[str, Dict[str, float]]
    model_version: str

@router.post("/", response_model=CalculationResponse)
async def calculate_impacts(request: CalculationRequest):
    """
    Calculate environmental impacts for given spending.
    
    Provide sector codes and dollar amounts. Returns environmental
    impacts including GHG emissions, energy use, water consumption, etc.
    """
    model = get_dio_model()
    
    # Build demand dict
    demand = {}
    for sector_input in request.sectors:
        # TODO: Add NAICS to BEA mapping here
        demand[sector_input.code] = sector_input.amount
    
    try:
        result = model.calculate(
            demand=demand,
            impact_categories=request.impact_categories
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Format response
    impacts = []
    for code, value in result.total_impacts.items():
        category = model.impact_categories[code]
        impacts.append(ImpactResult(
            code=code,
            name=category.name,
            value=value,
            unit=category.unit
        ))
    
    return CalculationResponse(
        total_spending=sum(s.amount for s in request.sectors),
        impacts=impacts,
        sector_breakdown=result.sector_contributions,
        model_version=result.model_version
    )
```

```python
# backend/app/api/routes/sectors.py

from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
from app.core.dio_model import get_dio_model

router = APIRouter(prefix="/sectors", tags=["sectors"])

class SectorResponse(BaseModel):
    code: str
    name: str
    description: Optional[str]
    is_defense_relevant: bool = False

@router.get("/", response_model=List[SectorResponse])
async def list_sectors(
    query: Optional[str] = Query(None, description="Search query"),
    defense_only: bool = Query(False, description="Only defense-relevant sectors")
):
    """List available sectors, optionally filtered."""
    model = get_dio_model()
    
    if defense_only:
        sectors = model.get_defense_sectors()
    elif query:
        sectors = model.search_sectors(query)
    else:
        sectors = list(model.sectors.values())
    
    defense_codes = {s.code for s in model.get_defense_sectors()}
    
    return [
        SectorResponse(
            code=s.code,
            name=s.name,
            description=s.description,
            is_defense_relevant=s.code in defense_codes
        )
        for s in sectors
    ]

@router.get("/{code}", response_model=SectorResponse)
async def get_sector(code: str):
    """Get details for a specific sector."""
    model = get_dio_model()
    sector = model.get_sector(code)
    
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    
    defense_codes = {s.code for s in model.get_defense_sectors()}
    
    return SectorResponse(
        code=sector.code,
        name=sector.name,
        description=sector.description,
        is_defense_relevant=sector.code in defense_codes
    )
```

```python
# backend/app/api/routes/compare.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
from pathlib import Path

router = APIRouter(prefix="/compare", tags=["compare"])

class CountryComparison(BaseModel):
    country: str
    annual_emissions_mt: float
    comparison_text: str

class EquivalentComparison(BaseModel):
    description: str
    value: float
    unit: str

class ComparisonRequest(BaseModel):
    ghg_emissions_kg: float  # kg CO2e

class ComparisonResponse(BaseModel):
    countries: List[CountryComparison]
    equivalents: List[EquivalentComparison]

# Load reference data
DATA_PATH = Path(__file__).parent.parent.parent / 'data' / 'reference'

def load_country_emissions():
    """Load country emissions data (World Bank, latest year)."""
    # In production, load from CSV
    # For now, hardcoded sample
    return {
        'Portugal': 48.0,
        'Denmark': 32.0,
        'Sweden': 37.0,
        'Switzerland': 37.0,
        'New Zealand': 36.0,
        'Norway': 41.0,
        'Ireland': 57.0,
        'Finland': 41.0,
        'Hungary': 52.0,
        'Morocco': 73.0,
    }

def load_equivalents():
    """Load equivalents for context."""
    return {
        'cars_annual': {
            'factor': 4.6,  # metric tons CO2/car/year
            'unit': 'cars for one year',
            'description': 'Passenger vehicles driven for one year'
        },
        'homes_annual': {
            'factor': 8.0,  # metric tons CO2/home/year
            'unit': 'homes for one year',
            'description': 'Average US homes powered for one year'
        },
        'flights_nyc_la': {
            'factor': 0.0009,  # metric tons CO2/flight
            'unit': 'NYC-LA flights',
            'description': 'One-way flights from New York to Los Angeles'
        },
        'gallons_gasoline': {
            'factor': 0.00891,  # metric tons CO2/gallon
            'unit': 'gallons of gasoline burned',
            'description': 'Gallons of gasoline consumed'
        }
    }

@router.post("/", response_model=ComparisonResponse)
async def get_comparisons(request: ComparisonRequest):
    """Get contextual comparisons for emission amounts."""
    
    emissions_mt = request.ghg_emissions_kg / 1_000_000  # Convert kg to million metric tons
    
    # Country comparisons
    country_data = load_country_emissions()
    countries = []
    
    # Find countries with similar emissions
    sorted_countries = sorted(country_data.items(), key=lambda x: abs(x[1] - emissions_mt))
    
    for country, country_emissions in sorted_countries[:5]:
        ratio = emissions_mt / country_emissions if country_emissions > 0 else 0
        if ratio >= 1:
            text = f"Equivalent to {ratio:.1f}x {country}'s annual emissions"
        else:
            text = f"Equivalent to {ratio*100:.0f}% of {country}'s annual emissions"
        
        countries.append(CountryComparison(
            country=country,
            annual_emissions_mt=country_emissions,
            comparison_text=text
        ))
    
    # Everyday equivalents
    equiv_data = load_equivalents()
    equivalents = []
    
    for key, data in equiv_data.items():
        value = emissions_mt * 1_000_000 / data['factor']  # Convert back to metric tons
        equivalents.append(EquivalentComparison(
            description=data['description'],
            value=value,
            unit=data['unit']
        ))
    
    return ComparisonResponse(
        countries=countries,
        equivalents=equivalents
    )
```

### 2.4 Main Application

```python
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import calculate, sectors, compare

app = FastAPI(
    title="Open DIO API",
    description="Calculate environmental impacts of defense spending using the Defense Input-Output model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://open-dio.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(calculate.router, prefix="/api/v1")
app.include_router(sectors.router, prefix="/api/v1")
app.include_router(compare.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "name": "Open DIO API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## 3. Frontend Implementation

### 3.1 Key Components

```tsx
// frontend/src/components/SectorInput.tsx

import { useState } from 'react';
import { Combobox } from '@headlessui/react';
import { useSectors } from '../hooks/useSectors';

interface SectorEntry {
  code: string;
  name: string;
  amount: number;
}

interface Props {
  entries: SectorEntry[];
  onChange: (entries: SectorEntry[]) => void;
}

export function SectorInput({ entries, onChange }: Props) {
  const { sectors, isLoading } = useSectors({ defenseOnly: true });
  const [query, setQuery] = useState('');

  const filteredSectors = query === ''
    ? sectors
    : sectors?.filter(s => 
        s.name.toLowerCase().includes(query.toLowerCase()) ||
        s.code.includes(query)
      );

  const addEntry = (sector: { code: string; name: string }) => {
    onChange([...entries, { ...sector, amount: 0 }]);
  };

  const updateAmount = (index: number, amount: number) => {
    const updated = [...entries];
    updated[index] = { ...updated[index], amount };
    onChange(updated);
  };

  const removeEntry = (index: number) => {
    onChange(entries.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium">Add Spending by Sector</h3>
      
      {/* Sector selector */}
      <Combobox onChange={addEntry}>
        <Combobox.Input
          className="w-full border rounded-lg px-4 py-2"
          placeholder="Search sectors (e.g., Aircraft, Ships, Engineering...)"
          onChange={(e) => setQuery(e.target.value)}
        />
        <Combobox.Options className="mt-1 max-h-60 overflow-auto rounded-lg border bg-white shadow-lg">
          {filteredSectors?.map((sector) => (
            <Combobox.Option
              key={sector.code}
              value={sector}
              className="px-4 py-2 hover:bg-blue-50 cursor-pointer"
            >
              <span className="font-medium">{sector.name}</span>
              <span className="text-gray-500 text-sm ml-2">({sector.code})</span>
            </Combobox.Option>
          ))}
        </Combobox.Options>
      </Combobox>

      {/* Selected entries */}
      <div className="space-y-2">
        {entries.map((entry, index) => (
          <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <span className="font-medium">{entry.name}</span>
              <span className="text-gray-500 text-sm ml-2">({entry.code})</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-500">$</span>
              <input
                type="number"
                value={entry.amount || ''}
                onChange={(e) => updateAmount(index, parseFloat(e.target.value) || 0)}
                className="w-40 border rounded px-3 py-1 text-right"
                placeholder="0"
                min="0"
                step="1000000"
              />
            </div>
            <button
              onClick={() => removeEntry(index)}
              className="text-red-500 hover:text-red-700"
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      {entries.length > 0 && (
        <div className="text-right font-medium">
          Total: ${entries.reduce((sum, e) => sum + e.amount, 0).toLocaleString()}
        </div>
      )}
    </div>
  );
}
```

```tsx
// frontend/src/components/ResultsDashboard.tsx

import { ImpactResult } from '../types';
import { formatNumber, formatUnit } from '../utils/formatters';

interface Props {
  results: {
    totalSpending: number;
    impacts: ImpactResult[];
    modelVersion: string;
  };
  isLoading: boolean;
}

const IMPACT_CONFIG: Record<string, { icon: string; color: string }> = {
  'GHG': { icon: '🌡️', color: 'bg-red-100 text-red-800' },
  'ENRG': { icon: '⚡', color: 'bg-yellow-100 text-yellow-800' },
  'WATR': { icon: '💧', color: 'bg-blue-100 text-blue-800' },
  'LAND': { icon: '🌍', color: 'bg-green-100 text-green-800' },
};

export function ResultsDashboard({ results, isLoading }: Props) {
  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="h-24 bg-gray-200 rounded-lg" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Environmental Impact Results</h2>
        <span className="text-sm text-gray-500">
          Model: {results.modelVersion}
        </span>
      </div>

      <div className="text-lg text-gray-600">
        Analyzing spending of{' '}
        <span className="font-bold text-black">
          ${formatNumber(results.totalSpending)}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {results.impacts.map((impact) => {
          const config = IMPACT_CONFIG[impact.code] || { icon: '📊', color: 'bg-gray-100' };
          
          return (
            <div
              key={impact.code}
              className={`p-6 rounded-xl ${config.color}`}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="text-2xl">{config.icon}</span>
                <span className="font-medium text-lg">{impact.name}</span>
              </div>
              <div className="text-3xl font-bold">
                {formatNumber(impact.value)}
              </div>
              <div className="text-sm opacity-75">
                {formatUnit(impact.unit)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

```tsx
// frontend/src/components/ComparisonCards.tsx

import { ComparisonResponse } from '../types';
import { formatNumber } from '../utils/formatters';

interface Props {
  comparisons: ComparisonResponse | null;
  isLoading: boolean;
}

export function ComparisonCards({ comparisons, isLoading }: Props) {
  if (isLoading || !comparisons) {
    return (
      <div className="animate-pulse">
        <div className="h-48 bg-gray-200 rounded-lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold">Putting It In Context</h3>

      {/* Country comparisons */}
      <div className="bg-blue-50 rounded-xl p-6">
        <h4 className="font-medium text-blue-900 mb-4">
          Compared to Country Emissions
        </h4>
        <div className="space-y-3">
          {comparisons.countries.slice(0, 3).map((c) => (
            <div key={c.country} className="flex justify-between items-center">
              <span className="text-blue-800">{c.country}</span>
              <span className="text-sm text-blue-600">{c.comparison_text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Everyday equivalents */}
      <div className="grid grid-cols-2 gap-4">
        {comparisons.equivalents.map((eq) => (
          <div
            key={eq.description}
            className="bg-gray-50 rounded-lg p-4 text-center"
          >
            <div className="text-2xl font-bold">
              {formatNumber(eq.value)}
            </div>
            <div className="text-sm text-gray-600">
              {eq.unit}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 3.2 API Client

```typescript
// frontend/src/api/client.ts

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface SectorInput {
  code: string;
  amount: number;
}

export interface CalculationResponse {
  total_spending: number;
  impacts: Array<{
    code: string;
    name: string;
    value: number;
    unit: string;
  }>;
  sector_breakdown: Record<string, Record<string, number>>;
  model_version: string;
}

export interface Sector {
  code: string;
  name: string;
  description?: string;
  is_defense_relevant: boolean;
}

export interface ComparisonResponse {
  countries: Array<{
    country: string;
    annual_emissions_mt: number;
    comparison_text: string;
  }>;
  equivalents: Array<{
    description: string;
    value: number;
    unit: string;
  }>;
}

class ApiClient {
  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'API request failed');
    }

    return response.json();
  }

  async calculate(sectors: SectorInput[]): Promise<CalculationResponse> {
    return this.fetch('/calculate/', {
      method: 'POST',
      body: JSON.stringify({ sectors }),
    });
  }

  async getSectors(options?: { 
    query?: string; 
    defenseOnly?: boolean 
  }): Promise<Sector[]> {
    const params = new URLSearchParams();
    if (options?.query) params.set('query', options.query);
    if (options?.defenseOnly) params.set('defense_only', 'true');
    
    return this.fetch(`/sectors/?${params}`);
  }

  async getComparisons(ghgEmissionsKg: number): Promise<ComparisonResponse> {
    return this.fetch('/compare/', {
      method: 'POST',
      body: JSON.stringify({ ghg_emissions_kg: ghgEmissionsKg }),
    });
  }
}

export const apiClient = new ApiClient();
```

---

## 4. Testing Strategy

### 4.1 Backend Tests

```python
# backend/tests/test_calculate.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCalculateEndpoint:
    def test_calculate_single_sector(self):
        response = client.post('/api/v1/calculate/', json={
            'sectors': [{'code': '336411', 'amount': 1_000_000}]
        })
        assert response.status_code == 200
        data = response.json()
        assert data['total_spending'] == 1_000_000
        assert len(data['impacts']) > 0
        assert data['model_version'] == 'DIO v2.0'
    
    def test_calculate_multiple_sectors(self):
        response = client.post('/api/v1/calculate/', json={
            'sectors': [
                {'code': '336411', 'amount': 1_000_000},
                {'code': '336611', 'amount': 500_000},
            ]
        })
        assert response.status_code == 200
        data = response.json()
        assert data['total_spending'] == 1_500_000
    
    def test_invalid_sector_code(self):
        response = client.post('/api/v1/calculate/', json={
            'sectors': [{'code': 'INVALID', 'amount': 1_000_000}]
        })
        assert response.status_code == 400
    
    def test_empty_sectors(self):
        response = client.post('/api/v1/calculate/', json={
            'sectors': []
        })
        assert response.status_code == 422  # Validation error

class TestSectorsEndpoint:
    def test_list_all_sectors(self):
        response = client.get('/api/v1/sectors/')
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
    
    def test_defense_only_filter(self):
        response = client.get('/api/v1/sectors/?defense_only=true')
        assert response.status_code == 200
        data = response.json()
        assert all(s['is_defense_relevant'] for s in data)
    
    def test_search_sectors(self):
        response = client.get('/api/v1/sectors/?query=aircraft')
        assert response.status_code == 200
        data = response.json()
        assert any('aircraft' in s['name'].lower() for s in data)

class TestCompareEndpoint:
    def test_get_comparisons(self):
        response = client.post('/api/v1/compare/', json={
            'ghg_emissions_kg': 59_000_000_000  # 59 million metric tons
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data['countries']) > 0
        assert len(data['equivalents']) > 0
```

### 4.2 Validation Against Known Results

```python
# backend/tests/test_validation.py

import pytest
from app.core.dio_model import get_dio_model

class TestValidation:
    """Validate calculations against known results from literature."""
    
    def test_against_costs_of_war_estimate(self):
        """
        Costs of War project found ~59 million metric tons CO2 in 2017
        from DOD with ~$600 billion budget.
        
        Our estimate should be in the same order of magnitude.
        """
        model = get_dio_model()
        
        # Simplified distribution across major defense sectors
        # Based on DOD budget breakdown
        demand = {
            '336411': 50_000_000_000,   # Aircraft
            '336611': 30_000_000_000,   # Ships
            '336414': 20_000_000_000,   # Missiles
            '541330': 60_000_000_000,   # Engineering
            '541512': 40_000_000_000,   # IT Services
            '324110': 20_000_000_000,   # Fuel
            # ... other sectors
        }
        
        result = model.calculate(demand)
        ghg_kg = result.total_impacts.get('GHG', 0)
        ghg_mt = ghg_kg / 1_000_000_000  # Convert to million metric tons
        
        # Should be within 50% of 59 million MT
        assert 30 < ghg_mt < 90, f"GHG estimate {ghg_mt} MT outside expected range"
```

---

## 5. Deployment

### 5.1 Docker Configuration

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY data/ data/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - ENVIRONMENT=production
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000/api/v1
```

---

## 6. Data Preparation Checklist

### Phase 0: Update DIO to Current USEEIO (R Environment)

Prerequisites:
- [ ] R installed with devtools package
- [ ] Git access to Cornerstone and USEPA repos

Steps:
- [ ] Fork USEPA/DIO repository
- [ ] Install Cornerstone useeior: `devtools::install_github("cornerstone-data/useeior")`
- [ ] Review DIO.Rmd for deprecated useeior API calls
- [ ] Update DIO.Rmd to work with current useeior
- [ ] Download/update defense-specific satellite account data
- [ ] Rebuild DIO model
- [ ] Validate outputs against DIO v2.0 (document differences)
- [ ] Export model in both Excel and JSON formats
- [ ] Post to Cornerstone discussions for community review

### Phase 1: Web Application Data

- [ ] Use updated DIO model from Phase 0 (or DIO v2.0 if Phase 0 incomplete)
- [ ] Extract and validate matrix shapes match documentation
- [ ] Create NAICS-to-BEA crosswalk CSV
- [ ] Download World Bank country emissions CSV
- [ ] Create equivalents reference JSON
- [ ] Document any data transformations required

---

## 7. MVP Implementation Checklist

### Phase 0: DIO Model Update (Week 1-4)
- [ ] Engage with Cornerstone community (GitHub discussions)
- [ ] Set up R environment with Cornerstone useeior
- [ ] Analyze differences between useeior v1.2.1 and current
- [ ] Update DIO.Rmd for current useeior API
- [ ] Rebuild DIO model
- [ ] Validate and document outputs
- [ ] Export for Python consumption (Excel + JSON)

### Phase 1: Calculation Engine (Week 5-6)
- [ ] Set up Python project repository
- [ ] Implement DIO model loading from updated exports
- [ ] Implement basic calculation engine
- [ ] Create `/calculate` endpoint
- [ ] Write unit tests for calculation

### Phase 2: API Completion (Week 7-8)
- [ ] Create `/sectors` endpoint with search
- [ ] Create `/compare` endpoint
- [ ] Add NAICS mapping
- [ ] Set up CORS and error handling
- [ ] Deploy backend to staging

### Phase 3: Frontend (Week 9-10)
- [ ] Set up React project with Vite
- [ ] Build sector input component
- [ ] Build results dashboard
- [ ] Build comparison cards
- [ ] Connect to API

### Phase 4: Polish & Launch (Week 11-12)
- [ ] Add CSV upload functionality
- [ ] Add report export (PDF)
- [ ] Write documentation
- [ ] Set up production deployment
- [ ] Beta testing with target users
- [ ] Launch MVP

### Post-MVP: Contribute Back
- [ ] Package defense extensions for Cornerstone
- [ ] Submit PR or proposal to Cornerstone repos
- [ ] Document methodology for peer review

---

*Document Version: 1.0*  
*Prepared for: Claude Code Prototype Development*
