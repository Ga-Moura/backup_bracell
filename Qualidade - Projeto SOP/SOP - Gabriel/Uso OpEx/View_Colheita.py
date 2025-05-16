#Automação do consumo de dados via OPEX para colheita florestal, Bracell. 
#Feito Por: Érico Mendes, Dez 2023


#IMPORTS
import psycopg2
import pandas as pd
import time

############################## Conexão com Banco

try:
    connection = psycopg2.connect(
        dbname='bracell_dwh',
        user='edomingues', # Informe seu usuário padrão.
        password='ednaminhavo', # Informe sua senha de acesso ao OPEX
        host='172.28.3.183',  
        port='5432'  
    )
    print("Conexão ao OPEX bem-sucedida!")

except psycopg2.Error as e:
    print("Erro ao conectar ao OPEX:", e)

############################## Consumo de dados

def consultar_dados():
    try:
        cursor = connection.cursor()
        
        # Exemplo de consulta SQL
        cursor.execute("select * from forestry.vw_cubo_col_vol_madeira_v2_bsp_all where data_operacao >= '2023-12-26';")
        
        # Exibindo mensagem de início da consulta
        print("Iniciando a consulta...")
        
        # Obtendo os resultados, se necessário
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
        
        # Não se esqueça de fechar o cursor quando terminar
        cursor.close()
      
        return df
    
    except psycopg2.Error as e:
        print("Erro ao executar a consulta:", e)
        return None

############################## Tratamento dos dados

df = consultar_dados()

if df is not None:
    df.columns = map(str.upper, df.columns)

    ############################## Salvando os dados
    df.to_parquet(r"F:\Planejamento_e_Controle\Fabricio - Base de dados - LUPA\DHColheita_BSP.parquet")
    
    print("Consulta finalizada. Dados salvos.")
