#!/usr/bin/env python
# coding: utf-8

# In[1]:


from arcgis.gis import GIS
import pandas as pd
import os
import shutil


# In[2]:


# Define variables
portalURL = r'https://gissp.bracell.com/portal/'
username = "Qualidade_Florestal"
password = "Qualidade@24"
save_path = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys'


# In[9]:


ids = pd.read_excel(
    r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\11 - Silvicultura\Survey - Silvicultura.xlsx')
print(ids)


# In[12]:


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


# In[11]:


for i in ids["ID"]:
    baixar_survey(i)


# In[ ]:
