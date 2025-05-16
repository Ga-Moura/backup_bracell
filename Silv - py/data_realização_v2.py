# %%
import pandas as pd 
import numpy as np
from python_calamine.pandas import pandas_monkeypatch
pandas_monkeypatch()

# %%
#path premissas 
path_premissas = r'F:\Silvicultura\01. SP\PROCESSOS\COI Silvicultura - Consulta\01. Programacoes e Controles\001. Rolling Forcast - RF\2025\00 - Sequencia de Operação\premissas.xlsx'

# %%
#def Premissas

premissas_df = pd.read_excel(path_premissas, sheet_name='path')

def input_file(file):
    premissas = premissas_df.copy()
    
    premissas = premissas[premissas['status'] == 'ativo']

    premissas = premissas[premissas['arquivos de consumo'] == file]

    path = premissas['path'].iloc[0]

    return path

# %%
#Mascara mês operacional

def mes_operacional(df, coluna, nome_coluna):
    # Garantir que a coluna é do tipo datetime
    if not pd.api.types.is_datetime64_any_dtype(df[coluna]):
        df[coluna] = pd.to_datetime(df[coluna], errors='coerce')
    
    
    def calcular_mes_operacional(data):
        
        if pd.isna(data):
            return None 
        
        
        dia = data.day
        mes = data.month
        ano = data.year
        
        
        if dia > 20:
            mes = (mes % 12) + 1
            if mes == 1:
                ano += 1
        
        # Retornar um Timestamp, garantindo que todos são inteiros
        return pd.Timestamp(year=int(ano), month=int(mes), day=1)

    # Aplicar a função para a coluna
    df[nome_coluna] = df[coluna].apply(calcular_mes_operacional)

    return df

# %%
# path_sequenciamento = input_file('path_fazenda_programa')

# sequenciamento = pd.read_excel(path_sequenciamento,
#                                sheet_name='SEQUENCIAMENTO',
#                                skiprows=6,
#                                usecols=['Nova Coordenação Plantio 2','  EPS Plantio','ORDEM PLANTIO','Id Projeto','DATA INÍCIO'],
#                                dtype={'Id Projeto':'object'}).rename({'Nova Coordenação Plantio 2':'Nova Coordenação Plantio'},axis=1)


# sequenciamento = sequenciamento[(sequenciamento['  EPS Plantio'] != '(vazio)') & (pd.notna(sequenciamento['  EPS Plantio']))]


# sequenciamento = mes_operacional(sequenciamento,'DATA INÍCIO','mes_operacional')

# %%
#Caminho do programa

path_programa = input_file('path_fazenda_programa')

programa = pd.read_excel(path_programa,sheet_name='BD',
                         usecols=['Id Projeto','Talhão','Expectativa de Plantio','Nova EPS Plantio','Área(ha)','ORDEM PLANTIO',
                                   'Data de Referência', 'Origem referência', 'cto baldeio', 'cto colheita'],
                         dtype={'Id Projeto':'object', 'Talhão':'object'},
                         engine='calamine')

#Objeto de locação
programa['objeto de locação'] = programa['Id Projeto'].astype(str) + programa['Talhão'].astype(str)

#Ordem de plantio
    #Rmovendo tudo que está vazio

programa = programa[pd.notna(programa['ORDEM PLANTIO'])]

#Ordenando as prioridades de execução de operação

programa = programa.sort_values(['ORDEM PLANTIO','Id Projeto','Talhão' ,'cto baldeio', 'cto colheita','Data de Referência','Nova EPS Plantio'], ascending=[True,True ,True,True,True,True, True])


#Definindo qual será a data start para cada operação
data_start = pd.to_datetime(input_file('data_start'))

data_start_bracell02 = pd.to_datetime(input_file('data_start_bracell02'))


#data start jfi dourado


data_start_jfi_dourado = pd.to_datetime(input_file('data_start_JFI DOURADO'))


# Número sequencial dentro de cada projeto
programa['n_talhao'] = programa.groupby('Id Projeto').cumcount() + 1

# Total de talhões dentro de cada projeto
programa['nt_talhao'] = programa.groupby('Id Projeto')['Talhão'].transform('count')


#Definindo data de início da fazenda
programa['Data Start'] = np.where((programa['Nova EPS Plantio'] == 'BRACELL 02') , data_start_bracell02,
                                np.where((programa['Nova EPS Plantio'] == 'JFI DOURADO'), data_start_jfi_dourado,
                                                                data_start))





programa = mes_operacional(programa, 'Data Start', 'Data Start Operacional')

# %%
#Garantir que não há duplicatas


