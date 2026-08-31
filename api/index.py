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
        "elements": ["Hydrogen", "Oxygen"],
        "molar_mass": 18.015,
        "state": "Liquid",
        "category": "Oxide",
        "description": "A colorless, odorless liquid essential to all known forms of life."
    },

    {
        "id": 2,
        "name": "Carbon Dioxide",
        "formula": "CO2",
        "elements": ["Carbon", "Oxygen"],
        "molar_mass": 44.01,
        "state": "Gas",
        "category": "Oxide",
        "description": "A colorless gas produced by respiration and combustion."
    },

    {
        "id": 3,
        "name": "Sodium Chloride",
        "formula": "NaCl",
        "elements": ["Sodium", "Chlorine"],
        "molar_mass": 58.44,
        "state": "Solid",
        "category": "Salt",
        "description": "Common table salt, formed from a metal and a halogen."
    },

    {
        "id": 4,
        "name": "Glucose",
        "formula": "C6H12O6",
        "elements": ["Carbon", "Hydrogen", "Oxygen"],
        "molar_mass": 180.16,
        "state": "Solid",
        "category": "Carbohydrate",
        "description": "A simple sugar and a key energy source for living cells."
    },

    {
        "id": 5,
        "name": "Ammonia",
        "formula": "NH3",
        "elements": ["Nitrogen", "Hydrogen"],
        "molar_mass": 17.03,
        "state": "Gas",
        "category": "Base",
        "description": "A pungent gas widely used in fertilizers and cleaning products."
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
        searchable_text = (
            f"{compound['name']} "
            f"{compound['formula']} "
            f"{' '.join(compound['elements'])} "
            f"{compound['category']}"
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