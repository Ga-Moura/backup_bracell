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
save_path = r'U:\Publica\Florestal\Relatórios de Qualidade\Avaliações de 2º nível de Silvicultura\Bases Survey'
save_path2 = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Viveiros'


# In[57]:


viveiro = ["c4ca74edc83e42b6858a33b837b376ad","c4c5649da3ee44d09b29c1cffbc37354","f3127278c4804f9f8b63ab5aab01a25e","48998e845c274d30be76817f6ab2be76",'35572da04c8f4193a518c888f20cda75','7082d2c2333b45ee9b7a023953c71600','29737721e5be4d67b8dc9aba61e6d4f4','16c4d486078d49738ffe2e0308a22db3','02d11d224360424fb95b9fce2e9614bb','8a37d8cdcef6478d89e89f23171582a4']

ids = pd.DataFrame(viveiro)

ids = ids.rename(columns={0: "Viveiros"})


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
        item_excel.download(save_path=save_path2)
        if not bool(keep_org_item):
            item_excel.delete(force=True)
    except:
        print("Tivemos Problemas ao baixar o survey:", survey_by_id.title)


# In[59]:


for i in ids['Viveiros']:
    baixar_survey(i)


# In[ ]:
