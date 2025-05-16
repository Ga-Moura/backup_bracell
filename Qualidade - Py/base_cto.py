import pandas as pd
import configparser 
import psycopg2 as pg 



path_login = r'F:\Qualidade_Florestal\03- ADMINISTRATIVO\2023\06- COLABORADORES\Gabriel\18 - SQL\sets.conf'

config = configparser.ConfigParser()

config.read(path_login)


db_config = config['informacoes']


conn_dwh = pg.connect(
    user =db_config['login'],
    password =db_config['senha'],
    host = db_config['host'],
    port = db_config['port'],
    database = db_config['data_base']
)


cursor = conn_dwh.cursor()

cursor.execute('select * from forestry.vw_f_vw_cubo_col_talhoes_cto_bsp_all')

base_de_dados = cursor.fetchall()

#fechando cursor e conexão
cursor.close()
conn_dwh.close()

colunas = [desc[0] for desc in cursor.description]

df = pd.DataFrame(base_de_dados,columns=colunas)


df['data_import_date'] = df['data_import_date'].dt.tz_localize(None)


df.to_excel(r"F:\Qualidade_Florestal\01- SÃO PAULO\03- Colheita\00 - Bases de Trabalho\Bases de Apoio\CTO.xlsx", index=False, sheet_name= "CTO")