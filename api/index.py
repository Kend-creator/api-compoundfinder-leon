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

# COMPOUND DATA
compounds = [

    {
        "id": 1,
        "name": "Water",
        "formula": "H2O",
        "smiles": "O",
        "compoundType": "other",
        "casNumber": "7732-18-5",
        "physicalProperties": {
        "molarMass": 18.015,
        "state": "liquid",
        "densityGPerCm3": 1.0,
        "meltingPointCelsius": 0.0,
        "boilingPointCelsius": 100.0,
        "pHValue": 7.0
        },
        "composition": [
        {"element": "Hydrogen", "symbol": "H", "atoms": 2},
        {"element": "Oxygen", "symbol": "O", "atoms": 1}
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Drinking water", "Solvent", "Coolant", "Hydration"],
        "description": "A colorless, odorless liquid essential to all known forms of life."
    },

    {
        "id": 2,
        "name": "Carbon Dioxide",
        "formula": "CO2",
        "smiles": "O=C=O",
        "compoundType": "other",
        "casNumber": "124-38-9",
        "physicalProperties": {
        "molarMass": 44.01,
        "state": "gas",
        "densityGPerCm3": 0.00184,
        "meltingPointCelsius": -56.6,
        "boilingPointCelsius": -78.5,
        "pHValue": None
        },
        "composition": [
        {"element": "Carbon", "symbol": "C", "atoms": 1},
        {"element": "Oxygen", "symbol": "O", "atoms": 2}
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Carbonation", "Fire extinguishers", "Dry ice", "Photosynthesis feedstock"],
        "description": "A colorless gas produced by respiration and combustion."
    },

    {
        "id": 3,
        "name": "Sodium Chloride",
        "formula": "NaCl",
        "smiles": "[Na+].[Cl-]",
        "compoundType": "salt",
        "casNumber": "7647-14-5",
        "physicalProperties": {
        "molarMass": 58.44,
        "state": "solid",
        "densityGPerCm3": 2.16,
        "meltingPointCelsius": 801.0,
        "boilingPointCelsius": 1465.0,
        "pHValue": 7.0
        },
        "composition": [
        {"element": "Sodium", "symbol": "Na", "atoms": 1},
        {"element": "Chlorine", "symbol": "Cl", "atoms": 1}
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Food seasoning", "Food preservative", "De-icing roads", "Water softening"],
        "description": "Common table salt, formed from a metal and a halogen."
    },

    {
        "id": 4,
        "name": "Glucose",
        "formula": "C6H12O6",
        "smiles": "OCC1OC(O)C(O)C(O)C1O",
        "compoundType": "organic",
        "casNumber": "50-99-7",
        "physicalProperties": {
        "molarMass": 180.16,
        "state": "solid",
        "densityGPerCm3": 1.54,
        "meltingPointCelsius": 150.0,
        "boilingPointCelsius": None,
        "pHValue": 6.0
        },
        "composition": [
        {"element": "Carbon", "symbol": "C", "atoms": 6},
        {"element": "Hydrogen", "symbol": "H", "atoms": 12},
        {"element": "Oxygen", "symbol": "O", "atoms": 6}
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Energy source for cells", "IV fluids", "Food sweetener", "Fermentation feedstock"],
        "description": "A simple sugar and a key energy source for living cells."
    },

    {
        "id": 5,
        "name": "Ammonia",
        "formula": "NH3",
        "smiles": "N",
        "compoundType": "base",
        "casNumber": "7664-41-7",
        "physicalProperties": {
        "molarMass": 17.03,
        "state": "gas",
        "densityGPerCm3": 0.00073,
        "meltingPointCelsius": -77.7,
        "boilingPointCelsius": -33.3,
        "pHValue": 11.6
        },
        "composition": [
        {"element": "Nitrogen", "symbol": "N", "atoms": 1},
        {"element": "Hydrogen", "symbol": "H", "atoms": 3}
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": True,
        "isToxic": True,
        "hazardStatements": ["H221", "H314", "H331"]
        },
                "uses": ["Fertilizer production", "Cleaning products", "Refrigerant"],
        "description": "A pungent gas widely used in fertilizers and cleaning products."
    },

    {
        "id": 6,
        "name": "Sulfuric Acid",
        "formula": "H2SO4",
        "smiles": "O=S(=O)(O)O",
        "compoundType": "acid",
        "casNumber": "7664-93-9",
        "physicalProperties": {
        "molarMass": 98.079,
        "state": "liquid",
        "densityGPerCm3": 1.83,
        "meltingPointCelsius": 10.31,
        "boilingPointCelsius": 337.0,
        "pHValue": 1.0
        },
        "composition": [
        {"element": "Hydrogen", "symbol": "H", "atoms": 2},
        {"element": "Sulfur", "symbol": "S", "atoms": 1},
        {"element": "Oxygen", "symbol": "O", "atoms": 4}
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H314", "H290"]
        },
                "uses": ["Car batteries", "Fertilizer production", "Industrial synthesis", "Metal processing"],
        "description": "A highly corrosive strong acid used widely in industrial processes."
    },

    {
        "id": 7,
        "name": "Ethanol",
        "formula": "C2H6O",
        "smiles": "CCO",
        "compoundType": "organic",
        "casNumber": "64-17-5",
        "physicalProperties": {
        "molarMass": 46.07,
        "state": "liquid",
        "densityGPerCm3": 0.789,
        "meltingPointCelsius": -114.1,
        "boilingPointCelsius": 78.37,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 2 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 6 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H225", "H319"]
        },
                "uses": ["Solvent", "Fuel additive", "Alcoholic beverages", "Disinfectant"],
        "description": "A volatile, flammable, and colorless liquid organic compound commonly used as a solvent, fuel source, and the active alcohol in beverages."
    },

    {
        "id": 8,
        "name": "Methane",
        "formula": "CH4",
        "smiles": "C",
        "compoundType": "organic",
        "casNumber": "74-82-8",
        "physicalProperties": {
        "molarMass": 16.04,
        "state": "gas",
        "densityGPerCm3": 0.000656,
        "meltingPointCelsius": -182.5,
        "boilingPointCelsius": -161.5,
        "pHValue": None
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 1 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 4 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H220"]
        },
                "uses": ["Fuel", "Natural gas heating", "Hydrogen production"],
        "description": "The simplest alkane and primary component of natural gas, highly flammable and commonly used as a fuel source."
    },

    {
        "id": 9,
        "name": "Hydrochloric Acid",
        "formula": "HCl",
        "smiles": "Cl",
        "compoundType": "acid",
        "casNumber": "7647-01-0",
        "physicalProperties": {
        "molarMass": 36.46,
        "state": "liquid",
        "densityGPerCm3": 1.19,
        "meltingPointCelsius": -30.0,
        "boilingPointCelsius": 108.5,
        "pHValue": 1.0
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H314", "H335"]
        },
                "uses": ["Metal pickling", "pH adjustment", "Food processing"],
        "description": "A strong, highly corrosive mineral acid with major industrial applications and a main constituent of gastric acid."
    },

    {
        "id": 11,
        "name": "Acetone",
        "formula": "C3H6O",
        "smiles": "CC(=O)C",
        "compoundType": "organic",
        "casNumber": "67-64-1",
        "physicalProperties": {
        "molarMass": 58.08,
        "state": "liquid",
        "densityGPerCm3": 0.784,
        "meltingPointCelsius": -94.7,
        "boilingPointCelsius": 56.05,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 3 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 6 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H225", "H319", "H336"]
        },
                "uses": ["Nail polish remover", "Industrial solvent", "Paint thinner"],
        "description": "A volatile, flammable organic solvent widely used in industrial cleaning, cosmetics, and paint thinners."
    },

    {
        "id": 12,
        "name": "Hydrogen Peroxide",
        "formula": "H2O2",
        "smiles": "OO",
        "compoundType": "other",
        "casNumber": "7722-84-1",
        "physicalProperties": {
        "molarMass": 34.014,
        "state": "liquid",
        "densityGPerCm3": 1.45,
        "meltingPointCelsius": -0.43,
        "boilingPointCelsius": 150.2,
        "pHValue": 4.5
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 2 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H271", "H314", "H332"]
        },
                "uses": ["Disinfectant", "Bleaching agent", "Antiseptic"],
        "description": "A pale blue, powerful oxidizing agent commonly used as a bleaching agent, disinfectant, and antiseptic."
    },

    {
        "id": 13,
        "name": "Acetic Acid",
        "formula": "C2H4O2",
        "smiles": "CC(=O)O",
        "compoundType": "acid",
        "casNumber": "64-19-7",
        "physicalProperties": {
        "molarMass": 60.05,
        "state": "liquid",
        "densityGPerCm3": 1.049,
        "meltingPointCelsius": 16.6,
        "boilingPointCelsius": 117.9,
        "pHValue": 2.4
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 2 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 4 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H226", "H314"]
        },
                "uses": ["Food preservative (vinegar)", "Solvent", "Textile dyeing"],
        "description": "A weak organic acid responsible for the sour taste and pungent smell of vinegar, used as a food preservative and solvent."
    },

    {
        "id": 14,
        "name": "Calcium Carbonate",
        "formula": "CaCO3",
        "smiles": "[Ca+2].[O-]C([O-])=O",
        "compoundType": "salt",
        "casNumber": "471-34-1",
        "physicalProperties": {
        "molarMass": 100.086,
        "state": "solid",
        "densityGPerCm3": 2.71,
        "meltingPointCelsius": 1339.0,
        "boilingPointCelsius": 0.0,
        "pHValue": 9.9
        },
        "composition": [
        { "element": "Calcium", "symbol": "Ca", "atoms": 1 },
        { "element": "Carbon", "symbol": "C", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Antacid", "Building material", "Calcium supplement"],
        "description": "A common white mineral substance found in rocks like limestone and marble, used as a building material and antacid."
    },

    {
        "id": 15,
        "name": "Nitric Acid",
        "formula": "HNO3",
        "smiles": "[O-][N+](=O)O",
        "compoundType": "acid",
        "casNumber": "7697-37-2",
        "physicalProperties": {
        "molarMass": 63.01,
        "state": "liquid",
        "densityGPerCm3": 1.51,
        "meltingPointCelsius": -42.0,
        "boilingPointCelsius": 83.0,
        "pHValue": 1.0
        },
        "composition": [
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 },
        { "element": "Nitrogen", "symbol": "N", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H272", "H314"]
        },
                "uses": ["Fertilizer production", "Explosives manufacturing", "Metal etching"],
        "description": "A highly corrosive and toxic mineral acid used primarily in the production of nitrogen fertilizers and explosives."
    },

    {
        "id": 16,
        "name": "Propane",
        "formula": "C3H8",
        "smiles": "CCC",
        "compoundType": "organic",
        "casNumber": "74-98-6",
        "physicalProperties": {
        "molarMass": 44.1,
        "state": "gas",
        "densityGPerCm3": 0.00183,
        "meltingPointCelsius": -187.7,
        "boilingPointCelsius": -42.1,
        "pHValue": None
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 3 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 8 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H220", "H280"]
        },
                "uses": ["Heating fuel", "Cooking gas", "Engine fuel"],
        "description": "A colorless, flammable hydrocarbon gas commonly compressed and used as fuel for heating, cooking, and engines."
    },

    {
        "id": 17,
        "name": "Sodium Bicarbonate",
        "formula": "NaHCO3",
        "smiles": "[Na+].OC([O-])=O",
        "compoundType": "salt",
        "casNumber": "144-55-8",
        "physicalProperties": {
        "molarMass": 84.007,
        "state": "solid",
        "densityGPerCm3": 2.2,
        "meltingPointCelsius": 50.0,
        "boilingPointCelsius": 0.0,
        "pHValue": 8.3
        },
        "composition": [
        { "element": "Sodium", "symbol": "Na", "atoms": 1 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 1 },
        { "element": "Carbon", "symbol": "C", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Baking (leavening agent)", "Antacid", "Cleaning agent"],
        "description": "A crystalline solid widely known as baking soda, used in leavening, cleaning, and neutralizing excess stomach acid."
    },

    {
        "id": 18,
        "name": "Isopropanol",
        "formula": "C3H8O",
        "smiles": "CC(C)O",
        "compoundType": "organic",
        "casNumber": "67-63-0",
        "physicalProperties": {
        "molarMass": 60.1,
        "state": "liquid",
        "densityGPerCm3": 0.786,
        "meltingPointCelsius": -89.0,
        "boilingPointCelsius": 82.6,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 3 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 8 },
        { "element": "Oxygen", "symbol": "O", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": False,
        "hazardStatements": ["H225", "H319", "H336"]
        },
                "uses": ["Rubbing alcohol / disinfectant", "Solvent", "Electronics cleaning"],
        "description": "A volatile, clear liquid commonly known as rubbing alcohol, extensively used as a solvent and topical disinfectant."
    },

    {
        "id": 19,
        "name": "Sucrose",
        "formula": "C12H22O11",
        "smiles": "C1(C(C(C(C(O1)CO)O)O)O)OC2(C(C(C(O2)CO)O)O)CO",
        "compoundType": "organic",
        "casNumber": "57-50-1",
        "physicalProperties": {
        "molarMass": 342.3,
        "state": "solid",
        "densityGPerCm3": 1.587,
        "meltingPointCelsius": 186.0,
        "boilingPointCelsius": 0.0,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Carbon", "symbol": "C", "atoms": 12 },
        { "element": "Hydrogen", "symbol": "H", "atoms": 22 },
        { "element": "Oxygen", "symbol": "O", "atoms": 11 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
                "uses": ["Sweetener", "Food preservative", "Fermentation feedstock"],
        "description": "A naturally occurring disaccharide composed of glucose and fructose, commonly extracted and refined as table sugar."
    },

    {
        "id": 20,
        "name": "Sulfur Dioxide",
        "formula": "SO2",
        "smiles": "O=S=O",
        "compoundType": "other",
        "casNumber": "7446-09-5",
        "physicalProperties": {
        "molarMass": 64.066,
        "state": "gas",
        "densityGPerCm3": 0.00263,
        "meltingPointCelsius": -72.0,
        "boilingPointCelsius": -10.0,
        "pHValue": 3.0
        },
        "composition": [
        { "element": "Sulfur", "symbol": "S", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H314", "H331"]
        },
                "uses": ["Food preservative", "Wine production", "Industrial bleaching agent"],
        "description": "A pungent, toxic gas produced by volcanic activity and industrial burning of coal or oil, used as a preservative."
    }

]

# Validation of dataset
validated_compounds = [Compound(**compound).model_dump() for compound in compounds]
compounds = validated_compounds

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