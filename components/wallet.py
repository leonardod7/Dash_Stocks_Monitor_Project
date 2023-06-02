
# Importando Bibliotecas ==============================================================================================

from dash import html, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import json
from tvDatafeed.main import TvDatafeed

# importando de outras pages ==============================================================================================

from app import *



# Criando a função para gerar um card =================================================================================
# Cada transação é um novo card. Vamos declarar uma função que vai criar um novo card
def generate_card(info_do_ativo):
    new_card =  dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-list-alt', style={"fontSize": '85%'}), " Nome: "], className='textoQuartenario'),
                                        html.H5(str(info_do_ativo['ativo']), className='textoQuartenarioBranco')
                                    ], md=2, style={'text-align' : 'left'}),
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-database', style={"fontSize": '85%'}), " Quantidade: "], className='textoQuartenario'),
                                        html.H5(str(info_do_ativo['vol']), className='textoQuartenarioBranco')
                                    ], md=2, style={'text-align' : 'left'}),
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-money', style={"fontSize": '85%'}), " Unitário: "], className='textoQuartenario'),
                                        html.H5('{:,.2f}'.format(info_do_ativo['preco']), className='textoQuartenarioBranco')
                                    ], md=2, style={'text-align' : 'left'}),
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-calendar', style={"fontSize": '85%'}), " Data: "], className='textoQuartenario'),
                                        html.H5(str(info_do_ativo['date'])[:10], className='textoQuartenarioBranco')
                                    ], md=2, style={'text-align' : 'left'}),
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-handshake-o', style={"fontSize": '85%'}), " Tipo: "], className='textoQuartenario'),
                                        html.H5(str(info_do_ativo['tipo']), className='textoQuartenarioBranco')
                                    ], md=2, style={'text-align' : 'left'}),
                                    dbc.Col([
                                        html.H5([html.I(className='fa fa-money', style={"fontSize": '85%'}), " Total: "], className='textoQuartenario'),
                                        html.H5('{:,.2f}'.format(info_do_ativo['preco']*info_do_ativo['vol']), className='textoQuartenarioBranco'), # estamos colocando {:,.2f} para formatar em 2 dígitos o valor float
                                    ], md=2, style={'text-align' : 'left'}),
                                ]),
                            ], md=11, xs=6, style={'text-align' : 'left'}),
                            dbc.Col([
                                dbc.Button([html.I(className = "fa fa-trash header-icon",
                                                    style={'font-size' : '150%'})],
                                                    id={'type': 'delete_event', 'index': info_do_ativo['id']},
                                                    style={'background-color' : 'transparent', 'border-color' : 'transparent', 'padding' : '0px'}
                                                ),
                            ], md=1, xs=12, style={'text-align' : 'right'})
                        ])
                    ])
                ], class_name=info_do_ativo['class_card'])
            ])
        ], className='g-2 my-auto')

    return new_card


# Criando a função para gerar uma lista de card =======================================================================
def generate_list_of_cards(df):
    lista_de_dicts = []
    for row in df.index: # para todas as linhas que estiverem no nosso dataframe,
        infos = df.loc[row].to_dict() # pegar as informações de cada uma dessas linhas e transformamos para um dicionário
        # Vamos atribuir a classe dependendo do tipo de conta de cada ativo. Se for uma compra, vamos atribuir uma classe do CSS que vai pintar a borda do card de verde e se for venda, vermelho
        if infos['tipo'] == 'compra':
            infos['class_card'] = 'card_compra' # essa foi o nome da classe que demos no CSS para o que for compra
        else:
            infos['class_card'] = 'card_venda'
        # vamos atribuir o conteúdo da row, que são as informacoes do card
        lista_de_dicts.append(infos)
    # a lista de dicionários representa cada um, uma transação. Agora vamos criar uma lista de cards que conterá o conteúdo desses dicionários

    lista_de_cards = []
    for dicionario in lista_de_dicts:
        card = generate_card(dicionario) # estamos chamando a função para criar um card com cada um dos didionários dentro da lista de dicionários
        lista_de_cards.append(card)

    return lista_de_cards


# tv =================================================================================================================
tv = TvDatafeed()


# Criando card sem registros ==========================================================================================
card_sem_registros = dbc.Card([
                        dbc.CardBody([
                            html.Legend("Nenhum registro efetuado", className='textoQuartenarioBranco')
                        ])
                    ], className='card_sem_registros')



# layout ==============================================================================================================
layout = dbc.Container([
    dbc.Row([
        dbc.Col([

        ], md=12, id='layout_wallet', style={"height": '100',
                                             "maxHeight": '36rem',
                                             "overflow-y": 'auto'})
    ], className='g-2 my-auto')
], fluid=True) # fluid True para que ele ocupe toda a tela



# callback 1) =========================================================================================================

#call back auxiliar para ativar o layout da wallet
@app.callback(
    Output(component_id='layout_wallet', component_property='children'),
    Input(component_id='layout_data', component_property='data')
)
def func_auxiliar(data):
    return data


# callback 2) =========================================================================================================
# callback que realiza alterações nos ativos da wallet. Essa lógca é o que vai fazer ele abrir ou fechar e adicionar um ativo
@app.callback(
    Output(component_id='modal', component_property='is_open'), # o is open é para verificarmos se o modal está aberto ou fechado a partir do nosso click
    Output(component_id='book_data_store', component_property='data'), # toda vez que o usuário inserir umm novo ativo, ele tem que atualizar o book_data_store por meio do id
    Output(component_id='layout_data', component_property='data'), # esse output vai ser atualizado e servirá de entrada para o callback anterior

    Input(component_id='add_button', component_property='n_clicks'), # o botão do modal para adicionar um novo ativo (esse botão estará no header)
    Input(component_id='submit_cadastro', component_property='n_clicks'), # o botão de submit cadastro que está em modal. Que salva o novo ativo
    Input(component_id='book_data_store', component_property='data'), # toda vez que atualizarmos o nosso book_data_store ele terá que atualizar a nossa lista de cards
    Input(component_id={'type': 'delete_event', 'index': ALL}, component_property='n_clicks'), # esse input é o botão de apagar os ativos (nossos cards). Esse botão é gerado dinamicamente, quando adicionamos um novo
    # ativo. Cada vez que adicionamos, o botão vem junto do card. Esse botão não pode ter um id genérico, ele precisa estar relacionado especificamente com aquele card gerado. Dentro desse input temos um callback avançado
    # dinâmico. Observe que colocamos o index: ALL. Ele vai trigar sempre quando dermos um click na lixeira. Toda vez que clicarmos no id delete_event, ele vai pegar o index de todos os cards e vai identificar qual index foi clicado
    # e vai apagar ele por meio do delete_event.


    # Vamos definir o estado dos componentes, que é aquilo que não é trigado mas altera ela quando ela é trigada pelos inputs.

    State('nome_ativo', component_property='value'),
    State('modal', component_property='is_open'), # precisamos saber quando ele está aberto ou fechado
    State('compra_venda_radio', component_property='value'),# o botão que permite o tipo de operação está no modal
    State('preco_ativo', component_property='value'), # o valor preenchido
    State('data_ativo', component_property='date'), # o valor preenchido
    State('quantidade_ativo', component_property='value') # o valor preenchido
)
def funcao_modal(n1, n2, book_data, event, ativo, open, radio, preco, periodo, vol): # n1, n2 para identificar os primeiros inputs, quando é para adicionar e quando é para salvar os ativos
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0] # identificar qual foi o id trigado (click). ele vem como dicionário e pegaremos a classe dela e devemos separar para pegarmos o index do card que foi clicado
    df_book_data = pd.DataFrame(book_data)
    df_book_data = df_book_data.sort_values(by='date', ascending=True) # ordenar os valores, sempre em ordem crescente pela data


    lista_de_cards = generate_list_of_cards(df_book_data)

    #verifica se nao tem nenhum ativo na lista de cards, caso nao tiver nada retorna o card com a msg 'nenhum registro efetuado'
    if len(lista_de_cards) == 0: # ou seja, se não tivemos ativos cadastrados ele retorna um card vazio
        lista_de_cards = card_sem_registros
    if trigg_id == '': # toda vez que o nosso dash inicializa, ele triga os botões e ele vai trigar o botão de deletar. Se não verificarmos quando o trigg_id é vazio que quanto eu atualizo o callback, ele vai sempre deletar um valor
        # se não colocarmos uma condição para ele fazer isso. Ou seja, se o meu botão delete for clicado e eu não tiver nenhum valor selecionado nele, que é o que contece quando iniciamos o dash, não faremos nada.
        df_book_data = df_book_data.sort_values(by='date', ascending=True)
        return [open, book_data, lista_de_cards]

    # 1. Botão de abrir modal. Se o nosso trigg_id for for igual ao add_button (se clicarmos para abrir o modal). ele serve para verificar se o modal foi aberto, ele retorna o modal, os dados e a lista de cards
    if trigg_id == 'add_button':
        return [not open, book_data, lista_de_cards]

    # com o modal aberto, precisaremos veririfcar se o trigg é o botão de salvar (submit cadastro)

    # 2. Salvando ativo
    elif trigg_id == 'submit_cadastro':  # Corrigir caso de erro - None
        if None in [ativo, preco, vol] and open: # verificar se nenhum tivo foi adicionado. Se estiver vazio, ele não vai fazer nenhuma alteração
            return [open, book_data, lista_de_cards]
        else: # se o usuário tiver inserido um valor
            ativo = ativo.upper()
            if tv.search_symbol(ativo, 'BMFBOVESPA'): # toda vez que clicarmos no submit cadastro, ele vai verificar se esse ativo existe dentro da BMFBOVESPA. (se o ativo que o usuário inseriu existe na Bovespa)
                exchange = 'BMFBOVESPA'
                preco = round(preco, 2)
                df_book_data.loc[len(df_book_data)] = [periodo, preco, radio, ativo, exchange, vol, vol * preco] # vamos localizar nela, na última posição dela vamos atribuir todos os valores da lista que passamos
                df_book_data['date'] = pd.to_datetime(df_book_data['date'], format='%Y-%m-%d') # Vamos pegar os valores da data e formatar eles para garantir o mesmo formato
                df_book_data.reset_index(drop=True, inplace=True) # reset do índice
                df_book_data = df_book_data.sort_values(by='date', ascending=True) # ordenando por data

                df_book_data.to_csv('book_data.csv') # atualizar ele como um CSV para salvarmos ele dentro de um CSV
                book_data = df_book_data.to_dict() # Transformar em um dicionário

                lista_de_cards = generate_list_of_cards(df_book_data) # atualizar a lista de cards com o novo df

                return [not open, book_data, lista_de_cards]

            else:
                return [not open, book_data, lista_de_cards]

    # 3. Caso de delete de card. Verificar se existe um evento de deletar
    if 'delete_event' in trigg_id:
        trigg_dict = callback_context.triggered[0]

        #verifica se nao foi clicado na atualização inicial do callback para nao deletar nenhum card
        if trigg_dict['value'] == None:
            return [open, book_data, lista_de_cards]

        trigg_id = json.loads(trigg_id) # converte em formato json
        df_book_data.drop([str(trigg_id['index'])], inplace=True) # tirar o card que tiver o trigg_id acima
        df_book_data.reset_index(drop=True, inplace=True)
        df_book_data = df_book_data.sort_values(by='date', ascending=True)
        df_book_data.to_csv('book_data.csv')
        book_data = df_book_data.to_dict()
        lista_de_cards = generate_list_of_cards(df_book_data)

        if len(lista_de_cards) == 0:
            lista_de_cards = card_sem_registros

        return [open, book_data, lista_de_cards]

    return [open, book_data, lista_de_cards]




# TODO: json:  a biblioteca json iremos utilizar para fazermos a manipulação de dicionários. isso é mais para a questão do trigger id,
# quando clicar num botão ele conseguir trigar o valor que foi clicado e ai ele transforma isso em um dicionário para conseguirmos identificar qual
# foi o id clicado para a gente fazer o delete corretamente do botão que foi clicado.

# TODO: TvDatafeed - biblioteca onde iremos fazer a requisição de todo o histórico de dados das ações da bolsa