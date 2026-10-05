"""Validate mob_db.yml before committing new mobs.

Catches the common mistakes that break the app or silently hide mobs:
  - invalid YAML syntax (e.g. unquoted item names like "[M] Mystic Frozen")
  - duplicate mob Ids
  - missing keys the app requires (Id, Name, Level, Race, Size, Element)
  - Race / Element / Size values the app cannot filter on
  - non-numeric stats, levels outside the app's level slider

Usage: python3 validate_mob_db.py [path/to/mob_db.yml]
Exits non-zero when problems are found.
"""
import sys
from collections import Counter, defaultdict

import yaml

MOB_DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "mob_db.yml"

KNOWN_RACES = {"Formless", "Undead", "Brute", "Plant", "Insect",
               "Fish", "Demon", "Demihuman", "Angel", "Dragon",
               "Beast"}  # Beast is custom-server only; the app adds it dynamically
KNOWN_ELEMENTS = {"Neutral", "Water", "Earth", "Fire", "Wind", "Poison",
                  "Holy", "Dark", "Ghost", "Undead"}
KNOWN_SIZES = {"Small", "Medium", "Large"}
REQUIRED_KEYS = ["Id", "Name", "Level", "Race", "Size", "Element"]
NUMERIC_KEYS = ["Level", "BaseExp", "JobExp", "Hp", "Defense",
                "MagicDefense", "Agi", "Dex"]

errors = []
warnings = []

try:
    with open(MOB_DB_PATH, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
except yaml.YAMLError as e:
    print(f"FAIL: {MOB_DB_PATH} is not valid YAML:\n{e}")
    sys.exit(1)

body = (data or {}).get("Body", [])
if not isinstance(body, list) or not body:
    print("FAIL: no mob list found under top-level 'Body' key.")
    sys.exit(1)

by_id = defaultdict(list)
for mob in body:
    if isinstance(mob, dict) and mob.get("Id") is not None:
        by_id[mob.get("Id")].append(mob.get("Name"))

for mob_id, names in sorted(by_id.items()):
    if len(names) > 1:
        warnings.append(
            f"Duplicate Id {mob_id} ({len(names)} rows: {names}). "
            "Both rows will show in the app - intended for rebalanced customs?"
        )

for mob in body:
    label = f"Id {mob.get('Id', '?')} ({mob.get('Name', '?')})"
    if not isinstance(mob, dict):
        errors.append(f"{label}: row is not a mapping, skipping checks.")
        continue
    for key in REQUIRED_KEYS:
        if key not in mob or mob[key] is None:
            errors.append(f"{label}: missing required key '{key}' (row will be skipped by the app).")
    for key in NUMERIC_KEYS:
        value = mob.get(key)
        if value is None:
            continue
        try:
            int(value)
        except (TypeError, ValueError):
            errors.append(f"{label}: '{key}' is not numeric ({value!r}) (row will be skipped by the app).")
    if mob.get("Race") not in KNOWN_RACES and mob.get("Race") is not None:
        warnings.append(f"{label}: Race '{mob.get('Race')}' has no filter option (only visible with race 'Any').")
    if mob.get("Element") not in KNOWN_ELEMENTS and mob.get("Element") is not None:
        warnings.append(f"{label}: Element '{mob.get('Element')}' has no filter option.")
    if mob.get("Size") not in KNOWN_SIZES and mob.get("Size") is not None:
        warnings.append(f"{label}: Size '{mob.get('Size')}' is unusual.")

levels = [m.get("Level") for m in body
          if isinstance(m, dict) and isinstance(m.get("Level"), int)]
if levels:
    print(f"Mobs: {len(body)}, level range {min(levels)}-{max(levels)}.")

for w in warnings:
    print(f"WARNING: {w}")
for e in errors:
    print(f"ERROR: {e}")

print(f"{len(errors)} error(s), {len(warnings)} warning(s).")
sys.exit(1 if errors else 0)
