#!/usr/bin/env python
# coding: utf-8

# In[22]:


import locale
import selenium
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


# In[23]:


# criando o web driver
options = webdriver.ChromeOptions()

#path chomedriver 
path_chrome =r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\7 - Py\chromedriver.exe"

# Definir o diretório de download padrão
prefs = {"download.default_directory": r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"}
options.add_experimental_option("prefs", prefs)

# definindo que o webdriver.chrome deve vir com as definições options
service = Service(executable_path=path_chrome)

# Inicialize o navegador com as opções e o serviço
nav = webdriver.Chrome(service=service, options=options)





# In[24]:


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
nav.find_element('xpath', '//*[@id="imbModuloC1"]').click()
sleep(2)


# In[25]:


# foi necessário abrir um menu secundário para poder clicar no ambiente do cadastro localização>Operacional>Uso do solo

menu_locator = (By.XPATH, '//*[@id="Menu1-menuItem000"]/div')
menu = WebDriverWait(nav, 5).until(
    EC.presence_of_element_located(menu_locator))

# move o cursor do mouse para o menu principal
ActionChains(nav).move_to_element(menu).perform()

# espera o submenu ser exibido
submenu_locator = (
    By.XPATH, '//*[@id="Menu1-menuItem000-subMenu-menuItem000"]')
submenu = WebDriverWait(nav, 5).until(
    EC.visibility_of_element_located(submenu_locator))

# move o cursor do mouse para o menu principal
ActionChains(nav).move_to_element(submenu).perform()

# espera o submenu2 a ser exibido
submenu_locator2 = (
    By.XPATH, '//*[@id="Menu1-menuItem000-subMenu-menuItem000-subMenu-menuItem002"]')
submenu2 = WebDriverWait(nav, 5).until(
    EC.visibility_of_element_located(submenu_locator2))

# clica no submenu
submenu2.click()
sleep(4)


# In[26]:


# Mudar para o contexto do iframe
# o Item estava dentro de um iframe e por isso não era possível baixar, foi necessário pegar o id do Iframe e usar o formato switch_to.frame e utilizar o xpath do iframe

iframe = WebDriverWait(nav, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo"]')))
nav.switch_to.frame(iframe)

# Aguarda até que o elemento com o título 'Exportar dados para Excel' seja visível na página
element = WebDriverWait(nav, 10).until(EC.visibility_of_element_located(
    (By.XPATH, "//input[@type='image'][@title='Exportar dados para Excel']")))

# Clica no elemento
element.click()

# Retorna para o contexto padrão (fora do iframe)
nav.switch_to.default_content()

sleep(20)
nav.quit()


# In[27]:


path = r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"
arquivos = [os.path.join(path, arquivo) for arquivo in os.listdir(path)]
arquivo_mais_recente = max(arquivos, key=os.path.getctime)


# In[28]:


with zf.ZipFile(arquivo_mais_recente, "r") as z:
    z.extractall(path)


# In[29]:


os.remove(arquivo_mais_recente)


# In[30]:


directory_path = r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados"

for file_name in os.listdir(directory_path):
    if 'gamoura' in file_name:
        file_path = os.path.join(directory_path, file_name)


# In[31]:


# Defina o locale correto para o seu sistema operacional
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# Carregue a tabela HTML e especifique o locale
tabela = pd.read_html(file_path, decimal=',',
                      thousands='.', header=0, index_col=False)[0]


# In[32]:


caminho_cadastro = r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados/Cadastro Florestal.xlsx'
cadastro = tabela.to_excel(caminho_cadastro, index=False)


# In[33]:


os.remove(file_path)


# In[34]:


# Ler o arquivo original
cadastro_excel = pd.read_excel(r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados/Cadastro Florestal.xlsx', dtype={' 25': float, ' 26': float})

# Tratar a coluna 'Talhão'
cadastro_excel['Talhão'] = cadastro_excel['Talhão'].fillna('').astype(str).str.zfill(3)

# Tratar a coluna 'Id Projeto'
cadastro_excel['Id Projeto'] = cadastro_excel['Id Projeto'].fillna('').astype(str).str.zfill(4)

# Criar a coluna 'Projeto e Talhão'
cadastro_excel["Projeto e Talhão"] = cadastro_excel['Id Projeto'] + cadastro_excel['Talhão']
# In[37]:


# Salvar em um novo arquivo com a nova aba
with pd.ExcelWriter(r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados/Cadastro Florestal.xlsx', engine='xlsxwriter') as writer:
    cadastro_excel.to_excel(writer, sheet_name='Export', index=False)


# In[38]:


caminho_destino = r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\14 - Cadastro Florestal"
shutil.copy(caminho_cadastro, caminho_destino)
