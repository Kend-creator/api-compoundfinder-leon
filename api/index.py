from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Simple Compound Element API",
    description="A beginner-friendly REST API containing information about chemical compounds.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# COMPOUND DATA
compounds = [

    {
        "id": 1,
        "name": "Water",
        "formula": "H2O",
        "smiles": "O",
        "physicalProperties": {
            "molarMass": 18.015,
            "state": "liquid",
            "densityGPerCm3": 1.0,
            "meltingPointCelsius": 0.0,
            "boilingPointCelsius": 100.0
        },
        "composition": [
            {"element": "Hydrogen", "symbol": "H", "atoms": 2},
            {"element": "Oxygen", "symbol": "O", "atoms": 1}
        ],
        "safetyData": {
            "signalWord": "None",
            "isCorrosive": False
        },
        "description": "A colorless, odorless liquid essential to all known forms of life."
    },

    {
        "id": 2,
        "name": "Carbon Dioxide",
        "formula": "CO2",
        "smiles": "O=C=O",
        "physicalProperties": {
            "molarMass": 44.01,
            "state": "gas",
            "densityGPerCm3": 0.00184,
            "meltingPointCelsius": -56.6,
            "boilingPointCelsius": -78.5
        },
        "composition": [
            {"element": "Carbon", "symbol": "C", "atoms": 1},
            {"element": "Oxygen", "symbol": "O", "atoms": 2}
        ],
        "safetyData": {
            "signalWord": "None",
            "isCorrosive": False
        },
        "description": "A colorless gas produced by respiration and combustion."
    },

    {
        "id": 3,
        "name": "Sodium Chloride",
        "formula": "NaCl",
        "smiles": "[Na+].[Cl-]",
        "physicalProperties": {
            "molarMass": 58.44,
            "state": "solid",
            "densityGPerCm3": 2.16,
            "meltingPointCelsius": 801.0,
            "boilingPointCelsius": 1465.0
        },
        "composition": [
            {"element": "Sodium", "symbol": "Na", "atoms": 1},
            {"element": "Chlorine", "symbol": "Cl", "atoms": 1}
        ],
        "safetyData": {
            "signalWord": "None",
            "isCorrosive": False
        },
        "description": "Common table salt, formed from a metal and a halogen."
    },

    {
        "id": 4,
        "name": "Glucose",
        "formula": "C6H12O6",
        "smiles": "OCC1OC(O)C(O)C(O)C1O",
        "physicalProperties": {
            "molarMass": 180.16,
            "state": "solid",
            "densityGPerCm3": 1.54,
            "meltingPointCelsius": 150.0,
            "boilingPointCelsius": None
        },
        "composition": [
            {"element": "Carbon", "symbol": "C", "atoms": 6},
            {"element": "Hydrogen", "symbol": "H", "atoms": 12},
            {"element": "Oxygen", "symbol": "O", "atoms": 6}
        ],
        "safetyData": {
            "signalWord": "None",
            "isCorrosive": False
        },
        "description": "A simple sugar and a key energy source for living cells."
    },

    {
        "id": 5,
        "name": "Ammonia",
        "formula": "NH3",
        "smiles": "N",
        "physicalProperties": {
            "molarMass": 17.03,
            "state": "gas",
            "densityGPerCm3": 0.00073,
            "meltingPointCelsius": -77.7,
            "boilingPointCelsius": -33.3
        },
        "composition": [
            {"element": "Nitrogen", "symbol": "N", "atoms": 1},
            {"element": "Hydrogen", "symbol": "H", "atoms": 3}
        ],
        "safetyData": {
            "signalWord": "Warning",
            "isCorrosive": True
        },
        "description": "A pungent gas widely used in fertilizers and cleaning products."
    },

    {
        "id": 6,
        "name": "Sulfuric Acid",
        "formula": "H2SO4",
        "smiles": "O=S(=O)(O)O",
        "physicalProperties": {
            "molarMass": 98.079,
            "state": "liquid",
            "densityGPerCm3": 1.83,
            "meltingPointCelsius": 10.31,
            "boilingPointCelsius": 337.0
        },
        "composition": [
            {"element": "Hydrogen", "symbol": "H", "atoms": 2},
            {"element": "Sulfur", "symbol": "S", "atoms": 1},
            {"element": "Oxygen", "symbol": "O", "atoms": 4}
        ],
        "safetyData": {
            "signalWord": "Danger",
            "isCorrosive": True
        },
        "description": "A highly corrosive strong acid used widely in industrial processes."
    }

]

# HOME
@app.get("/")
def home():

    return {
        "message": "Welcome to the Simple Compound Element API!",
        "endpoints": [
            "/compounds",
            "/compounds/{id}",
            "/compounds/search"
        ]
    }


# GET ALL COMPOUNDS
@app.get("/compounds")
def get_compounds():

    return {
        "count": len(compounds),
        "compounds": compounds
    }


# SEARCH COMPOUNDS
@app.get("/compounds/search")
def search_compounds(q: str = Query(..., min_length=1)):
    q = q.lower()
    results = []
    for compound in compounds:
        element_names = " ".join(c["element"] for c in compound["composition"])
        element_symbols = " ".join(c["symbol"] for c in compound["composition"])
        searchable_text = (
            f"{compound['name']} "
            f"{compound['formula']} "
            f"{element_names} "
            f"{element_symbols}"
        ).lower()

        if q in searchable_text:
            results.append(compound)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# GET ONE COMPOUND
@app.get("/compounds/{compound_id}")
def get_compound(compound_id: int):

    for compound in compounds:

        if compound["id"] == compound_id:
            return compound

    raise HTTPException(
        status_code=404,
        detail="Compound not found."
    )