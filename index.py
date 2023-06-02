
# Importando Bibliotecas ==============================================================================================
from dash import dcc

# importando de outras pages ==============================================================================================

from components import home, header, wallet, fixed_row
from app import *
from funcoes.functions import *

# Armazenagem dos ativos ==============================================================================================

# Vamos tentar ler um arquivo que inicialmente nao existe (na primeira vez que rodamos ele não existe). Se ele não existir
# vamos criar um com as colunas determinadas. Observe que nesse primeiro try, ele tentará ler os arquivos que estão armazenados
# os meus ativos, que o usuário cadastrou. Porém, precisamos também tentar ler um outro arquivo que vai ser o histórico completo da bolsa

ativo_org = {}
try:
    df_book = pd.read_csv('book_data.csv', index_col=0)
    ativo_org = iterar_sobre_df_book(df_book)
except:
    df_book = pd.DataFrame(columns= ['date', 'preco', 'tipo', 'ativo', 'echange', 'vol', 'valor_total'])

try:
    df_historical_data = pd.read_csv('historical_data.csv', index_col=0)
except:
    df_historical_data = pd.DataFrame(columns= ['datetime', 'symbol', 'close'])

df_historical_data = atualizar_historical_data(df_historical_data, ativo_org)

# precisamos transformar os df acima em dicionários
df_historical_data = df_historical_data.to_dict()
df_book = df_book.to_dict()

# app layout =========================================================================================================

app.layout = dbc.Container([
    dcc.Location(id='url'),
    dcc.Store(id='book_data_store', data=df_book, storage_type='memory'),
    dcc.Store(id='historical_data_store', data=df_historical_data, storage_type='memory'),
    dcc.Store(id='layout_data', data=[], storage_type='memory'),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    header.layout
                ], className= 'header_layout'),
            ]),
            dbc.Row([
                dbc.Col([
                   fixed_row.layout
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                ]),
            ],id="page-content"),
        ])
    ])
], fluid=True)




if __name__ == "__main__":
    app.run_server(debug=True, port=8050)