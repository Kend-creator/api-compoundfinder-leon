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
    },

    
    {
        "id": 7,
        "name": "Ethanol",
        "formula": "C2H6O",
        "smiles": "CCO",
        "physicalProperties": {
        "molarMass": 46.07,
        "state": "liquid",
        "densityGPerCm3": 0.789,
        "meltingPointCelsius": -114.1,
        "boilingPointCelsius": 78.37
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 2 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 6 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False
        }
    },

    {
        "id": 8,
        "name": "Methane",
        "formula": "CH4",
        "smiles": "C",
        "physicalProperties": {
        "molarMass": 16.04,
        "state": "gas",
        "densityGPerCm3": 0.000656,
        "meltingPointCelsius": -182.5,
        "boilingPointCelsius": -161.5
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 1 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 4 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False
        }
    },

    {
        "id": 9,
        "name": "Hydrochloric Acid",
        "formula": "HCl",
        "smiles": "Cl",
        "physicalProperties": {
        "molarMass": 36.46,
        "state": "liquid",
        "densityGPerCm3": 1.19,
        "meltingPointCelsius": -30.0,
        "boilingPointCelsius": 108.5
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True
        }
    },

    {
        "id": 10,
        "name": "Sodium Hydroxide",
        "formula": "NaOH",
        "smiles": "[OH-].[Na+]",
        "physicalProperties": {
        "molarMass": 39.997,
        "state": "solid",
        "densityGPerCm3": 2.13,
        "meltingPointCelsius": 323.0,
        "boilingPointCelsius": 1388.0
        },
        "composition": [
        { "element": "Sodium", "symbol": "Na", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True
        }
    },

    {
        "id": 11,
        "name": "Acetone",
        "formula": "C3H6O",
        "smiles": "CC(=O)C",
        "physicalProperties": {
        "molarMass": 58.08,
        "state": "liquid",
        "densityGPerCm3": 0.784,
        "meltingPointCelsius": -94.7,
        "boilingPointCelsius": 56.05
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 3 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 6 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False
        }
    }


    {
        "id": 12,
        "name": "Hydrogen Peroxide",
        "formula": "H2O2",
        "smiles": "OO",
        "physicalProperties": {
        "molarMass": 34.014,
        "state": "liquid",
        "densityGPerCm3": 1.45,
        "meltingPointCelsius": -0.43,
        "boilingPointCelsius": 150.2
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 2 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": true
        }
    },
    
    {
        "id": 13,
        "name": "Acetic Acid",
        "formula": "C2H4O2",
        "smiles": "CC(=O)O",
        "physicalProperties": {
        "molarMass": 60.05,
        "state": "liquid",
        "densityGPerCm3": 1.049,
        "meltingPointCelsius": 16.6,
        "boilingPointCelsius": 117.9
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 2 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 4 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": true
        }
    },

    {
        "id": 14,
        "name": "Calcium Carbonate",
        "formula": "CaCO3",
        "smiles": "[Ca+2].[O-]C([O-])=O",
        "physicalProperties": {
        "molarMass": 100.086,
        "state": "solid",
        "densityGPerCm3": 2.71,
        "meltingPointCelsius": 1339.0,
        "boilingPointCelsius": 0.0
        },
        "composition": [
        { "element": "Calcium", "symbol": "Ca", "atoms": 1 },
        { "element": "Carbon", "symbol": "C", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": false
        }
    },

    {
        "id": 15,
        "name": "Nitric Acid",
        "formula": "HNO3",
        "smiles": "[O-][N+](=O)O",
        "physicalProperties": {
        "molarMass": 63.01,
        "state": "liquid",
        "densityGPerCm3": 1.51,
        "meltingPointCelsius": -42.0,
        "boilingPointCelsius": 83.0
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 },
        { "element": "Nitrogen", "symbol": "N", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": true
        }
    },

    {
        "id": 16,
        "name": "Propane",
        "formula": "C3H8",
        "smiles": "CCC",
        "physicalProperties": {
        "molarMass": 44.1,
        "state": "gas",
        "densityGPerCm3": 0.00183,
        "meltingPointCelsius": -187.7,
        "boilingPointCelsius": -42.1
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 3 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 8 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": false
        }
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