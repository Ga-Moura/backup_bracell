#!/usr/bin/env python
# coding: utf-8

# In[1]:


import locale
import calendar
import selenium
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import zipfile as zf
import os
import shutil
import xlsxwriter
import datetime

# In[2]:


# criando o web driver
options = webdriver.ChromeOptions()

#path chomedriver 
path_chrome =r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\7 - Py\chromedriver.exe"


# atualizando a preferência
prefs = {"download.default_directory": r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"}

# definindo que a nova preferência seja atualizada
options.add_experimental_option("prefs", prefs)


# definindo que o webdriver.chrome deve vir com as definições options
service = Service(executable_path=path_chrome)

# Inicialize o navegador com as opções e o serviço
nav = webdriver.Chrome(service=service, options=options)


# In[3]:


link = r'https://sgf-sp.bracell.com/sgf/'
login = 'gamoura'
password = 'Jupiter.09'
# mazimizando a janela
nav.maximize_window()
# abrindo site
nav.get(link)
sleep(2)
nav.find_element('xpath', '//*[@id="txtLogin"]').send_keys(login)
sleep(2)
nav.find_element('xpath', '//*[@id="txtSenha"]').send_keys(password)
sleep(2)
nav.find_element('xpath', '//*[@id="btnOk"]').click()
sleep(3)
nav.find_element('xpath', '//*[@id="imbModuloP3"]').click()
sleep(2)
element = WebDriverWait(nav, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="IcMessage"]/table/tbody/tr/td[2]/div/img')))
element.click()
sleep(2)
nav.find_element('xpath', '//*[@id="Menu1-menuItem005"]/div').click()
element1 = WebDriverWait(nav, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="Menu1-menuItem005-subMenu-menuItem011"]')))
element1.click()


# In[4]:


iframe = WebDriverWait(nav, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo"]')))
nav.switch_to.frame(iframe)


# In[5]:


hoje = datetime.datetime.now()
mes = hoje.month
ano = hoje.year
_, num_dias = calendar.monthrange(ano, mes)
max_dias = str(num_dias)
mes = "{:02d}".format(mes)

data_inicio = '01' + str(mes) + str(ano) + " 00" + "00"
data_fim = str(max_dias) + str(mes)+str(ano) + "23" + "59"


# In[6]:

sleep(5)

element2 = WebDriverWait(nav, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="ctl03_ctl01_ctl03_DataChegadaBalanca"]')))
element2.send_keys(data_inicio)

# In[7]:

sleep(5)


element3 = WebDriverWait(nav, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="ctl03_ctl01_ctl03_DataChegadaBalancaATE"]')))
element3.send_keys(data_fim)

sleep(5)

# In[8]:


element4 = WebDriverWait(nav, 10).until(EC.presence_of_element_located(
    (By.XPATH, ' //*[@id="VwCuboDadosGuiaCemDao"]/div/table/tbody/tr[2]/td[1]/a[1]/img')))
element4.click()
sleep(10)


# In[9]:


element5 = WebDriverWait(nav, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="VwCuboDadosGuiaCemDao"]/span/input[3]')))

element5.click()
sleep(20)


# In[10]:


nav.quit()


# In[11]:


path = r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"
arquivos = [os.path.join(path, arquivo) for arquivo in os.listdir(path)]
arquivo_mais_recente = max(arquivos, key=os.path.getctime)


# In[12]:


if arquivo_mais_recente.endswith('.zip'):
    with zf.ZipFile(arquivo_mais_recente, "r") as z:
        z.extractall(path)
    os.remove(arquivo_mais_recente)


# In[13]:


directory_path = 'F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados'

for file_name in os.listdir(directory_path):
    if 'gamoura' in file_name:
        file_path = os.path.join(directory_path, file_name)


# In[14]:


# Defina o locale correto para o seu sistema operacional
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Carregue a tabela HTML e especifique o locale
tabela = pd.read_html(file_path, decimal=',',
                      thousands='.', header=0, index_col=False)[0]


# In[15]:


caminho_sgf = 'F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados/SGF_export {}.{}.xlsx'.format(
    mes, ano)
sgf_export = tabela.to_excel(caminho_sgf, index=False)
os.remove(file_path)


# In[16]:


# Ler o arquivo original
sgf = pd.read_excel(caminho_sgf)
# Salvar em um novo arquivo com a nova aba
with pd.ExcelWriter('F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados/SGF_export {}.{}.xlsx'.format(mes, ano), engine='xlsxwriter') as writer:
    sgf.to_excel(writer, sheet_name='Export', index=False)


# In[17]:


df_sgf = pd.DataFrame()  # inicializa um dataframe vazio para armazenar a concatenação

for arquivos in os.listdir(directory_path):
    url = str(directory_path) + "/" + str(arquivos)
    if "SGF_export" in arquivos:
        concatenado = pd.read_excel(url)
        df_sgf = pd.concat([df_sgf, concatenado], axis=0, ignore_index=True)

df_sgf['Talhão'] = df_sgf.apply(lambda x: x['Quadra/Pilha Origem'][-3:] if pd.isnull(x['Talhão']) else x['Talhão'], axis=1)

df_sgf['Projeto'] = df_sgf.apply(lambda x: x['Quadra/Pilha Origem'].split("-")[1] if pd.isnull(x['Projeto']) else x['Projeto'], axis=1)

df_sgf['Id Projeto'] = df_sgf.apply(
    lambda x: 1094 if "caieiras" in x['Projeto'].lower()  else
    1110 if "piracema" in x['Projeto'].lower() else
    1109 if "guanabara" in x['Projeto'].lower() else x["Id Projeto"],
    axis=1
)
# In[18]:


df_sgf.to_excel(r"F:\Qualidade_Florestal\01- SÃO PAULO\04- Logística, transporte e estradas\00 - Bases de Trabalho\export_sgf_carregamento.xlsx", sheet_name="Export")
