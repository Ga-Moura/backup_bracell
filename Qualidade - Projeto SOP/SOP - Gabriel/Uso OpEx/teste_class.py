#IMPORTS
import psycopg2
import pandas as pd
import time
import configparser

from datetime import datetime
import os


class ConnectOpex():
    
        def __init__(self) -> None:

            self.connect_to_opex()     
    
    
        def connect_to_opex(self):
                """
                Connect to gis server.
                """
                        
                parser = configparser.ConfigParser()
                parser.read('pipeline.conf')

                dbname = parser.get('opex_credentials', 'dbname')
                user = parser.get('opex_credentials', 'user')
                password = parser.get('opex_credentials', 'password')
                host = parser.get('opex_credentials', 'host')
                port = parser.get('opex_credentials', 'port')
                
                try:

                    self.connection = psycopg2.connect(
                        dbname=dbname,
                        user=user,
                        password=password,
                        host=host,
                        port=port
                    )
                    print("Conexão ao OPEX bem-sucedida!")

                except psycopg2.Error as e:
                    print("Erro ao conectar ao OPEX:", e)
                    self.connection = None            

                return self.connection



class OpexConsult(ConnectOpex):
    
    def __init__(self) -> None:
                   
            super().__init__()# Chama o __init__ da classe base
              
            
            
    def consultar_dados(self,sql) -> pd.DataFrame:
            
            connection = self.connection
            
            if connection:
                try:
                    cursor = connection.cursor()
                    
                    # Exemplo de consulta SQL
                    cursor.execute(sql)
                    # cursor.execute("select * from forestry f_vw_cubo_uso_solo where cd_ >= '2023-12-26';")
                    
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
        
        
    

