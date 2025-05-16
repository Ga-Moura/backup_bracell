#!/usr/bin/env python
# coding: utf-8

# In[396]:


import pandas as pd
import openpyxl as px
import os
import datetime as dt


# In[397]:


path_cadastro = r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\14 - Transformação digital\01 - Processamento de dados\Cadastro Florestal.xlsx'


# In[398]:


path_adubacao_cob = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_adubacao_de_cobertura.xlsx"


# In[399]:


path_formiga_dose = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_formiga_manual_dosagem.xlsx"


# In[400]:


path_formiga_acomp = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_formiga_manual_acompanhamento.xlsx"


# In[401]:


path_covas = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_marcacao_covas_manual.xlsx"


# In[402]:


path_desbrota = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_desbrota.xlsx"


# In[403]:


path_pulverizacao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_avaliacao_de_pulverizacao.xlsx"


# In[404]:


path_plantio = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_plantio_operacional.xlsx"


# In[405]:


path_precisao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_adubacao_precisao_e_pulverizacao.xlsx"


# In[406]:


path_irrigacao = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_irrigacao_silvicultura.xlsx"


# In[407]:


path_preparo = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_preparo_de_solo.xlsx"


# In[408]:


path_calcario = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_aplicacao_calcario.xlsx"


# In[409]:


path_cap_manual = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_capina_quimica_manual.xlsx'


# In[410]:


path_drone = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_pulverizacao_com_drone.xlsx'


# In[411]:


path_sobrevivencia = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_sobrevivencia_silvicultura.xlsx'


# In[412]:


path_de_para = r'\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\01 - Silvicultura\01- Base de dados\00 - Apontamento 2 nível produção\de_para - 2º Nível.xlsx'


# In[413]:


###Cadastro####

