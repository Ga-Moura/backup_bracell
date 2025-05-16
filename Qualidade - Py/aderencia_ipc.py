#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import os
import openpyxl as px


# In[24]:


path = r'F:\Planejamento_e_Controle\Relatório Inventário Pré-corte'


# In[25]:


df = pd.DataFrame()

colunas = ['Talhão', 'Área (ha)', 'IMA (m3/ha/ano)']

aba = 'rel'

for root,dirs, files in os.walk(path):
    for i in files:
        try:
            if i[-5:] == ".xlsx":
                # Obtém o nome do sheet
                sheet_name = pd.ExcelFile(os.path.join(root, i)).sheet_names[0]

                if sheet_name.lower().startswith(aba):
                # Configura a coluna 'Talhão' para ser lida como string
                    ipc = pd.read_excel(os.path.join(root, i), skiprows=1, usecols=colunas, sheet_name=sheet_name, dtype={'Talhão': str, 'Área (ha)': float,'IMA (m3/ha/ano)':float})
                    ipc['arquivo'] = i
                    ipc['pasta'] = root
                    df = pd.concat([df, ipc], ignore_index=True)
                    df = df[df['Talhão'].notnull()]
        except Exception as e:
            print(f"Erro ao processar {i}: {e}")


# In[26]:


df.to_excel(r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\14 - Transformação digital\01 - Processamento de dados",index=False,sheet_name="Aderência IPC")

