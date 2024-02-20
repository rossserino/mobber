import streamlit as st
import pandas as pd
import numpy as np
import csv

from operator import itemgetter, attrgetter

st.set_page_config(layout="wide")

st.title('Find those mobs')
count = 0
matchingMobs = {}
mobs = []

sizeMap = {
    0: "Small",
    1: "Medium",
    2: "Large",
    3: "Big"
}

raceMap = {
    0: "Formless",
    1: "Undead",
    2: "Brute",
    3: "Plant",
    4: "Insect",
    5: "Fish",
    6: "Demon",
    7: "DemiHuman",
    8: "Angel",
    9: "Dragon",
    10: "Player",
    21: "Unknown"
}

elementMap = {
    0: "Neutral",
    1: "Water",
    2: "Earth",
    3: "Fire",
    4: "Wind",
    5: "Poison",
    6: "Holy",
    7: "Shadow",
    8: "Ghost",
    9: "Undead"
}

# raceSelected= st.selectbox(
#     'Which race are you targeting?',
#     (
#         'Any',
#         'Angel',
#         'Brute',
#         'DemiHuman',
#         'Demon',
#         'Dragon',
#         'Fish',
#         'Formless',
#         'Insect',
#         'Plant',
#         'Player',
#         'Undead'
#     )
# )

elementSelected = st.selectbox(
    'Which element are you targeting?',
    ('Any',
        'Neutral',
        'Water',
        'Earth',
        'Fire',
        'Wind',
        'Poison',
        'Holy',
        'Shadow',
        'Ghost',
        'Undead'
    )
)

maxResults = st.slider(
    'Max Results to return',
    25, 200, 100)
minMaxLevel = st.slider(
    'Min / Max Level',
    1, 114, (20,60))
printCount = 0

with open('mobs.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            id = lines["ID"]
            level = lines["LV"]
            name = lines["kROName"]
            #race = lines["Race"]
            element = lines["Element"]
            try:
                elementMod10 = int(element) % 10
            except:
                print("Could not modulo" + element)
                elementMod10 = 0
            
            #Handle Element Selection
            if (elementSelected != 'Any' and len(lines["Scale"]) > 0):
                calculatedElementSelected = elementMap[elementMod10]
            
                scale = sizeMap[int(lines["Scale"])]

                race = raceMap[int(lines["Race"])]

                if (elementSelected == calculatedElementSelected):
                    
                    if (printCount < maxResults):
                        try:
                            if (int(level) >= minMaxLevel[0] and int(level) <= minMaxLevel[1]):
                                #name, EXP, HP, DEF, MDEF,Scale,AGI,Base EXP / HP
                                mobs.append({"ID":id, "Name":name,"Level":int(level),"BaseExp":int(lines["EXP"]),"JobExp":int(lines["JEXP"]),   "HP":int(lines["HP"]),"DEF":int(lines["DEF"]),"MDEF":int(lines["MDEF"]),"AGI":int(lines["AGI"]),"DEX":int(lines["DEX"]),"Scale":scale,"Race":race,"Element":calculatedElementSelected, "RMSLink":"https://ratemyserver.net/index.php?page=mob_db&quick=1&mob_name="+id.replace("//","")+"&mob_search=Search"})
                                #mobs.append((id,name,int(level),calculatedElementSelected))
                                #st.write("Name: " + name + ", Race: " + race + ", Element: " + element + ", ElementMod10: " + str(elementMod10))
                                printCount+=1 
                        except:
                            print("Could not parse level for id " + id)
            

#st.table(mobs)
#st.table(sorted(mobs,key=lambda mob: mob[2], reverse=True))
#st.dataframe(mobs)

mob_db = pd.DataFrame(mobs)
data_df = pd.DataFrame(
    {
        "mobs": mobs
    }
)

st.data_editor(
    mob_db,
    column_config={
        "RMSLink": st.column_config.LinkColumn("RMSLink",display_text="RMSLink")   
    },
    hide_index=True,
)