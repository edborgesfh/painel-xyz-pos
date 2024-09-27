from dash import Dash, html, dcc, Input, Output, clientside_callback
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

# Leitura do arquivo

# Carrega o DataFrame

df_cursos = pd.read_csv('df_cursos.csv')

df_cursos['data final'] = pd.to_datetime(df_cursos['data final'], format='ISO8601')
df_cursos['data inicial'] = pd.to_datetime(df_cursos['data inicial'], format='ISO8601')

# Estilo

## Para os Gráficos
grafico_config = {
    'showlegend': False,
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'margin': {'pad': 0}
}

## Para mudar o tema
color_mode_switch = html.Div(
    html.Span(
        [
            dbc.Label(className="fa fa-moon", html_for="switch"),
            dbc.Switch(id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
            dbc.Label(className="fa fa-sun", html_for="switch"),
        ], className='ms-3 mt-3',
    )
)

load_figure_template(['journal', 'journal_dark'])

# Configuração do aplicativo
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.FONT_AWESOME, '/assets/styles.css'])

server = app.server

titulo_div = [
    html.Div(
        [
            html.H5('Painel — Pós-Graduações',
                    id='titulo',
                    className='titulos m-0'),
            html.P('Bittar Unicorp',
                   id='subtitulo',
                   className='subtitulos m-1')
        ], className='p-2'
    )
]

filtro_cursos = [
    html.Div(
        [
            dcc.Dropdown(id='filtro-curso',
                         options=[
                             {'label': curso, 'value': curso}
                             for curso in df_cursos['curso'].unique()
                         ],
                         placeholder='Selecione o Curso',
                         value=None,
                         multi=True,
                         searchable=True,
                         className='dropdown'
                         )
        ], className='p-2'
    )
]

filtro_modulo = [
    html.Div(
        [
            dcc.Dropdown(id='filtro-modulo',
                         options=[
                             {'label': modulo, 'value': modulo, }
                             for modulo in df_cursos['curso'].unique()
                         ],
                         placeholder='Selecione o Módulo',
                         value=None,
                         multi=True,
                         searchable=True,
                         className='dropdown',
                         )
        ], className='p-2',
    )
]

card_3_geral = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                id='geral',
                config={'responsive': True},
            )
        ], className='p-0',
    ), id='card-3-geral', className='dbc-card',
)

card_4_gantt = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                id='gantt',
                config={'responsive': True},
            )
        ], className='p-0',
    ), id='card-4-gantt'
)

card_5_linhas = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='g-linhas',
                      config={'responsive': True}
                      )
        ], className='p-2'
    ), id='card-5-linhas'
)

card_6_indicadores = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([dcc.Graph(id='g-progresso', config={'responsive': True})], width=12)
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='g-duracao', config={'responsive': True})], width=12)
            ]),
        ], className='p-2'
    ), id='card-6-indicadores'
)

card_7_barras = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='g-barras',
                      config={'responsive': True}
                      )
        ], className='p-2'
    ), id='card-7-barras'
)

card_8_professores = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(id='g-professores',
                      config={'responsive': True}
                      )
        ], className='p-2'
    ), id='card-8-professores'
)

card_9_responsavel = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                dcc.Graph(id='g-responsavel',
                          config={'responsive': True},
                          ),
                style={'height': '400px', 'overflowY': 'auto'}
            )
        ], className='p-2'
    ), id='card-9-responsavel'
)

linha_1 = dbc.Row(
    [
        dbc.Col(color_mode_switch, width=1),
        dbc.Col(titulo_div, width=3),
        dbc.Col(filtro_cursos, width=4),
        dbc.Col(filtro_modulo, width=4)

    ], className='w-100 g-2 mt-1'
)

linha_2 = dbc.Row(
    [
        dbc.Col(card_3_geral)
    ], id='linha-2', className='w-100 g-2 mt-1'
)

linha_3 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_4_gantt)),
    ], id='linha-3', className='w-100 g-2 mt-1',
)

linha_4 = dbc.Row(
    [
        dbc.Col(card_5_linhas, width=8),
        dbc.Col(card_6_indicadores, width=4)
    ], id='linha-4', className='w-100 g-2 mt-1',
)

linha_5 = dbc.Row(
    [
        dbc.Col(card_7_barras, width=4),
        dbc.Col(card_8_professores, width=4),
        dbc.Col(card_9_responsavel, width=4),

    ], id='linha-5', className='w-100 g-2 mt-1',
)

app.layout = dbc.Container(
    [
        linha_1,
        linha_2,
        linha_3,
        linha_4,
        linha_5
    ], className='g-2',
)

# Callbacks

