# %%
import os
os.environ["KRB5_CONFIG"] = "NUL"


import arcgis
from arcgis.gis import GIS
import pandas as pd
import locale
import traceback

# %%
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

# %%
#path premissas 
path_premissas = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Consulta\01. Programacoes e Controles\009. Índice de Padronização do Prestador - IPP\04_Automação Export\premissas_dowload_survey.xlsx'

# %%
#login

portal_url = pd.read_excel(path_premissas, sheet_name='login')

portal_url = portal_url[portal_url['Nome Parâmetro'] == 'portal_url']

portal_url = portal_url['Parâmetro'].iloc[0]

# %%
#username

username = pd.read_excel(path_premissas, sheet_name='login')

username = username[username['Nome Parâmetro'] == 'username']

username = username['Parâmetro'].iloc[0]

# %%
#Password

password = pd.read_excel(path_premissas, sheet_name='login')

password = password[password['Nome Parâmetro'] == 'password']

password = password['Parâmetro'].iloc[0]


# %%
#local save

local_save = pd.read_excel(path_premissas, sheet_name='login')

local_save = local_save[local_save['Nome Parâmetro'] == 'local_save']

local_save = local_save['Parâmetro'].iloc[0]


# %%
# Define variables
portalURL = portal_url
username = username
password = password
save_path = local_save


# %%
#Lista de itens para download

list_itens = pd.read_excel(path_premissas, sheet_name='lista_download', usecols=['Id Formulário'])

# %%


def baixar_survey(survey_id):
    keep_org_item = False
    try:
        gis = GIS(portalURL, username, password)
        survey_by_id = gis.content.get(survey_id)
        print(survey_by_id.title)
        
        rel_fs = survey_by_id.related_items('Survey2Service', 'forward')[0]
        item_excel = rel_fs.export(title=survey_by_id.title, export_format='Excel')
        item_excel.download(save_path=save_path)
        
        if not keep_org_item:
            item_excel.delete(force=True)

    except Exception as e:
        print("Tivemos problemas ao baixar o survey:", survey_id)
        print("Erro:", e)
        traceback.print_exc()

# %%
for i in list_itens['Id Formulário']:
    baixar_survey(i)


