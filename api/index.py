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
API_KEY = os.environ["API_KEY"]
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

class CraftElementInput(BaseModel):
    symbol: str = Field(min_length=1, max_length=3)
    atoms: int = Field(gt=0)

class CraftRequest(BaseModel):
    elements: list[CraftElementInput] = Field(min_length=2, max_length=2)


# ===========================================================
# DATABASE HELPERS (Supabase)
# ===========================================================
# Joins each compound with its rows from compound_composition
COMPOUND_SELECT = "*, compound_composition(element, symbol, atoms)"

def to_api(row):
    """Convert a database row (snake_case, flat) into the API's response shape,
    validating it against the Compound model on the way out."""
    compound = {
        "id": row["id"],
        "name": row["name"],
        "formula": row["formula"],
        "smiles": row["smiles"],
        "compoundType": row["compound_type"],
        "casNumber": row["cas_number"],
        "physicalProperties": {
            "molarMass": row["molar_mass"],
            "state": row["state"],
            "densityGPerCm3": row["density"],
            "meltingPointCelsius": row["melting_point"],
            "boilingPointCelsius": row["boiling_point"],
            "pHValue": row["ph_value"],
        },
        "composition": row["compound_composition"],
        "safetyData": {
            "signalWord": row["signal_word"],
            "isCorrosive": row["is_corrosive"],
            "isFlammable": row["is_flammable"],
            "isToxic": row["is_toxic"],
            "hazardStatements": row["hazard_statements"] or [],
        },
        "uses": row["uses"] or [],
        "description": row["description"],
    }
    return Compound(**compound).model_dump()

def fetch_all():
    result = (
        supabase.table("compounds")
        .select(COMPOUND_SELECT)
        .order("id")
        .execute()
    )
    return [to_api(row) for row in result.data]

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
    compounds = fetch_all()
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

    for compound in fetch_all():
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
    result = (
        supabase.table("compounds")
        .select(COMPOUND_SELECT)
        .eq("id", compound_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Compound not found.")

    return to_api(result.data[0])

# ===========================================================
# GET ALL ELEMENTS (Protected)
# ===========================================================
@app.get("/api/v1/elements", dependencies=[Depends(verify_API_KEY)])
def get_elements():
    result = (
        supabase.table("elements")
        .select("*")
        .order("atomic_number")
        .execute()
    )
    return {
        "count": len(result.data),
        "elements": result.data
    }