#!/usr/bin/env python
# coding: utf-8

# In[8]:


import json
import requests
import pandas as pd


# In[9]:


PLATFORM_API = 'https://stage.platforms.axds.co/'
params = { 'verbosity': 2 }


# In[10]:


device = 'Sfin-3f0022001847363439353035'
search_tag = f'packrat_source_id:{device}*'
sessions = requests.get(f'{PLATFORM_API}/tags/search/{search_tag}', params=params).json()['tags']
display(f'Found {len(sessions)} platforms tagged with "{search_tag}"')


# In[11]:


csv_files = []
for k, c in sessions.items():
    files = list(c.values())[0]['files']
    for fname, fc in files.items():
        if fname.endswith('csv'):
            csv_files.append(
                fc['url']
            )
display(f'Found {len(csv_files)} CSV files for this session')


# In[12]:


dfs = []

for url in csv_files:
    df = pd.read_csv(url, index_col=None, header=0)
    dfs.append(df)

frame = pd.concat(dfs, axis=0, ignore_index=True)
display(f'Found {len(frame)} data rows')


# In[13]:


start = '2020-07-01'

frame['time'] = pd.to_datetime(frame.time)
frame = frame[frame.time > start]
display(f'Subset to {len(frame)} data rows')


# In[14]:


frame.to_csv(f'{device}.csv', index=False)


# In[ ]:




