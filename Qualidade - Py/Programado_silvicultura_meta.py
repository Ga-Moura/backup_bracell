import pandas as pd
import os
from time import sleep

print("O script rodando é o arquivo de metas")


meta = r"F:\Qualidade_Florestal\01- SÃO PAULO\10- Planejamento e Controle 2°nível\2023\01 - Silvicultura\02- Processamento\01 - Metas"


# Inicializa um dataframe vazio para armazenar a concatenação
df = pd.DataFrame()

for root, dirs, files in os.walk(meta):
    for file in files:
        if "programado" in file.lower() and not "~" in file:
            file_path = os.path.join(root, file)
            tabelas = pd.read_excel(file_path, sheet_name='export', header=6)
            tabelas["Nome origem"] = file
            df = pd.concat([df, tabelas], axis=0, ignore_index=True)


df.to_excel(r"F:/Qualidade_Florestal/03- ADMINISTRATIVO/2023/06- COLABORADORES/Gabriel/1 - Processamento de dados/Programado Silvicultura - Meta.xlsx")


print("O script foi executado com sucesso!")


sleep(5)
