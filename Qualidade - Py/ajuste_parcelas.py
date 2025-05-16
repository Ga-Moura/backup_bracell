#!/usr/bin/env python
# coding: utf-8

# In[95]:


import pandas as pd
import os


# In[96]:


path = os.listdir(r"F:/Qualidade_Florestal/01- SÃO PAULO/10- Planejamento e Controle 2°nível/2023/12 - Programações Sobrevivência/06 - Resultados/01 - Base de dados")


# In[97]:


df = pd.DataFrame()

for arquivo in path:
    if "resultados operacionais" in arquivo.lower() and not "~" in arquivo:
        tabela = pd.read_excel(f"F:/Qualidade_Florestal/01- SÃO PAULO/10- Planejamento e Controle 2°nível/2023/12 - Programações Sobrevivência/06 - Resultados/01 - Base de dados/{arquivo}",sheet_name="DadosBrutos",skiprows=1)
        tabela['Nome Origem'] = arquivo
        df = pd.concat([df,tabela])


# In[98]:


df = df.dropna(subset=['OBSERVACAO'])


# In[99]:


df.to_excel('F:/Qualidade_Florestal/01- SÃO PAULO/10- Planejamento e Controle 2°nível/2023/12 - Programações Sobrevivência/06 - Resultados/01 - Base de dados/ajuste_parcela.xlsx', sheet_name="ajustes")

df.to_excel('F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados/ajuste_parcela.xlsx', sheet_name="ajustes")

