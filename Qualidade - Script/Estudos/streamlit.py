{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st \n",
    "import pandas as pd\n",
    "import plotly.express as px"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "path = r\"F:\\Qualidade_Florestal\\01- SÃO PAULO\\10- Planejamento e Controle 2°nível\\2023\\14 - Cadastro Florestal\\Cadastro Florestal.xlsx\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_excel(path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Id</th>\n",
       "      <th>Tipo Propriedade</th>\n",
       "      <th>Cód. Região</th>\n",
       "      <th>Região</th>\n",
       "      <th>Id Projeto</th>\n",
       "      <th>Projeto</th>\n",
       "      <th>Localidade</th>\n",
       "      <th>Talhão</th>\n",
       "      <th>Ciclo</th>\n",
       "      <th>Rotação</th>\n",
       "      <th>...</th>\n",
       "      <th>Reg Oper Colheita</th>\n",
       "      <th>Reg Oper Silvicultura</th>\n",
       "      <th>Região Climática</th>\n",
       "      <th>Terra</th>\n",
       "      <th>Bioma</th>\n",
       "      <th>Classe</th>\n",
       "      <th>#FlagCTOVirtual</th>\n",
       "      <th>Registro</th>\n",
       "      <th>Ativo</th>\n",
       "      <th>Projeto e Talhão</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>53868</td>\n",
       "      <td>Próprio</td>\n",
       "      <td>1</td>\n",
       "      <td>BRACELL SP</td>\n",
       "      <td>1</td>\n",
       "      <td>MAMEDINA</td>\n",
       "      <td>Brasil \\ SP \\ Lençóis Paulista</td>\n",
       "      <td>1</td>\n",
       "      <td>4.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>Lençóis Paulista</td>\n",
       "      <td>Central</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>Current</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>N</td>\n",
       "      <td>29/11/2021</td>\n",
       "      <td>A</td>\n",
       "      <td>1001</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>21432</td>\n",
       "      <td>Próprio</td>\n",
       "      <td>1</td>\n",
       "      <td>BRACELL SP</td>\n",
       "      <td>1</td>\n",
       "      <td>MAMEDINA</td>\n",
       "      <td>Brasil \\ SP \\ Lençóis Paulista</td>\n",
       "      <td>2</td>\n",
       "      <td>4.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>Lençóis Paulista</td>\n",
       "      <td>Central</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>Current</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>N</td>\n",
       "      <td>08/01/2020</td>\n",
       "      <td>A</td>\n",
       "      <td>1002</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>11228</td>\n",
       "      <td>Próprio</td>\n",
       "      <td>1</td>\n",
       "      <td>BRACELL SP</td>\n",
       "      <td>1</td>\n",
       "      <td>MAMEDINA</td>\n",
       "      <td>Brasil \\ SP \\ Lençóis Paulista</td>\n",
       "      <td>3</td>\n",
       "      <td>4.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>Lençóis Paulista</td>\n",
       "      <td>Central</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>Current</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>N</td>\n",
       "      <td>03/01/2020</td>\n",
       "      <td>A</td>\n",
       "      <td>1003</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>48142</td>\n",
       "      <td>Próprio</td>\n",
       "      <td>1</td>\n",
       "      <td>BRACELL SP</td>\n",
       "      <td>1</td>\n",
       "      <td>MAMEDINA</td>\n",
       "      <td>Brasil \\ SP \\ Lençóis Paulista</td>\n",
       "      <td>4</td>\n",
       "      <td>4.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>Lençóis Paulista</td>\n",
       "      <td>Central</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>Current</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>N</td>\n",
       "      <td>18/06/2021</td>\n",
       "      <td>A</td>\n",
       "      <td>1004</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>48267</td>\n",
       "      <td>Próprio</td>\n",
       "      <td>1</td>\n",
       "      <td>BRACELL SP</td>\n",
       "      <td>1</td>\n",
       "      <td>MAMEDINA</td>\n",
       "      <td>Brasil \\ SP \\ Lençóis Paulista</td>\n",
       "      <td>5</td>\n",
       "      <td>4.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>...</td>\n",
       "      <td>Lençóis Paulista</td>\n",
       "      <td>Central</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>Current</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>CZ2</td>\n",
       "      <td>N</td>\n",
       "      <td>18/06/2021</td>\n",
       "      <td>A</td>\n",
       "      <td>1005</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30671</th>\n",
       "      <td>89184</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2</td>\n",
       "      <td>BRACELL MS</td>\n",
       "      <td>6387</td>\n",
       "      <td>BOM RETIRO</td>\n",
       "      <td>Brasil \\ MS \\ Ribas do Rio Pardo</td>\n",
       "      <td>502</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>...</td>\n",
       "      <td>Ribas do Rio Pardo</td>\n",
       "      <td>MS</td>\n",
       "      <td>CZ3</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>NaN</td>\n",
       "      <td>N</td>\n",
       "      <td>14/06/2023</td>\n",
       "      <td>A</td>\n",
       "      <td>6387502</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30672</th>\n",
       "      <td>89180</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2</td>\n",
       "      <td>BRACELL MS</td>\n",
       "      <td>6387</td>\n",
       "      <td>BOM RETIRO</td>\n",
       "      <td>Brasil \\ MS \\ Santa Rita do Pardo</td>\n",
       "      <td>503</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>...</td>\n",
       "      <td>Ribas do Rio Pardo</td>\n",
       "      <td>MS</td>\n",
       "      <td>CZ3</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>NaN</td>\n",
       "      <td>N</td>\n",
       "      <td>14/06/2023</td>\n",
       "      <td>A</td>\n",
       "      <td>6387503</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30673</th>\n",
       "      <td>89179</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2</td>\n",
       "      <td>BRACELL MS</td>\n",
       "      <td>6387</td>\n",
       "      <td>BOM RETIRO</td>\n",
       "      <td>Brasil \\ MS \\ Santa Rita do Pardo</td>\n",
       "      <td>504</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>...</td>\n",
       "      <td>Ribas do Rio Pardo</td>\n",
       "      <td>MS</td>\n",
       "      <td>CZ3</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>NaN</td>\n",
       "      <td>N</td>\n",
       "      <td>14/06/2023</td>\n",
       "      <td>A</td>\n",
       "      <td>6387504</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30674</th>\n",
       "      <td>89181</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2</td>\n",
       "      <td>BRACELL MS</td>\n",
       "      <td>6387</td>\n",
       "      <td>BOM RETIRO</td>\n",
       "      <td>Brasil \\ MS \\ Santa Rita do Pardo</td>\n",
       "      <td>507</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>...</td>\n",
       "      <td>Ribas do Rio Pardo</td>\n",
       "      <td>MS</td>\n",
       "      <td>CZ3</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>NaN</td>\n",
       "      <td>N</td>\n",
       "      <td>14/06/2023</td>\n",
       "      <td>A</td>\n",
       "      <td>6387507</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>30675</th>\n",
       "      <td>95501</td>\n",
       "      <td>NaN</td>\n",
       "      <td>2</td>\n",
       "      <td>BRACELL MS</td>\n",
       "      <td>6387</td>\n",
       "      <td>BOM RETIRO</td>\n",
       "      <td>Brasil \\ MS \\ Santa Rita do Pardo</td>\n",
       "      <td>509</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>...</td>\n",
       "      <td>Ribas do Rio Pardo</td>\n",
       "      <td>MS</td>\n",
       "      <td>CZ3</td>\n",
       "      <td>NaN</td>\n",
       "      <td>Cerrado</td>\n",
       "      <td>NaN</td>\n",
       "      <td>N</td>\n",
       "      <td>22/09/2023</td>\n",
       "      <td>A</td>\n",
       "      <td>6387509</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>30676 rows × 57 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "          Id Tipo Propriedade  Cód. Região      Região  Id Projeto  \\\n",
       "0      53868          Próprio            1  BRACELL SP           1   \n",
       "1      21432          Próprio            1  BRACELL SP           1   \n",
       "2      11228          Próprio            1  BRACELL SP           1   \n",
       "3      48142          Próprio            1  BRACELL SP           1   \n",
       "4      48267          Próprio            1  BRACELL SP           1   \n",
       "...      ...              ...          ...         ...         ...   \n",
       "30671  89184              NaN            2  BRACELL MS        6387   \n",
       "30672  89180              NaN            2  BRACELL MS        6387   \n",
       "30673  89179              NaN            2  BRACELL MS        6387   \n",
       "30674  89181              NaN            2  BRACELL MS        6387   \n",
       "30675  95501              NaN            2  BRACELL MS        6387   \n",
       "\n",
       "          Projeto                         Localidade  Talhão  Ciclo  Rotação  \\\n",
       "0        MAMEDINA     Brasil \\ SP \\ Lençóis Paulista       1    4.0      1.0   \n",
       "1        MAMEDINA     Brasil \\ SP \\ Lençóis Paulista       2    4.0      1.0   \n",
       "2        MAMEDINA     Brasil \\ SP \\ Lençóis Paulista       3    4.0      1.0   \n",
       "3        MAMEDINA     Brasil \\ SP \\ Lençóis Paulista       4    4.0      1.0   \n",
       "4        MAMEDINA     Brasil \\ SP \\ Lençóis Paulista       5    4.0      1.0   \n",
       "...           ...                                ...     ...    ...      ...   \n",
       "30671  BOM RETIRO   Brasil \\ MS \\ Ribas do Rio Pardo     502    NaN      NaN   \n",
       "30672  BOM RETIRO  Brasil \\ MS \\ Santa Rita do Pardo     503    NaN      NaN   \n",
       "30673  BOM RETIRO  Brasil \\ MS \\ Santa Rita do Pardo     504    NaN      NaN   \n",
       "30674  BOM RETIRO  Brasil \\ MS \\ Santa Rita do Pardo     507    NaN      NaN   \n",
       "30675  BOM RETIRO  Brasil \\ MS \\ Santa Rita do Pardo     509    NaN      NaN   \n",
       "\n",
       "       ...   Reg Oper Colheita Reg Oper Silvicultura Região Climática  \\\n",
       "0      ...    Lençóis Paulista               Central              CZ2   \n",
       "1      ...    Lençóis Paulista               Central              CZ2   \n",
       "2      ...    Lençóis Paulista               Central              CZ2   \n",
       "3      ...    Lençóis Paulista               Central              CZ2   \n",
       "4      ...    Lençóis Paulista               Central              CZ2   \n",
       "...    ...                 ...                   ...              ...   \n",
       "30671  ...  Ribas do Rio Pardo                    MS              CZ3   \n",
       "30672  ...  Ribas do Rio Pardo                    MS              CZ3   \n",
       "30673  ...  Ribas do Rio Pardo                    MS              CZ3   \n",
       "30674  ...  Ribas do Rio Pardo                    MS              CZ3   \n",
       "30675  ...  Ribas do Rio Pardo                    MS              CZ3   \n",
       "\n",
       "         Terra    Bioma Classe #FlagCTOVirtual    Registro Ativo  \\\n",
       "0      Current  Cerrado    CZ2               N  29/11/2021     A   \n",
       "1      Current  Cerrado    CZ2               N  08/01/2020     A   \n",
       "2      Current  Cerrado    CZ2               N  03/01/2020     A   \n",
       "3      Current  Cerrado    CZ2               N  18/06/2021     A   \n",
       "4      Current  Cerrado    CZ2               N  18/06/2021     A   \n",
       "...        ...      ...    ...             ...         ...   ...   \n",
       "30671      NaN  Cerrado    NaN               N  14/06/2023     A   \n",
       "30672      NaN  Cerrado    NaN               N  14/06/2023     A   \n",
       "30673      NaN  Cerrado    NaN               N  14/06/2023     A   \n",
       "30674      NaN  Cerrado    NaN               N  14/06/2023     A   \n",
       "30675      NaN  Cerrado    NaN               N  22/09/2023     A   \n",
       "\n",
       "      Projeto e Talhão  \n",
       "0                 1001  \n",
       "1                 1002  \n",
       "2                 1003  \n",
       "3                 1004  \n",
       "4                 1005  \n",
       "...                ...  \n",
       "30671          6387502  \n",
       "30672          6387503  \n",
       "30673          6387504  \n",
       "30674          6387507  \n",
       "30675          6387509  \n",
       "\n",
       "[30676 rows x 57 columns]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.1"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
