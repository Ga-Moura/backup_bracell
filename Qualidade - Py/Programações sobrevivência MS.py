#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import datetime
import time


# In[2]:


pross = os.listdir(r"F:\Qualidade_Florestal\02- MATO GROSSO DO SUL\08- Planejamento e Controle 2°nível\01 - Programação de Sobrevivência\Histórico")
envio = os.listdir(r"F:\Qualidade_Florestal\02- MATO GROSSO DO SUL\08- Planejamento e Controle 2°nível\01 - Programação de Sobrevivência")


# In[7]:


df = pd.DataFrame()

for arquivo in pross:
    if "processamento" in arquivo.lower() and not "~" in arquivo:
        tabela = pd.read_excel(f"F:\Qualidade_Florestal/02- MATO GROSSO DO SUL/08- Planejamento e Controle 2°nível/01 - Programação de Sobrevivência/Histórico/{arquivo}")
        tabela ["ID TALHAO"].astype(str)
        tabela ["ID FAZENDA"].astype(str)
        df = df.append(tabela)


# In[8]:


directory = r"F:\Qualidade_Florestal\02- MATO GROSSO DO SUL\08- Planejamento e Controle 2°nível\01 - Programação de Sobrevivência"

df1 = pd.DataFrame()

for root, dirs, files in os.walk(directory):
    for file in files:
        if "envio" in file.lower():
            file_path = os.path.join(root, file)
            envio = pd.read_excel(file_path)
            envio["Nome da Origem"] = file
            envio["ID TALHAO"] = envio["ID TALHAO"].astype(str)
            envio["ID FAZENDA"] = envio["ID FAZENDA"].astype(str)
            df1 = pd.concat([df1, envio])


# In[9]:


tt = pd.concat([df1, df])


# In[11]:


tt.to_excel(r"F:\Qualidade_Florestal\02- MATO GROSSO DO SUL\08- Planejamento e Controle 2°nível\01 - Programação de Sobrevivência\Histórico\Programações sobrevivência.xlsx")


# In[13]:


