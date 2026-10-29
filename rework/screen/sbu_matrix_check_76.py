"""Check of the SBU involvement matrix for record 76 (third pass, 20 October 2026).

This is a consistency check on assignments, not a statistical model, so there is no random
draw and no seed. It reads the assignment table below, verifies the rules the record states,
counts the distinct accountable owner roles, tallies the roles per unit, and writes a results
JSON and a Markdown matrix that the record copies.

Change in this pass (verifier items on sourcing): the matrix now holds only units that have a
published source (rule 8). Two functions with no published unit are hosted by sourced units:
- R&D and quality is a role inside Plants, supply chain and procurement (U10). The plant
  companies claim the quality standards (S, COMPANY CLAIM) and advertise a packaging science
  post at a plant company (S).
- The brand and legal head is a role inside Singha Corporation executive management (U1), where
  the user placed the Gate 7 sign-off on 19 October 2026 (CLAUDE.md section 5). The Gate 7
  owner is an open question for the user (record section 7, limit 14).

Rules checked:
1. Every gate (0 to 9) and every phase without its own gate (2, 4, 5, 6) has exactly one
   accountable unit (A), and that unit is in the unit list.
2. No unit appears twice in one column.
3. Every unit named in a column exists in the unit list.
4. Each gate that blocks sale (1, 2, 7, 9) has an accountable unit AND an owner role that
   belongs to that unit (the role-to-unit map below).
5. Phase mapping: Phase 0 is Gate 0; Phase 1 is Gates 1 to 7; Phase 3 is Gates 8 and 9;
   each phase column is listed once and the phase owners equal the owners of their columns.
6. Every unit holds at least one cell in the matrix (no unit is named without a place).
7. Owners are roles: every accountable role is in the fixed role vocabulary, and no role
   is held by two units.
8. Every unit has a published source tier of P or S (SOURCE_TIER below). No unit is kept
   without a source.

Counts reported: distinct accountable owner roles across all 14 columns, and across the
ten gates only (Gates 0 to 9). The count is the number of distinct role strings.

Run: python rework/screen/sbu_matrix_check_76.py   (well under 50 MB of memory)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

UNITS = {
    "U1": "Singha Corporation executive management (executive sponsor; brand and legal head)",
    "U2": "Soda and drinking-water business",
    "U3": "Beer and alcoholic beverages",
    "U4": "Other non-alcoholic beverages",
    "U5": "Food and restaurants",
    "U6": "Singha Park",
    "U7": "International",
    "U8": "Marketing and brand (Boon Rawd Trading)",
    "U9": "Sales, channel and distribution (Boon Rawd Trading)",
    "U10": "Plants, supply chain and procurement (R&D and quality role)",
    "U11": "Packaging (BG Container Glass)",
    "U12": "Finance",
    "U13": "Sustainability and community",
}

# Source tier of each unit's existence and scope, from the record's section 2.
SOURCE_TIER = {
    "U1": "S, COMPANY CLAIM (English About page; Thai profile page; both undated, footers 2014 and 2020)",
    "U2": "P (company product listing under Beverages)",
    "U3": "P (company product listing)",
    "U4": "P (company product listing)",
    "U5": "P for brands (Masita, Pun Dee Rice); S for restaurants",
    "U6": "S (Our Group list; press)",
    "U7": "S (Our Group list; press)",
    "U8": "P (Boon Rawd Trading release, 13 March 2026)",
    "U9": "S (efinancethai, 12 March 2026; company history; Siri Pro, 2021)",
    "U10": "S, COMPANY CLAIM (plant pages, footer 2016; a packaging science post at a plant company)",
    "U11": "S (listed group company; efinancethai, Bright TV)",
    "U12": "S (board page title; press, 2568 BE)",
    "U13": "S (plant and CSR pages; Phraya Bhirombhakdi Foundation)",
}

# The owner role for each accountable step. A role is a job title inside a unit, never a
# person. ROLE_UNIT maps each role to the unit that holds it.
ROLE_OF = {
    "G0": "executive sponsor",
    "G1": "regulatory affairs head",
    "G2": "regulatory affairs head",
    "G3": "R&D lead",
    "G4": "sensory lead",
    "G5": "packaging and procurement lead",
    "G6": "operations director",
    "G7": "brand and legal head",
    "P2": "marketing lead",
    "G8": "sales and channel head",
    "G9": "pack release lead",
    "P4": "sales and channel head",
    "P5": "executive sponsor",
    "P6": "product owner, soda and drinking water",
}
ROLE_UNIT = {
    "executive sponsor": "U1",
    "brand and legal head": "U1",
    "regulatory affairs head": "U10",
    "R&D lead": "U10",
    "sensory lead": "U10",
    "packaging and procurement lead": "U10",
    "operations director": "U10",
    "pack release lead": "U10",
    "marketing lead": "U8",
    "sales and channel head": "U9",
    "product owner, soda and drinking water": "U2",
}

# Columns in plan order. Phase 0 = G0; Phase 1 = G1 to G7; Phase 3 = G8 and G9.
COLUMNS = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "P2", "G8", "G9", "P4", "P5", "P6"]
GATE_COLUMNS = ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]

# A = accountable (and does the work), R = responsible for part of the work,
# C = consulted before the result is final, I = informed after. A unit appears once per column.
ASSIGN = {
    "G0": dict(A="U1", R=[], C=["U2", "U8", "U9", "U10", "U12"],
               I=["U3", "U4", "U5", "U6", "U7", "U11", "U13"]),
    "G1": dict(A="U10", R=[], C=["U1", "U2", "U12"], I=["U8", "U9"]),
    "G2": dict(A="U10", R=[], C=["U1", "U2"], I=["U8", "U9"]),
    "G3": dict(A="U10", R=[], C=["U2"], I=["U1", "U8"]),
    "G4": dict(A="U10", R=[], C=["U2", "U8"], I=["U1", "U9"]),
    "G5": dict(A="U10", R=[], C=["U11", "U12", "U13"], I=["U1", "U9"]),
    "G6": dict(A="U10", R=[], C=["U2"], I=["U1", "U8", "U9"]),
    "G7": dict(A="U1", R=["U8"], C=["U2", "U3", "U13"], I=["U9", "U10"]),
    "P2": dict(A="U8", R=[], C=["U1", "U2", "U12"], I=["U9", "U10"]),
    "G8": dict(A="U9", R=["U8", "U12"], C=["U2", "U10"], I=["U1"]),
    "G9": dict(A="U10", R=[], C=["U1", "U8"], I=["U9", "U12"]),
    "P4": dict(A="U9", R=["U8", "U10"], C=["U1", "U12"], I=["U2"]),
    "P5": dict(A="U1", R=["U8", "U9", "U12"], C=["U2", "U10"],
               I=["U3", "U4", "U5", "U6", "U7", "U13"]),
    "P6": dict(A="U2", R=["U8", "U9", "U10"], C=["U1", "U11", "U12"], I=["U13"]),
}

PHASE_MAP = {
    "Phase 0 Mobilise": ["G0"],
    "Phase 1 Readiness gates": ["G1", "G2", "G3", "G4", "G5", "G6", "G7"],
    "Phase 2 Concept pre-test": ["P2"],
    "Phase 3 Pilot readiness": ["G8", "G9"],
    "Phase 4 Marketing pilot": ["P4"],
    "Phase 5 Measured outcome": ["P5"],
    "Phase 6 Scale": ["P6"],
}
SALE_BLOCKING = ["G1", "G2", "G7", "G9"]
PILOT_BATCH_ALSO = ["G3", "G4", "G5", "G6", "G8"]

# Legacy mapping from the second pass (U10 R&D and quality and U15 brand and legal are removed as
# separate units; the old U11 to U14 are renumbered U10 to U13).
LEGACY_MAP = {
    "U10 (R&D and quality)": "role inside U10 (plants, supply chain and procurement)",
    "U11 (plants, supply chain and procurement)": "U10",
    "U12 (packaging)": "U11",
    "U13 (finance)": "U12",
    "U14 (sustainability and community)": "U13",
    "U15 (brand and legal function)": "role inside U1 (Singha Corporation executive management)",
}

# Per-cube design masses (grams) from submission 05 and 09: potassium bicarbonate 0.81,
# citric acid 2.10, sucralose about 0.033 (33 mg), binder and filler 0.80 (ASSUMPTION),
# lemon flavour 0.05 (ASSUMPTION). Annual volumes are the three rows of the valuation grid.
GRAMS_PER_CUBE = {
    "potassium_bicarbonate": 0.81,
    "citric_acid": 2.10,
    "sucralose": 0.033,
    "binder_and_filler": 0.80,
    "lemon_flavour": 0.05,
}
CUBES_PER_YEAR = [50_000, 200_000, 1_000_000]


def annual_need_kg():
    out = {}
    for cubes in CUBES_PER_YEAR:
        out[str(cubes)] = {k: round(g * cubes / 1000.0, 3) for k, g in GRAMS_PER_CUBE.items()}
    return out


def check():
    problems = []
    for col in COLUMNS:
        if col not in ASSIGN:
            problems.append(f"rule 1: {col} has no assignment")
            continue
        a = ASSIGN[col]
        names = [a["A"]] + a["R"] + a["C"] + a["I"]
        if not a["A"]:
            problems.append(f"rule 1: {col} has no accountable unit")
        elif names.count(a["A"]) != 1:
            problems.append(f"rule 1: {col} accountable unit listed more than once")
        if len(names) != len(set(names)):
            dup = sorted({n for n in names if names.count(n) > 1})
            problems.append(f"rule 2: {col} unit listed twice: {dup}")
        for n in names:
            if n not in UNITS:
                problems.append(f"rule 3: {col} unknown unit {n}")
        if col not in ROLE_OF:
            problems.append(f"rule 7: {col} has no owner role")
    extra = set(ASSIGN) - set(COLUMNS)
    if extra:
        problems.append(f"assignments without a column: {sorted(extra)}")

    # Rule 4: sale-blocking gates have an accountable unit and a role held by that unit.
    for g in SALE_BLOCKING:
        role = ROLE_OF.get(g)
        if not ASSIGN[g]["A"]:
            problems.append(f"rule 4: sale-blocking {g} has no accountable unit")
        elif role is None or ROLE_UNIT.get(role) != ASSIGN[g]["A"]:
            problems.append(f"rule 4: sale-blocking {g} role {role!r} is not held by {ASSIGN[g]['A']}")

    # Rule 5: phase mapping.
    if PHASE_MAP["Phase 0 Mobilise"] != ["G0"]:
        problems.append("rule 5: Phase 0 is not Gate 0")
    if PHASE_MAP["Phase 1 Readiness gates"] != ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]:
        problems.append("rule 5: Phase 1 is not Gates 1 to 7")
    if PHASE_MAP["Phase 3 Pilot readiness"] != ["G8", "G9"]:
        problems.append("rule 5: Phase 3 is not Gates 8 and 9")
    mapped = [c for cols in PHASE_MAP.values() for c in cols]
    if sorted(mapped) != sorted(COLUMNS):
        problems.append("rule 5: phase map does not cover the columns exactly once")

    # Rule 6: every unit holds at least one cell.
    named = set()
    for col in COLUMNS:
        a = ASSIGN[col]
        named.update([a["A"]] + a["R"] + a["C"] + a["I"])
    unnamed = sorted(set(UNITS) - named)
    if unnamed:
        problems.append(f"rule 6: units with no cell in the matrix: {unnamed}")

    # Rule 7: owners are roles from the vocabulary, and each role belongs to one unit.
    vocabulary = set(ROLE_UNIT)
    for col in COLUMNS:
        role = ROLE_OF.get(col)
        if role not in vocabulary:
            problems.append(f"rule 7: {col} role {role!r} is not in the role vocabulary")
        elif ROLE_UNIT[role] != ASSIGN[col]["A"]:
            problems.append(f"rule 7: {col} role {role!r} is held by {ROLE_UNIT[role]}, "
                            f"not by the accountable unit {ASSIGN[col]['A']}")

    # Rule 8: every unit has a published source tier of P or S.
    for u in UNITS:
        tier = SOURCE_TIER.get(u, "")
        if not (tier.startswith("P") or tier.startswith("S")):
            problems.append(f"rule 8: {u} has no P or S source tier")
    extra_src = set(SOURCE_TIER) - set(UNITS)
    if extra_src:
        problems.append(f"rule 8: source tiers for units not in the list: {sorted(extra_src)}")
    return problems


def cell(unit, col):
    a = ASSIGN[col]
    if a["A"] == unit:
        return "A"
    if unit in a["R"]:
        return "R"
    if unit in a["C"]:
        return "C"
    if unit in a["I"]:
        return "I"
    return ""


def main():
    problems = check()
    tally = {}
    for u in UNITS:
        row = [cell(u, c) for c in COLUMNS]
        tally[u] = {
            "name": UNITS[u],
            "source_tier": SOURCE_TIER.get(u, ""),
            "A": [c for c, v in zip(COLUMNS, row) if v == "A"],
            "R": [c for c, v in zip(COLUMNS, row) if v == "R"],
            "C": [c for c, v in zip(COLUMNS, row) if v == "C"],
            "I": [c for c, v in zip(COLUMNS, row) if v == "I"],
        }
        tally[u]["count_A"] = len(tally[u]["A"])
        tally[u]["count_R"] = len(tally[u]["R"])
        tally[u]["count_C"] = len(tally[u]["C"])
        tally[u]["count_I"] = len(tally[u]["I"])
        tally[u]["columns_touched"] = sum(1 for v in row if v)

    owners = {c: ASSIGN[c]["A"] for c in COLUMNS}
    phase_owner = {ph: [owners[c] for c in cols] for ph, cols in PHASE_MAP.items()}
    sale_block_owners = {g: {"unit": owners[g], "role": ROLE_OF[g]} for g in SALE_BLOCKING}
    pilot_owners = {g: {"unit": owners[g], "role": ROLE_OF[g]} for g in PILOT_BATCH_ALSO}
    a_counts = {u: tally[u]["count_A"] for u in UNITS if tally[u]["count_A"]}
    top_unit = max(a_counts, key=a_counts.get)
    share_top = a_counts[top_unit] / len(COLUMNS)

    roles_all = sorted({ROLE_OF[c] for c in COLUMNS})
    roles_gates = sorted({ROLE_OF[c] for c in GATE_COLUMNS})
    roles_per_unit = {u: sorted({ROLE_OF[c] for c in COLUMNS if ASSIGN[c]["A"] == u})
                      for u in UNITS if tally[u]["count_A"]}

    results = {
        "check": "SBU involvement matrix for record 76",
        "date": "2026-10-20",
        "revision": "third pass (verifier items: sourced units only; host roles; rule 8 added)",
        "seed": "none (no random draw)",
        "columns": COLUMNS,
        "n_columns": len(COLUMNS),
        "n_units": len(UNITS),
        "rules": "1 to 8 (see the module docstring)",
        "problems": problems,
        "all_rules_pass": not problems,
        "legacy_map_from_second_pass": LEGACY_MAP,
        "accountable_owner_by_column": owners,
        "owner_role_by_column": {c: ROLE_OF[c] for c in COLUMNS},
        "accountable_owner_by_phase": phase_owner,
        "sale_blocking_gate_owners": sale_block_owners,
        "pilot_batch_gate_owners": pilot_owners,
        "distinct_owner_roles_all_columns": len(roles_all),
        "distinct_owner_roles_all_columns_list": roles_all,
        "distinct_owner_roles_gates_0_to_9": len(roles_gates),
        "distinct_owner_roles_gates_0_to_9_list": roles_gates,
        "owner_roles_per_unit": roles_per_unit,
        "accountable_columns_per_unit": a_counts,
        "busiest_accountable_unit": top_unit,
        "busiest_accountable_unit_name": UNITS[top_unit],
        "busiest_accountable_count": a_counts[top_unit],
        "busiest_share_of_columns": round(share_top, 3),
        "units_with_no_accountable_column": [u for u in UNITS if not tally[u]["count_A"]],
        "units_touching_most_columns": sorted(
            ((u, tally[u]["columns_touched"]) for u in UNITS), key=lambda t: -t[1])[:5],
        "annual_ingredient_need_kg_by_cubes_per_year": annual_need_kg(),
        "annual_need_basis": "grams per cube times cubes per year divided by 1000; "
                             "design masses are DERIVED or ASSUMPTION inputs in submission 05 and 09",
        "per_unit": tally,
    }
    out_json = os.path.join(HERE, "sbu_matrix_check_76_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    lines = []
    lines.append("| Unit | " + " | ".join(COLUMNS) + " | A | R | C | I |")
    lines.append("|---|" + "---|" * (len(COLUMNS) + 4))
    for u in UNITS:
        row = [cell(u, c) or " " for c in COLUMNS]
        t = tally[u]
        lines.append(f"| {u} {UNITS[u]} | " + " | ".join(row) +
                     f" | {t['count_A']} | {t['count_R']} | {t['count_C']} | {t['count_I']} |")
    out_md = os.path.join(HERE, "sbu_matrix_check_76_matrix.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("rules pass:", results["all_rules_pass"], "problems:", problems)
    print("owners:", owners)
    print("distinct owner roles, all 14 columns:", len(roles_all))
    print("distinct owner roles, gates 0 to 9:", len(roles_gates), roles_gates)
    print("accountable columns per unit:", a_counts)
    print("busiest:", top_unit, a_counts[top_unit], "of", len(COLUMNS), "share", round(share_top, 3))
    print("units with no accountable column:", results["units_with_no_accountable_column"])
    print("units touching most columns:", results["units_touching_most_columns"])
    print("annual need (kg):", results["annual_ingredient_need_kg_by_cubes_per_year"])


if __name__ == "__main__":
    main()
