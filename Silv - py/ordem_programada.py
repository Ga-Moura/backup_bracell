# %%
import pandas as pd
import psycopg2 as pg
import configparser


# %%
import locale

# Configurar o locale para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# %%
crendenciais_path = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\04. Pessoas\Gabriel Moura\00 - Silvicultura\00 - Credenciais\credenciais.conf'

# %%
save_path = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\01. Programações & Controles\016. Insumos\Novo Fluxo Insumos\ApontamentosSGF\ordem_programada.xlsx'

# %%
#Senhas e credênciais 

credenciais = configparser.ConfigParser()

credenciais.read(crendenciais_path)

logins = credenciais['credenciais']


conn_dwh = pg.connect(
    user =logins['login'],
    password =logins['senha_sql'],
    host = logins['host'],
    port = logins['port'],
    database = logins['data_base']
)

# %%
cursor = conn_dwh.cursor()

cursor.execute(

"""
select  
cd_ordem_servico,
dcr_ordem_servico,
dcr_operacao,
vlr_producao,
id_projeto,
cd_talhao,
data_reg

from forestry.f_vw_operacao_programada

where
source = 'BSP' and 
est_reg = 'A' and 
tip_programacao = 'O' and 
id_regiao = 1 and 
dcr_ordem_servico notnull 

"""

)

dados_consulta = cursor.fetchall()

cursor.close()


colunas = [desc[0] for desc in cursor.description]

colunas_maisculuas = [ str(i).upper() for i in colunas]



ctl_boletim = pd.DataFrame(dados_consulta, columns=colunas_maisculuas)

# %%
#Alterando o tipo de quantidade utilizada
ctl_boletim['VLR_PRODUCAO'] = ctl_boletim['VLR_PRODUCAO'].astype('float')

# %%
ctl_boletim.to_excel(save_path,index = False)


