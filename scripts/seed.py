import os
from supabase import create_client
from seed_data import compounds

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

compound_rows, composition_rows = [], []

for c in compounds:
    p, s = c["physicalProperties"], c["safetyData"]
    compound_rows.append({
        "id": c["id"], "name": c["name"], "formula": c["formula"], "smiles": c["smiles"],
        "compound_type": c["compoundType"], "cas_number": c["casNumber"],
        "molar_mass": p["molarMass"], "state": p["state"], "density": p["densityGPerCm3"],
        "melting_point": p.get("meltingPointCelsius"),
        "boiling_point": p.get("boilingPointCelsius") or None,
        "ph_value": p.get("pHValue"),
        "signal_word": s["signalWord"], "is_corrosive": s["isCorrosive"],
        "is_toxic": s["isToxic"], "is_flammable": s["isFlammable"],
        "hazard_statements": s.get("hazardStatements", []),
        "uses": c.get("uses", []), "description": c["description"],
    })
    for e in c["composition"]:
        composition_rows.append({
            "compound_id": c["id"], "element": e["element"],
            "symbol": e["symbol"], "atoms": e["atoms"],
        })

supabase.table("compounds").upsert(compound_rows).execute()
supabase.table("compound_composition").insert(composition_rows).execute()
print(f"Loaded {len(compound_rows)} compounds, {len(composition_rows)} composition rows")