# Callbacks
## Callback para atualizar o gráfico geral  #
@app.callback(
    Output('geral', 'figure'),
    Input('color-mode-switch', 'value'),
)
##Geral
def gerar_grafico_geral(switch_on):
### Operação com o df para gerar o gráfico
    aulas_prontas = df_cursos[df_cursos['progresso'] == 100]
    aulas_prontas = aulas_prontas.groupby(['data final', 'curso', 'Módulo'])['Aula'].sum().reset_index()
    aulas_prontas['Aula'] = 1
    aulas_prontas = aulas_prontas.sort_values(by=['curso', 'data final'])
    aulas_prontas['aulas prontas'] = aulas_prontas.groupby(['curso'])['Aula'].cumsum() 
   
### Plotagem do gráfico
    g_geral = px.line(aulas_prontas,
                      height=600,
                      x='data final',
                      y='aulas prontas',
                      color='curso',
                      hover_data={'Aula': True}
                      )

    g_geral.update_layout(grafico_config, showlegend=True,
                          legend=dict(title='Cursos', yanchor='top', y=0.90, xanchor='left', x=0.10),
                          title={'text': 'Progresso de Aulas Finalizadas por Curso', 'x': 0.5})

    g_geral.update_yaxes(title='Aulas Finalizadas')
    g_geral.update_xaxes(title=None, rangeslider=dict(visible=True, thickness=0.07))

    g_geral.update_traces(mode='lines+markers',
                          customdata=np.stack(
                              (aulas_prontas['curso'], aulas_prontas['Módulo'], aulas_prontas['Aula']),
                              axis=-1),
                          hovertemplate='Módulo %{customdata[1]}<br>'
                                        'Aula: %{customdata[2]}<br>'
                                        'Concluída em %{x}<br>'
                          )

### Modificações de tema no gráfico
    template = pio.templates['journal'] if switch_on else pio.templates['journal_dark']
    g_geral.update_layout(template=template)
### Retorno
    return g_geral

## Callback para atualizar os gráficos
@app.callback(
    Output('gantt', 'figure'),
    Output('g-linhas', 'figure'),
    Output('g-progresso', 'figure'),
    Output('g-duracao', 'figure'),
    Output('g-barras', 'figure'),
    Output('g-professores', 'figure'),
    Output('g-responsavel', 'figure'),
    Input('filtro-modulo', 'value'),
    Input('filtro-curso', 'value'),
    Input('color-mode-switch', 'value'),
)

def atualizar_graficos(modulo_selecionado, curso_selecionado, switch_on):
##  Manipulando df para gerar os gráficos  ##
    df_filtrado = df_cursos.copy()
    if curso_selecionado:
        df_filtrado = df_filtrado[df_filtrado['curso'].isin(curso_selecionado)]
    if modulo_selecionado:
        df_filtrado = df_filtrado[df_filtrado['Módulo'].isin(modulo_selecionado)]
## Gantt
### Plotando
    gantt = px.timeline(df_filtrado,
                        height=600,
                        x_start='data inicial',
                        x_end='data final',
                        y='Aula',
                        color='progresso',
                        color_continuous_scale=['rgb(0,32,255)', 'rgb(1,255,176)', 'rgb(51,254,0)', 'rgb(34,201,8)'],
                        hover_data={'ID': True, 'Aula': True, 'Módulo': True, 'Responsável': True, 'Etapa': True}
                        )

    gantt.update_layout(title={'text': 'Linha do tempo — Produção das Aulas', 'x': 0.5})
    gantt.update_yaxes(autorange='reversed', title='Aulas',)
    gantt.update_xaxes(title=None, rangeslider=dict(visible=True, thickness=0.07))
    gantt.update_coloraxes(showscale=False)
    gantt.update_traces(marker_line_width=0)

    gantt.update_traces(customdata=np.stack((df_filtrado['Módulo'], df_filtrado['Etapa'],
                                             df_filtrado['Responsável']), axis=-1),
                        hovertemplate='<b>Aula %{y}</b><br>'
                                      'Módulo %{customdata[0]}<br>'
                                      'Início: %{base}<br>'
                                      'Término: %{x}<br>'
                                      'Etapa: %{customdata[1]}<br>'
                                      'Responsável: %{customdata[2]}<br>'
                        )

## Linhas e Indicadores
### Configurando

    df_linhas = df_filtrado.sort_values(by=['Aula', 'ordem_etapa', 'data final'])
### Plotando
    g_linhas = px.line(df_linhas,
                       height=400,
                       x='data final',
                       y='progresso',
                       color='Aula',
                       markers=True,
                       hover_data={'ID': False, 'Aula': True, 'Módulo': True}
                       )

    g_linhas.update_layout(grafico_config,
                           margin=dict(b=20),
                           title={'text': 'Progresso das aulas', 'x': 0.5},
                           )
    g_linhas.update_yaxes(title='Progresso (%)', range=[0, 100])
    g_linhas.update_xaxes(showgrid=False, title=None,
                          rangeslider=dict(visible=True, thickness=0.15))

    g_linhas.update_traces(
        hovertemplate='<b>Data</b> %{x}<br>'
                      '<b>Progresso</b> %{y:.0f}%<br>'  # '.0f' formata como inteiro
                      '<b>Aula</b> %{customdata[1]}<br>'  # 'Aula' está em customdata[1]
                      '<b>Módulo</b> %{customdata[2]}<br>'  # 'Módulo' está em customdata[2]
    )

### Configurando indicador progresso
    df_progresso = df_filtrado.groupby('Aula')['progresso'].max().mean()
### Plotando
    g_progresso = go.Figure()
    g_progresso.add_trace(go.Indicator(
        value=df_progresso,
        mode='gauge+number',
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]}},

    ))

    g_progresso.update_layout(grafico_config,
                              height=200,
                              margin=dict(b=10, t=50),
                              title={'text': 'Progresso Total (%)', 'x': 0.5},
                              )

### Configurando indicador duração
    data_min = df_filtrado.groupby('Aula')['data inicial'].min()
    data_max = df_filtrado.groupby('Aula')['data final'].max()
    duracao = data_max - data_min

    def cor_gauge_duracao(duracao):
        if duracao <= 45:
            return 'green'
        elif 45 < duracao <= 90:
            return 'blue'
        else:
            return 'red'
###Plotando
    g_duracao = go.Figure()
    g_duracao.add_trace(go.Indicator(
        value=duracao.mean().days,
        mode='gauge+number',
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, duracao.max().days]},
               'bar': {'color': cor_gauge_duracao(duracao.mean().days)}}

    ))

    g_duracao.update_layout(grafico_config,
                              height=200,
                              margin=dict(b=10, t=50),
                              title={'text': 'Produção (dias)', 'x': 0.5},
                              )

##  Barras (3)
### Modificação para Aula por Status
    aulas_status = df_filtrado.groupby(['curso', 'Módulo', 'Aula', 'status']).agg({'data final': 'max'}).reset_index()
    aulas_status = aulas_status.drop(columns=['data final'])
    aulas_status = aulas_status.groupby(['status']).size().to_frame(name='Aula').reset_index()
### Plotando
    g_barras = px.bar(
        aulas_status,
        x='status',
        y='Aula',
        labels=False,
        color='status',
        color_discrete_map={'CONCLUÍDA': 'green',
                            'EM ANDAMENTO': 'blue',
                            'PENDENTE': 'gray'},
        text_auto=True,
        hover_data=None,
    )

    g_barras.update_layout(grafico_config,
                           height=400,
                           margin=dict(r=20, l=20, b=20, t=50),
                           title={'text': 'Aulas por Status', 'x': 0.5},
                           )
    g_barras.update_yaxes(showticklabels=False, showgrid=False, title=None, zeroline=False)
    g_barras.update_xaxes(title=None)
    g_barras.update_traces(textfont_size=20, )

### Modificação para Aulas por Professor(a)
    professor_aulas = df_filtrado.groupby(['curso', 'Professor', 'Módulo', 'Aula', 'status']).agg({'data final': 'max'})
    professor_aulas = professor_aulas.reset_index()
    professor_aulas = professor_aulas.groupby(['curso', 'Professor', 'Módulo', 'status']).size().to_frame(name='Aula')
    professor_aulas = professor_aulas.reset_index()
### Plotando
    g_professores = px.bar(
        professor_aulas,
        y='Professor',
        x='Aula',
        color='status',
        orientation='h',
        color_discrete_map={
            'CONCLUÍDA': 'green',
            'EM ANDAMENTO': 'blue',
            'PENDENTE': 'gray',
        },
        hover_data={'Módulo': True, 'status': False, 'Aula': True},
        text_auto=True,
    )

    g_professores.update_layout(grafico_config,
                                height=400,
                                margin=dict(r=20, l=20, b=20, t=50),
                                title={'text': 'Aulas por professor(a)', 'x': 0.5},
                                )

    g_professores.update_xaxes(showticklabels=False, showgrid=False, title=None, zeroline=False)
    g_professores.update_yaxes(title=None)
    g_professores.update_traces(textfont_size=12,
                                customdata=np.stack((professor_aulas['Módulo'],
                                                     professor_aulas['Aula']), axis=-1),
                                hovertemplate='<b>Professor(a) %{y}</b><br>'
                                              'Módulo %{customdata[0]}<br>'
                                              '%{x} aulas<br>')

