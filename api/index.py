import os
from supabase import create_client

from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Literal

# ================================
# CONFIGURATION
# ================================
API_KEY = "student-api-key-123"
API_VERSION = "1.0.0"

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

app = FastAPI(
    title="Simple Compound Element API",
    description="A beginner-friendly REST API containing information about chemical compounds.",
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================================
# DATA MODEL
# ===========================================================

class CompositionElement(BaseModel):
    element: str = Field(min_length=1)
    symbol: str = Field(min_length=1, max_length=3)
    atoms: int = Field(gt=0)

class PhysicalProperties(BaseModel):
    molarMass: float = Field(gt=0)
    state: Literal["solid", "liquid", "gas", "aqueous"]
    densityGPerCm3: float = Field(gt=0)
    meltingPointCelsius: Optional[float] = None
    boilingPointCelsius: Optional[float] = None
    pHValue: Optional[float] = Field(default=None, ge=0, le=14)

class SafetyData(BaseModel):
    signalWord: Literal["None", "Warning", "Danger"]
    isCorrosive: bool
    isFlammable: bool
    isToxic: bool
    hazardStatements: list[str] = Field(default_factory=list)

class Compound(BaseModel):
    id: int
    name: str = Field(min_length=1)
    formula: str = Field(min_length=1)
    smiles: str = Field(min_length=1)
    compoundType: Literal["acid", "base", "salt", "organic", "element", "other"]
    casNumber: str = Field(min_length=1)
    physicalProperties: PhysicalProperties
    composition: list[CompositionElement]
    safetyData: SafetyData
    uses: list[str] = Field(default_factory=list)
    description: str = Field(min_length=1)

# ===========================================================
# API KEY AUTHENTICATION
# ===========================================================
def verify_API_KEY(x_API_KEY: Optional[str] = Header(default=None)):
    if x_API_KEY != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key."
        )
    return True

# ===========================================================
# HEALTH CHECK (Public)
# ===========================================================
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "Simple Compound Element API",
        "version": API_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# ===========================================================
# HOME (Public)
# ===========================================================
@app.get("/")
def home():
    return {
        "message": "Welcome to the Simple Compound Element API!",
        "endpoints": [
            "/api/v1/compounds",
            "/api/v1/compounds/{id}",
            "/api/v1/compounds/search"
        ]
    }

# ===========================================================
# GET ALL COMPOUNDS (Protected)
# ===========================================================
@app.get("/api/v1/compounds", dependencies=[Depends(verify_API_KEY)])
def get_compounds():
    return {
        "count": len(compounds),
        "compounds": compounds
    }

# ===========================================================
# SEARCH COMPOUNDS (Protected)
# ===========================================================
@app.get("/api/v1/compounds/search", dependencies=[Depends(verify_API_KEY)])
def search_compounds(q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []

    for compound in compounds:
        element_names = " ".join(c["element"] for c in compound["composition"])
        element_symbols = " ".join(c["symbol"] for c in compound["composition"])
        uses_text = " ".join(compound.get("uses", []))
        hazard_text = " ".join(compound["safetyData"].get("hazardStatements", []))

        searchable_text = (
            f"{compound['name']} "
            f"{compound['formula']} "
            f"{compound['smiles']} "
            f"{compound.get('compoundType', '')} "
            f"{compound.get('casNumber', '')} "
            f"{element_names} "
            f"{element_symbols} "
            f"{uses_text} "
            f"{compound['physicalProperties']['state']} "
            f"{compound['safetyData']['signalWord']} "
            f"{hazard_text}"
        ).lower()

        if q in searchable_text:
            results.append(compound)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# ===========================================================
# GET ONE COMPOUND (Protected)
# ===========================================================
@app.get("/api/v1/compounds/{compound_id}", dependencies=[Depends(verify_API_KEY)])
def get_compound(compound_id: int):
    for compound in compounds:
        if compound["id"] == compound_id:
            return compound

    raise HTTPException(status_code=404, detail="Compound not found.")