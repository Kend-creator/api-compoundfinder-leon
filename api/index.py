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
        "id": 10,
        "name": "Titanium Diboride",
        "formula": "TiB2",
        "smiles": "B#[Ti]#B",
        "compoundType": "other",
        "casNumber": "12045-63-5",
        "physicalProperties": {
        "molarMass": 69.49,
        "state": "solid",
        "densityGPerCm3": 4.52,
        "meltingPointCelsius": 3225.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Titanium", "symbol": "Ti", "atoms": 1 },
        { "element": "Boron", "symbol": "B", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H315", "H319", "H335"]
        },
        "uses": ["Ceramic armor", "Cutting tools", "Aluminum smelting electrodes", "Wear-resistant coatings"],
        "description": "An extremely hard, electrically conductive ceramic with a very high melting point and strong resistance to wear and corrosion."
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
        "name": "Zinc Selenide",
        "formula": "ZnSe",
        "smiles": "[Zn]=[Se]",
        "compoundType": "other",
        "casNumber": "1315-09-9",
        "physicalProperties": {
        "molarMass": 144.38,
        "state": "solid",
        "densityGPerCm3": 5.27,
        "meltingPointCelsius": 1525.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Zinc", "symbol": "Zn", "atoms": 1 },
        { "element": "Selenium", "symbol": "Se", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H301", "H331", "H373", "H410"]
        },
        "uses": ["Infrared optics", "CO2 laser lenses and windows", "Thermal imaging", "Blue-green LEDs"],
        "description": "A pale yellow semiconductor that transmits infrared light extremely well, making it a standard material for high-power laser optics."
    },

    {
        "id": 21,
        "name": "Potassium Iodide",
        "formula": "KI",
        "smiles": "[K+].[I-]",
        "compoundType": "salt",
        "casNumber": "7681-11-0",
        "physicalProperties": {
        "molarMass": 166.0,
        "state": "solid",
        "densityGPerCm3": 3.123,
        "meltingPointCelsius": 681.0,
        "boilingPointCelsius": 1330.0,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Potassium", "symbol": "K", "atoms": 1 },
        { "element": "Iodine", "symbol": "I", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H372"]
        },
        "uses": ["Iodized salt", "Thyroid protection during radiation emergencies", "Photography", "Expectorant"],
        "description": "A white crystalline salt that is the most common source of iodine in nutrition and medicine."
    },

    {
        "id": 22,
        "name": "Magnesium Fluoride",
        "formula": "MgF2",
        "smiles": "[Mg+2].[F-].[F-]",
        "compoundType": "salt",
        "casNumber": "7783-40-6",
        "physicalProperties": {
        "molarMass": 62.30,
        "state": "solid",
        "densityGPerCm3": 3.148,
        "meltingPointCelsius": 1263.0,
        "boilingPointCelsius": 2260.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Magnesium", "symbol": "Mg", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H315", "H319", "H335"]
        },
        "uses": ["Anti-reflective lens coatings", "Optical windows", "Ceramics", "Aluminum metallurgy"],
        "description": "A transparent, poorly soluble ionic solid valued for its optical clarity from ultraviolet to infrared wavelengths."
    },

    {
        "id": 23,
        "name": "Aluminium Phosphide",
        "formula": "AlP",
        "smiles": "[Al]#P",
        "compoundType": "other",
        "casNumber": "20859-73-8",
        "physicalProperties": {
        "molarMass": 57.96,
        "state": "solid",
        "densityGPerCm3": 2.85,
        "meltingPointCelsius": 2550.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Aluminium", "symbol": "Al", "atoms": 1 },
        { "element": "Phosphorus", "symbol": "P", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": True,
        "isToxic": True,
        "hazardStatements": ["H260", "H300", "H330", "H400"]
        },
        "uses": ["Grain fumigant", "Rodenticide", "Semiconductor research"],
        "description": "A dark crystalline compound that releases highly toxic phosphine gas on contact with moisture, used as a pest fumigant."
    },

    {
        "id": 24,
        "name": "Lithium Bromide",
        "formula": "LiBr",
        "smiles": "[Li+].[Br-]",
        "compoundType": "salt",
        "casNumber": "7550-35-8",
        "physicalProperties": {
        "molarMass": 86.85,
        "state": "solid",
        "densityGPerCm3": 3.464,
        "meltingPointCelsius": 552.0,
        "boilingPointCelsius": 1310.0,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Lithium", "symbol": "Li", "atoms": 1 },
        { "element": "Bromine", "symbol": "Br", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H315", "H319", "H335"]
        },
        "uses": ["Absorption chillers (air conditioning)", "Desiccant", "Organic synthesis"],
        "description": "A highly hygroscopic salt used as a desiccant and as the working fluid in industrial absorption refrigeration systems."
    },

    {
        "id": 25,
        "name": "Gallium Arsenide",
        "formula": "GaAs",
        "smiles": "[Ga]#[As]",
        "compoundType": "other",
        "casNumber": "1303-00-0",
        "physicalProperties": {
        "molarMass": 144.64,
        "state": "solid",
        "densityGPerCm3": 5.316,
        "meltingPointCelsius": 1238.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Gallium", "symbol": "Ga", "atoms": 1 },
        { "element": "Arsenic", "symbol": "As", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H350", "H360F", "H372"]
        },
        "uses": ["Solar cells", "LEDs and laser diodes", "Microwave integrated circuits"],
        "description": "A III-V semiconductor with high electron mobility, used in high-frequency electronics and optoelectronic devices."
    },

    {
        "id": 26,
        "name": "Cadmium Telluride",
        "formula": "CdTe",
        "smiles": "[Cd]=[Te]",
        "compoundType": "other",
        "casNumber": "1306-25-8",
        "physicalProperties": {
        "molarMass": 240.01,
        "state": "solid",
        "densityGPerCm3": 5.85,
        "meltingPointCelsius": 1041.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Cadmium", "symbol": "Cd", "atoms": 1 },
        { "element": "Tellurium", "symbol": "Te", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H341", "H350", "H361fd", "H372", "H410"]
        },
        "uses": ["Thin-film solar panels", "Infrared optics", "Radiation detectors"],
        "description": "A crystalline semiconductor widely used as the light-absorbing layer in thin-film photovoltaic modules."
    },

    {
        "id": 27,
        "name": "Silicon Tetrafluoride",
        "formula": "SiF4",
        "smiles": "F[Si](F)(F)F",
        "compoundType": "other",
        "casNumber": "7783-61-1",
        "physicalProperties": {
        "molarMass": 104.08,
        "state": "gas",
        "densityGPerCm3": 0.00469,
        "meltingPointCelsius": -90.2,
        "boilingPointCelsius": -86.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Silicon", "symbol": "Si", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 4 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H280", "H314", "H331"]
        },
        "uses": ["Semiconductor manufacturing", "Fluorosilicic acid production", "Plasma etching"],
        "description": "A colorless, pungent gas that fumes in moist air and is used in electronics manufacturing and fluoride chemistry."
    },

    {
        "id": 28,
        "name": "Xenon Difluoride",
        "formula": "XeF2",
        "smiles": "F[Xe]F",
        "compoundType": "other",
        "casNumber": "13709-36-9",
        "physicalProperties": {
        "molarMass": 169.29,
        "state": "solid",
        "densityGPerCm3": 4.32,
        "meltingPointCelsius": 129.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Xenon", "symbol": "Xe", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H272", "H314", "H330"]
        },
        "uses": ["Silicon etching in MEMS fabrication", "Fluorinating agent", "Semiconductor processing"],
        "description": "A rare, stable compound of a noble gas, forming white crystals that act as a strong fluorinating and oxidizing agent."
    },

    {
        "id": 29,
        "name": "Iron(III) Bromide",
        "formula": "FeBr3",
        "smiles": "Br[Fe](Br)Br",
        "compoundType": "salt",
        "casNumber": "10031-26-2",
        "physicalProperties": {
        "molarMass": 295.56,
        "state": "solid",
        "densityGPerCm3": 4.5,
        "meltingPointCelsius": 200.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Iron", "symbol": "Fe", "atoms": 1 },
        { "element": "Bromine", "symbol": "Br", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H314"]
        },
        "uses": ["Lewis acid catalyst", "Aromatic bromination", "Organic synthesis"],
        "description": "A dark red-brown, moisture-sensitive solid used as a Lewis acid catalyst for brominating aromatic compounds."
    },

    {
        "id": 30,
        "name": "Lead(II) Iodide",
        "formula": "PbI2",
        "smiles": "I[Pb]I",
        "compoundType": "salt",
        "casNumber": "10101-63-0",
        "physicalProperties": {
        "molarMass": 461.01,
        "state": "solid",
        "densityGPerCm3": 6.16,
        "meltingPointCelsius": 402.0,
        "boilingPointCelsius": 954.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Lead", "symbol": "Pb", "atoms": 1 },
        { "element": "Iodine", "symbol": "I", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H332", "H360", "H373", "H410"]
        },
        "uses": ["Perovskite solar cells", "X-ray and gamma-ray detectors", "Thermoelectric materials", "Photography"],
        "description": "A bright yellow, poorly soluble solid known for forming 'golden rain' crystals and used as a precursor for perovskite solar cells."
    },

    {
        "id": 31,
        "name": "Mercury(II) Iodide",
        "formula": "HgI2",
        "smiles": "I[Hg]I",
        "compoundType": "salt",
        "casNumber": "7774-29-0",
        "physicalProperties": {
        "molarMass": 454.4,
        "state": "solid",
        "densityGPerCm3": 6.36,
        "meltingPointCelsius": 259.0,
        "boilingPointCelsius": 350.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Mercury", "symbol": "Hg", "atoms": 1 },
        { "element": "Iodine", "symbol": "I", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H300", "H310", "H330", "H373", "H410"]
        },
        "uses": ["Radiation detectors", "Nessler's reagent", "Thermochromic materials"],
        "description": "A highly toxic red solid that changes color to yellow when heated, used in specialized detectors and analytical reagents."
    },

    {
        "id": 32,
        "name": "Silver Bromide",
        "formula": "AgBr",
        "smiles": "[Ag+].[Br-]",
        "compoundType": "salt",
        "casNumber": "7785-23-1",
        "physicalProperties": {
        "molarMass": 187.77,
        "state": "solid",
        "densityGPerCm3": 6.473,
        "meltingPointCelsius": 432.0,
        "boilingPointCelsius": 1502.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Silver", "symbol": "Ag", "atoms": 1 },
        { "element": "Bromine", "symbol": "Br", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H410"]
        },
        "uses": ["Photographic film and paper", "Photochromic lenses", "Silver halide emulsions"],
        "description": "A pale yellow, light-sensitive salt that darkens on exposure to light, forming the basis of traditional photography."
    },

    {
        "id": 33,
        "name": "Lanthanum Hexaboride",
        "formula": "LaB6",
        "smiles": "[B].[B].[B].[B].[B].[B].[La]",
        "compoundType": "other",
        "casNumber": "12008-21-8",
        "physicalProperties": {
        "molarMass": 203.77,
        "state": "solid",
        "densityGPerCm3": 4.72,
        "meltingPointCelsius": 2210.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Lanthanum", "symbol": "La", "atoms": 1 },
        { "element": "Boron", "symbol": "B", "atoms": 6 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H315", "H319", "H335"]
        },
        "uses": ["Electron microscope cathodes", "Electron beam sources", "Hall-effect thrusters", "X-ray tubes"],
        "description": "A refractory ceramic with a very low work function, prized as a long-lasting electron emitter in scientific instruments."
    },

    {
        "id": 34,
        "name": "Bismuth(III) Iodide",
        "formula": "BiI3",
        "smiles": "I[Bi](I)I",
        "compoundType": "salt",
        "casNumber": "7787-64-6",
        "physicalProperties": {
        "molarMass": 589.69,
        "state": "solid",
        "densityGPerCm3": 5.78,
        "meltingPointCelsius": 408.6,
        "boilingPointCelsius": 542.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Bismuth", "symbol": "Bi", "atoms": 1 },
        { "element": "Iodine", "symbol": "I", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H315", "H319", "H335"]
        },
        "uses": ["Dragendorff's reagent (alkaloid detection)", "Radiation detectors", "Lead-free perovskite solar cell research"],
        "description": "A dark gray to brown crystalline solid that is a relatively low-toxicity heavy-metal halide, used in analytical chemistry and emerging photovoltaic research."
    },

    {
        "id": 35,
        "name": "Indium Antimonide",
        "formula": "InSb",
        "smiles": "[In]#[Sb]",
        "compoundType": "other",
        "casNumber": "1312-41-0",
        "physicalProperties": {
        "molarMass": 236.58,
        "state": "solid",
        "densityGPerCm3": 5.775,
        "meltingPointCelsius": 525.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Indium", "symbol": "In", "atoms": 1 },
        { "element": "Antimony", "symbol": "Sb", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H332", "H411"]
        },
        "uses": ["Infrared detectors", "Thermal imaging cameras", "Magnetic field sensors", "High-speed transistors"],
        "description": "A narrow-gap semiconductor with very high electron mobility, widely used in infrared sensing and imaging."
    },

    {
        "id": 36,
        "name": "Tin(II) Fluoride",
        "formula": "SnF2",
        "smiles": "F[Sn]F",
        "compoundType": "salt",
        "casNumber": "7783-47-3",
        "physicalProperties": {
        "molarMass": 156.71,
        "state": "solid",
        "densityGPerCm3": 4.57,
        "meltingPointCelsius": 213.0,
        "boilingPointCelsius": 850.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Tin", "symbol": "Sn", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H314", "H332"]
        },
        "uses": ["Fluoride toothpaste", "Dental cavity prevention", "Tin plating", "Ceramic glazes"],
        "description": "A white crystalline salt, also called stannous fluoride, best known as an active ingredient in toothpaste."
    },

    {
        "id": 37,
        "name": "Copper(I) Iodide",
        "formula": "CuI",
        "smiles": "[Cu]I",
        "compoundType": "salt",
        "casNumber": "7681-65-4",
        "physicalProperties": {
        "molarMass": 190.45,
        "state": "solid",
        "densityGPerCm3": 5.67,
        "meltingPointCelsius": 606.0,
        "boilingPointCelsius": 1290.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Copper", "symbol": "Cu", "atoms": 1 },
        { "element": "Iodine", "symbol": "I", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H302", "H315", "H319", "H410"]
        },
        "uses": ["Cloud seeding", "Cross-coupling catalyst in organic synthesis", "Thermochromic materials"],
        "description": "A white to tan, poorly soluble solid used as a catalyst in organic synthesis and in atmospheric cloud seeding."
    },

    {
        "id": 38,
        "name": "Tungsten Hexafluoride",
        "formula": "WF6",
        "smiles": "F[W](F)(F)(F)(F)F",
        "compoundType": "other",
        "casNumber": "7783-82-6",
        "physicalProperties": {
        "molarMass": 297.83,
        "state": "gas",
        "densityGPerCm3": 0.0124,
        "meltingPointCelsius": 2.3,
        "boilingPointCelsius": 17.1,
        "pHValue": None
        },
        "composition": [
        { "element": "Tungsten", "symbol": "W", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 6 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H280", "H314", "H330"]
        },
        "uses": ["Chemical vapor deposition of tungsten", "Semiconductor interconnects", "Microchip manufacturing"],
        "description": "One of the densest known gases, used to deposit thin tungsten metal layers in microelectronics."
    },

    {
        "id": 39,
        "name": "Cobalt(II) Bromide",
        "formula": "CoBr2",
        "smiles": "Br[Co]Br",
        "compoundType": "salt",
        "casNumber": "7789-43-7",
        "physicalProperties": {
        "molarMass": 218.74,
        "state": "solid",
        "densityGPerCm3": 4.909,
        "meltingPointCelsius": 678.0,
        "boilingPointCelsius": 927.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Cobalt", "symbol": "Co", "atoms": 1 },
        { "element": "Bromine", "symbol": "Br", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H317", "H334", "H350", "H360F", "H410"]
        },
        "uses": ["Humidity indicators", "Invisible ink", "Catalyst in organic synthesis"],
        "description": "A green crystalline solid that turns pink when hydrated, which makes it useful as a moisture indicator."
    },

    {
        "id": 40,
        "name": "Barium Fluoride",
        "formula": "BaF2",
        "smiles": "[Ba+2].[F-].[F-]",
        "compoundType": "salt",
        "casNumber": "7787-32-8",
        "physicalProperties": {
        "molarMass": 175.32,
        "state": "solid",
        "densityGPerCm3": 4.89,
        "meltingPointCelsius": 1368.0,
        "boilingPointCelsius": 2260.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Barium", "symbol": "Ba", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H301", "H332"]
        },
        "uses": ["Infrared optical windows", "Scintillation radiation detectors", "Enamels and glazes"],
        "description": "A colorless crystalline solid that transmits light from ultraviolet to infrared, used in optics and radiation detection."
    },

    {
        "id": 41,
        "name": "Zirconium Tetrafluoride",
        "formula": "ZrF4",
        "smiles": "F[Zr](F)(F)F",
        "compoundType": "salt",
        "casNumber": "7783-64-4",
        "physicalProperties": {
        "molarMass": 167.22,
        "state": "solid",
        "densityGPerCm3": 4.43,
        "meltingPointCelsius": 932.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Zirconium", "symbol": "Zr", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 4 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H314", "H332"]
        },
        "uses": ["Fluoride glass optical fibers (ZBLAN)", "Nuclear fuel processing", "Zirconium metal production"],
        "description": "A white, sublimating solid that is a key ingredient in fluoride glasses used for infrared fiber optics."
    },

    {
        "id": 42,
        "name": "Cesium Fluoride",
        "formula": "CsF",
        "smiles": "[Cs+].[F-]",
        "compoundType": "salt",
        "casNumber": "13400-13-0",
        "physicalProperties": {
        "molarMass": 151.9,
        "state": "solid",
        "densityGPerCm3": 4.64,
        "meltingPointCelsius": 703.0,
        "boilingPointCelsius": 1251.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Cesium", "symbol": "Cs", "atoms": 1 },
        { "element": "Fluorine", "symbol": "F", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H301", "H311", "H331"]
        },
        "uses": ["Fluorinating reagent in organic synthesis", "Specialty glass", "Brazing flux"],
        "description": "A highly hygroscopic white salt and a common, strongly basic fluoride source for organic chemistry."
    },

    {
        "id": 43,
        "name": "Rubidium Chloride",
        "formula": "RbCl",
        "smiles": "[Rb+].[Cl-]",
        "compoundType": "salt",
        "casNumber": "7791-11-9",
        "physicalProperties": {
        "molarMass": 120.92,
        "state": "solid",
        "densityGPerCm3": 2.80,
        "meltingPointCelsius": 718.0,
        "boilingPointCelsius": 1390.0,
        "pHValue": 7.0
        },
        "composition": [
        { "element": "Rubidium", "symbol": "Rb", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 1 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H302"]
        },
        "uses": ["Biochemical research (density gradient centrifugation)", "Electrophysiology", "Atomic clock research"],
        "description": "A white, water-soluble alkali metal halide used mainly in biochemical and physiological research."
    },

    {
        "id": 44,
        "name": "Strontium Titanate",
        "formula": "SrTiO3",
        "smiles": "[O-2].[O-2].[O-2].[Ti+4].[Sr+2]",
        "compoundType": "other",
        "casNumber": "12060-59-2",
        "physicalProperties": {
        "molarMass": 183.49,
        "state": "solid",
        "densityGPerCm3": 5.12,
        "meltingPointCelsius": 2080.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Strontium", "symbol": "Sr", "atoms": 1 },
        { "element": "Titanium", "symbol": "Ti", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
        "uses": ["Capacitors", "Varistors", "Substrate for thin-film superconductors", "Optical lenses"],
        "description": "A perovskite oxide with a very high dielectric constant, widely used in electronic components and as a crystal growth substrate."
    },

    {
        "id": 45,
        "name": "Germanium Tetrachloride",
        "formula": "GeCl4",
        "smiles": "Cl[Ge](Cl)(Cl)Cl",
        "compoundType": "other",
        "casNumber": "10038-98-9",
        "physicalProperties": {
        "molarMass": 214.4,
        "state": "liquid",
        "densityGPerCm3": 1.844,
        "meltingPointCelsius": -49.5,
        "boilingPointCelsius": 86.5,
        "pHValue": None
        },
        "composition": [
        { "element": "Germanium", "symbol": "Ge", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 4 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H314", "H331"]
        },
        "uses": ["Fiber-optic cable manufacturing", "Germanium metal production", "Polymerization catalyst"],
        "description": "A colorless, fuming liquid that hydrolyzes in moist air and is a key precursor for the cores of optical fibers."
    },

    {
        "id": 46,
        "name": "Nickel(II) Chloride",
        "formula": "NiCl2",
        "smiles": "Cl[Ni]Cl",
        "compoundType": "salt",
        "casNumber": "7718-54-9",
        "physicalProperties": {
        "molarMass": 129.6,
        "state": "solid",
        "densityGPerCm3": 3.55,
        "meltingPointCelsius": 1001.0,
        "boilingPointCelsius": None,
        "pHValue": 4.0
        },
        "composition": [
        { "element": "Nickel", "symbol": "Ni", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H301", "H331", "H350", "H360D", "H372", "H410"]
        },
        "uses": ["Nickel electroplating", "Catalyst in organic synthesis", "Ammonia absorption", "Ceramic pigments"],
        "description": "A yellow anhydrous solid that forms green hydrated crystals, widely used in electroplating and as a source of nickel."
    },

    {
        "id": 47,
        "name": "Chromium(III) Oxide",
        "formula": "Cr2O3",
        "smiles": "O=[Cr]O[Cr]=O",
        "compoundType": "other",
        "casNumber": "1308-38-9",
        "physicalProperties": {
        "molarMass": 151.99,
        "state": "solid",
        "densityGPerCm3": 5.22,
        "meltingPointCelsius": 2435.0,
        "boilingPointCelsius": 4000.0,
        "pHValue": None
        },
        "composition": [
        { "element": "Chromium", "symbol": "Cr", "atoms": 2 },
        { "element": "Oxygen", "symbol": "O", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
        "uses": ["Green pigment", "Refractory bricks", "Metal polishing compounds", "Ceramic glazes"],
        "description": "A very stable, dark green oxide used as a pigment and as a hard, heat-resistant industrial material."
    },

    {
        "id": 48,
        "name": "Manganese Dioxide",
        "formula": "MnO2",
        "smiles": "O=[Mn]=O",
        "compoundType": "other",
        "casNumber": "1313-13-9",
        "physicalProperties": {
        "molarMass": 86.94,
        "state": "solid",
        "densityGPerCm3": 5.026,
        "meltingPointCelsius": 535.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Manganese", "symbol": "Mn", "atoms": 1 },
        { "element": "Oxygen", "symbol": "O", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "Warning",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": True,
        "hazardStatements": ["H302", "H332"]
        },
        "uses": ["Dry-cell and alkaline batteries", "Glass decolorizing", "Oxidizing catalyst", "Pigments"],
        "description": "A dark brown-black solid and the main cathode material in common batteries, also used as an oxidizing agent and catalyst."
    },

    {
        "id": 49,
        "name": "Molybdenum Disulfide",
        "formula": "MoS2",
        "smiles": "S=[Mo]=S",
        "compoundType": "other",
        "casNumber": "1317-33-5",
        "physicalProperties": {
        "molarMass": 160.07,
        "state": "solid",
        "densityGPerCm3": 5.06,
        "meltingPointCelsius": 2375.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Molybdenum", "symbol": "Mo", "atoms": 1 },
        { "element": "Sulfur", "symbol": "S", "atoms": 2 }
        ],
        "safetyData": {
        "signalWord": "None",
        "isCorrosive": False,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": []
        },
        "uses": ["Solid lubricant", "Hydrodesulfurization catalyst", "Transistors and electronics research"],
        "description": "A silvery-black layered material that works as a dry lubricant and is studied as a two-dimensional semiconductor."
    },

    {
        "id": 50,
        "name": "Gold(III) Chloride",
        "formula": "AuCl3",
        "smiles": "Cl[Au](Cl)Cl",
        "compoundType": "salt",
        "casNumber": "13453-07-1",
        "physicalProperties": {
        "molarMass": 303.33,
        "state": "solid",
        "densityGPerCm3": 3.9,
        "meltingPointCelsius": 254.0,
        "boilingPointCelsius": None,
        "pHValue": None
        },
        "composition": [
        { "element": "Gold", "symbol": "Au", "atoms": 1 },
        { "element": "Chlorine", "symbol": "Cl", "atoms": 3 }
        ],
        "safetyData": {
        "signalWord": "Danger",
        "isCorrosive": True,
        "isFlammable": False,
        "isToxic": False,
        "hazardStatements": ["H302", "H314"]
        },
        "uses": ["Gold plating", "Gold nanoparticle synthesis", "Catalyst in organic synthesis", "Photography toning"],
        "description": "A red crystalline solid that is a common starting material for gold chemistry and nanoparticle production."
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