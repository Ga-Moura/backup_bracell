#!/usr/bin/env python
# coding: utf-8

# In[6]:


import imghdr
import shutil
import arcgis
from arcgis.gis import GIS
import re
import csv
import pandas as pd
import os
# Define variables
portalURL = r'https://gissp.bracell.com/portal/'
username = "Qualidade_Florestal"
password = "Qualidade@24"
survey_item_id = "650bc0e5ac424603a61c90eef694999e"
save_path = r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\00 - Base de Dados"


# In[7]:


# Deleta os arquivos existentes na pasta de imagens para não dar erro ao salvar
caminho_completo = os.path.abspath(
    r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\00 - Base de Dados\iniciofotos_attachments")
for arquivo in os.listdir(caminho_completo):
    caminho_arquivo = os.path.join(caminho_completo, arquivo)
    try:
        os.remove(caminho_arquivo)
    except OSError as e:
        print(f"Erro ao deletar arquivo {arquivo}: {e}")


# In[8]:


keep_org_item = False
store_csv_w_attachments = False

# Connect to GIS Portal and identify Survey form
gis = GIS(portalURL, username, password)
survey_by_id = gis.content.get(survey_item_id)
print(survey_by_id.type)
survey_by_id

# Download service
rel_fs = survey_by_id.related_items('Survey2Service', 'forward')[0]
rel_fs

item_excel = rel_fs.export(title=survey_by_id.title, export_format='Excel')
item_excel.download(save_path=save_path)
if not bool(keep_org_item):
    item_excel.delete(force=True)


# In[9]:


# Process feature layers and attachments
layers = rel_fs.layers + rel_fs.tables
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
            for j in range(len(feature_object_ids['objectIds'])):
                current_oid = feature_object_ids['objectIds'][j]
                current_oid_attachments = i.attachments.get_list(current_oid)
                if current_oid_attachments is not None and len(current_oid_attachments) > 0:
                    for k in range(len(current_oid_attachments)):
                        attachment_id = current_oid_attachments[k]['id']
                        global_id = str(i.query(where="1=1", return_geometry=False,
                                        return_ids_only=True, order_by_fields='objectid ASC')['objectIds'][j])
                        current_attachment_path = i.attachments.download(
                            oid=current_oid, attachment_id=attachment_id, save_path=feature_layer_folder)
                        if current_attachment_path is not None:
                            new_attachment_path = os.path.join(
                                feature_layer_folder, global_id + "_" + os.path.split(current_attachment_path[0])[1])
                            shutil.move(
                                current_attachment_path[0], new_attachment_path)
                            csvwriter.writerow([current_oid, os.path.join('{}_attachments'.format(re.sub(
                                r'[^A-Za-z0-9]+', '', i.properties.name)), os.path.split(new_attachment_path)[1])])
                        else:
                            print("Item: ", i, "DOES NOT HAVE ATTACHMENTS")
print('Done!')


# Ao final, as mensagens indicarão as respostas dos formulários que não tem foto e quando tiver concluído.


# In[10]:


tabela = pd.read_excel(
    r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\00 - Base de Dados\Produção_Segundo_Nível.xlsx")

caminho_completo = os.path.abspath(
    r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\00 - Base de Dados\iniciofotos_attachments")

for imagem in os.listdir(caminho_completo):
    if imghdr.what(os.path.join(caminho_completo, imagem)):
        for index, objectid in enumerate(tabela["objectid"]):
            if str(objectid) == str(imagem).split("_")[0]:
                novo_nome = str(tabela["projeto"][index]) + " - " + str(tabela["talhao"]
                                                                        [index]) + " - " + str(tabela["equipe_equilibrio"][index]) + " - " + imagem
                novo_caminho = os.path.join(caminho_completo, novo_nome)
                os.rename(os.path.join(caminho_completo, imagem), novo_caminho)
                break
    else:
        print(f"O arquivo {imagem} não é uma imagem")


# %%


# url_base_survey = r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\00 - Base de Dados\Produção_Segundo_Nível.xlsx"
# base = pd.read_excel(url_base_survey)

# for index, row in base.iterrows():
#    if str(row['unidade']) == "MS" and str(row['projeto'])[0] == '2':
#        base.at[index, 'projeto'] = str("6" + str(row['projeto'])[-3:])
#    else:
#        base.at[index, 'projeto'] = str(row['projeto'])

# base.to_excel(url_base_survey, index=False)
