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
save_path = r'F:\Qualidade_Florestal\01- SÃO PAULO\01 - Viveiros\00 - Arquivos Surveys'


# In[57]:




viveiro = ["c4ca74edc83e42b6858a33b837b376ad","c4c5649da3ee44d09b29c1cffbc37354","f3127278c4804f9f8b63ab5aab01a25e","48998e845c274d30be76817f6ab2be76",'35572da04c8f4193a518c888f20cda75','7082d2c2333b45ee9b7a023953c71600',]

#viveiro = [cred['QLD_minijardim_viveiro'],cred['QLD_plantio_de_estacas_viveiro '],cred['QLD_1_selecao_de_mudas_viveiro'],cred['QLD_2_selecao_de_mudas_viveiro']]



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
        if not bool(keep_org_item):
            item_excel.delete(force=True)
    except:
        print("Tivemos Problemas ao baixar o survey:", survey_by_id.title)


# In[59]:


for i in ids['Viveiros']:
    baixar_survey(i)


# In[ ]:
