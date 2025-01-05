import streamlit as st
import pandas as pd
import numpy as np
import csv
import yaml

from operator import itemgetter, attrgetter

from mobHelper import MobHelper

st.set_page_config(layout="wide",initial_sidebar_state='collapsed')

st.title('Find those mobs')
count = 0
matchingMobs = {}
mobs = []



def extractValueFromMob(lines,valueToExtract,valueIfMissing=0):
    if valueToExtract in lines:
        return lines[valueToExtract]
    else:
        return valueIfMissing

with st.expander("Search Criteria", True):
    elementSelected = st.selectbox(
        'Which element are you targeting?',
        MobHelper.elementMap.values()
    )

    raceSelected = st.selectbox(
        'Which race are you targeting?',
        MobHelper.raceMap.values()
    )

    #maxResults = st.slider(
    #    'Max Results to return',
    #    25, 200, 100)
    maxResults = 200

    minMaxLevel = st.slider(
        'Min / Max Level',
        1, 114, (20,100))

    hideZeroExpMobs = st.checkbox("Hide 0 Exp Mobs", True)
printCount = 0

@st.cache_data
def get_all_mobs():
    with open('mob_db.yml', 'r') as file:
        all_mobs = yaml.safe_load(file)

    return all_mobs

all_mobs = get_all_mobs()
#with open('mobs.csv', mode ='r') as file:    
for lines in all_mobs["Body"]:
    #csvFile = csv.DictReader(file)
    #for lines in csvFile:
        #print(lines)
        #st.write(lines)
        #id = lines["ID"]
        id = lines["Id"]
        #level = lines["LV"]
        level = lines["Level"]
        #name = lines["kROName"]
        name = lines["Name"]
        race = lines["Race"]
        element = lines["Element"]

        if ("Class" in lines):
            mobClass =  lines["Class"]
        else: 
            mobClass = "Normal"

        #baseExp = lines["EXP"]
        baseExp = extractValueFromMob(lines,"BaseExp")
        jobExp = extractValueFromMob(lines,"JobExp")
        hp = extractValueFromMob(lines,"Hp")

        defense = extractValueFromMob(lines,"Defense")
        agi = extractValueFromMob(lines,"Agi")
        dex = extractValueFromMob(lines,"Dex")
        if "MagicDefense" in lines:
            magicDefense = lines["MagicDefense"]
        else: 
            magicDefense = 0

        if (hideZeroExpMobs and baseExp != '0' and baseExp != 0):
            # try:
            #     elementMod10 = int(element) % 10
            # except:
            #     print("Could not modulo" + element)
            #     elementMod10 = 0
            
            #Handle Element Selection
            #if (elementSelected != 'Any'):
                #calculatedElementSelected = MobHelper.elementMap[elementMod10]
            #    calculatedElementSelected = element

            calculatedElementSelected = lines["Element"]

            #scale = MobHelper.sizeMap[int(lines["Scale"])]
            scale = lines["Size"]

            #race = MobHelper.raceMap[int(lines["Race"])]
            race = lines["Race"]

            if (elementSelected == 'Any' or elementSelected == calculatedElementSelected):
                if (raceSelected == 'Any' or raceSelected == race): 

                    if (printCount < maxResults):
                        #try:
                            if (int(level) >= minMaxLevel[0] and int(level) <= minMaxLevel[1]):
                                #name, EXP, HP, DEF, MDEF,Scale,AGI,Base EXP / HP
                                mobs.append({"ID":id, "Name":name,"Level":int(level),"BaseExp":int(baseExp),"JobExp":int(jobExp),"HP":int(hp),"Class":mobClass, "DEF":int(defense),"MDEF":int(magicDefense),"AGI":int(agi),"DEX":int(dex),"Scale":scale,"Race":race,"Element":calculatedElementSelected, "RMSLink":"https://ratemyserver.net/index.php?page=mob_db&quick=1&mob_name="+str(id)+"&mob_search=Search"})
                                #mobs.append((id,name,int(level),calculatedElementSelected))
                                #st.write("Name: " + name + ", Race: " + race + ", Element: " + element + ", ElementMod10: " + str(elementMod10))
                                printCount+=1 
                        #except:
                        #    print("Could not parse level for id " + str(id))
                        #    print(lines)
        

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