#!/usr/bin/env python
# coding: utf-8

# In[7]:
import configparser
config = configparser.ConfigParser()
config.read('sets.conf')
cred = config['survey']



# Deleta os arquivos existentes na pasta de imagens para não dar erro ao salvar
import csv
import re
import datetime
import calendar
import pandas as pd
from arcgis.gis import GIS
import arcgis
import shutil
import os


caminho_completo = os.path.abspath(
    r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLDmarcacaocovasmanual_attachments")
for arquivo in os.listdir(caminho_completo):
    caminho_arquivo = os.path.join(caminho_completo, arquivo)
    try:
        os.remove(caminho_arquivo)
    except OSError as e:
        print(f"Erro ao deletar arquivo {arquivo}: {e}")


# In[8]:


# Define variables
portalURL = cred['portal']
username = cred['login']
password = cred['senha']
survey_item = cred['QLD_marcacao_covas_manual']
save_path = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys'


keep_org_item = False
store_csv_w_attachments = False

# Connect to GIS Portal and identify Survey form
gis = GIS(portalURL, username, password)
survey_by_id = gis.content.get(survey_item)
print(survey_by_id.type)
survey_by_id

# Download service
rel_fs = survey_by_id.related_items('Survey2Service', 'forward')[0]
rel_fs

item_excel = rel_fs.export(title=survey_by_id.title, export_format='Excel')
item_excel.download(save_path=save_path)
if not bool(keep_org_item):
    item_excel.delete(force=True)
layers = rel_fs.layers + rel_fs.tables


# In[9]:


hoje = datetime.datetime.now()
mes = hoje.month
ano = hoje.year
_, num_dias = calendar.monthrange(ano, mes)
max_dias = str(num_dias)
mes = "{:02d}".format(mes)

data_filtro = str(mes) + "-" + str(ano)


# In[10]:


url_base_survey = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_marcacao_covas_manual.xlsx'

base_survey = pd.read_excel(url_base_survey)

base_survey = base_survey[['objectid', 'data']]

base_survey['mes_ano'] = base_survey['data'].dt.to_period('M')

base_survey = base_survey.loc[base_survey['mes_ano'] == data_filtro]

base_survey = base_survey['objectid'].astype(int)

base_survey = tuple(base_survey)


# In[11]:


# Process feature layers and attachments
for i in layers:
    if i.properties.hasAttachments:
        print("Item: ", i, "HAS ATTACHMENTS")
        feature_layer_folder = os.path.join(save_path, '{}_attachments'.format(
            re.sub(r'[^A-Za-z0-9]+', '', i.properties.name)))
        if not os.path.exists(feature_layer_folder):
            os.mkdir(feature_layer_folder)
        if bool(store_csv_w_attachments):
            path = os.path.join(feature_layer_folder,
                                "{}_attachments.csv".format(i.properties.name))
        elif not bool(store_csv_w_attachments):
            path = os.path.join(
                save_path, "{}_attachments.csv".format(i.properties.name))
        csv_fields = ['Parent objectId', 'Attachment path']
        with open(path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(csv_fields)
            feature_object_ids = i.query(
                where="1=1", return_ids_only=True, order_by_fields='objectid ASC')
            # Verificar se o ID atual está na lista de IDs da base_survey
            for j in feature_object_ids['objectIds']:
                current_oid = j
                if any(oid == current_oid for oid in base_survey):
                    current_oid_attachments = i.attachments.get_list(
                        current_oid)
                    if current_oid_attachments is not None and len(current_oid_attachments) > 0:
                        for k in range(len(current_oid_attachments)):
                            attachment_id = current_oid_attachments[k]['id']
                            global_id = str(current_oid)
                            current_attachment_path = i.attachments.download(
                                oid=current_oid, attachment_id=attachment_id, save_path=feature_layer_folder)
                            if current_attachment_path is not None:
                                new_attachment_path = os.path.join(
                                    feature_layer_folder, global_id + "-" + os.path.split(current_attachment_path[0])[1])
                                shutil.move(
                                    current_attachment_path[0], new_attachment_path)
                                csvwriter.writerow([current_oid, os.path.join('{}_attachments'.format(re.sub(
                                    r'[^A-Za-z0-9]+', '', i.properties.name)), os.path.split(new_attachment_path)[1])])
                            else:
                                print("Item with ID:", current_oid,
                                      "DOES NOT HAVE ATTACHMENTS")
                else:
                    print("Item with ID:", current_oid,
                          "is not in the base_survey and will be skipped.")


# In[12]:


pasta_publica = r'U:\Publica\Florestal\Relatórios de Qualidade\Avaliações de 2º nível de Silvicultura\Bases Survey'

shutil.copy(url_base_survey, pasta_publica)
