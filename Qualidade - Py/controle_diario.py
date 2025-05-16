#!/usr/bin/env python
# coding: utf-8

# In[1]:


import selenium
from selenium import webdriver
import time
import pandas as pd
import os
import openpyxl
from openpyxl import load_workbook


# In[2]:


# criando o web driver
options = webdriver.ChromeOptions()

# atualizando a preferência
prefs = {"download.default_directory": r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"}

# definindo que a nova preferência seja atualizada
options.add_experimental_option("prefs", prefs)

# definindo que o webdriver.chrome deve vir com as definições options
nav = webdriver.Chrome(options=options)


# In[8]:


#maximize a janela
nav.maximize_window()
#abrindo site
nav.get(r"https://eflorestal-my.sharepoint.com/:f:/g/personal/resultados_eflorestal_onmicrosoft_com/EsKFrQ07MoZEqMoW8iAh8vYBsc8rlIFXkG3evAtxGJ21Cg?e=OXeBDH")
time.sleep(5)
#selecionando pasta controle de produção
nav.find_element("xpath", '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[3]').click()
time.sleep(5)

#Clicando na pasta
nav.find_element("xpath",'//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[2]/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[5]/div/div/div[1]/div/div/i[2]').click()
time.sleep(5)
#clicando para Donwload

nav.find_element('xpath', '//*[@id="appRoot"]/div/div[2]/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div[3]/button/span/span').click()
time.sleep(15)
#Fechar o executor
nav.quit()

# In[9]:


# alterando o arquivo de xlxb para xlsx
path = r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"
arquivos = [os.path.join(path, arquivo) for arquivo in os.listdir(path)]
arquivo_mais_recente = max(arquivos, key=os.path.getctime)


# In[10]:


df_programacao = pd.read_excel(
    arquivo_mais_recente, engine='pyxlsb', sheet_name="Base_programação")
df_entregas = pd.read_excel(
    arquivo_mais_recente, engine='pyxlsb', sheet_name="Base_entregas")

with pd.ExcelWriter(r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Controle diário de Produção e Programação.xlsx") as writer:
    df_programacao.to_excel(writer, sheet_name="Base_programação")
    df_entregas.to_excel(writer, sheet_name="Base_entregas")


# In[11]:


os.remove(arquivo_mais_recente)