### Modificação para Subtarefas por responsável
    responsavel_subtarefas = df_filtrado.groupby(['Responsável', 'Módulo', 'status']).size().to_frame(
        name='Número de subtarefas')
    responsavel_subtarefas = responsavel_subtarefas.reset_index()

    ordem_responsavel = responsavel_subtarefas.groupby('Responsável')['Número de subtarefas'].sum()
    ordem_responsavel = ordem_responsavel.sort_values(ascending=True).index
### Plotando
    g_responsavel = px.bar(
        responsavel_subtarefas,
        y='Responsável',
        x='Número de subtarefas',
        color='status',
        orientation='h',
        color_discrete_map={
            'CONCLUÍDA': 'green',
            'EM ANDAMENTO': 'blue',
            'PENDENTE': 'gray',
        },
        hover_data={'Módulo': True, 'status': False},
        text_auto=True
    )

    g_responsavel.update_layout(grafico_config,
                                height=1200,
                                margin=dict(r=20, l=20, b=20, t=50),
                                title={'text': 'Subtarefas por Responsável', 'x': 0.5},
                                )

    g_responsavel.update_xaxes(showticklabels=False, showgrid=False, title=None, zeroline=False)
    g_responsavel.update_yaxes(title=None, categoryorder='array', categoryarray=ordem_responsavel)
    g_responsavel.update_traces(textfont_size=12, )
    g_responsavel.update_traces(customdata=np.stack((responsavel_subtarefas['Responsável'],
                                                     responsavel_subtarefas['Módulo'],
                                                     responsavel_subtarefas['Responsável']), axis=-1),
                                hovertemplate='<b>%{y}</b> <br>'
                                              'Módulo %{customdata[1]}<br>'
                                              'Subtarefas: %{x}<br>'
                                )

### Modificações de tema nos gráficos
    template = pio.templates['journal'] if switch_on else pio.templates['journal_dark']
    gantt.update_layout(template=template)
    g_linhas.update_layout(template=template)
    g_progresso.update_layout(template=template)
    g_duracao.update_layout(template=template)
    g_barras.update_layout(template=template)
    g_professores.update_layout(template=template)
    g_responsavel.update_layout(template=template)

### Retorno
    return (gantt,
            g_linhas,
            g_progresso,
            g_duracao,
            g_barras,
            g_professores,
            g_responsavel
            )

## Callback para controlar a visibilidade dos elementos
@app.callback([
    Output('filtro-modulo', 'style'),
    Output('card-3-geral', 'style'),
    Output('card-4-gantt', 'style'),
    Output('card-5-linhas', 'style'),
    Output('card-6-indicadores', 'style'),
    Output('card-7-barras', 'style'),
    Output('card-8-professores', 'style'),
    Output('card-9-responsavel', 'style'),
],
    Input('filtro-curso', 'value'),
)
def controlar_visibilidade(curso_selecionado):
    if curso_selecionado:
        return (
            {'display': 'block'},  # dropdown de módulo
            {'display': 'none'},  # gráfico geral na linha_2
            {'display': 'block'},  # gantt na Linha_3
            {'display': 'block'}, {'display': 'block'},  # g_linha e g_indicadores na linha_4
            {'display': 'block'}, {'display': 'block'}, {'display': 'block'} # gráficos de barras na linha_5
        )
    else:
        return (
            {'display': 'none'},
            {'display': 'block'},
            {'display': 'none'},
            {'display': 'none'}, {'display': 'none'},
            {'display': 'none'}, {'display': 'none'}, {'display': 'none'},
        )

## Callback para atualizar as opções do dropdown de módulo
@app.callback(
    Output('filtro-modulo', 'options'),
    [Input('filtro-curso', 'value')]
)
def atualizar_opcoes_modulo(curso_selecionado):
    # Retorna todos os módulos se nenhum curso for selecionado
    if curso_selecionado is None:
        return [{'label': modulo, 'value': modulo} for modulo in df_cursos['Módulo'].unique()]
    else:
        modulos_unicos = df_cursos[df_cursos['curso'].isin(curso_selecionado)]['Módulo'].unique()
        return [{'label': modulo, 'value': modulo} for modulo in modulos_unicos]

## Callback para mudar o tema
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output('color-mode-switch', 'id'),
    Input('color-mode-switch', 'value'),
)
# Exercutar o app
if __name__ == '__main__':
    app.run(debug=True, port=8066)
