#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd 
import time
from bs4 import BeautifulSoup


# In[2]:


origURL = 'https://www.myshiptracking.com/ports-arrivals-departures/&pp=50&page='

data = []
i = 1
while(i <= 10):
    url = origURL + '%d' % i

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    rows = soup.select('div.cs-table div.table-group')
    for row in rows:
        list = row.select_one('div.table-row').text.strip().splitlines()
        type = row.select_one('div.table-row div.td_vesseltype img')
        list.append(type.get('src'))
        data.append(list)
    
    print(i)
    i+= 1
    #time.sleep(0.05)
    
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Event', 'Time', 'Port', 'Vessel', 'VesselType']) 


# In[3]:


df.to_csv("rawData.csv")