cadastro = pd.read_excel(path_cadastro)
cadastro['Talhão'] = cadastro['Talhão'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
cadastro['Id Projeto'] = cadastro['Id Projeto'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
cadastro["Projeto e Talhão"] = cadastro['Id Projeto']+ cadastro['Talhão']
cadastro = cadastro[['Projeto e Talhão','Projeto','Área(ha)']]


# In[414]:


###Adubação e Pulverização de Precisão###

adb_precisao = pd.read_excel(path_precisao)

adb_precisao['id_talhao'] = adb_precisao['id_talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
adb_precisao['fazenda'] = adb_precisao['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
adb_precisao['operacao'] = "Adubação & Pulverização de Precisão (Preparo de solo)"
adb_precisao['maquina'] = adb_precisao.apply(lambda x: x['outro_trator'] if x['trator'] == 'Outro' else x['trator'], axis = 1) 
adb_precisao['Avaliação realizada'] = 'SILVICULTURA'
adb_precisao = adb_precisao[['fazenda', 'id_talhao','objectid', 'data_avaliacao', 'regiao', 'nivel', 'equipe', 'equipe_equilibrio','houve_acompanhamento', 'maquina','operacao','Avaliação realizada']]
adb_precisao = adb_precisao.rename(columns={'data_avaliacao': 'data'})


# In[415]:


###Adubação de Cobertura###

adb_cob = pd.read_excel(path_adubacao_cob)
adb_cob['equipe'] = adb_cob.apply(lambda x: x['equipe_ms'] if pd.isnull(x['equipe_sp']) else x['equipe_sp'],axis=1)
adb_cob['id_talhao'] = adb_cob['id_talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
adb_cob['fazenda'] = adb_cob['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
adb_cob['operacao'] = "Adubação de Cobertura"
adb_cob['Avaliação realizada'] = 'SILVICULTURA'
adb_cob = adb_cob.rename({'trator':'maquina'},axis=1)
adb_cob = adb_cob[['fazenda','id_talhao','objectid' ,'data','regiao','nivel','equipe','equipe_equilibrio','acompanhamento','operacao', 'maquina','Avaliação realizada']]
adb_cob = adb_cob.rename(columns={'acompanhamento': 'houve_acompanhamento'})

#DF duplicado para manter duas bases, uma de produção e outra de apontamentos
adb_cob_silv = adb_cob.copy()

#gerar uma base cópia para criar um novo DF com as informações duplicadas

#dropar colunas duplicadas
#chave: objeto de locacao; operacao; equipe; mes operacional; maquina
adb_cob = adb_cob.query('nivel == "2° Nível"') 
adb_cob = adb_cob.sort_values(['data'])
adb_cob = adb_cob.drop_duplicates(subset=['fazenda','id_talhao','operacao'], keep= 'first')


# In[416]:


###Formiga Dose###
form_dose = pd.read_excel(path_formiga_dose,sheet_name='Formiga_Manual_Dosagem')
form_dose['talhao'] = form_dose['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
form_dose['fazenda'] = form_dose['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
form_dose['operacao'] = "Formiga Manual (somente dosagem)"
form_dose['maquina'] = None
form_dose['Avaliação realizada'] = 'SILVICULTURA'
form_dose = form_dose[['fazenda', 'talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao', 'maquina','Avaliação realizada']]
form_dose = form_dose.rename(columns={'talhao':'id_talhao'})


# In[417]:


###Formiga Acompanhamento###
form_acmp = pd.read_excel(path_formiga_acomp,sheet_name='QLD_formiga_manual_acompanhamen')
form_acmp['talhao'] = form_acmp['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
form_acmp['fazenda'] = form_acmp['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
form_acmp['operacao'] = "Formiga Manual & Operacional"
form_acmp['maquina'] = None
form_acmp['Avaliação realizada'] = 'SILVICULTURA'
form_acmp = form_acmp[['fazenda', 'talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','maquina','Avaliação realizada']]
form_acmp = form_acmp.rename(columns={'talhao':'id_talhao'})


# In[418]:


###Irrigação###
irrig = pd.read_excel(path_irrigacao, sheet_name= 'QLD_irrigacao_silvicultura')
irrig['id_talhao'] = irrig['id_talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
irrig['fazenda'] = irrig['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
irrig['equipe'] = irrig.apply(lambda x: x['equipe_ms'] if pd.isnull(x['equipe_sp']) else x['equipe_sp'],axis=1)
irrig['operacao'] = 'Irrigação' 
irrig = irrig.rename({'trator':'maquina'},axis=1)
irrig['Avaliação realizada'] = 'SILVICULTURA'
irrig_silv = irrig.copy()
irrig_silv = irrig_silv[['fazenda', 'id_talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','acompanhamento','operacao','maquina','Avaliação realizada']]
irrig_silv = irrig_silv.rename(columns={'acompanhamento':'houve_acompanhamento'})

#Chave, fazenda, Talhão e sequencia - Removendo duplicatas e mantendo o primeiro apontamento
#Devido a sequencia de operação
irrig = irrig.query('nivel == "2° Nível"')
irrig = irrig.sort_values(['data'])
irrig = irrig.drop_duplicates(['fazenda','id_talhao','sequencia'], keep='first')

irrig = irrig[['fazenda', 'id_talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','acompanhamento','operacao','maquina','Avaliação realizada']]
irrig = irrig.rename(columns={'acompanhamento':'houve_acompanhamento'})


# In[419]:


###Plantio###
plantio = pd.read_excel(path_plantio, sheet_name='QLD_plantio_operacional')
plantio['talhao'] = plantio['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
plantio['fazenda'] = plantio['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
plantio['operacao'] = 'Plantio'
plantio['maquina'] = None
plantio['Avaliação realizada'] = 'SILVICULTURA'
plantio = plantio[['fazenda', 'talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','maquina','Avaliação realizada']]
plantio = plantio.rename(columns={'talhao': 'id_talhao'})


# In[420]:


###Pulverização###
pulv = pd.read_excel(path_pulverizacao, sheet_name='QLD_avaliacao_de_pulverizacao')
pulv['talhao'] = pulv['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
pulv['fazenda'] = pulv['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
pulv['operacao'] = 'Pulverização'
pulv = pulv.rename({'trator':'maquina'},axis=1)
pulv['Avaliação realizada'] = 'SILVICULTURA'

pulv_silv = pulv.copy()
pulv_silv = pulv_silv[['fazenda', 'talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','maquina','Avaliação realizada']]
pulv_silv = pulv_silv.rename(columns={'talhao': 'id_talhao'})

#Remover duplicatas da chave - fazenda, talhao, mês operacional
#Criando apenas chave para remover a duplicata
pulv['mes_operacional'] = pulv['data'].apply(lambda x: (
    (x + dt.timedelta(days=11)).replace(day=1)
).strftime('01/%m/%y') if x.day > 20 else (x.replace(day=1)).strftime('01/%m/%y'))


pulv = pulv.query('nivel == "2° Nível"')

pulv = pulv.sort_values('data')

pulv['chave'] = pulv['fazenda'] + pulv['talhao'] + pulv['mes_operacional']

pulv = pulv.drop_duplicates(['chave'],keep='first')

pulv = pulv[['fazenda', 'talhao', 'objectid', 'data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','maquina','Avaliação realizada']]
pulv = pulv.rename(columns={'talhao': 'id_talhao'})


# In[421]:


###Preparo de Solos e Savannah###
prep = pd.read_excel(path_preparo,sheet_name='QLD_preparo_de_solo')
prep['talhao'] = prep['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
prep['nome_fazenda'] = prep['nome_fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
prep['equipe'] = prep.apply(lambda x:x['equipe_ms'] if pd.isnull(x['equipe_sp']) else x['equipe_sp'],axis=1)
prep['operacao'] = 'Preparo de solo'
prep['Avaliação realizada'] = 'SILVICULTURA'
prep['maquina'] = prep.apply(lambda x: x['outro_trator'] if x['trator'] == 'outro' else x['trator'],axis = 1)
prep = prep[['nome_fazenda', 'talhao', 'objectid', 'datahoje','regiao','nivel','equipe','equipe_equilibrio','acompanhamento','operacao', 'maquina','Avaliação realizada']]
prep = prep.rename(columns={'datahoje':'data', 'nome_fazenda': 'fazenda', 'acompanhamento': 'houve_acompanhamento', 'talhao':'id_talhao'})


# In[422]:


###Desbrota###
desb = pd.read_excel(path_desbrota,sheet_name='QLD_desbrota')
desb['talhao'] = desb['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
desb['fazenda'] = desb['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
desb['operacao'] = 'Desbrota'
desb['maquina'] = None
desb['Avaliação realizada'] = 'SILVICULTURA'
desb = desb[['fazenda','talhao','objectid','data','regiao', 'nivel','equipe','equipe_equilibrio', 'houve_acompanhamento','operacao','maquina','Avaliação realizada']]
desb = desb.rename(columns={'talhao':'id_talhao'})


# In[423]:


###Marcação de Covas###
marc = pd.read_excel(path_covas, sheet_name='QLD_marcacao_covas_manual')
marc['talhao'] = marc['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
marc['fazenda'] = marc['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
marc['operacao'] = 'Marcação de Covas'
marc['maquina'] = None
marc['Avaliação realizada'] = 'SILVICULTURA'
marc = marc[['fazenda','talhao','objectid','data','regiao', 'nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao', 'maquina','Avaliação realizada']]
marc = marc.rename(columns={'talhao':'id_talhao'})


# In[424]:


###calcário###

calc = pd.read_excel(path_calcario,sheet_name='QLD_aplicacao_calcario')
calc['talhao'] = calc['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
calc['fazenda'] = calc['fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
calc['operacao'] = 'Calcário'
calc['Avaliação realizada'] = 'SILVICULTURA'
calc = calc.rename({'trator' : 'maquina'}, axis=1)
calc = calc[['fazenda','talhao','objectid','data','regiao', 'nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao', 'maquina', 'Avaliação realizada']]
calc = calc.rename(columns={'talhao':'id_talhao'})


# In[425]:


###Capina Quimica Manual###

cap_man = pd.read_excel(path_cap_manual, sheet_name='QLD_capina_quimica_manual')
cap_man['talhao'] = cap_man['talhao'].fillna('').astype(str).str.split(".").str[0].str.zfill(3)
cap_man['fazenda'] = cap_man['fazenda'].fillna('').astype(str).str.split(".").str[0].str.zfill(4)
cap_man['operacao'] = 'Capina Química Manual'
cap_man['maquina'] = None
cap_man['Avaliação realizada'] = 'SILVICULTURA'
cap_man = cap_man[['fazenda','talhao','objectid','data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao', 'maquina', 'Avaliação realizada']]
cap_man = cap_man.rename(columns={'talhao':'id_talhao'})
#Não foi adicionado a Prod_silv por não ter apontamentos o suficiente


# In[426]:


###Pulverização com Drone###

drone = pd.read_excel(path_drone,sheet_name='QLD_pulverizacao_com_drone')
drone['talhao'] = drone['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
drone['fazenda'] = drone['fazenda'].fillna('').astype(str).str.split(".").str[0].str.zfill(4)
drone['operacao'] = "Pulverização com Drone"
drone['maquina'] = None
drone['Avaliação realizada'] =  'SILVICULTURA'
drone = drone[['fazenda','talhao','objectid','data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','maquina','Avaliação realizada']]
drone = drone.rename(columns={'talhao':'id_talhao'})

#Não foi adicionado a Prod_silv por não ter apontamentos o suficiente


# In[427]:


sobrevivencia = pd.read_excel(path_sobrevivencia,sheet_name='QLD_sobrevivencia_silvicultura')
sobrevivencia['talhao'] = sobrevivencia['talhao'].fillna('').astype(str).str.split('.').str[0].str.zfill(3)
sobrevivencia['nome_fazenda'] = sobrevivencia['nome_fazenda'].fillna('').astype(str).str.split('.').str[0].str.zfill(4)
sobrevivencia['operacao'] = 'Sobrevivência'
sobrevivencia['Avaliação realizada'] = 'SOBREVIVÊNCIA'
sobrevivencia = sobrevivencia.rename({'nome_fazenda':'fazenda','datahoje':'data', 'acompanhamento':'houve_acompanhamento','talhao':'id_talhao'},axis=1)
sobrevivencia = sobrevivencia[['fazenda','id_talhao','objectid','data','regiao','nivel','equipe','equipe_equilibrio','houve_acompanhamento','operacao','Avaliação realizada','descarte','motivo_descarte','avaliacao']]
sobrevivencia['nivel'] = sobrevivencia['nivel'].replace({'2º Nível':'2° Nível'})


# In[428]:


###Juntando todas as bases - Produção Silvicultura###

prod_2n = [prep,calc, marc, desb, pulv, plantio, irrig, form_acmp, form_dose, adb_precisao, adb_cob,sobrevivencia]

prod_2n = pd.concat(prod_2n, ignore_index=True)

prod_2n['fazenda'] = prod_2n.apply(lambda x: "6"+x['fazenda'][-3:] if x['regiao'] == "MS" and x['fazenda'][0] == "2" else x['fazenda'] , axis = 1)

prod_2n['objeto de locacao'] = prod_2n['fazenda']+prod_2n['id_talhao']

prod_2n['data'] = pd.to_datetime(prod_2n['data'], format='%d/%m/%y')

prod_2n['mes_operacional'] = prod_2n['data'].apply(lambda x: (
    (x + dt.timedelta(days=11)).replace(day=1)
).strftime('01/%m/%y') if x.day > 20 else (x.replace(day=1)).strftime('01/%m/%y'))

prod_2n['nivel'] = prod_2n['nivel'].replace({'1º Nível':'1° Nível'})

prod_2n = prod_2n.merge(cadastro, left_on = 'objeto de locacao', right_on = 'Projeto e Talhão', how = 'left')

prod_2n = prod_2n.rename(columns = {'objectid':'Código de identificação', 'operacao': 'Operação', 'id_talhao': 'Talhão', 'regiao': 'Região', 'nivel': 'Nível', 'mes_operacional': 'Mês Operacional'})

prod_2n = prod_2n.drop('Projeto e Talhão', axis=1)

prod_2n['week'] = prod_2n['data'].apply(lambda x: str(x.isocalendar()[1]) + " - " + str(x.strftime('%b')))

###Filtro para apenas segundo nível e regiã SP###

prod_2n = prod_2n.query("""Nível == '2° Nível'""")

prod_2n = prod_2n.query("""Região == 'SP' """)


# In[429]:


### De para - 2º Nível###

de_para_empresa = pd.read_excel(path_de_para, sheet_name="empresa_servico")
de_para_empresa = de_para_empresa[['de_empresa','para_empresa']]


de_para_equipe_avl = pd.read_excel(path_de_para,sheet_name='equipe_avaliadora')
de_para_equipe_avl = de_para_equipe_avl[['de_equipe','para_equipe']]


de_para_operacao = pd.read_excel(path_de_para, sheet_name='operacao')
de_para_operacao = de_para_operacao[['de_operacao','para_operacao']]


prod_2n = prod_2n.merge(de_para_operacao[['para_operacao','de_operacao']], left_on='Operação', right_on='de_operacao', how='left').drop(columns=['de_operacao'],axis=1)
prod_2n = prod_2n.merge(de_para_empresa[['para_empresa','de_empresa']], left_on='equipe', right_on='de_empresa', how='left').drop(columns=['de_empresa'],axis=1)
prod_2n = prod_2n.merge(de_para_equipe_avl[['de_equipe','para_equipe']], left_on='equipe_equilibrio', right_on='de_equipe',how='left').drop(columns=['de_equipe'],axis=1)


# In[430]:


#Apenas para ver os apontamentos duplicados
#Apenas  

prod_op = prod_2n.groupby(by = ['objeto de locacao', 'Operação', 'equipe', 'Mês Operacional','maquina']).size().reset_index(name = 'nº de avaliações')


# In[431]:


path_producao_2n =r'F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\01 - Silvicultura\01- Base de dados\00 - Apontamento 2 nível produção\Apontamentos de Produção 2°Nível.xlsx'

prod_2n.to_excel(path_producao_2n, index= False)


# In[432]:


###Juntando todas as bases - Produção Silvicultura###

#Bases: irrig_silv; adb_cob_silv; pulv_silv

prod_silv = [prep,calc, marc, desb, pulv_silv, plantio, irrig_silv, form_acmp, form_dose, adb_precisao, adb_cob_silv,sobrevivencia]

prod_silv = pd.concat(prod_silv, ignore_index=True)

prod_silv['fazenda'] = prod_silv.apply(lambda x: "6"+x['fazenda'][-3:] if x['regiao'] == "MS" and x['fazenda'][0] == "2" else x['fazenda'] , axis = 1)

prod_silv['objeto de locacao'] = prod_silv['fazenda']+prod_silv['id_talhao']

prod_silv['data'] = pd.to_datetime(prod_silv['data'], format='%d/%m/%y')

prod_silv['mes_operacional'] = prod_silv['data'].apply(lambda x: (
    (x + dt.timedelta(days=11)).replace(day=1)
).strftime('01/%m/%y') if x.day > 20 else (x.replace(day=1)).strftime('01/%m/%y'))

prod_silv['nivel'] = prod_silv['nivel'].replace({'1º Nível':'1° Nível'})

prod_silv = prod_silv.merge(cadastro, left_on = 'objeto de locacao', right_on = 'Projeto e Talhão', how = 'left')

prod_silv = prod_silv.rename(columns = {'objectid':'Código de identificação', 'operacao': 'Operação', 'id_talhao': 'Talhão', 'regiao': 'Região', 'nivel': 'Nível', 'mes_operacional': 'Mês Operacional'})

prod_silv = prod_silv.drop('Projeto e Talhão', axis=1)

prod_silv['week'] = prod_silv['data'].apply(lambda x: str(x.isocalendar()[1]) + " - " + str(x.strftime('%b')))

###Filtro para apenas segundo nível e regiã SP###

prod_silv = prod_silv.query("""Nível == '2° Nível'""")


# In[433]:


path_save =r'F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\01 - Silvicultura\01- Base de dados\00 - Apontamento 2 nível produção\Apontamentos de Silvicultura 2°Nível.xlsx'

prod_silv.to_excel(path_save, index = False)