#Número de talhões 

print(programa.shape[0])

#Se for > 1, está errado

print(programa[programa['objeto de locação'].duplicated()].shape[0])


#Removendo duplicatas para garantir que não há problemas de talhão
programa = programa.drop_duplicates('objeto de locação')


print(programa.shape[0])


# %%
#Curva de dias trabalhados

curva_plantio_dias = pd.read_excel(path_premissas,sheet_name='dias_trabalhados')

curva_plantio_dias = curva_plantio_dias.melt(id_vars=['Provider'],
                                   value_vars=['03_25', '04_25', '05_25', '06_25',
                                    '07_25', '08_25', '09_25', '10_25', '11_25', '12_25',
                                    '01_26', '02_26', '03_26', '04_26','05_26','06_26',
                                    '07_26', '08_26', '09_26', '10_26', '11_26', '12_26'],
                                    var_name='Mês Operacional', value_name='dias operacionais')

curva_plantio_dias['Mês Operacional'] = pd.to_datetime(curva_plantio_dias['Mês Operacional'],format='%m_%y')

curva_plantio_dias['dias operacionais'] = pd.to_numeric(curva_plantio_dias['dias operacionais'], errors='coerce')


#Curva de Plantio

curva_plantio = pd.read_excel(path_premissas,sheet_name='Programa de Plantio')

curva_plantio = curva_plantio.melt(id_vars=['Provider'],
                                   value_vars=['03_25', '04_25', '05_25', '06_25',
                                    '07_25', '08_25', '09_25', '10_25', '11_25', '12_25',
                                    '01_26', '02_26', '03_26', '04_26','05_26','06_26',
                                    '07_26', '08_26', '09_26', '10_26', '11_26', '12_26'],
                                    var_name='Mês Operacional', value_name='capacidade')

curva_plantio['Mês Operacional'] = pd.to_datetime(curva_plantio['Mês Operacional'],format='%m_%y')

curva_plantio = curva_plantio.merge(curva_plantio_dias, left_on = ['Provider', 'Mês Operacional'], right_on = ['Provider', 'Mês Operacional'], how='left')

curva_plantio['Rendimento'] = curva_plantio['capacidade'] / curva_plantio['dias operacionais']


#Definindo a capacidade acumulada
curva_plantio['capacidade_acumulada'] = curva_plantio.groupby(['Provider'])['capacidade'].cumsum()

# %%
#Rendimento considerado

#Soma acumulada de produção Definindo qual rendimento deve ser considerado

#1º Ordenar as ordens de EPS e ordem de plantio
    #A base já foi ordenada, mas para esse momento deve ser considerado a eps independente da sua ordem

programa = programa.sort_values(['Nova EPS Plantio', 'ORDEM PLANTIO','n_talhao'], ascending=[True, True,True])


#Com a base ordenada o objetivo é realizar a soma acumulada dos talhões

programa['soma_acumulada'] = programa.groupby('Nova EPS Plantio')['Área(ha)'].cumsum()


#trazer a curva de plantio, volume a ser considerado para o volume de plantio

programa = programa.merge(curva_plantio[['Mês Operacional','capacidade_acumulada','Provider']],left_on=['Nova EPS Plantio'], right_on=['Provider'], how='left').drop('Provider', axis=1).rename({'Mês Operacional': 'Mês cop capacidade'},axis=1)


#Definindo o que esta dentro da capacidade 

#Dentro da capacidade == 0

#Fora da capacidade == 1

programa['status cap'] = np.where(programa['soma_acumulada'] <= programa['capacidade_acumulada'], 0, 1)

#Remover o que é igual a fora da capacidade, dessa forma, sempre terei os meses que estão dentro da capacidade e garante que sempre terá apenas opções que estão dentro da capacidade

#Antes de remover, importante garantir que sempre terei uma unidade do talhão, dessa forma, se o mínimo do talhão for 1, necessário considerar ele zero e definir capacidade 0

programa['status mínimo'] = programa.groupby('objeto de locação')['status cap'].transform('min')

#Garantindo o status mínimo, assim todas as linhas serão mantidas
programa = programa[(programa['status cap'] != 1) | (programa['status mínimo'] != 0 )]


#Removendo as duplicatas para garantir que tenha somente um único talhão
programa = programa.drop_duplicates('objeto de locação', keep='first')

#Para os talhões que status mínimo é igual a 1, eles devem ter o mês cop capacidade zerado, pois não podem ter capacidade atrelada

programa['Mês cop capacidade'] = np.where((programa['status mínimo'] == 1), pd.NaT, programa['Mês cop capacidade'])


