import cx_Oracle as cx
import time
from datetime import date
import datetime

# definindo o dia de execução do script atual #
data_atual = date.today()

d7 = datetime.timedelta(days=7)
d1 = datetime.timedelta(days=1)
m1 = datetime.timedelta(days=30)

yesterday = data_atual - d1
week = yesterday - d7
month = yesterday - m1

ontem = yesterday.strftime("%Y%m%d")
semana = week.strftime("%Y%m%d")
mes = month.strftime("%Y%m%d")


# tempo Inicial #
t_ini = (time.time())

# estabelecendo uma conexão com o banco de dados Oracle
connection = cx.connect('USER/SENHA@IP:PORTA/NOME_BANCO')

# criando um cursor para executar as consultas
cursor = connection.cursor()

# executando uma consulta
cursor.execute(f"SELECT de.EQUIPMENT_DESCRIPTION AS Placa, de.PROJECT_NAME as Fazenda, de.COMPOSITION_TYPE_DESCRIPTION as Composição, ft.ARRIVAL_DATE_TIME as Chegada_Fábrica, YARD_LEAVING_TIME as Saída_Fábrica, DISTANCE as Distância, UNPAVED_ROAD_DISTANCE as Terra, PAVED_ROAD_DISTANCE as ASFALTO, GROSS_WEIGHT AS PESO_BRUTO, TARE_WEIGHT AS PESO_TARA, NET_WEIGHT AS PESO_LIQUIDO FROM P_SGF_DW.fact_transportation ft JOIN P_SGF_DW.dim_equipment de ON ft.DIM_IMPLEMENT_EQUIPMENT_ID = de.DIM_EQUIPMENT_ID JOIN P_SGF_DW.DIM_PROJECT de ON ft.DIM_PROJECT_ID = de.DIM_PROJECT_ID join P_SGF_DW.DIM_Composition_Type de ON ft.DIM_COMPOSITION_TYPE_ID = de.DIM_COMPOSITION_TYPE_ID WHERE ft.DIM_YARD_LEAVING_DATE_ID >= '{semana}' and ft.dim_yard_leaving_date_id <= '{ontem}'")

# nome das colunas#
column_names = [desc[0] for desc in cursor.description]


# abrindo o arquivo#
nome_arquivo = "F:/PASTA/NOME_DO_EXCEL{}.xls".format(data_atual.strftime("%d-%m-%Y"))

f=open(nome_arquivo, "w")

# cabeçalho #
f.write('\t'.join(column_names) + '\n')

# obtendo o resultado da consulta
result = cursor.fetchall()

# imprimindo o resultado
for row in result:
    line = '\t'.join(str(val).replace('.', ',') if isinstance(val, float) else str(val) for val in row)
    f.write(line + '\n')

# fechando a conexão e o cursor
f.close()
cursor.close()
connection.close()

t_fim = (time.time()) # em segundos

#Print do tempo que demorou para rodar a parte específica do código
print({t_fim - t_ini})