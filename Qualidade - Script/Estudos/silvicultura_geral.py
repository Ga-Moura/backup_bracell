# In[447]:
import pandas as pd
import openpyxl as px
import os
import datetime as dt


# In[448]:


path_cadastro = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Cadastro Florestal.xlsx'


# In[449]:


path_adubacao_cob = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Adubação_de_Cobertura_-_Silvicultura.xlsx"


# In[450]:


path_formiga_dose = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Formiga_Manual_Dosagem.xlsx"


# In[451]:


path_formiga_acomp = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Formiga_Manual_Acompanhamento.xlsx"


# In[452]:


path_covas = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Avaliação_de_Marcação_de_Covas_Manual.xlsx"


# In[453]:


path_desbrota = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Desbrota.xlsx"


# In[454]:


path_pulverizacao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Avaliação_de_Pulverização.xlsx"


# In[455]:


path_plantio = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Plantio_Operacional.xlsx"


# In[456]:


path_precisao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Adubação_de_Precisão_e_Pulverização.xlsx"


# In[457]:


path_irrigacao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Irrigação_-_Silvicultura.xlsx"


# In[458]:


path_preparo = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Qualidade_de_Preparo_de_Solo.xlsx"


# In[459]:


path_calcario = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Calcário.xlsx"


# In[460]:


