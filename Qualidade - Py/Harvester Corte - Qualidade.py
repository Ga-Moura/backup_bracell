#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import shutil

import configparser
config = configparser.ConfigParser()
config.read('sets.conf')
cred = config['survey']


# Lista de diretórios
diretorios = [
    os.path.abspath(r"F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\feixe_attachments"),
    os.path.abspath(r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Avaliação - HV'),
]

for diretorio in diretorios:
    try:
        # Remove o diretório e todo o seu conteúdo
        shutil.rmtree(diretorio)
        print(f"Diretório {diretorio} e todo o seu conteúdo foram removidos com sucesso.")
    except Exception as e:
        print(f"Erro ao remover diretório {diretorio}: {e}")


# In[ ]:


import shutil
import arcgis
from arcgis.gis import GIS
import re, csv
import pandas as pd
# Define variables
portalURL = cred['portal']
username = cred['login']
password = cred['senha']
survey_item = cred['QLD_harvester_colheita']
save_path = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho'



keep_org_item = False
store_csv_w_attachments = False

# Connect to GIS Portal and identify Survey form
gis = GIS(portalURL, username, password)
survey_by_id = gis.content.get(survey_item)
print(survey_by_id.type)
survey_by_id

# Download service
rel_fs = survey_by_id.related_items('Survey2Service','forward')[0]
rel_fs

item_excel = rel_fs.export(title=survey_by_id.title, export_format='Excel')
item_excel.download(save_path=save_path)
if not bool(keep_org_item):
    item_excel.delete(force=True)

# Process feature layers and attachments
layers = rel_fs.layers + rel_fs.tables


# In[ ]:


import calendar
import datetime
hoje = datetime.datetime.now()
mes = hoje.month
ano = hoje.year
_,num_dias = calendar.monthrange(ano,mes)
max_dias = str(num_dias)
mes = "{:02d}".format(mes)

data_filtro = str(mes) +"-"+ str(ano)


time_delta = datetime.timedelta(days=30)

delta_rr = hoje - time_delta

mes_rr = delta_rr.month

ano_rr = delta_rr.year

mes_anterior = str(mes_rr) + "-"+str(ano_rr)


# In[ ]:


url_base_survey = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\QLD_harvester_colheita.xlsx'

base_survey = pd.read_excel(url_base_survey, sheet_name= 'QLD_harvester_colheita')

base_parcela = pd.read_excel(url_base_survey, sheet_name= 'parcela')

base_feixe = pd.read_excel(url_base_survey, sheet_name='feixe')



# In[ ]:


base_survey = base_survey[['objectid','uniquerowid','nivel_avaliacao','modulo_corte','fazenda','talhao','date_1']]
base_parcela = base_parcela[['objectid','parentrowid','uniquerowid', 'operador','cod_maquina']]
base_feixe = base_feixe[['objectid','parentrowid']]


# In[ ]:


base_survey = base_survey.rename({'objectid': 'objectid_avaliacao'}, axis=1)
base_survey['objectid'] = base_survey['objectid_avaliacao']

base_parcela = base_parcela.rename({'objectid':'objectid_parcela'}, axis=1)
base_parcela['objectid'] = base_parcela['objectid_parcela']

base_feixe = base_feixe.rename({'objectid':'objectid_feixe'},axis=1)
base_feixe['objectid'] = base_feixe['objectid_feixe']


# In[ ]:


base_download = base_parcela.copy()

base_download = base_download.merge(base_survey[['uniquerowid','nivel_avaliacao','modulo_corte','fazenda','talhao','date_1']], left_on='parentrowid', right_on='uniquerowid', how= 'left')

base_download = base_download.merge(base_feixe[['objectid_feixe','parentrowid']], left_on='uniquerowid_x', right_on='parentrowid', how='left')


# In[ ]:


path_save = r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Bases de Apoio\cadastro_fotos_hv.xlsx'

base_download.to_excel(path_save,index=False)


# In[ ]:


base_download = base_download[['objectid_feixe','date_1']]

base_download['mes_ano'] = base_download['date_1'].dt.to_period('M')

base_download = base_download.loc[(base_download['mes_ano'] == data_filtro) | (base_download['mes_ano'] == mes_anterior)]

base_download_unique = base_download['objectid_feixe'].drop_duplicates()

base_download = base_download['objectid_feixe'].astype(int)

base_download = tuple(base_download_unique)


# In[ ]:


for i in layers:
    if i.properties.hasAttachments:
        print("Item: ", i, "HAS ATTACHMENTS")
        feature_layer_folder = os.path.join(save_path, '{}_attachments'.format(re.sub(r'[^A-Za-z0-9]+', '', i.properties.name)))
        if not os.path.exists(feature_layer_folder):
            os.mkdir(feature_layer_folder)         
        if bool(store_csv_w_attachments):
            path = os.path.join(feature_layer_folder, "{}_attachments.csv".format(i.properties.name))
        elif not bool(store_csv_w_attachments):
            path = os.path.join(save_path, "{}_attachments.csv".format(i.properties.name))
        csv_fields = ['Parent objectId','Attachment path']
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(csv_fields)
            feature_object_ids = i.query(where="1=1", return_ids_only=True, order_by_fields='objectid ASC')
            # Verificar se o ID atual está na lista de IDs da base_survey
            for j in feature_object_ids['objectIds']:
                current_oid = j
                if any(oid == current_oid for oid in base_download):
                    current_oid_attachments = i.attachments.get_list(current_oid)
                    if current_oid_attachments is not None and len(current_oid_attachments) > 0:
                        for k in range(len(current_oid_attachments)):
                            attachment_id = current_oid_attachments[k]['id']
                            global_id = str(current_oid)
                            current_attachment_path = i.attachments.download(oid=current_oid, attachment_id=attachment_id, save_path=feature_layer_folder)
                            if current_attachment_path is not None:
                                new_attachment_path = os.path.join(feature_layer_folder, global_id + "-" + os.path.split(current_attachment_path[0])[1])
                                shutil.move(current_attachment_path[0], new_attachment_path)
                                csvwriter.writerow([current_oid, os.path.join('{}_attachments'.format(re.sub(r'[^A-Za-z0-9]+', '', i.properties.name)), os.path.split(new_attachment_path)[1])])
                            else:
                                print("Item with ID:", current_oid, "DOES NOT HAVE ATTACHMENTS")
                else:
                    print("Item with ID:", current_oid, "is not in the base_survey and will be skipped.")


# In[ ]:


parcelas = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\feixe_attachments'
avaliacao_hv = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Avaliação - HV'

os.rename(parcelas,avaliacao_hv)

