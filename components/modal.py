
# Importando Bibliotecas ==============================================================================================

from dash import dcc, Input, Output, no_update, callback_context
import dash_bootstrap_components as dbc
from datetime import date

# importando de outras pages ==============================================================================================

from app import *

# Estrutura do modal ==================================================================================================

layout = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de Ativos"), className='modal_header'),

    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Input(id='nome_ativo', placeholder='Nome', type='text')
            ]),
            dbc.Col([
                dbc.Input(id='preco_ativo', placeholder='Preco (R$)', type='number', min=0, step=0.01)
            ])
        ]),
        dbc.Row([
            dbc.Col([
                "Data:   ",
                dcc.DatePickerSingle( # adiciona o calendário
                    id='data_ativo',
                    className='dbc', # dbc ele importa a estilização do bootstrap
                    min_date_allowed=date(2005, 1, 1), # data mínima
                    max_date_allowed=date.today(), # data máxima, que no caso, é a data do dia
                    initial_visible_month=date(2017, 8, 5), # data de início por default
                    date=date.today() # data de início que vai aparecer quando abrirmos a janela, que é data do dia
                ),
            ], xs=6, md=6),
            dbc.Col([
                dbc.Input(id="quantidade_ativo", placeholder="Quantidade", type='number', min=0, step=1),
            ], xs=6, md=6)
        ], style={'margin-top': '1rem'}),
        dbc.Row([
            dbc.Col([
                dbc.RadioItems(id='compra_venda_radio',
                               options=[{"label": "Compra", "value": 'Compra'}, {"label": "Venda", "value": 'Venda'}],
                               value='Compra'), # value='Compra' valor default
            ], style={'padding-top': '20px'}),
        ])
    ], className='modal_body'),

    dbc.ModalFooter([
        dbc.Row([
            dbc.Col([dbc.Button("Salvar", id="submit_cadastro")])
        ])
    ], className='modal_footer'),

], id="modal", is_open=False, size='lg', centered=True)


# callback para abrir ele =============================================================================================
# que é o que vai fazer quando clicarmos no botão add

# Callback para checar o loading state
@app.callback(
    Output(component_id='submit_cadastro', component_property='children'),
    Input(component_id='submit_cadastro', component_property='n_clicks'),
    Input(component_id='add_button', component_property='n_clicks'),
)
def add_spinner(n, n2):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    print(trigg_id)

    if trigg_id == 'submit_cadastro':
        return [dbc.Spinner(size="sm"), " Processando registro"]
    elif trigg_id == 'add_button':
        return "Salvar"
    else:
        return no_update

# observe que o que triga o nosso comando é o botão add ou o nosso botão de submit