programa['Status Capacidade'] = np.where(pd.isna(programa['Mês cop capacidade']), 'Equipe sem capacidade', pd.NaT)

programa['Mês cop capacidade'] = pd.to_datetime(programa['Mês cop capacidade'], errors='ignore')


# %%
#Programa & curva de plantio

programa = programa.merge(curva_plantio[['Provider', 'Mês Operacional', 'Rendimento']],
                           left_on=['Nova EPS Plantio', 'Mês cop capacidade'],
                           right_on=['Provider', 'Mês Operacional'],
                           how='left').drop('Mês Operacional', axis=1)

# %%
#Agrupar para encontrar o volume de produção da fazenda

agg = {'Área(ha)': 'sum',
       'n_talhao': 'max',
       'nt_talhao': 'max',
       'Rendimento': 'max',
       'Data Start':'max',
       'ORDEM PLANTIO':'min'}

programa_agrupado = programa.groupby(['Id Projeto','Nova EPS Plantio','Talhão']).agg(agg).reset_index()

programa_agrupado = programa_agrupado.sort_values(['Nova EPS Plantio','ORDEM PLANTIO'], ascending=[True, True])

# %%
#Dias de deslocamento

dia_deslocamento = float(input_file('dias_deslocamento'))

# %%
#Dias para operação

programa_agrupado['dias_operacao'] = programa_agrupado['Área(ha)'] / programa_agrupado['Rendimento']


programa_agrupado['deslocamento'] = np.where(programa_agrupado['n_talhao'] == programa_agrupado['nt_talhao'], dia_deslocamento, np.nan)

programa_agrupado['dias_acumulados'] = np.where( pd.isna(programa_agrupado['deslocamento']),
                                                 programa_agrupado['dias_operacao'],
                                                 programa_agrupado['dias_operacao'] + programa_agrupado['deslocamento'])


# %%
#Soma Acumulada de dias para trabalho
programa_agrupado['soma_acumulada'] = programa_agrupado.groupby(['Nova EPS Plantio'])['dias_acumulados'].transform('cumsum')

programa_agrupado['data_referencia'] = np.where(programa_agrupado['Nova EPS Plantio'] == 'BRACELL 02',data_start_bracell02,
                                                
                                                np.where(programa_agrupado['Nova EPS Plantio'] == 'JFI DOURADO', data_start_jfi_dourado, 
                                                
                                                data_start))


# %%
#Data fim da operação


#Se for bracell, trabalha de sabado, caso contrário, só considera trablho em dias úteis

programa_agrupado['fim_operacao'] = programa_agrupado.apply(
    lambda x: (
        np.busday_offset(
            x['data_referencia'].strftime('%Y-%m-%d'), 
            x['soma_acumulada'],
            weekmask='1111110',
            roll='forward'
        ) if x['Nova EPS Plantio'] in ['BRACELL 01', 'BRACELL 02']
        else np.busday_offset(
            x['data_referencia'].strftime('%Y-%m-%d'), 
            x['soma_acumulada'],
            weekmask='1111100',
            roll='forward'
        )
    ) if not (pd.isna(x['data_referencia']) or pd.isna(x['soma_acumulada'])) else np.nan,  # Se algum valor for NaN, retorna NaN
    axis=1
)





# %%
#Definindo qual é a data start de cada operação

programa_agrupado['Data Start'] = np.where( (programa_agrupado['ORDEM PLANTIO'] == 1) & (programa_agrupado['n_talhao'] == 1),
                                            programa_agrupado['Data Start'],
                                            programa_agrupado['fim_operacao'].shift(1))

# %%
programa_agrupado = mes_operacional(programa_agrupado, 'Data Start', 'Data Start_cop')

# %%
programa_agrupado = mes_operacional(programa_agrupado,'fim_operacao','fim_operacao_cop')

# %%
programa_agrupado = programa_agrupado.rename({
    'Nova EPS Plantio':'EPS Plantio',
    'Área(ha)': 'Área ha',
    'Rendimento':'Rendimento ha/dia',
    'ORDEM PLANTIO':'Ordem Plantio',
    'dias_operacao': 'Dias para operação',
    'dias_acumulados': 'Dias totais para operação e deslocamento',
    'fim_operacao' :'Data Final',
    'fim_operacao_cop': 'Data Final Mês Operacional'

}, axis=1)

# %%
programa_agrupado = programa_agrupado.drop(['soma_acumulada','data_referencia'],axis=1)

# %%
programa_agrupado.to_excel('sequenciamento.xlsx',index=False)


