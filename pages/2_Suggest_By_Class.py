import os
import streamlit as st
import pandas as pd
import yaml

from classHelper import ClassHelper

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

st.title('Suggest mobs by class')
st.caption('Pre-renewal leveling recommendations for Project Alfheim (2-1 / 2-2 / Trans). '
           'Profiles are starting points - Alfheim has custom skill and monster adjustments, so verify in game. '
           '[Alfheim Wiki](https://projectalfheim.net/wiki/index.php/Main_Page) | '
           '[Skill Simulator](https://projectalfheim.net/skillsim)')

MOB_DB_PATH = 'mob_db.yml'


def extractValueFromMob(mob, valueToExtract, valueIfMissing=0):
    if valueToExtract in mob and mob[valueToExtract] is not None:
        return mob[valueToExtract]
    else:
        return valueIfMissing


def safe_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@st.cache_data
def get_all_mobs(_file_mtime):
    # _file_mtime is only used to bust the cache when mob_db.yml changes.
    with open(MOB_DB_PATH, 'r') as file:
        all_mobs = yaml.safe_load(file)

    return all_mobs


try:
    all_mobs = get_all_mobs(os.path.getmtime(MOB_DB_PATH))
except FileNotFoundError:
    st.error(f"Could not find {MOB_DB_PATH}. Did the data file get committed?")
    st.stop()
except yaml.YAMLError as e:
    st.error(f"{MOB_DB_PATH} could not be parsed. Recently added mobs may have broken the YAML - check the details below.")
    st.exception(e)
    st.stop()

body = all_mobs.get("Body", [])

data_elements = [e for e in ClassHelper.ELEMENTS_ALL if any(str(m.get("Element")) == e for m in body)]
data_races = sorted({str(m.get("Race")) for m in body if m.get("Race")})
data_sizes = [s for s in ["Small", "Medium", "Large"] if any(str(m.get("Size")) == s for m in body)]

mob_levels = [safe_int(m.get("Level")) for m in body]
mob_levels = [level for level in mob_levels if level is not None]
max_level = max(mob_levels) if mob_levels else 99
max_level = max(max_level, 1)

class_labels = [f"{name} ({branch} {tier})" for (name, branch, tier, _, _) in ClassHelper.CLASSES]
selected_label = st.selectbox('Which class are you leveling?', class_labels)
name, branch, tier, profile_key, band = ClassHelper.CLASSES[class_labels.index(selected_label)]
profile = ClassHelper.PROFILES[profile_key]

st.subheader(f"{name} hunts: {', '.join(profile['elements']) if profile['elements'] else 'any element'}")
for note in profile["notes"]:
    st.markdown(f"- {note}")
if tier == "Trans":
    st.markdown(f"- _{ClassHelper.TRANS_NOTE}_")

default_elements = profile["elements"] if profile["elements"] else data_elements
default_races = profile["races"] if profile["races"] else data_races
default_sizes = profile["sizes"] if profile["sizes"] else data_sizes

with st.expander("Target filters (prefilled from the class profile, adjust freely)", True):
    elementsSelected = st.multiselect('Target elements', data_elements, default=default_elements)
    racesSelected = st.multiselect('Target races', data_races, default=default_races)
    sizesSelected = st.multiselect('Target sizes', data_sizes, default=default_sizes)

    band_lo = min(band[0], max_level)
    band_hi = min(band[1], max_level)
    if band_lo > band_hi:
        band_lo = band_hi
    minMaxLevel = st.slider('Min / Max Level', 1, max_level, (band_lo, band_hi))

    sortSelected = st.selectbox('Sort by', ['EXP per HP', 'Base EXP', 'Level'])
    hideZeroExpMobs = st.checkbox("Hide 0 Exp Mobs", True)
    hideBossMobs = st.checkbox("Hide Boss / Guardian class mobs", True)
    maxResults = 200

if not elementsSelected or not racesSelected or not sizesSelected:
    st.warning("Select at least one element, race and size to see recommendations.")
    st.stop()

mobs = []
skippedMobs = 0

for lines in body:
    try:
        id = lines["Id"]
        level = int(lines["Level"])
        mob_name = lines["Name"]
        race = lines["Race"]
        element = lines["Element"]
        size = lines["Size"]
        mobClass = lines.get("Class") or "Normal"

        baseExp = extractValueFromMob(lines, "BaseExp")
        jobExp = extractValueFromMob(lines, "JobExp")
        hp = extractValueFromMob(lines, "Hp")

        defense = extractValueFromMob(lines, "Defense")
        agi = extractValueFromMob(lines, "Agi")
        dex = extractValueFromMob(lines, "Dex")
        magicDefense = extractValueFromMob(lines, "MagicDefense")

        if hideBossMobs and mobClass in ("Boss", "Guardian"):
            continue
        if hideZeroExpMobs and (baseExp == '0' or baseExp == 0):
            continue
        if element not in elementsSelected:
            continue
        if race not in racesSelected:
            continue
        if size not in sizesSelected:
            continue
        if not (minMaxLevel[0] <= level <= minMaxLevel[1]):
            continue

        baseExp = int(baseExp)
        hp = int(hp)
        expPerHp = round(baseExp / hp, 2) if hp else 0

        mobs.append({"ID": id, "Name": mob_name, "Level": int(level), "BaseExp": baseExp,
                     "JobExp": int(jobExp), "HP": hp, "ExpPerHp": expPerHp, "Class": mobClass,
                     "DEF": int(defense), "MDEF": int(magicDefense), "AGI": int(agi), "DEX": int(dex),
                     "Scale": size, "Race": race, "Element": element,
                     "RMSLink": "https://ratemyserver.net/index.php?page=mob_db&quick=1&mob_name=" + str(id) + "&mob_search=Search"})
        if len(mobs) >= maxResults:
            break
    except (KeyError, TypeError, ValueError):
        skippedMobs += 1
        continue

if skippedMobs:
    st.warning(f"Skipped {skippedMobs} mob record(s) with missing or invalid data. Run validate_mob_db.py to find them.")

if sortSelected == 'EXP per HP':
    mobs.sort(key=lambda m: m["ExpPerHp"], reverse=True)
elif sortSelected == 'Base EXP':
    mobs.sort(key=lambda m: m["BaseExp"], reverse=True)
else:
    mobs.sort(key=lambda m: m["Level"])

mob_db = pd.DataFrame(mobs)

st.data_editor(
    mob_db,
    column_config={
        "RMSLink": st.column_config.LinkColumn("RMSLink", display_text="RMSLink")
    },
    hide_index=True,
)
