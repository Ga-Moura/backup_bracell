#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import shutil
import openpyxl as px 
import imghdr
import os


# ###  FW ###

# In[153]:


path = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Bases de Apoio\cadastro_fotos_fw.xlsx'


# In[154]:


df = pd.read_excel(path,engine='openpyxl')

dtype = {
    'objectid_operador': pd.Int32Dtype(),
    'objectid_parcela':pd.Int32Dtype(),
    'objectid_avaliacao':pd.Int32Dtype(),
    'fazenda' : pd.Int32Dtype(),
    'talhao' : pd.Int32Dtype(),
    'operador' : pd.Int32Dtype()
}

df = df.astype(dtype= dtype ,errors= 'ignore')


df['operador'] = df['operador'].fillna(0)


# In[155]:


parcelas = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Madeira Não removida - FW'


# In[156]:


operadores = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Nota operadores -FW'


# In[157]:


fotos_parcela = os.listdir(parcelas)


# In[158]:


for imagem in os.listdir(parcelas):
    if imghdr.what(os.path.join(parcelas, imagem)):
        for index, objectid in enumerate(df["objectid_parcela"]):
            if str(objectid) == str(imagem).split("-")[0]:
                novo_nome = str(df['avaliacao'][index]) + " - "+ str(df["modulo_baldeio"][index]) + " - " + str(df['fazenda'][index])+ " - " + str(df['talhao'][index]) + " - " + str(imagem)
                novo_nome = novo_nome.replace("/", "-")  # substitui o ponto por hífen
                try:
                    shutil.move(os.path.join(parcelas, imagem), os.path.join(parcelas, novo_nome))
                except Exception:
                    print(f"O arquivo {imagem} não foi encontrado")
                break
    else:
        print(f"O arquivo {imagem} não é uma imagem")


# In[159]:


for imagem in os.listdir(operadores):
    if imghdr.what(os.path.join(operadores, imagem)):
        for index, objectid in enumerate(df["objectid_operador"]):
            if str(objectid) == str(imagem).split("-")[0]:
                novo_nome = str(df['avaliacao'][index]) + " - "+ str(df["modulo_baldeio"][index]) + " - " + str(df['operador'][index]) + " - " + str(df['fazenda'][index])+ " - " + str(df['talhao'][index]) + " - " + str(imagem)
                novo_nome = novo_nome.replace("/", "-")  # substitui o ponto por hífen
                try:
                    shutil.move(os.path.join(operadores, imagem), os.path.join(operadores, novo_nome))
                except Exception:
                    print(f"O arquivo {imagem} não foi encontrado")
                break
    else:
        print(f"O arquivo {imagem} não é uma imagem")


# ### HV ###

# In[5]:


path_hv = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Bases de Apoio\cadastro_fotos_hv.xlsx'


# In[6]:


feixe = pd.read_excel(path_hv, engine= 'openpyxl')


# In[7]:


dtype = {
    'objectid_feixe': pd.Int32Dtype(),
    'fazenda' : pd.Int32Dtype(),
    'talhao' : pd.Int32Dtype(),
    'operador' : pd.Int32Dtype(),
    }

feixe = feixe.astype(dtype = dtype, errors = 'ignore')


# In[8]:


feixe_fotos = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Avaliação - HV'


# In[9]:


for imagem in os.listdir(feixe_fotos):
    if imghdr.what(os.path.join(feixe_fotos, imagem)):
        for index, objectid in enumerate(feixe["objectid_feixe"]):
            if str(objectid) == str(imagem).split("-")[0]:
                novo_nome = str(feixe['nivel_avaliacao'][index]) + " - "+ str(feixe["modulo_corte"][index]) + " - " +str(feixe['cod_maquina'][index]) +" - " + str(feixe['operador'][index]) + " - " + str(feixe['fazenda'][index])+ " - " + str(feixe['talhao'][index]) + " - " + str(imagem)
                novo_nome = novo_nome.replace("/", "-")  # substitui o ponto por hífen
                try:
                    shutil.move(os.path.join(feixe_fotos, imagem), os.path.join(feixe_fotos, novo_nome))
                except Exception:
                    print(f"O arquivo {imagem} não foi encontrado")
                break
    else:
        print(f"O arquivo {imagem} não é uma imagem")


# ### FIM HV ###
