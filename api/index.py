import os
import math
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

class CombineRequest(BaseModel):
    compoundIds: list[int] = Field(min_length=2, max_length=2)

class DiscoveryCreate(BaseModel):
    compoundId: int = Field(gt=0)
    userId: Optional[str] = None

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
# AUTH HELPERS
# ===========================================================

def get_current_user(
    authorization: Optional[str] = Header(default=None),
) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization Bearer token.",
        )

    token = authorization.split(" ", 1)[1].strip()
    user_res = supabase.auth.get_user(token)
    if not user_res or not user_res.user:
        raise HTTPException(status_code=401, detail="Invalid or expired user session.")

    user_id = str(user_res.user.id)
    profile_res = (
        supabase.table("profiles")
        .select("id, role, created_at")
        .eq("id", user_id)
        .execute()
    )

    role = profile_res.data[0]["role"] if profile_res.data else "user"
    return {
        "id": user_id,
        "role": role,
    }

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required.")
    return current_user

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
            "/api/v1/compounds/search",
            "/api/v1/elements",
            "/api/v1/compounds/craft",
            "/api/v1/compounds/combine"
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
# HELPER: VOWEL DROP FOR PREFIX + ROOT
# ===========================================================
def format_prefix_and_root(prefix: str, root: str) -> str:
    if not prefix:
        return f"{root}ide"
    if prefix[-1] in ("o", "a") and root[0] in ("a", "e", "i", "o", "u"):
        prefix = prefix[:-1]
    return f"{prefix}{root}ide"


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

# ===========================================================
# COMPOUND CRAFT (Combine Elements -> Existing/Named Compound)
# ===========================================================
@app.post("/api/v1/compounds/craft", dependencies=[Depends(verify_API_KEY)])
def craft_compound(payload: CraftRequest):
    # Normalize input into {symbol: atoms}
    target_comp = {}
    for item in payload.elements:
        sym = item.symbol.strip().capitalize()
        target_comp[sym] = target_comp.get(sym, 0) + item.atoms

    if len(target_comp) != 2:
        raise HTTPException(status_code=400, detail="Please select 2 distinct elements.")

    # Check if this exact composition already exists in the `compounds` table
    for existing in fetch_all():
        existing_comp = {
            c["symbol"]: c["atoms"] for c in existing["composition"]
        }
        if existing_comp == target_comp:
            return {
                "isKnownCompound": True,
                "compound": existing
            }

    # If not in `compounds` yet, 
    # Generate IUPAC name from `elements` & `number_prefixes`
    symbols = list(target_comp.keys())
    atom_counts = list(target_comp.values())

    elem_res = supabase.table("elements").select("*").in_("symbol", symbols).execute()
    if len(elem_res.data) != 2:
        raise HTTPException(status_code=404, detail="One or more elements not found in database.")

    elem_map = {row["symbol"]: row for row in elem_res.data}

    prefix_res = supabase.table("number_prefixes").select("*").in_("atom_count", atom_counts).execute()
    prefix_map = {row["atom_count"]: row["prefix"] for row in prefix_res.data}

    items = []
    for sym, atoms in target_comp.items():
        db_el = elem_map[sym]
        items.append({
            "element": db_el["name"],
            "symbol": sym,
            "atoms": atoms,
            "root": db_el["name_root"] or db_el["name"].lower(),
            "category": db_el["category"],
            "group_num": db_el["group_num"] or 0,
            "period": db_el["period"],
        })

    if any(x["category"] == "noble gas" for x in items):
        raise HTTPException(status_code=400, detail="Noble gases rarely form compounds.")

    nonmetal_types = {"nonmetal", "halogen", "metalloid"}
    is_nonmetal = [x["category"] in nonmetal_types for x in items]

    if is_nonmetal[0] != is_nonmetal[1]:
        # Ionic: Metal first, Nonmetal second (no Greek prefixes)
        bond_type = "ionic"
        first = items[0] if not is_nonmetal[0] else items[1]
        second = items[1] if not is_nonmetal[0] else items[0]
        crafted_name = f"{first['element']} {second['root']}ide".capitalize()

    elif all(is_nonmetal):
        # Covalent: Sort by IUPAC group/period order, apply Greek prefixes from DB
        bond_type = "covalent"
        items.sort(key=lambda x: (x["group_num"], -x["period"]))
        first, second = items[0], items[1]

        first_prefix = "" if first["atoms"] == 1 else prefix_map.get(first["atoms"], "")
        second_prefix = prefix_map.get(second["atoms"], "")

        first_part = f"{first_prefix}{first['element'].lower()}".capitalize()
        second_part = format_prefix_and_root(second_prefix, second["root"])
        crafted_name = f"{first_part} {second_part}"

    else:
        raise HTTPException(status_code=400, detail="Two metals form an alloy, not a compound.")

    formula = "".join(
        f"{el['symbol']}{el['atoms'] if el['atoms'] > 1 else ''}"
        for el in (first, second)
    )

    return {
        "isKnownCompound": False,
        "compound": {
            "name": crafted_name,
            "formula": formula,
            "bondType": bond_type,
            "composition": [
                {"element": first["element"], "symbol": first["symbol"], "atoms": first["atoms"]},
                {"element": second["element"], "symbol": second["symbol"], "atoms": second["atoms"]}
            ]
        }
    }


