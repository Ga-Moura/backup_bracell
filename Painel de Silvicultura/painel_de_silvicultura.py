import streamlit as st
from PIL import Image
import os


 # Configurando a largura da tela e ativando o desativando o sidebar
st.set_page_config(
    page_title="Painel de Silvicultura",
    layout='wide',
    page_icon=":evergreen_tree:",
    initial_sidebar_state="expanded"
                )



#Power Bi

pbi_monitoramento_agua = r'm'

pdf_irrig = r'irrigacao'

pdf_informe =  r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\Informativos Diario e Saldos 25 02 2025.pdf'

pbi_follow_up = r'https://app.powerbi.com/groups/4b9c4d56-7a78-4739-89ab-42afa1c01b73/reports/f4343a09-510e-4aa2-942a-991f65cafdda/ReportSection?experience=power-bi'

pbi_performance = r'https://powerbi.bracell.com/reports/powerbi/Forestry/Silviculture/BSP/Painel%20%20M%C3%A9tricas%20Operacionais?rs:embed=true'

pbi_premio = r'https://powerbi.bracell.com/reports/powerbi/Forestry/Silviculture/BSP/Painel%20de%20M%C3%A9tricas%20-%20Premio'

weed_competition = r'https://gissp.bracell.com/portal/apps/experiencebuilder/experience/?id=261e95ada1ee437f9ead91b3267c4ada&page=page_6'

performance = r'https://gissp.bracell.com/portal/apps/experiencebuilder/experience/?id=261e95ada1ee437f9ead91b3267c4ada&page=page_9'

audit_plantatition ='https://gissp.bracell.com/portal/apps/experiencebuilder/experience/?id=261e95ada1ee437f9ead91b3267c4ada&page=page_10'

pbi_sensoriamento_performance = r'https://powerbi.bracell.com/reports/powerbi/Forestry/GEO/BSP/Sensoriamento%20Remoto/Indicadores%20Performance%20SP'

pbi_captacao_agua = r''

pbi_consumo_mudas = r''

pbi_pragas_doencas = r''

pbi_sop = r'https://app.powerbi.com/groups/me/apps/ca9954f9-0d3b-4f9d-8897-b0d76d4a34b2/reports/89bcfb94-3be3-4516-bf9a-f857ca96205f/cc30c0285018d25d8fd6?ctid=582d9d84-4800-4487-9b24-cdc6471551ae&experience=power-bi'

pbi_qualidade = r'https://app.powerbi.com/groups/8f026f89-78ef-45ac-957e-15ae919e99fc/reports/2b3bbb87-aae4-40b1-8c33-89c298cc16e9/ReportSectionb66afd3c296f365a01f1?experience=power-bi'

solinftec = r'https://bracell.saas-solinftec.com/#!/login/'

johndeere = r'https://signin.johndeere.com/'


#icones

informe_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\informe_diario.png'

geo_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\calendario.png'

follow_up_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\follow_up.png'

pragas_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\monitoramento_de_pragas.png'

loading_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\loading.png'

qualidade_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\qualidade.png'

capt_agua_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\captacao_agua.png'

consumo_mudas_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\mudas.png'

performance_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\performance.png'

logo_path = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\logo - Bracell.jpg'

premio_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\premio.png'

solinftec_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\solinftec.png'

johndeere_icon = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\04 - Painel de Silvicultura\icones\johndeere.png'



#Download informe
def informe():
        
    with open(pdf_informe, 'rb') as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label='Baixar informe',
        data=pdf_bytes,
        file_name='informe_diário.pdf',
        mime='application/pdf'

    )




def monitoramento():
  
    st.image(Image.open(logo_path).resize((200, 50)))

    st.subheader("BSPF/COI - Silvicultura")

    st.write('<b>São Paulo</b>', unsafe_allow_html=True)

    st.write('<b>Monitoramento</b>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top: 1px solid #40d925;">',unsafe_allow_html=True)


    #Container de Títulos
    with st.container():
        st.subheader('Indicadores')


   #ícones


        #Container de Fotos
    with st.container():

        col1,_,col2, _ ,col3,_,col4,_, col5 = st.columns(9)

        col1.image(Image.open(informe_icon).resize((100, 100)))
        
        col2.image(Image.open(follow_up_icon).resize((100, 100)))

        col3.image(Image.open(capt_agua_icon).resize((100, 100)))

        col4.image(Image.open(consumo_mudas_icon).resize((80, 80)))
        
        col5.image(Image.open(pragas_icon).resize((80, 80)))

     #Container de indicadores

    with st.container():

        col11, col12,col13,col14,col15 = st.columns(5)

        col11.markdown(f'&nbsp;&nbsp;Informe diário',unsafe_allow_html = True)
        col11.write(f'&nbsp;&nbsp;Att: 26/02/25 12:07', unsafe_allow_html=True)
        informe()

        col12.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Follow Up de Áreas]({pbi_follow_up})',unsafe_allow_html = True)

        col13.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Captação de Água]({pbi_captacao_agua})',unsafe_allow_html = True)

        col14.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Consumo de Mudas]({pbi_consumo_mudas})',unsafe_allow_html = True)

        col15.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Pragas e Doenças]({pbi_pragas_doencas})',unsafe_allow_html = True)


def torre():

      
    st.image(Image.open(logo_path).resize((200, 50)))

    st.subheader("BSPF/COI - Silvicultura")

    st.write('<b>São Paulo</b>', unsafe_allow_html=True)

    st.write('<b>Central - Torre de Controle</b>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top: 1px solid #40d925;">',unsafe_allow_html=True)

    with st.container():
        st.subheader('Indicadores de Performance')


    with st.container():

        col1,_,col2, _ ,col3,_,col4,_, col5 = st.columns(9)

        col1.image(Image.open(performance_icon).resize((100, 100)))

        col2.image(Image.open(premio_icon).resize((100,100)))
        

    with st.container():

        col11,_,col12,_,col13,_,col14,_,_ = st.columns(9)

        col11.markdown(f'&nbsp;[Performance]({pbi_performance})',unsafe_allow_html = True)

        col12.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Prêmio]({pbi_premio})',unsafe_allow_html = True)


    with st.container():
        st.subheader('')
        st.subheader('Tenologia Embarcada')


    with st.container():

        col21,_,col22,_,col23,_,col24,_,_ = st.columns(9)

        col21.image(Image.open(johndeere_icon).resize((90,90)))
        
        col22.image(Image.open(solinftec_icon).resize((90,90)))
        
        col21.markdown(f'&nbsp;&nbsp;[John Deere]({johndeere})',unsafe_allow_html = True)

        col22.markdown(f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Solinftec]({solinftec})',unsafe_allow_html = True)

        
def areas_apoio():
    
    st.image(Image.open(logo_path).resize((200, 50)))

    st.subheader("BSPF/COI - Silvicultura")

    st.write('<b>São Paulo</b>', unsafe_allow_html=True)

    st.write('<b>Áreas de Apoio</b>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top: 1px solid #40d925;">',unsafe_allow_html=True)

    with st.container():
        st.subheader('Geoprocessamento')
    
        with st.container():
            
            st.markdown(f'[Weed Competition]({weed_competition})',unsafe_allow_html = True)

            st.markdown(f'[Audit Plantation]({audit_plantatition})',unsafe_allow_html = True)

            st.markdown(f'[Performance da Floresta]({performance})',unsafe_allow_html = True)

            st.markdown(f'[Power BI - Performance da Floresta]({pbi_sensoriamento_performance})',unsafe_allow_html = True)

    with st.container():
        st.subheader('Qualidade')

        with st.container():

            st.markdown(f'[SOP]({pbi_sop})',unsafe_allow_html = True)

            st.markdown(f'[Qualidade]({pbi_qualidade})',unsafe_allow_html = True)



#Botões e Páginas
with st.container():
    st.sidebar.title('Navegação')
    paginas = ['Monitoramento','Central - Torre de Controle', 'Áreas de Apoio']
    escolha_pagina = st.sidebar.radio('Escolha uma página', paginas, index=0)

    if escolha_pagina == 'Monitoramento':
        monitoramento()
    elif escolha_pagina == 'Central - Torre de Controle':
        torre()
    elif escolha_pagina == 'Áreas de Apoio':
        areas_apoio()

