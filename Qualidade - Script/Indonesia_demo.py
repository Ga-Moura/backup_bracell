import pandas as pd
import os
import openpyxl as opx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from PIL import Image


# ***Configurando a página antes de qualquer etapa***

# Criando a primeira página

# Inicialize as variáveis de sessão


if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False


# Página de Login
def login_page():

    logo_path = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\2 - Modelagem\logo - Bracell.jpg'

    st.image(Image.open(logo_path).resize((200, 50)))

    st.subheader("Forestry Quality - São Paulo")

    st.markdown('<hr style="border-top: 1px solid #40d925;">',
                unsafe_allow_html=True)

    st.title("Login Page")
    # Campos de entrada para o nome de usuário e senha
    username = st.text_input("Login")
    password = st.text_input("Password", type="password")

    # Botão de login
    if st.button("Login"):
        if username == "bracell" and password == "1234":
            st.session_state.is_authenticated = True
            st.success("Correct login")
    # Se o login for bem-sucedido, exibe o botão para ir para a próxima página
            if st.session_state.is_authenticated:
                if st.button("Next Page"):
                    st.write("You are on the next page!")
        else:
            st.error("Invalid credentials. Try again")


if not st.session_state.is_authenticated:
    login_page()


else:

    # Configurando a largura da tela e ativando o desativando o sidebar
    st.set_page_config(
        page_title="Forestry Quality",
        layout='wide',
        page_icon=":bar_chart:",
        initial_sidebar_state="collapsed"
    )

    # ***Fim de configuração de Página***

    # ***Paths***

    path_adub = r"F:\Qualidade_Florestal\01- SÃO PAULO\02- Silvicultura e Sobrevivência\00 - Arquivos Surveys\Adubação_de_Cobertura_-_Silvicultura.xlsx"

    path_cad = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\Cadastro Florestal.xlsx'

    path_xy = r"F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\1 - Processamento de dados\lat_long.xlsx"
    # ***Fim Paths***

    # ***Tratar Base Cadastro***

    @st.cache_data
    def carregar_dados_cad():

        dtype_cad = {
            'Projeto e Talhão': str
        }

        df_cad = pd.read_excel(path_cad, dtype=dtype_cad)

        dtype_xy = {
            'OBJETO_LOCACAO': str
        }

        df_xy = pd.read_excel(path_xy, dtype=dtype_xy)

        df_xy['OBJETO_LOCACAO'] = df_xy['OBJETO_LOCACAO'].drop_duplicates()

        df_cad = df_cad.merge(df_xy[['OBJETO_LOCACAO', 'Long', 'Lat']],
                              left_on='Projeto e Talhão', right_on='OBJETO_LOCACAO', how='left')
        return df_cad

    df_cad = carregar_dados_cad()

    # ***Fim Base Cadastro***

    # ***Tratar base Adubo***

    @st.cache_data
    def carregar_dados():

        df_adub = pd.read_excel(path_adub)

        df_adub['Mascara_fazenda'] = df_adub['fazenda'].fillna(
            '').astype(str).str.split('.').str[0].str.zfill(4)

        df_adub['Mascara_talhao'] = df_adub['id_talhao'].fillna(
            '').astype(str).str.split('.').str[0].str.zfill(3)

        df_adub['Mes_ano'] = df_adub['data'].dt.strftime('%m/%Y').astype(str)

        df_adub['data'] = pd.to_datetime(df_adub['data'].dt.strftime('%d%m%y'))

        df_adub['Objeto_loc'] = df_adub['Mascara_fazenda'].astype(
            str) + df_adub['Mascara_talhao'].astype(str)

        df_adub = df_adub.merge(df_cad[['Projeto e Talhão', 'Projeto', 'Long', 'Lat']],
                                left_on='Objeto_loc', right_on='Projeto e Talhão', how='left')

        df_adub['equipe'] = df_adub.apply(lambda x: x['equipe_ms'] if pd.isnull(
            x['equipe_sp']) else x['equipe_sp'], axis=1)

        # ***Fim Base Adubo***

        # ***Calculos de Desvio Adubo***

        df_adub['variacao_r'] = df_adub.apply(lambda x: (
            (x['qtd_adubo1']*100) / x['qtd_adubo2'])-100 if x['qtd_adubo2'] != 0 else 0, axis=1).abs()

        df_adub['qtd_total'] = df_adub.apply(
            lambda x: x['qtd_adubo1'] + x['qtd_adubo2'], axis=1)

        df_adub['dose_obtida_r'] = df_adub.apply(lambda x:
                                                 (x['qtd_total'] * 200) / (x['espac_linha'] * x['ruas']), axis=1)

        df_adub['dose_desvio_r'] = df_adub.apply(lambda x:
                                                 ((x['dose_obtida_r'] - x['dose_recomendada'])/x['dose_recomendada'])*100 if x['dose_obtida_r'] > 0 else None, axis=1).abs()

        df_adub['desvio_dose_un'] = df_adub.apply(
            lambda x: x['dose_obtida_r'] - x['dose_recomendada'], axis=1)

        df_adub['status'] = df_adub.apply(lambda x: "Conforme" if x['dose_desvio_r'] <= 2 and x['regiao'] == "SP"
                                          else
                                          "Conforme" if x['dose_desvio_r'] <= 3 and x['regiao'] == "MS" else "Não Conforme", axis=1)

        df_adub['n_conf'] = df_adub.apply(
            lambda x: "0" if x['status'] == "Não Conforme" else "1" if x['status'] == "Conforme" else "0", axis=1).astype(int)

        df_adub['nc_conf'] = df_adub.apply(
            lambda x: "1" if x['status'] == "Não Conforme" else "0" if x['status'] == "Conforme" else "1", axis=1).astype(int)

        return df_adub

    df_adub = carregar_dados()

    # ***Fim Calculos de Adubo***

    # ***Formatando Cabeçalho***

    logo_path = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\2 - Modelagem\logo - Bracell.jpg'

    st.image(Image.open(logo_path).resize((200, 50)))

    st.subheader("Forestry Quality - São Paulo")

    st.write('<b>Cover Fertilization</b>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top: 1px solid #40d925;">',
                unsafe_allow_html=True)

    col01, col02, col03, col04 = st.columns(4)
    col04.write('<font color="red">Target 2% </font>', unsafe_allow_html=True)

    # ***Adicionando Filtros***

    filtro_regiao = st.sidebar.multiselect(
        key=1,
        label="Unidade",
        options=df_adub['regiao'].unique(),
        default=df_adub['regiao'].unique()
    )

    filtro_nivel = st.sidebar.multiselect(
        key=2,
        label='Nivel',
        options=df_adub['nivel'].unique(),
        default=['2° Nível']
    )

    df_adub = df_adub.query('regiao == @filtro_regiao')

    df_adub = df_adub.query('nivel == @filtro_nivel')

    # Fim de Filtros Adicionados

    # ***Gerando medidas***

    nc_nivel = df_adub.groupby('nivel')[['dose_desvio_r']].mean().reset_index()

    nc_nivel['dose_desvio_r'] = nc_nivel.apply(
        lambda x: f'{x["dose_desvio_r"] :.1f}%', axis=1)

    nc_mes = df_adub.groupby('Mes_ano')[['dose_desvio_r']].mean().reset_index()

    nc_mes['dose_desvio_r'] = nc_mes.apply(
        lambda x: f'{x["dose_desvio_r"]:.1f}%', axis=1)

    nc_equipe = df_adub.groupby(
        'equipe')[['dose_desvio_r']].mean().reset_index()

    nc_equipe['dose_desvio_r'] = nc_equipe.apply(
        lambda x: f'{x["dose_desvio_r"]:.1f}%', axis=1)

    nc_projeto = df_adub.groupby('Projeto')[
        ['dose_recomendada', 'dose_obtida_r', 'desvio_dose_un', 'dose_desvio_r']].mean().reset_index()

    nc_projeto['dose_recomendada'] = nc_projeto.apply(
        lambda x: f'{x["dose_recomendada"]:.2f}', axis=1)

    nc_projeto['dose_obtida_r'] = nc_projeto.apply(
        lambda x: f'{x["dose_obtida_r"]:.2f}', axis=1)

    nc_projeto['desvio_dose_un'] = nc_projeto.apply(
        lambda x: f'{x["desvio_dose_un"]:.2f}', axis=1)

    nc_projeto['status'] = nc_projeto.apply(
        lambda x:  "Conforme" if x['dose_desvio_r'] <= 2 else "Não Conforme", axis=1)

    nc_projeto['dose_desvio_r'] = nc_projeto.apply(
        lambda x: f'{x["dose_desvio_r"]:.1f}%', axis=1)

    rename_colums = {
        'dose_recomendada': 'Dose Recomendada (kg/ha)',
        'dose_obtida_r': "Dose Aplicada (kg/ha)",
        'desvio_dose_un': "Desvio de Dose (un)",
        'dose_desvio_r': "% NC"
    }

    nc_projeto.rename(columns=rename_colums, inplace=True)

    desvio_de_dose = f'{df_adub["dose_desvio_r"].mean():.1f}%'

    dose_recomendada = f'{df_adub["dose_recomendada"].mean():.2f}'

    dose_aplicada = f'{df_adub["dose_obtida_r"].mean():.2f}'

    dose_delta = f'{df_adub["desvio_dose_un"].mean():.2f}'

    per_c = df_adub.groupby('Mes_ano')[
        ['n_conf', 'nc_conf']].sum().reset_index()

    per_c['perc_c'] = per_c.apply(
        lambda x:  x['n_conf'] / (x['n_conf'] + x['nc_conf']), axis=1).astype('float64')
    per_c['perc_nc'] = per_c.apply(
        lambda x:  x['nc_conf'] / (x['n_conf'] + x['nc_conf']), axis=1).astype('float64')

    per_c['perc_c'] = per_c.apply(
        lambda x: f'{(x["perc_c"]*100):.1f}%', axis=1)
    per_c['perc_nc'] = per_c.apply(
        lambda x: f'{(x["perc_nc"]*100):.1f}%', axis=1)

    # ***Fim Gerar Medidas***

    # ***Gerando Cards metricas****

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="Recommended Average Dose (kg/ha)",
                value=dose_recomendada,
                )

    col2.metric(label="Average Applied Dose (Kg/ha)",
                value=dose_aplicada,
                )

    col3.metric(label="Delta Average Dose (kg/ha)",
                value=dose_delta)

    col4.metric(label="% Non - Compliance",
                value=desvio_de_dose)

    st.write("""
        #
        #
    """)

    # ***Gerando Graficos****

    col5, col6 = st.columns(2)

    renomear_coluna = {'Projeto': 'Project',
                       'Dose Recomendada (kg/ha)': 'Recommended Average Dose (kg/ha)',
                       'Dose Aplicada (kg/ha)': 'Average Applied Dose (Kg/ha)',
                       'Desvio de Dose (un)': 'Dose Deviation (un)',
                       'status': 'Status'}

    nc_projeto.rename(columns=renomear_coluna, inplace=True)

    col5.dataframe(nc_projeto, hide_index=True)

    # ***Criar Mapa para plotar***

    df_mapa = df_adub.dropna(subset=['Lat', 'Long'])

    cor_map = {'Conforme': '#A4D061',
               'Não Conforme': '#C00000'}

    mapa = px.scatter_mapbox(df_mapa,
                             lat='Lat',
                             lon="Long",
                             color='status',
                             color_discrete_map=cor_map,
                             mapbox_style='carto-positron',
                             zoom=5,
                             )

    mapa.update_layout(title='Espacialization', title_x=0.5)
    mapa.update_layout(legend=dict(
        x=0.4, y=1, traceorder='normal', orientation='h'))

    col6.plotly_chart(mapa)

    # ***Segunda Linha***

    st.write("""
            #
            # 
            """)

    col7, col8 = st.columns(2)

    # ***distancia conforme planta***

    color_map = {"Yes": '#A4D061',
                 "No": '#C00000'}

    df_adub['distancia_minima'] = df_adub['distancia_minima'].replace(
        {'Sim': 'Yes', 'Não': 'No'})

    dt_conforme = px.pie(df_adub, names='distancia_minima',
                         title="Distância Mínima da Planta",
                         color='distancia_minima',
                         color_discrete_map=color_map)

    dt_conforme.update_layout(title='% of Plants with Distance according to application',
                              title_x=0.3,
                              legend_orientation='v',
                              legend_title_side="top")

    col7.plotly_chart(dt_conforme, use_container_width=True)

    # percentual de avaliações conformes

    bar_perc = px.bar(per_c,
                      x='Mes_ano',
                      y='perc_c',
                      labels={'Mes_ano': 'Month',
                              'perc_c': '',
                              },
                      text='perc_c',
                      color_discrete_sequence=['#2251A3'])

    bar_perc.update_layout(
        title="% Compliance Assessments",
        title_x=0.5,  # Configuração para empilhar as barras com porcentagens
    )

    bar_perc.update_xaxes(showgrid=False)
    bar_perc.update_yaxes(showgrid=False, showticklabels=False)

    col8.plotly_chart(bar_perc, use_container_width=True)

    # ***Desvio por equipe***

    col10, col11 = st.columns(2)

    # ***Desvio Mensal***

    bar_equipe = px.bar(nc_mes,
                        x="Mes_ano",
                        y='dose_desvio_r',
                        labels={"Mes_ano": "Month", 'dose_desvio_r': ''},
                        text='dose_desvio_r',
                        color_discrete_sequence=['#2251A3'])
    bar_equipe.update_layout(title="% Deviation per months", title_x=0.5)
    bar_equipe.update_xaxes(showgrid=False)
    bar_equipe.update_yaxes(showgrid=False, showticklabels=False)

    target = 2

    # Adicionando a linha horizontal ao gráfico
    bar_equipe.add_shape(
        type='line',
        x0=0,
        x1=len(nc_mes['Mes_ano']),
        y0=target,
        y1=target,
        line=dict(color='red', width=2),
        name='Target'
    )

    col10.plotly_chart(bar_equipe, use_container_width=True)

    # Avaliação por equipe

    bar_equipe = px.bar(nc_equipe,
                        x='equipe',
                        y='dose_desvio_r',
                        labels={'equipe': ' ', 'dose_desvio_r': " "},
                        text='dose_desvio_r',
                        color_discrete_sequence=['#2251A3']
                        )

    bar_equipe.update_layout(title="Team Assessment", title_x=0.5)
    bar_equipe.update_xaxes(showgrid=False)
    bar_equipe.update_yaxes(showgrid=False, showticklabels=False)

    # Adicionando a linha horizontal ao gráfico

    bar_equipe.add_shape(
        type='line',
        x0=0,
        x1=len(nc_equipe['equipe']),
        y0=target,
        y1=target,
        line=dict(color='red', width=2),
        name='Target'
    )

    col11.plotly_chart(bar_equipe, use_container_width=True)
