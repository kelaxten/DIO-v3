"""
Open DIO FastAPI Backend

Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import calculate, sectors
from app.api.schemas.response import HealthResponse

# Create FastAPI app
app = FastAPI(
    title="Open DIO API",
    description="""
    Calculate environmental impacts of defense spending using the
    Defense Input-Output (DIO) model.

    ## Features
    - **Calculate impacts**: POST /api/v1/calculate
    - **List sectors**: GET /api/v1/sectors
    - **Health check**: GET /health

    ## Data Source
    Based on EPA's Defense Input-Output Model v2.0

    ## Method
    Environmentally-Extended Input-Output Analysis
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "http://localhost:3000",  # Alternative local
        "https://kelaxten.github.io",  # GitHub Pages
        "*"  # Allow all for now (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    calculate.router,
    prefix="/api/v1/calculate",
    tags=["calculate"]
)

app.include_router(
    sectors.router,
    prefix="/api/v1/sectors",
    tags=["sectors"]
)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "name": "Open DIO API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "calculate": "/api/v1/calculate",
            "sectors": "/api/v1/sectors",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model="DIO v2.0"
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize calculator on startup"""
    from app.core.calculator import get_calculator
    try:
        calculator = get_calculator()
        print(f"✓ Calculator initialized with {len(calculator.multipliers)} sectors")
    except Exception as e:
        print(f"✗ Failed to initialize calculator: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
