#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import datetime
import time


# In[2]:


path = os.listdir(
    "F:/Qualidade_Florestal/Qualidade/2° Nível\Avaliação de Sobrevivência/Processamento e Resultados/BD/BD Dados de campo")
tabela_total = pd.DataFrame()


# In[3]:


for arquivo in path:
    if "Aval. Sobrev" in arquivo and ("23" in arquivo or "22" in arquivo) and not "21" in arquivo:
     # carrega a tabela Excel em um DataFrame usando o caminho absoluto do arquivo
        tabela = pd.read_excel(
            fr"F:/Qualidade_Florestal/Qualidade/2° Nível\Avaliação de Sobrevivência/Processamento e Resultados/BD/BD Dados de campo/{arquivo}")
 # adiciona uma coluna com o nome do arquivo
        tabela["Nome do arquivo"] = arquivo
 # adiciona a tabela ao DataFrame tabela_total
        tabela_total = tabela_total.append(tabela)


# In[4]:


tabela_total.to_excel(
    r"F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados/Equilíbrio - Aval. Sobrev. Resultados Operacionais Consolidados.xlsx")


# In[5]:


print(tabela_total)


# In[ ]:
