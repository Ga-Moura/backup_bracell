#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import openpyxl as px
import datetime as dt


# In[2]:


path = r'F:\Colheita\COLHEITA FLORESTAL\CONTROLES\Controles - 2024\05 - PREMIO PRODUÇÃO\Gestão à Vista'


# In[3]:


colunas_desejadas_fw = ['Matricula','Meta Produtividade', 'Real Produtividade', 'Aderência Produtividade','COLABORADOR','Aderência Produtividade final','Aderência Produtividade Ponderada']

df_fw = pd.DataFrame()

for root, dir, files in os.walk(path):
    for file in files:


        if 'gestão a vista' in file.lower() and "xsl" in file.lower() and not "~$" in file:
            file_path = os.path.join(root,file)

            base_fw = pd.read_excel(file_path, 
                     engine='openpyxl',
                     sheet_name="PRODUTIVIDADE_FW",
                     skiprows=6 ,
                     dtype={"Matricula":"object"})
            colunas = list(base_fw.columns)

            colunas_comuns = list(set(colunas_desejadas_fw) & set(colunas))
            
            base_fw = base_fw[colunas_comuns]
            
            base_fw = base_fw[base_fw['Matricula'].notna()]
            
            base_fw['Operação'] = "Forwarder"
            
            base_fw['Data de Referência'] = file.lower().partition(".")[0].split('-')[1]
            
            df_fw = pd.concat([df_fw,base_fw],ignore_index=True,axis=0)

df_fw['Aderencia FW'] = df_fw.apply(lambda x: x['Aderência Produtividade Ponderada'] if pd.isna(x['Aderência Produtividade final']) else x['Aderência Produtividade final'], axis=1)

df_fw = df_fw.drop(['Aderência Produtividade final','Aderência Produtividade Ponderada'],axis=1)

df_fw = df_fw[df_fw['Aderencia FW'].notna()]


# In[4]:


colunas_desejadas_hv = ['Matricula','Meta Produtividade', 'Real Produtividade','Aderência Produtividade','COLABORADOR','Produtividade Final']

df_hv = pd.DataFrame()


for root, dir, files in os.walk(path):
    for file in files:
        if 'gestão a vista' in file.lower() and "xsl" in file.lower() and not "~$" in file:
            file_path = os.path.join(root,file)
            base_hv = pd.read_excel(file_path, 
                     engine='openpyxl',
                     sheet_name="PRODUTIVIDADE_HV",
                     skiprows=6 ,
                     dtype={"Matricula":"object"})
            
            colunas = list(base_hv.columns)

            colunas_comuns = list(set(colunas_desejadas_hv) & set(colunas))

            base_hv = base_hv[colunas_comuns]

            base_hv = base_hv[base_hv['Matricula'].notna()]

            base_hv['Operação'] = "Harvester"

            base_hv['Data de Referência'] = file.lower().partition(".")[0].split('-')[1]

            base_hv = base_hv[base_hv['Produtividade Final'].notna()]

            df_hv = pd.concat([df_hv,base_hv],ignore_index=True,axis=0)


# In[5]:


with pd.ExcelWriter(r"F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Produtividade.xlsx") as writer:
    df_fw.to_excel(writer,sheet_name="Produtividade Forwarder", index=False)
    df_hv.to_excel(writer, sheet_name="Produtividade Harvester", index=False)

