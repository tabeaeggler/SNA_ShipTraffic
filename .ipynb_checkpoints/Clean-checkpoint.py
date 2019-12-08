#!/usr/bin/env python
# coding: utf-8

# In[37]:


import requests
import pandas as pd 
pd.set_option('mode.chained_assignment', None)


# In[38]:


df = pd.read_csv("./rawData.csv") 


# In[39]:


def setVesselType(number):
    type = '';
    if(number == '6_'):
        type = 'passenger';
    if(number == '7_'):
        type = 'cargo';
    if(number == '8_'):
        type = 'tanker';
    if(number == '3_'):
        type = 'tug';
    if(number == '0_'):
        type = 'undefined';
    if(number == '9_'):
        type = 'yacht';
    if(number == '4_'):
        type = 'high speed';
    if(number == '10'):
        type = 'fishing';
    if(number == '13'):
        type = 'navigation aid';
    return type;


# In[40]:


#clean VesselType
for i in df.index:
    number = df['VesselType'][i][11:13]
    df['VesselType'][i] = setVesselType(number)


# In[41]:


print(df) 


# In[42]:


#create set of vessels
vessels = set(df.Vessel)


# In[43]:


#create new df for linked values (arrival and departure)
timetable = pd.DataFrame([], columns = ['DeparturePort', 'DepartureTime', 'ArrivalPort', 'ArrivalTime', 'Vessel', 'VesselType'])


# In[44]:


#vessel filter and combine arrival and deaprture
for v in vessels:
    allEntriesOfVessel = df[df['Vessel'].isin([v])]
    depFirst = False
    for index, row in allEntriesOfVessel[::-1].iterrows():
        arrivalPort, arrivalTime = "", ""
        
        if(allEntriesOfVessel.Event[index] == "Departure"):
            departurePort = (allEntriesOfVessel.Port[index])
            departureTime = (allEntriesOfVessel.Time[index])
            vessel = (allEntriesOfVessel.Vessel[index])
            vesselType = (allEntriesOfVessel.VesselType[index])
            depFirst = True
        if(allEntriesOfVessel.Event[index] == "Arrival" and depFirst):
            arrivalPort = (allEntriesOfVessel.Port[index])
            arrivalTime = (allEntriesOfVessel.Time[index])
            depFirst = False

            if(departurePort != "" or departureTime != "" or vessel != "" or vesselType != "" or arrivalPort != "" or arrivalTime!= ""):
                newEntry = pd.DataFrame([[departurePort, departureTime, arrivalPort, arrivalTime, vessel, vesselType]], columns = ['DeparturePort', 'DepartureTime', 'ArrivalPort', 'ArrivalTime', 'Vessel', 'VesselType'])
                timetable = timetable.append(newEntry, ignore_index = True)
            


# In[46]:


#drop all rows that have any NaN values
timetable = timetable.dropna()


# In[48]:


print(timetable)
timetable.to_csv("timetable.csv")

