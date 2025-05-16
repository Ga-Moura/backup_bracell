#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
import calendar
import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from matplotlib import pyplot as plt


# In[3]:


caminho_completo = os.path.abspath(
    r"F:/Qualidade_Florestal/01- SÃO PAULO/02- Silvicultura e Sobrevivência/00 - Arquivos Surveys/Arquivos PDF/Adubação de Cobertura")
for arquivo in os.listdir(caminho_completo):
    caminho_arquivo = os.path.join(caminho_completo, arquivo)
    try:
        os.remove(caminho_arquivo)
    except OSError as e:
        print(f"Erro ao deletar arquivo {arquivo}: {e}")



logo_bracel = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\2 - Modelagem\logo - Bracell.jpg'


# In[4]:


logo_msf = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\2 - Modelagem\logo msf jpg.jpg'


# In[5]:


foto_branco = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\2 - Modelagem\Imagem em Branco - Pdfs.png'


path = r"\\GLWFS02.lwart.net\LWC-FLORESTAL\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLDadubacaodecobertura_attachments"


# In[6]:


path_fotos = []
for i in os.listdir(path):
    fotos = os.path.join(path, i)
    path_fotos.append(fotos)

base_fotos = pd.DataFrame(path_fotos)
base_fotos = base_fotos.rename(columns={0: 'url'})


# In[7]:


base_fotos['nome_foto'] = base_fotos['url'].apply(lambda x: x.split("\\")[-1])
base_fotos['tipo'] = base_fotos['nome_foto'].apply(
    lambda x: x.split("-")[1] if len(x.split("-")) > 1 else None)
base_fotos['objectid'] = base_fotos['nome_foto'].apply(
    lambda x: x.split("-")[0] if len(x.split("-")) > 1 else -1).astype(int)
base_fotos = base_fotos.loc[base_fotos['objectid'].notna()]


# In[8]:


base_fotos_assinatura = base_fotos.loc[base_fotos['tipo'] == 'assinatura']
base_fotos_assinatura = base_fotos_assinatura.rename(
    columns={"tipo": "tipo_assinatura", 'url': 'url_assinatura'})

base_fotos_identificacao_maq = base_fotos.loc[base_fotos['tipo']
                                              == 'identificacao_maquina']
base_fotos_identificacao_maq = base_fotos_identificacao_maq.rename(
    columns={"tipo": "tipo_evidencia", 'url': 'url_identificacao_maquina'})

base_fotos_local_coleta = base_fotos.loc[base_fotos['tipo'] == 'local_coleta']
base_fotos_local_coleta = base_fotos_local_coleta.rename(
    columns={'tipo': 'tipo_coleta', 'url': 'url_coleta'})

base_fotos_avaliacao = base_fotos.loc[base_fotos['tipo']
                                      == 'evidencia_avaliacao']
base_fotos_avaliacao = base_fotos_avaliacao.rename(
    columns={'tipo': 'tipo_avaliacao', 'url': 'url_avaliacao'})


# In[9]:


url_base_att = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_adubacao_de_cobertura_attachments.csv'


# In[10]:


url_base_survey = r'F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\QLD_adubacao_de_cobertura.xlsx'


# In[11]:


path_cadastro = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Cadastro Florestal.xlsx'


# In[12]:


base_att = pd.read_csv(url_base_att, delimiter=",")