# ===========================================================
# COMPOUND COMBINE (Combine 2 Compounds -> Products)
# ===========================================================
@app.post("/api/v1/compounds/combine", dependencies=[Depends(verify_API_KEY)])
def combine_compounds(payload: CombineRequest):
    # Normalize reactant_key by sorting IDs numerically
    sorted_ids = sorted(payload.compoundIds)
    reactant_key = f"{sorted_ids[0]}+{sorted_ids[1]}"

    # Look up the reaction in Supabase
    reaction_res = (
        supabase.table("reactions")
        .select("*")
        .eq("reactant_key", reactant_key)
        .execute()
    )

    # If no reaction is found in database
    if not reaction_res.data:
        # Dynamic Fallback: Attempt double-replacement ion swap using DB tables
        comp_res = supabase.table("compounds").select(COMPOUND_SELECT).in_("id", sorted_ids).execute()
        if len(comp_res.data) < 2:
            raise HTTPException(status_code=404, detail="One or both compounds not found.")

        c1, c2 = comp_res.data[0], comp_res.data[1]
        elem_map = {r["symbol"]: r for r in supabase.table("elements").select("*").execute().data}
        poly_map = {r["formula"]: r for r in supabase.table("polyatomic_ions").select("*").execute().data}

        parsed1 = parse_ionic_compound(c1["formula"], elem_map, poly_map)
        parsed2 = parse_ionic_compound(c2["formula"], elem_map, poly_map)

        if parsed1 and parsed2:
            (cat1, an1), (cat2, an2) = parsed1, parsed2
            if cat1["formula"] != cat2["formula"] and an1["formula"] != an2["formula"]:
                prod1 = build_ionic_product(cat1, an2)
                prod2 = build_ionic_product(cat2, an1)
                return {
                    "reacted": True,
                    "isKnownReaction": False,
                    "reactantKey": reactant_key,
                    "reaction": {
                        "name": "Double Replacement Reaction",
                        "reactionType": "double-replacement",
                        "equation": f"{c1['formula']} + {c2['formula']} -> {prod1['formula']} + {prod2['formula']}",
                        "description": f"{c1['name']} and {c2['name']} exchange ions to form {prod1['name']} and {prod2['name']}."
                    },
                    "products": [
                        {"coefficient": 1, "compound": prod1},
                        {"coefficient": 1, "compound": prod2}
                    ]
                }

        return {
            "reacted": False,
            "reactantKey": reactant_key,
            "message": "No chemical reaction occurs between these compounds.",
            "products": []
        }


    reaction = reaction_res.data[0]

    # Fetch ALL participants (both reactants and products) to build equation + products
    participants_res = (
        supabase.table("reaction_participants")
        .select("compound_id, coefficient, role")
        .eq("reaction_id", reaction["id"])
        .execute()
    )

    if not participants_res.data:
        return {
            "reacted": False,
            "reactantKey": reactant_key,
            "message": "Reaction found, but no participants are linked.",
            "products": []
        }

    # Fetch full compound details for all participants
    all_ids = list({p["compound_id"] for p in participants_res.data})
    compounds_res = (
        supabase.table("compounds")
        .select(COMPOUND_SELECT)
        .in_("id", all_ids)
        .execute()
    )
    compound_map = {row["id"]: to_api(row) for row in compounds_res.data}

    reactant_terms = []
    product_terms = []
    products = []

    for p in participants_res.data:
        comp = compound_map.get(p["compound_id"])
        if not comp:
            continue

        coeff = p["coefficient"] or 1
        prefix = f"{coeff} " if coeff > 1 else ""
        term = f"{prefix}{comp['formula']}"

        if p["role"] == "reactant":
            reactant_terms.append(term)
        elif p["role"] == "product":
            product_terms.append(term)
            products.append({
                "coefficient": coeff,
                "compound": comp
            })

    equation = (
        f"{' + '.join(reactant_terms)} -> {' + '.join(product_terms)}"
        if reactant_terms and product_terms
        else None
    )

    return {
        "reacted": True,
        "reactantKey": reactant_key,
        "reaction": {
            "id": reaction["id"],
            "name": reaction.get("name"),
            "reactionType": reaction.get("reaction_type"),
            "equation": equation,
            "description": reaction.get("description")
        },
        "products": products
    }

# ===========================================================
# HELPER FUNCTION (Parsing Ionic Compounds)
# ===========================================================

def parse_ionic_compound(formula: str, elem_map: dict, poly_map: dict):
    """Splits a formula like 'AgNO3' or 'CaCl2' into (cation_dict, anion_dict) using DB data."""
    # Check if compound starts with a polyatomic cation (e.g., NH4)
    cation = None
    rest = formula
    for p_form, p_data in sorted(poly_map.items(), key=lambda x: -len(x[0])):
        if p_data["charge"] > 0 and rest.startswith(p_form):
            cation = {"formula": p_form, "name": p_data["name"], "charge": p_data["charge"], "is_poly": True}
            rest = rest[len(p_form):].lstrip("0123456789")
            break

    # Otherwise match a metal/hydrogen cation from `elements`
    if not cation:
        for sym, e_data in sorted(elem_map.items(), key=lambda x: -len(x[0])):
            if e_data["default_charge"] > 0 and rest.startswith(sym):
                cation = {"formula": sym, "name": e_data["name"], "charge": e_data["default_charge"], "is_poly": False}
                rest = rest[len(sym):].lstrip("0123456789")
                break

    if not cation or not rest:
        return None

    # Strip parentheses around polyatomic ions like Ca(OH)2 -> OH
    clean_rest = rest.strip("()0123456789")

    # Match polyatomic anion first
    for p_form, p_data in sorted(poly_map.items(), key=lambda x: -len(x[0])):
        if p_data["charge"] < 0 and (rest.startswith(p_form) or clean_rest == p_form):
            anion = {"formula": p_form, "name": p_data["name"], "charge": p_data["charge"], "is_poly": True}
            return cation, anion

    # Otherwise match monatomic nonmetal anion from `elements`
    for sym, e_data in sorted(elem_map.items(), key=lambda x: -len(x[0])):
        if e_data["default_charge"] < 0 and rest.startswith(sym):
            root = e_data["name_root"] or e_data["name"].lower()
            anion = {"formula": sym, "name": f"{root}ide", "charge": e_data["default_charge"], "is_poly": False}
            return cation, anion

    return None

def build_ionic_product(cation: dict, anion: dict) -> dict:
    """Balances charges (crisscross method) and builds name + formula."""
    c_charge = abs(cation["charge"])
    a_charge = abs(anion["charge"])
    divisor = math.gcd(c_charge, a_charge)
    c_sub = a_charge // divisor
    a_sub = c_charge // divisor

    c_part = f"({cation['formula']}){c_sub}" if (cation["is_poly"] and c_sub > 1) else f"{cation['formula']}{c_sub if c_sub > 1 else ''}"
    a_part = f"({anion['formula']}){a_sub}" if (anion["is_poly"] and a_sub > 1) else f"{anion['formula']}{a_sub if a_sub > 1 else ''}"

    return {
        "name": f"{cation['name']} {anion['name']}".capitalize(),
        "formula": f"{c_part}{a_part}"
    }

# ===========================================================
# GET USER COMPOUND DISCOVERIES (Protected)
# ===========================================================

@app.get(
    "/api/v1/discoveries",
    dependencies=[Depends(verify_API_KEY)],
)
def get_discoveries(
    all_users: bool = Query(default=False),
    user_id: Optional[str] = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    is_admin = current_user["role"] == "admin"

    query = (
        supabase.table("compound_discoveries")
        .select("id, user_id, compound_id, discovered_at")
        .order("discovered_at", desc=True)
    )

    if all_users and is_admin:
        if user_id:
            query = query.eq("user_id", user_id)
    else:
        target_user_id = user_id if (user_id and is_admin) else current_user["id"]
        query = query.eq("user_id", target_user_id)

    disc_res = query.execute()
    discovery_rows = disc_res.data or []

    if not discovery_rows:
        return {
            "count": 0,
            "discoveries": [],
        }

    compound_ids = list({row["compound_id"] for row in discovery_rows})
    comp_res = (
        supabase.table("compounds")
        .select(COMPOUND_SELECT)
        .in_("id", compound_ids)
        .execute()
    )
    compound_map = {row["id"]: to_api(row) for row in (comp_res.data or [])}

    items = []
    for row in discovery_rows:
        comp = compound_map.get(row["compound_id"])
        if comp:
            items.append({
                "id": row.get("id"),
                "userId": row["user_id"],
                "compoundId": row["compound_id"],
                "discoveredAt": row["discovered_at"],
                "compound": comp,
            })

    return {
        "count": len(items),
        "discoveries": items,
    }
