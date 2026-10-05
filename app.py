import os
import streamlit as st
import pandas as pd
import yaml

from mobHelper import MobHelper

st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

st.title('Find those mobs')

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

# Build filter options from the data so custom values (e.g. Race "Beast")
# stay selectable. Known values keep their MobHelper ordering, extras
# found in the data are appended.
data_races = sorted({str(mob.get("Race")) for mob in body if mob.get("Race")})
data_elements = sorted({str(mob.get("Element")) for mob in body if mob.get("Element")})
data_sizes = {str(mob.get("Size")) for mob in body if mob.get("Size")}


def options_with_extras(known_ordered, data_values):
    options = [v for v in known_ordered if v in data_values or v == "Any"]
    options += [v for v in sorted(data_values) if v not in options]
    return options


race_options = options_with_extras(list(MobHelper.raceMap.values()), set(data_races))
element_options = options_with_extras(list(MobHelper.elementMap.values()), set(data_elements))
size_order = ["Any"] + list(MobHelper.sizeMap.values())
size_options = [s for s in size_order if s == "Any" or s in data_sizes]
size_options += sorted(s for s in data_sizes if s not in size_options)

mob_levels = [safe_int(mob.get("Level")) for mob in body]
mob_levels = [level for level in mob_levels if level is not None]
max_level = max(mob_levels) if mob_levels else 99
max_level = max(max_level, 1)
default_max = min(100, max_level)

with st.expander("Search Criteria", True):
    elementSelected = st.selectbox(
        'Which element are you targeting?',
        element_options
    )

    raceSelected = st.selectbox(
        'Which race are you targeting?',
        race_options
    )

    sizeSelected = st.selectbox(
        'Which size are you targeting?',
        size_options
    )

    #maxResults = st.slider(
    #    'Max Results to return',
    #    25, 200, 100)
    maxResults = 200

    minMaxLevel = st.slider(
        'Min / Max Level',
        1, max_level, (min(20, default_max), default_max))

    hideZeroExpMobs = st.checkbox("Hide 0 Exp Mobs", True)

mobs = []
skippedMobs = 0

for lines in body:
    try:
        id = lines["Id"]
        level = int(lines["Level"])
        name = lines["Name"]
        race = lines["Race"]
        element = lines["Element"]
        size = lines["Size"]

        if ("Class" in lines):
            mobClass = lines["Class"]
        else:
            mobClass = "Normal"

        baseExp = extractValueFromMob(lines, "BaseExp")
        jobExp = extractValueFromMob(lines, "JobExp")
        hp = extractValueFromMob(lines, "Hp")

        defense = extractValueFromMob(lines, "Defense")
        agi = extractValueFromMob(lines, "Agi")
        dex = extractValueFromMob(lines, "Dex")
        if "MagicDefense" in lines and lines["MagicDefense"] is not None:
            magicDefense = lines["MagicDefense"]
        else:
            magicDefense = 0

        if (not hideZeroExpMobs or (baseExp != '0' and baseExp != 0)):
            if (elementSelected == 'Any' or elementSelected == element):
                if (raceSelected == 'Any' or raceSelected == race):
                    if (sizeSelected == 'Any' or sizeSelected == size):
                        if (len(mobs) < maxResults):
                            if (int(level) >= minMaxLevel[0] and int(level) <= minMaxLevel[1]):
                                #name, EXP, HP, DEF, MDEF,Scale,AGI,Base EXP / HP
                                mobs.append({"ID": id, "Name": name, "Level": int(level), "BaseExp": int(baseExp), "JobExp": int(jobExp), "HP": int(hp), "Class": mobClass, "DEF": int(defense), "MDEF": int(magicDefense), "AGI": int(agi), "DEX": int(dex), "Scale": size, "Race": race, "Element": element, "RMSLink": "https://ratemyserver.net/index.php?page=mob_db&quick=1&mob_name=" + str(id) + "&mob_search=Search"})
    except (KeyError, TypeError, ValueError):
        skippedMobs += 1
        continue

if skippedMobs:
    st.warning(f"Skipped {skippedMobs} mob record(s) with missing or invalid data. Run validate_mob_db.py to find them.")

mob_db = pd.DataFrame(mobs)

st.data_editor(
    mob_db,
    column_config={
        "RMSLink": st.column_config.LinkColumn("RMSLink", display_text="RMSLink")
    },
    hide_index=True,
)