cadastro = pd.read_excel(path_cadastro)
cadastro = cadastro[['Talhão', 'Id Projeto', 'Projeto', 'Região']]
cadastro.loc[:, 'Talhão'] = cadastro['Talhão'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
cadastro.loc[:, 'Id Projeto'] = cadastro['Id Projeto'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
cadastro["Projeto e Talhão"] = cadastro['Id Projeto'] + cadastro['Talhão']


hoje = datetime.datetime.now()
mes = hoje.month
ano = hoje.year
_, num_dias = calendar.monthrange(ano, mes)
max_dias = str(num_dias)
mes = "{:02d}".format(mes)

data_filtro = str(mes) + "-" + str(ano)


# In[13]:

# Filtro para o nível, não é necessário fazer todos os prints e sim apenas os que competem a função
survey = pd.read_excel(url_base_survey)
survey = survey[['objectid', 'fazenda', 'id_talhao',
                 'nivel', 'data', 'observacoes', 'regiao']]
# survey = survey.loc[survey['nivel'] =='2° Nível']
survey['mes_ano'] = survey['data'].dt.to_period('M')
survey = survey.loc[survey['mes_ano'] == data_filtro]
survey['talhao'] = survey['id_talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
survey['nome_fazenda'] = survey['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
survey['Projeto e Talhão'] = survey['nome_fazenda'] + survey['talhao']
survey['datahoje'] = survey['data'].dt.date
survey['observacoes_gerais'] = survey['observacoes'].fillna("")
survey['mes_ano'] = survey['data'].dt.to_period('M')
survey= survey.loc[survey['mes_ano'] == data_filtro]

# In[14]:


# Filtro para o nível, não é necessário fazer todos os prints e sim apenas os que competem a função
survey = pd.read_excel(url_base_survey)
survey = survey[['objectid', 'fazenda', 'id_talhao',
                 'nivel', 'data', 'observacoes', 'regiao']]
# survey = survey.loc[survey['nivel'] =='2° Nível']
survey['talhao'] = survey['id_talhao'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(3)
survey['nome_fazenda'] = survey['fazenda'].fillna(
    '').astype(str).str.split('.').str[0].str.zfill(4)
survey['Projeto e Talhão'] = survey['nome_fazenda'] + survey['talhao']
survey['datahoje'] = survey['data'].dt.date
survey['observacoes_gerais'] = survey['observacoes'].fillna("")


# In[15]:


survey = survey.merge(cadastro, left_on='Projeto e Talhão',
                      right_on='Projeto e Talhão', how='left')


# In[16]:


survey = survey.merge(base_fotos_assinatura[[
                      'url_assinatura', 'tipo_assinatura', 'objectid']], left_on='objectid', right_on='objectid', how='left')


# In[17]:


survey = survey.merge(base_fotos_avaliacao[[
                      'url_avaliacao', 'tipo_avaliacao', 'objectid']], left_on='objectid', right_on='objectid', how='left')


# In[18]:


survey = survey.merge(base_fotos_local_coleta[[
                      'url_coleta', 'tipo_coleta', 'objectid']], left_on='objectid', right_on='objectid', how='left')


# In[19]:


survey = survey.merge(base_fotos_identificacao_maq[[
                      'url_identificacao_maquina', 'tipo_evidencia', 'objectid']], left_on='objectid', right_on='objectid', how='left')


survey['url_assinatura'] = survey['url_assinatura'].apply(
    lambda x: foto_branco if pd.isnull(x) else x)
survey['url_avaliacao'] = survey['url_avaliacao'].apply(
    lambda x: foto_branco if pd.isnull(x) else x)
survey['url_coleta'] = survey['url_coleta'].apply(
    lambda x: foto_branco if pd.isnull(x) else x)
survey['url_identificacao_maquina'] = survey['url_identificacao_maquina'].apply(
    lambda x: foto_branco if pd.isnull(x) else x)


# In[20]:




# In[21]:


for i, row in survey.iterrows():
    try:
        filename = 'CDI{} - {} {} - {} - {} - {}.pdf'.format(
            row['objectid'], row['Projeto'], row['Talhão'], row['nivel'], row['regiao'], row['datahoje'])
        cnv = canvas.Canvas(
            r'F:/Qualidade_Florestal/01- SÃO PAULO/02- Silvicultura e Sobrevivência/00 - Arquivos Surveys/Arquivos PDF/Adubação de Cobertura/' + filename)
        # cnv = canvas.Canvas(survey['Projeto'][0] + " " + str(survey['Talhão'][0]) + " - " + str(survey['datahoje'][0]) + '.pdf')

        if row['regiao'] == "SP":
            logo = logo_bracel
        else:
            logo = logo_msf

        cnv.drawImage(logo, 0, (820 - 25), width=100, height=25)
        cnv.setFont("Helvetica-Bold", 15)
        cnv.drawString(110, (820-20), "Evidência de Adubação de Cobertura")
        cor_linha = HexColor("#A4d061")
        cnv.setStrokeColor(cor_linha)
        cnv.line(10, (820-40), 596, (820-40))

        cnv.drawString(10, (820-70), "Código de Identificação:")

        cnv.setFont('Helvetica', 13)
        cnv.drawString(190, (820-70), str(row['objectid']))
        cnv.setFont("Helvetica-Bold", 15)
        cnv.drawString(10, (820-100), "Data:")

        cnv.setFont("Helvetica", 13)
        cnv.drawString(50, (820-100), str(row['datahoje']))

        cnv.setFont("Helvetica-Bold", 15)
        cnv.drawString(10, (820-130), "Fazenda:")
        cnv.setFont("Helvetica", 13)
        cnv.drawString(80, (820-130), str(row['Projeto']))

        cnv.setFont("Helvetica-Bold", 15)
        cnv.drawString(10, (820-160), "Talhão:")
        cnv.setFont("Helvetica", 13)
        cnv.drawString(80, (820-160), str(row['Talhão']))

        cnv.setFont("Helvetica-Bold", 15)
        cnv.drawString(10, (820-190), "Região:")
        cnv.setFont("Helvetica", 13)
        cnv.drawString(80, (820-190), str(row['Região']))

        cnv.setFont("Helvetica", 13)
        cnv.drawString(40, (550), "Evidência da Avaliação:")

    # Evidência Avaliação
        cnv.drawImage(str(row['url_avaliacao']), 40,
                      (330), width=200, height=200)

        cnv.setFont('Helvetica', 13)
        cnv.drawString(360, (550), "Local de Coleta:")

    # Adicionar imagem aqui
        cnv.drawImage(str(row['url_coleta']), 360,
                      (330), width=200, height=200)

        cnv.setFont('Helvetica', 13)
        cnv.drawString(40, (300), "Identificação da Máquina:")

    # Adicionar imagem aqui
        cnv.drawImage(str(row['url_identificacao_maquina']),
                      40, 80, width=200, height=200)

        cnv.setFont('Helvetica', 13)
        cnv.drawString(360, (300), "Assinatura:")

        cnv.drawImage(str(row['url_assinatura']),
                      360, 80, width=200, height=200)

    # Adicionar imagem aqui

        cnv.setFont('Helvetica', 13)
        cnv.drawString(250, (60), "Observações")

        cnv.setFont('Helvetica', 10)
        cnv.drawString(100, (40), str(row['observacoes_gerais']))

        cnv.save()
    except Exception as e:
        print(
            f"Erro ao processar arquivo para o objeto de identificação {row['objectid']}: {e}")
        continue


# In[ ]:
