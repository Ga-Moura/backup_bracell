#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Deleta os arquivos existentes na pasta de imagens para não dar erro ao salvar
import os
caminho_completo = os.path.abspath(r"F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\QLDsujidadedepilhacolheita_attachments")
for arquivo in os.listdir(caminho_completo):
    caminho_arquivo = os.path.join(caminho_completo, arquivo)
    try:
       os.remove(caminho_arquivo)
    except OSError as e:
        print(f"Erro ao deletar arquivo {arquivo}: {e}")


# In[2]:


import shutil
import arcgis
from arcgis.gis import GIS
import re, csv
import pandas as pd
import os
import configparser
config = configparser.ConfigParser()
config.read('sets.conf')
cred = config['survey']


# Define variables
portalURL = cred['portal']
username = cred['login']
password = cred['senha']
survey_item = cred['QLD_sujidade_de_pilha_colheita']
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


# In[3]:


import calendar
import datetime
hoje = datetime.datetime.now()
mes = hoje.month
ano = hoje.year
_,num_dias = calendar.monthrange(ano,mes)
max_dias = str(num_dias)
mes = "{:02d}".format(mes)

data_filtro = str(mes) +"-"+ str(ano)





# In[4]:


time_delta = datetime.timedelta(days=30)

delta_rr = hoje - time_delta

mes_rr = delta_rr.month

ano_rr = delta_rr.year

mes_rr = "{:02d}".format(mes_rr)

mes_anterior = str(mes_rr) + "-"+str(ano_rr)


# In[5]:


url_base_survey = r'F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\QLD_sujidade_de_pilha_colheita.xlsx'

base_survey = pd.read_excel(url_base_survey)

base_survey = base_survey[['objectid','datacoleta']]

base_survey['mes_ano'] = base_survey['datacoleta'].dt.to_period('M')

base_survey = base_survey.loc[(base_survey['mes_ano'] == data_filtro) | (base_survey['mes_ano'] == mes_anterior)]

base_survey = base_survey['objectid'].astype(int)

base_survey = tuple(base_survey)


# In[6]:


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
                if any(oid == current_oid for oid in base_survey):
                    current_oid_attachments = i.attachments.get_list(current_oid)
                    if current_oid_attachments is not None and len(current_oid_attachments) > 0:
                        for k in range(len(current_oid_attachments)):
                            attachment_id = current_oid_attachments[k]['id']
                            global_id = str(current_oid)
                            current_attachment_path = i.attachments.download(oid=current_oid, attachment_id=attachment_id, save_path=feature_layer_folder)
                            if current_attachment_path is not None:
                                new_attachment_path = os.path.join(feature_layer_folder, global_id + "_" + os.path.split(current_attachment_path[0])[1])
                                shutil.move(current_attachment_path[0], new_attachment_path)
                                csvwriter.writerow([current_oid, os.path.join('{}_attachments'.format(re.sub(r'[^A-Za-z0-9]+', '', i.properties.name)), os.path.split(new_attachment_path)[1])])
                            else:
                                print("Item with ID:", current_oid, "DOES NOT HAVE ATTACHMENTS")
                else:
                    print("Item with ID:", current_oid, "is not in the base_survey and will be skipped.")