cadastro = pd.read_excel(path_cadastro)
cadastro.loc[:, 'Talhão'] = cadastro['Talhão'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
cadastro.loc[:, 'Id Projeto'] = cadastro['Id Projeto'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
cadastro["Projeto e Talhão"] = cadastro['Id Projeto'] + cadastro['Talhão']
cadastro = cadastro[['Projeto e Talhão', 'Projeto', 'Área(ha)']]


# In[461]:


### Adubação e Pulverização de Precisão###

adb_precisao = pd.read_excel(path_precisao)
adb_precisao = adb_precisao[['fazenda', 'id_talhao', 'objectid', 'data_avaliacao',
                             'regiao', 'nivel', 'equipe', 'equipe_equilibrio', 'houve_acompanhamento']]
adb_precisao['id_talhao'] = adb_precisao['id_talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
adb_precisao['fazenda'] = adb_precisao['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
adb_precisao['operacao'] = "Adubação & Pulverização de Precisão (Preparo de solo)"
adb_precisao = adb_precisao.rename(columns={'data_avaliacao': 'data'})


# In[462]:


### Adubação de Cobertura###

adb_cob = pd.read_excel(path_adubacao_cob)
adb_cob['equipe'] = adb_cob.apply(lambda x: x['equipe_ms'] if pd.isnull(
    x['equipe_sp']) else x['equipe_sp'], axis=1)
adb_cob['id_talhao'] = adb_cob['id_talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
adb_cob['fazenda'] = adb_cob['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
adb_cob['operacao'] = "Adubação de Cobertura"
adb_cob = adb_cob[['fazenda', 'id_talhao', 'objectid', 'data', 'regiao',
                   'nivel', 'equipe', 'equipe_equilibrio', 'acompanhamento', 'operacao']]
adb_cob = adb_cob.rename(columns={'acompanhamento': 'houve_acompanhamento'})


# In[463]:


### Formiga Dose###
form_dose = pd.read_excel(
    path_formiga_dose, sheet_name='Formiga_Manual_Dosagem')
form_dose['talhao'] = form_dose['talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
form_dose['fazenda'] = form_dose['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
form_dose['operacao'] = "Formiga Manual (somente dosagem)"
form_dose = form_dose[['fazenda', 'talhao', 'objectid', 'data', 'regiao',
                       'nivel', 'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
form_dose = form_dose.rename(columns={'talhao': 'id_talhao'})


# In[464]:


### Formiga Acompanhamento###
form_acmp = pd.read_excel(
    path_formiga_acomp, sheet_name='Formiga_Manual_Acompanhamento')
form_acmp['talhao'] = form_acmp['talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
form_acmp['fazenda'] = form_acmp['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
form_acmp['operacao'] = "Formiga Manual & Operacional"
form_acmp = form_acmp[['fazenda', 'talhao', 'objectid', 'data', 'regiao',
                       'nivel', 'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
form_acmp = form_acmp.rename(columns={'talhao': 'id_talhao'})


# In[465]:


### Irrigação###
irrig = pd.read_excel(path_irrigacao, sheet_name='Irrigacao___Silvicultura')
irrig['id_talhao'] = irrig['id_talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
irrig['fazenda'] = irrig['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
irrig['equipe'] = irrig.apply(lambda x: x['equipe_ms'] if pd.isnull(
    x['equipe_sp']) else x['equipe_sp'], axis=1)
irrig['operacao'] = 'Irrigação'
irrig = irrig[['fazenda', 'id_talhao', 'objectid', 'data', 'regiao',
               'nivel', 'equipe', 'equipe_equilibrio', 'acompanhamento', 'operacao']]
irrig = irrig.rename(columns={'acompanhamento': 'houve_acompanhamento'})


# In[466]:


### Plantio###
plantio = pd.read_excel(path_plantio, sheet_name='Plantio_Operacional')
plantio['talhao'] = plantio['talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
plantio['fazenda'] = plantio['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
plantio['operacao'] = 'Plantio operacional'
plantio = plantio[['fazenda', 'talhao', 'objectid', 'data', 'regiao',
                   'nivel', 'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
plantio = plantio.rename(columns={'talhao': 'id_talhao'})


# In[467]:


### Pulverização###
pulv = pd.read_excel(path_pulverizacao, sheet_name='Avaliacao_de_Pulverizacao')
pulv['talhao'] = pulv['talhao'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(3)
pulv['fazenda'] = pulv['fazenda'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(4)
pulv['operacao'] = 'Pulverização'
pulv = pulv[['fazenda', 'talhao', 'objectid', 'data', 'regiao', 'nivel',
             'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
pulv = pulv.rename(columns={'talhao': 'id_talhao'})


# In[468]:


### Preparo de Solos e Savannah###
prep = pd.read_excel(path_preparo, sheet_name='Qualidade_de_Preparo_de_Solo')
prep['talhao'] = prep['talhao'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(3)
prep['nome_fazenda'] = prep['nome_fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
prep['equipe'] = prep.apply(lambda x: x['equipe_ms'] if pd.isnull(
    x['equipe_sp']) else x['equipe_sp'], axis=1)
prep['operacao'] = 'Preparo de solo'
prep = prep[['nome_fazenda', 'talhao', 'objectid', 'datahoje', 'regiao',
             'nivel', 'equipe', 'equipe_equilibrio', 'acompanhamento', 'operacao']]
prep = prep.rename(columns={'datahoje': 'data', 'nome_fazenda': 'fazenda',
                   'acompanhamento': 'houve_acompanhamento', 'talhao': 'id_talhao'})


# In[469]:


### Desbrota###
desb = pd.read_excel(path_desbrota, sheet_name='Desbrota')
desb['talhao'] = desb['talhao'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(3)
desb['fazenda'] = desb['fazenda'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(4)
desb['operacao'] = 'Desbrota'
desb = desb[['fazenda', 'talhao', 'objectid', 'data', 'regiao', 'nivel',
             'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
desb = desb.rename(columns={'talhao': 'id_talhao'})


# In[470]:


### Marcação de Covas###
marc = pd.read_excel(path_covas, sheet_name='Marcacao_de_Covas_Manual')
marc['talhao'] = marc['talhao'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(3)
marc['fazenda'] = marc['fazenda'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(4)
marc['operacao'] = 'Marcação de Covas'
marc = marc[['fazenda', 'talhao', 'objectid', 'data', 'regiao', 'nivel',
             'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
marc = marc.rename(columns={'talhao': 'id_talhao'})


# In[471]:


### calcário###

calc = pd.read_excel(path_calcario, sheet_name='Calcario')
calc['talhao'] = calc['talhao'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(3)
calc['fazenda'] = calc['fazenda'].fillna('').astype(
    str).str.split('.').str[0].str.zfill(4)
calc['operacao'] = 'Calcário'
calc = calc[['fazenda', 'talhao', 'objectid', 'data', 'regiao', 'nivel',
             'equipe', 'equipe_equilibrio', 'houve_acompanhamento', 'operacao']]
calc = calc.rename(columns={'talhao': 'id_talhao'})


# In[472]:


### Juntando todas as bases - Produção Silvicultura###

prod_silv = [prep, calc, marc, desb, pulv, plantio,
             irrig, form_acmp, form_dose, adb_precisao, adb_cob]

prod_silv = pd.concat(prod_silv, ignore_index=True)

prod_silv['fazenda'] = prod_silv.apply(
    lambda x: "6"+x['fazenda'][-3:] if x['regiao'] == "MS" and x['fazenda'][0] == "2" else x['fazenda'], axis=1)

prod_silv['objeto de locacao'] = prod_silv['fazenda']+prod_silv['id_talhao']

prod_silv['data'] = pd.to_datetime(prod_silv['data'], format='%d/%m/%y')

prod_silv['mes_operacional'] = prod_silv['data'].apply(lambda x: (
    (x + dt.timedelta(days=11)).replace(day=1)
).strftime('01/%m/%y') if x.day > 20 else (x.replace(day=1)).strftime('01/%m/%y'))

prod_silv['nivel'] = prod_silv['nivel'].replace({'1º Nível': '1° Nível'})

prod_silv = prod_silv.merge(
    cadastro, left_on='objeto de locacao', right_on='Projeto e Talhão', how='left')

prod_silv = prod_silv.rename(columns={'objectid': 'Código de identificação', 'operacao': 'Operação',
                             'id_talhao': 'Talhão', 'regiao': 'Região', 'nivel': 'Nível', 'mes_operacional': 'Mês Operacional'})

prod_silv = prod_silv.drop('Projeto e Talhão', axis=1)


### Filtro para apenas segundo nível###

prod_silv = prod_silv.query("""Nível == '2° Nível'""")


# In[474]:


### Primeiro Save###
path_save = r'F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\01 - Silvicultura\01- Base de dados\00 - Apontamento 2 nível produção\Apontamentos de Silvicultura 2°Nível.xlsx'

prod_silv.to_excel(path_save, index=False)


### Segundo Save###
path_save2 = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Apontamentos de Silvicultura 2°Nível.xlsx'

prod_silv.to_excel(path_save2, index=False)
