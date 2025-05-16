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
save_path = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Edicao\01. Programações & Controles\016. Insumos\Novo Fluxo Insumos\ApontamentosSGF\ApontamentoSGF.xlsx'

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
cd_boletim_insumo,
qtd_utilizada,
data_reg,
est_reg,
data_utilizacao,
cd_boletim_silvicultura,
cd_uso_solo,
cd_processo,
cd_material,
cd_unidade,
dcr_obs

from forestry.f_ctl_boletim_insumo

where 

source = 'BSP' and 
dcr_obs <> '' and
data_reg >= '11/14/2024' and
cd_material NOT IN (30, 39, 40, 55, 277, 257, 258, 259, 276, 268, 89, 93, 88, 90, 91, 92, 35, 33, 32, 31, 17, 246, 1, 37, 38, 94, 56, 34, 36);

"""

)

dados_consulta = cursor.fetchall()

cursor.close()


colunas = [desc[0] for desc in cursor.description]

colunas_maisculuas = [ str(i).upper() for i in colunas]



ctl_boletim = pd.DataFrame(dados_consulta, columns=colunas_maisculuas)

# %%
#Alterando o tipo de quantidade utilizada
ctl_boletim['QTD_UTILIZADA'] = ctl_boletim['QTD_UTILIZADA'].astype('float')

# %%
ctl_boletim.to_excel(save_path,index = False)

