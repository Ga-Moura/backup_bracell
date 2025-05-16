#!/usr/bin/env python
# coding: utf-8

# In[38]:
from arcgis.gis import GIS
import pandas as pd
import os
import shutil
from math import sqrt
import locale
import configparser
config = configparser.ConfigParser()
config.read('sets.conf')
cred = config['survey']




# In[39]:


locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


# In[55]:


# Define variables
portalURL = cred['portal']
username = cred['login']
password = cred['senha']
save_path = r'F:\Qualidade_Florestal\02- MATO GROSSO DO SUL\16 - Bases Survey'

# In[57]:


survey = ['8dab1db5a48f41c79f2cb9063829fdc1','b89c2ead5a514d5f9e40b46fde508f4b','986c1fb2f0fc4bed83538238f3983d46','29737721e5be4d67b8dc9aba61e6d4f4','0a289f6c2bc6464abfb70cd13c9157e2','02d11d224360424fb95b9fce2e9614bb','8a37d8cdcef6478d89e89f23171582a4']

ids = pd.DataFrame(survey)

ids = ids.rename(columns={0: "surveys"})


# In[58]:


def baixar_survey(survey_id):
    keep_org_item = False
    try:
        gis = GIS(portalURL, username, password)
        survey_by_id = gis.content.get(survey_id)
        print(survey_by_id.title)
        rel_fs = survey_by_id.related_items('Survey2Service', 'forward')[0]
        item_excel = rel_fs.export(
            title=survey_by_id.title, export_format='Excel')
        item_excel.download(save_path=save_path)
        if not bool(keep_org_item):
            item_excel.delete(force=True)
    except:
        print("Tivemos Problemas ao baixar o survey:", survey_by_id.title)


# In[59]:


for i in ids['surveys']:
    baixar_survey(i)


# In[ ]:
