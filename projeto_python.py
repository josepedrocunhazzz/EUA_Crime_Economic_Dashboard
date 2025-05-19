from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
from datetime import datetime

# Configurações iniciais (mantidas da pagina principal)
#data_dir = '/Users/josecunha/Documents/Mestrado/Visualização Avançada de Dados/Projeto/Projeto/Dataset/Crime_by_state'
#economic_dir = '/Users/josecunha/Documents/Mestrado/Visualização Avançada de Dados/Projeto/Projeto/Dataset/economic_all_data'
#debug_file_path = '/Users/josecunha/Documents/Mestrado/Visualização Avançada de Dados/Projeto/Projeto/debug.txt'
#economic_file_path = '/Users/josecunha/Documents/Mestrado/Visualização Avançada de Dados/Projeto/Projeto/Dataset/economic_all_data/ecom_data.csv'


data_dir = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/Crime_by_state'
economic_dir = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/economic_all_data'
debug_file_path = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/debug.txt'
economic_file_path = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/economic_all_data/ecom_data.csv'

# Função para limpar o arquivo de debug
def reset_debug():
    with open(debug_file_path, 'w') as debug_file:
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        debug_file.write(f"=== DEBUG LOG - {date_time} ===\n\n")

# Chamar a função no inicio da execução
reset_debug()

# Função para debug
def write_debug(message):
    with open(debug_file_path, 'a') as debug_file:
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        debug_file.write(f"\n{date_time}: \n{message}\n")

# Dicionario de estados (mantido da pagina principal)
state_abbr = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

# Lista especifica de crimes que devem aparecer (mantida da pagina principal)
VALID_CRIMES = [
    "Aggravated Assault Reported by Population",
    "All Other Larceny Reported by Population",
    "Animal Cruelty Reported by Population",
    "Arson Reported by Population",
    "Assisting or Promoting Prostitution Reported by Population",
    "Betting_Wagering Reported by Population",
    "Bribery Reported by Population",
    "Burglary Reported by Population",
    "Counterfeiting_Forgery Reported by Population",
    "Credit Card_Automated Teller Machine Fraud Reported by Population",
    "Criminal Sexual Contact Reported by Population",
    "Destruction_Damage_Vandalism of Property Reported by Population",
    "Drug Equipment Violations Reported by Population",
    "Drug_Narcotic Violations Reported by Population",
    "Embezzlement Reported by Population",
    "Espionage Reported by Population",
    "Explosives Violation Reported by Population",
    "Export Violations Reported by Population",
    "Extortion_Blackmail Reported by Population",
    "Failure to Register as a Sex Offender Reported by Population",
    "False Citizenship Reported by Population",
    "False Pretenses_Swindle_Confidence Game Reported by Population",
    "Federal Liquor Offenses Reported by Population",
    "Federal Tobacco Offenses Reported by Population",
    "Flight to Avoid Deportation Reported by Population",
    "Flight to Avoid Prosecution Reported by Population",
    "Gambling Equipment Violation Reported by Population",
    "Hacking_Computer Invasion Reported by Population",
    "Harboring Escapee_Concealing from Arrest Reported by Population",
    "Homicide Reported by Population",
    "Human Trafficking, Commercial Sex Acts Reported by Population",
    "Human Trafficking, Involuntary Servitude Reported by Population",
    "Identity Theft Reported by Population",
    "Illegal Entry into the United States Reported by Population",
    "Impersonation Reported by Population",
    "Import Violations Reported by Population",
    "Incest Reported by Population",
    "Intimidation Reported by Population",
    "Justifiable Homicide Reported by Population",
    "Kidnapping_Abduction Reported by Population",
    "Larceny-theft Reported by Population",
    "Money Laundering Reported by Population",
    "Motor Vehicle Theft Reported by Population",
    "Murder and Nonnegligent Manslaughter Reported by Population",
    "Negligent Manslaughter Reported by Population",
    "Not Specified Reported by Population",
    "Operating_Promoting_Assisting Gambling Reported by Population",
    "Pocket-picking Reported by Population",
    "Pornography_Obscene Material Reported by Population",
    "Prostitution Reported by Population",
    "Purchasing Prostitution Reported by Population",
    "Purse-snatching Reported by Population",
    "Rape Reported by Population",
    "Re-entry after Deportation Reported by Population",
    "Robbery Reported by Population",
    "Shoplifting Reported by Population",
    "Simple Assault Reported by Population",
    "Smuggling Aliens Reported by Population",
    "Sports Tampering Reported by Population",
    "Statutory Rape Reported by Population",
    "Stolen Property Offenses Reported by Population",
    "Theft From Building Reported by Population",
    "Theft From Coin-Operated Machine or Device Reported by Population",
    "Theft From Motor Vehicle Reported by Population",
    "Theft of Motor Vehicle Parts or Accessories Reported by Population",
    "Treason Reported by Population",
    "Violation of National Firearm Act of 1934 Reported by Population",
    "Weapon Law Violations Reported by Population",
    "Weapons of Mass Destruction Reported by Population",
    "Welfare Fraud Reported by Population",
    "Wildlife Trafficking Reported by Population",
    "Wire Fraud Reported by Population"
]

# =============================================
# CARREGAMENTO E PROCESSAMENTO DOS DADOS (mantido da pagina principal)
# =============================================

data = []
crime_list = set()

for file in os.listdir(data_dir):
    if file.endswith('.csv'):
        try:
            state_name = file.replace('.csv', '')
            file_path = os.path.join(data_dir, file)
            
            if os.path.getsize(file_path) > 0:
                df = pd.read_csv(file_path, encoding='ISO-8859-1')
                
                if 'series' in df.columns:
                    df['series'] = df['series'].str.replace(r'_.*$', '', regex=True)
                    df = df[df['series'].isin(VALID_CRIMES)]
                    
                    if not df.empty:
                        crime_list.update(df['series'].unique())
                        df = df.dropna(axis=1, how='all')
                        
                        df_melted = df.melt(id_vars=['series'], var_name='Date', value_name='Value')
                        df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%m-%Y', errors='coerce')
                        df_melted = df_melted.dropna(subset=['Date'])
                        
                        df_melted['YearMonth'] = df_melted['Date'].dt.to_period('M')
                        df_melted['Year'] = df_melted['Date'].dt.year
                        df_melted['State'] = state_name
                        
                        data.append(df_melted)

        except Exception as e:
            write_debug(f"Erro ao processar arquivo {file}: {str(e)}")

if not data:
    raise ValueError("Nenhum dado valido foi carregado. Verifique os arquivos CSV no diretorio.")

df_map = pd.concat(data, ignore_index=True)
crime_list = sorted(crime_list)
months_available = sorted(df_map['YearMonth'].dropna().astype(str).unique())

# =============================================
# CARREGAMENTO E PROCESSAMENTO DOS DADOS ECONoMICOS (mantido da pagina principal)
# =============================================

economic_metrics_translation = {
    "weekly_earnings_yoy_percent_change": "Weekly Earnings",
    "total_employment_yoy_percent_change": "Total Employment",
    "retail_trade_employment_yoy_percent_change": "Retail Trade Employment",
    "public_employment_yoy_percent_change": "Public Employment",
    "private_employment_yoy_percent_change": "Private Employment",
    "manufacturing_employment_yoy_percent_change": "Manufacturing Employment",
    "retail_trade_state_gdp_yoy_percent_change": "Retail Trade GDP",
    "manufacturing_state_gdp_yoy_percent_change": "Manufacturing GDP",
    "government_state_gdp_yoy_percent_change": "Government GDP",
    "accommodation_and_food_services_state_gdp_yoy_percent_change": "Accommodation and Food Services GDP",
    "house_price_index_yoy_percent_change": "House Prices"
}

# Lista de metricas economicas que queremos usar
VALID_ECONOMIC_METRICS = list(economic_metrics_translation.keys())

# Caminho para o arquivo consolidado
#economic_file_path = '/Users/josecunha/Documents/Mestrado/Visualização Avançada de Dados/Projeto/Projeto/Dataset/economic_all_data/ecom_data.csv'
#economic_file_path = 'C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/economic_all_data/ecom_data.csv'

# Carregar os dados economicos
try:
    df_economic = pd.read_csv(economic_file_path)
    
    # Filtrar apenas as metricas que queremos
    df_economic = df_economic[df_economic['Metric'].isin(VALID_ECONOMIC_METRICS)]
    
    # Verificar e converter colunas necessarias
    if 'Date' in df_economic.columns:
        df_economic['Date'] = pd.to_datetime(df_economic['Date'])
    else:
        raise ValueError("Coluna 'Date' não encontrada no arquivo economico")
    
    if 'YearMonth' in df_economic.columns:
        df_economic['YearMonth'] = pd.to_datetime(df_economic['YearMonth']).dt.to_period('M')
    else:
        # Criar YearMonth a partir da coluna Date se não existir
        df_economic['YearMonth'] = df_economic['Date'].dt.to_period('M')
    
    # Traduzir os nomes das metricas para portugues
    df_economic['Metric'] = df_economic['Metric'].map(economic_metrics_translation)
    
    # Verificar se temos os dados minimos necessarios
    required_columns = ['State', 'Date', 'YearMonth', 'Value', 'Metric']
    if not all(col in df_economic.columns for col in required_columns):
        missing = [col for col in required_columns if col not in df_economic.columns]
        raise ValueError(f"Colunas obrigatorias faltando: {missing}")
    
    # Mapear abreviações de estado para nomes completos (se necessario)
    state_abbr_rev = {v: k for k, v in state_abbr.items()}
    df_economic['State'] = df_economic['State'].map(state_abbr_rev).fillna(df_economic['State'])
    
    # Lista de metricas economicas disponiveis (ja traduzidas)
    economic_metrics = sorted(df_economic['Metric'].unique())
    
    write_debug(f"Dados economicos carregados com sucesso. {len(df_economic)} registros. Metricas: {economic_metrics}")
    
except Exception as e:
    write_debug(f"Erro ao carregar dados economicos: {str(e)}")
    df_economic = pd.DataFrame(columns=['State', 'Date', 'YearMonth', 'Value', 'Metric'])
    economic_metrics = []

# =============================================
# LAYOUT DA APLICAÇÃO (modificado para incluir abas)
# =============================================

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-main', children=[
        # Tab principal (original)
        dcc.Tab(label='Main Dashboard', value='tab-main', children=[
            # Conteudo da pagina principal (mantido do codigo original)
            html.H1('Map of Crime in the USA (Temporal Evolution - Monthly)', 
                    style={'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Horizon Graph
            html.Div([
                dcc.Graph(id='horizon-graph', style={'height': '150px'})
            ], style={'width': '90%', 'margin': '0 auto', 'marginBottom': '20px', 'margin-left': '50px'}),
            
            # Controles temporais
            html.Div([
                html.Div([
                    dcc.Slider(
                        id='month-slider',
                        min=0,
                        max=len(months_available) - 1,
                        value=0,
                        marks={i: str(pd.Period(months_available[i]).year) for i in range(len(months_available)) if '-01' in months_available[i]},
                        step=1,
                        tooltip={"placement": "bottom", "always_visible": True},
                        included=False
                    )
                ], style={'width': '80%', 'margin': '0 auto'}),
                
                html.Div([
                    html.Button('▶ Play', id='play-button', n_clicks=0,
                              style={'margin': '10px 5px', 'padding': '5px 15px', 
                                     'backgroundColor': '#4CAF50', 'color': 'white'}),
                    html.Span(id='current-month-display',
                             style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#555'})
                ], style={'textAlign': 'center', 'margin': '10px 0'})
            ], style={'marginBottom': '20px'}),
            
            dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
            
            # Layout principal com duas colunas
            html.Div([
                # Coluna esquerda - Seletores
                html.Div([
                    # Seletor de Crimes
                    html.Div([
                        html.H3('Select crimes', style={
                            'marginBottom': '10px',
                            'fontSize': '16px',
                            'textAlign': 'center'
                        }),
                        dcc.Input(
                            id='crime-search',
                            type='text',
                            placeholder='Search for crimes...',
                            style={'width': '90%', 'margin': '0 auto 10px', 'padding': '5px'}
                        ),
                        html.Div([
                            dcc.Checklist(
                                id='select-all-crimes',
                                options=[{'label': 'Select all', 'value': 'all'}],
                                value=[],
                                labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'}
                            ),
                            html.Hr(style={'margin': '5px 0'}),
                            dcc.Checklist(
                                id='crime-selector',
                                options=[{'label': crime, 'value': crime} for crime in crime_list],
                                value=[crime_list[0]] if crime_list else [],
                                labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'},
                                inputStyle={'marginRight': '5px', 'transform': 'scale(0.8)'}
                            )
                        ], style={
                            'height': '200px',
                            'overflowY': 'auto',
                            'border': '1px solid #ddd',
                            'padding': '5px',
                            'borderRadius': '5px',
                            'backgroundColor': '#f9f9f9'
                        })
                    ], style={'marginBottom': '30px'}),
                    
                    # Seletor de Indicadores Economicos
                    html.Div([
                        html.H3('Select Economic Indicators', style={
                            'marginBottom': '10px',
                            'fontSize': '16px',
                            'textAlign': 'center'
                        }),
                        dcc.Input(
                            id='economic-search',
                            type='text',
                            placeholder='Search for indicators...',
                            style={'width': '90%', 'margin': '0 auto 10px', 'padding': '5px'}
                        ),
                        html.Div([
                            dcc.Checklist(
                                id='select-all-economics',
                                options=[{'label': 'Select all', 'value': 'all'}],
                                value=[],
                                labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'}
                            ),
                            html.Hr(style={'margin': '5px 0'}),
                            dcc.Checklist(
                                id='economic-selector',
                                options=[{'label': metric, 'value': metric} for metric in economic_metrics],
                                value=[economic_metrics[0]] if economic_metrics else [],
                                labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'},
                                inputStyle={'marginRight': '5px', 'transform': 'scale(0.8)'}
                            )
                        ], style={
                            'height': '200px',
                            'overflowY': 'auto',
                            'border': '1px solid #ddd',
                            'padding': '5px',
                            'borderRadius': '5px',
                            'backgroundColor': '#f9f9f9'
                        })
                    ])
                ], style={
                    'width': '25%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'padding': '10px',
                    'borderRight': '1px solid #eee'
                }),
                
                # Coluna direita - Mapa
                html.Div(
                    dcc.Graph(id='crime-map', style={'height': '600px'}),
                    style={
                        'width': '75%',
                        'display': 'inline-block',
                        'padding': '10px'
                    }
                )
            ], style={
                'display': 'flex',
                'border': '1px solid #eee',
                'borderRadius': '5px',
                'overflow': 'hidden'
            }),
            
            # Modal para detalhes do estado
            dcc.Store(id='click-data', data={'state': None}),

            html.Div(
                id="state-modal",
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'width': '60%',
                    'maxWidth': '800px',
                    'height': '70%',
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 8px rgba(0,0,0,0.2)',
                    'zIndex': '1000',
                    'overflowY': 'auto'
                },
                children=[
                    html.Div(
                        style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'marginBottom': '15px'
                        },
                        children=[
                            html.H2(id='modal-title', style={'margin': '0'}),
                            html.Button(
                                '✕',
                                id='close-modal',
                                style={
                                    'background': 'none',
                                    'border': 'none',
                                    'fontSize': '20px',
                                    'cursor': 'pointer',
                                    'color': '#999'
                                }
                            )
                        ]
                    ),
                    dcc.Graph(id='crime-bar-chart'),
                    
                    # Nova seção para dados economicos
                    html.Div([
                        html.H3("Economic indicators", style={'marginTop': '30px'}),
                        
                        # Heatmap temporal
                        dcc.Graph(id='economic-heatmap', style={'height': '400px'})
                    ], style={'marginTop': '30px'})
                ]
            ),
            
            # Overlay do modal
            html.Div(
                id='modal-overlay',
                style={
                    'display': 'none',
                    'position': 'fixed',
                    'top': '0',
                    'left': '0',
                    'right': '0',
                    'bottom': '0',
                    'backgroundColor': 'rgba(0,0,0,0.5)',
                    'zIndex': '999'
                }
            )
        ]),
        
        # Nova aba de comparação entre estados
        dcc.Tab(label='State Comparison', value='tab-comparison', children=[
            html.Div([
                html.H1('State Comparison Dashboard', style={'textAlign': 'center', 'marginBottom': '20px'}),
                
                # Controles de seleção de estados
                html.Div([
                    html.Div([
                        html.H3('Select States for Comparison (up to 3)', style={'marginBottom': '10px'}),
                        dcc.Dropdown(
                            id='state-comparison-dropdown',
                            options=[{'label': state, 'value': state} for state in state_abbr.keys()],
                            value=[],
                            multi=True,
                            maxHeight=150,
                            placeholder="Select states..."
                        )
                    ], style={'width': '80%', 'margin': '0 auto 20px'}),
                    
                    # Controles temporais (reutilizados da pagina principal)
                    html.Div([
                        html.Div([
                            dcc.Slider(
                                id='comparison-month-slider',
                                min=0,
                                max=len(months_available) - 1,
                                value=0,
                                marks={i: str(pd.Period(months_available[i]).year) for i in range(len(months_available)) if '-01' in months_available[i]},
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": True},
                                included=False
                            )
                        ], style={'width': '80%', 'margin': '0 auto'}),
                        
                        html.Div([
                            html.Button('▶ Play', id='comparison-play-button', n_clicks=0,
                                      style={'margin': '10px 5px', 'padding': '5px 15px', 
                                             'backgroundColor': '#4CAF50', 'color': 'white'}),
                            html.Span(id='comparison-current-month-display',
                                     style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#555'})
                        ], style={'textAlign': 'center', 'margin': '10px 0'})
                    ], style={'marginBottom': '20px'}),
                    
                    dcc.Interval(id='comparison-interval-component', interval=1000, n_intervals=0, disabled=True),
                ]),
                
                # Layout principal com duas colunas
                html.Div([
                    # Coluna esquerda - Seletores (reutilizados da pagina principal)
                    html.Div([
                        # Seletor de Crimes
                        html.Div([
                            html.H3('Select crimes', style={
                                'marginBottom': '10px',
                                'fontSize': '16px',
                                'textAlign': 'center'
                            }),
                            dcc.Input(
                                id='comparison-crime-search',
                                type='text',
                                placeholder='Search for crimes...',
                                style={'width': '90%', 'margin': '0 auto 10px', 'padding': '5px'}
                            ),
                            html.Div([
                                dcc.Checklist(
                                    id='comparison-select-all-crimes',
                                    options=[{'label': 'Select all', 'value': 'all'}],
                                    value=[],
                                    labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'}
                                ),
                                html.Hr(style={'margin': '5px 0'}),
                                dcc.Checklist(
                                    id='comparison-crime-selector',
                                    options=[{'label': crime, 'value': crime} for crime in crime_list],
                                    value=[crime_list[0]] if crime_list else [],
                                    labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'},
                                    inputStyle={'marginRight': '5px', 'transform': 'scale(0.8)'}
                                )
                            ], style={
                                'height': '200px',
                                'overflowY': 'auto',
                                'border': '1px solid #ddd',
                                'padding': '5px',
                                'borderRadius': '5px',
                                'backgroundColor': '#f9f9f9'
                            })
                        ], style={'marginBottom': '30px'}),
                        
                        # Seletor de Indicadores Economicos
                        html.Div([
                            html.H3('Select Economic Indicators', style={
                                'marginBottom': '10px',
                                'fontSize': '16px',
                                'textAlign': 'center'
                            }),
                            dcc.Input(
                                id='comparison-economic-search',
                                type='text',
                                placeholder='Search for indicators...',
                                style={'width': '90%', 'margin': '0 auto 10px', 'padding': '5px'}
                            ),
                            html.Div([
                                dcc.Checklist(
                                    id='comparison-select-all-economics',
                                    options=[{'label': 'Select all', 'value': 'all'}],
                                    value=[],
                                    labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'}
                                ),
                                html.Hr(style={'margin': '5px 0'}),
                                dcc.Checklist(
                                    id='comparison-economic-selector',
                                    options=[{'label': metric, 'value': metric} for metric in economic_metrics],
                                    value=[economic_metrics[0]] if economic_metrics else [],
                                    labelStyle={'display': 'block', 'fontSize': '12px', 'margin': '5px 0', 'padding': '3px 5px'},
                                    inputStyle={'marginRight': '5px', 'transform': 'scale(0.8)'}
                                )
                            ], style={
                                'height': '200px',
                                'overflowY': 'auto',
                                'border': '1px solid #ddd',
                                'padding': '5px',
                                'borderRadius': '5px',
                                'backgroundColor': '#f9f9f9'
                            })
                        ])
                    ], style={
                        'width': '25%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'padding': '10px',
                        'borderRight': '1px solid #eee'
                    }),
                    
                    # Coluna direita - Visualizações de comparação
                    html.Div([
                        # Graficos de crimes sobrepostos
                        html.Div([
                            html.H3('Crime Trends Comparison', style={'textAlign': 'center'}),
                            dcc.Graph(id='crime-comparison-graph')
                        ], style={
                            'overflowY': 'auto',
                            'maxHeight': '400px',
                            }),
                        
                        # Heatmap economico (similar ao da pagina principal)
                        html.Div([
                            html.H3('Economic Indicators Comparison', style={'textAlign': 'center'}),
                            dcc.Graph(id='economic-comparison-heatmap')
                        ])
                    ], style={
                        'width': '75%',
                        'display': 'inline-block',
                        'padding': '10px'
                    })
                ], style={
                    'display': 'flex',
                    'border': '1px solid #eee',
                    'borderRadius': '5px',
                    'overflow': 'hidden'
                })
            ])
        ]),

        # Information Tab
        dcc.Tab(label='Information', value='tab-info', children=[
            html.Div([
                html.H1('Methodology & Data Documentation', style={'textAlign': 'center', 'marginBottom': '30px'}),
                
                html.Div([
                    html.H2('Dataset Overview', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px'}),
                    dcc.Markdown("""
                    This dashboard combines two primary datasets:

                    - **Crime Statistics**  
                      - 72 distinct crime types reported monthly 
                      - Covers all 50 U.S. states + District of Columbia
                      - Absolute values

                    - **Economic Indicators**  
                      - 11 key metrics tracking year-over-year changes in:  
                        - Employment levels (total/public/private/retail/manufacturing)  
                        - GDP components (retail/manufacturing/government/services)  
                        - Housing market trends  
                      - Originally reported at varying frequencies
                    """),

                    html.H2('Data Processing', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px', 'marginTop': '30px'}),
                    dcc.Markdown("""
                    Temporal Alignment:
                    - Economic indicators reported as 3-month changes were converted to monthly estimates by dividing values by 3  
                    - All time series were standardized to monthly frequency

                    Crime Classification (IQR Method):
                    
                    # Calculated across all states and time periods
                    Q1 = 25th percentile, Q3 = 75th percentile
                    IQR = Q3 - Q1
                    
                    if value < (Q1 - 1.5*IQR):  # Extremely Low
                    elif value < (Q1 - 0.75*IQR): # Very Low
                    elif value < Q1:             # Low
                    elif value < Q3:             # Average
                    elif value < (Q3 + 0.75*IQR): # High
                    elif value < (Q3 + 1.5*IQR):  # Very High
                    else:                        # Extremely High
                    
⁠                     This robust scaling minimizes outlier effects while highlighting significant deviations.
                    """),
                    
                    html.H2('National Average Calculation', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px', 'marginTop': '30px'}),
                    dcc.Markdown("""
                    **National Average for Crime Statistics**:  
                    The national average for each crime type was calculated by summing the total number of reported cases for that crime across all 51 jurisdictions (50 states + District of Columbia), and then dividing the total by 51. This provides an average value for each crime type at the national level, accounting for variations in reporting between states.
                    """),
                    
                    html.H2('Economic Data Scaling', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px', 'marginTop': '30px'}),
                    dcc.Markdown("""
                    **Visualization Approach**:
                    - Each economic indicator is standardized using **Z-score normalization**:  
                      `z = (x - μ) / σ`  
                      (μ = historical mean for that state & metric, σ = standard deviation)
                    
                    **Color Encoding**:  
                    - Red hues: Values above historical average  
                    - Blue hues: Values below historical average  
                    - Intensity reflects magnitude of deviation

                    **Why Normalize?**  
                    Enables comparison across different metrics while preserving:  
                    - Direction of change (improving/declining)  
                    - Relative performance vs. a state's own history
                    """),

                    html.H2('Data Sources', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px', 'marginTop': '30px'}),
                    dcc.Markdown("""
                    - **Crime Data**: FBI Uniform Crime Reporting Program  
                    - **Economic Data **: Urban Institute Economic Data 
                    """),

                    html.H2('Project Information', style={'color': '#2c3e50', 'borderBottom': '1px solid #eee', 'paddingBottom': '10px', 'marginTop': '30px'}),
                    dcc.Markdown("""
                    Developed by **José Cunha** ([josecunha.8989@gmail.com](mailto:josecunha.8989@gmail.com))  
                    and **Marta Antunes** ([martantunes2003@gmail.com](mailto:martantunes2003@gmail.com))   
                    as part of the **Advanced Data Visualization** course.

                    *University of Coimbra, 2025*
                    """)
                ], style={
                    'maxWidth': '900px',
                    'margin': '0 auto',
                    'padding': '25px',
                    'backgroundColor': 'white',
                    'boxShadow': '0 2px 15px rgba(0,0,0,0.1)',
                    'borderRadius': '10px',
                    'lineHeight': '1.7'
                })
            ], style={
                'padding': '20px', 
                'backgroundColor': '#f8f9fa',
                'fontFamily': 'Arial, sans-serif'
            })
        ])
    ])
])

# =============================================
# CALLBACKS DA PaGINA PRINCIPAL (mantidos do codigo original)
# =============================================

# Atualiza lista de crimes com base na pesquisa
@app.callback(
    Output('crime-selector', 'options'),
    Input('crime-search', 'value')
)
def update_crime_options(search_value):
    if not search_value:
        return [{'label': crime, 'value': crime} for crime in crime_list]
    filtered = [crime for crime in crime_list if search_value.lower() in crime.lower()]
    return [{'label': crime, 'value': crime} for crime in filtered]

# Sincroniza checkboxes de crimes
@app.callback(
    [Output('crime-selector', 'value'),
     Output('select-all-crimes', 'value')],
    [Input('select-all-crimes', 'value'),
     Input('crime-selector', 'value')],
    [State('crime-selector', 'options')]
)
def sync_crime_checkboxes(select_all, selected_crimes, available_options):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'select-all-crimes':
        if 'all' in select_all:
            return [option['value'] for option in available_options], ['all']
        else:
            return [], []
    else:
        if len(selected_crimes) == len(available_options):
            return selected_crimes, ['all']
        elif not selected_crimes:
            return [], []
        else:
            return selected_crimes, []

# Atualiza lista de indicadores economicos com base na pesquisa
@app.callback(
    Output('economic-selector', 'options'),
    Input('economic-search', 'value')
)
def update_economic_options(search_value):
    if not search_value:
        return [{'label': metric, 'value': metric} for metric in economic_metrics]
    filtered = [metric for metric in economic_metrics if search_value.lower() in metric.lower()]
    return [{'label': metric, 'value': metric} for metric in filtered]

# Sincroniza checkboxes de indicadores economicos
@app.callback(
    [Output('economic-selector', 'value'),
     Output('select-all-economics', 'value')],
    [Input('select-all-economics', 'value'),
     Input('economic-selector', 'value')],
    [State('economic-selector', 'options')]
)
def sync_economic_checkboxes(select_all, selected_metrics, available_options):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'select-all-economics':
        if 'all' in select_all:
            return [option['value'] for option in available_options], ['all']
        else:
            return [], []
    else:
        if len(selected_metrics) == len(available_options):
            return selected_metrics, ['all']
        elif not selected_metrics:
            return [], []
        else:
            return selected_metrics, []

# Controle de animação
@app.callback(
    Output('interval-component', 'disabled'),
    Input('play-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_play(n_clicks):
    return n_clicks % 2 == 0

# Atualiza slider e display do mes
@app.callback(
    [Output('month-slider', 'value'),
     Output('current-month-display', 'children'),
     Output('play-button', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('month-slider', 'value'),
     Input('play-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_slider(n_intervals, current_value, n_clicks):
    if current_value < len(months_available) - 1:
        new_value = current_value + 1
    else:
        new_value = 0
    
    current_month = pd.Period(months_available[new_value])
    formatted_month = current_month.strftime('%b %Y')

    button_text = '❚❚ Pause' if n_clicks % 2 == 1 else '▶ Play'
    
    return new_value, f"Current Period: {formatted_month}", button_text

# Horizon Graph
@app.callback(
    Output('horizon-graph', 'figure'),
    [Input('crime-selector', 'value'),
     Input('month-slider', 'value')]
)
def update_horizon_graph(selected_crimes, selected_month_index):
    if not selected_crimes:
        return go.Figure()
    
    try:
        df_filtered = df_map[df_map['series'].isin(selected_crimes)]
        df_sum = df_filtered.groupby('YearMonth')['Value'].sum().reset_index()
        
        if df_sum.empty:
            return go.Figure()
        
        df_sum['YearMonth'] = df_sum['YearMonth'].astype(str)
        df_sum = df_sum.sort_values('YearMonth')
        df_sum['X_index'] = range(len(df_sum))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sum['X_index'],
            y=df_sum['Value'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4),
            name='Soma dos crimes selecionados',
            hovertext=df_sum['YearMonth'],
            hoverinfo='text+y'
        ))
        
        if selected_month_index < len(df_sum):
            fig.add_vline(
                x=selected_month_index,
                line=dict(color='red', width=2, dash='dot'),
                annotation_text="Current month",
                annotation_position="top right"
            )
        
        fig.update_layout(
            height=150,
            margin=dict(l=20, r=20, t=20, b=20),
            #xaxis=dict(showgrid=False, tickvals=df_sum['X_index'][::12], ticktext=df_sum['YearMonth'][::12].str[:4]),
            xaxis=dict(showgrid=False, visible=False),
            #yaxis=dict(title='Sum of all crimes', showgrid=False, rangemode='tozero'),
            hovermode='x unified'
        )
        
        return fig
    
    except Exception as e:
        write_debug(f"Erro ao criar Horizon Graph: {str(e)}")
        return go.Figure()

# Mapa Choropleth
@app.callback(
    Output('crime-map', 'figure'),
    [Input('crime-selector', 'value'),
     Input('month-slider', 'value')]
)
def update_map(selected_crimes, selected_month_index):
    selected_month = months_available[selected_month_index]
    
    # Caso nenhum crime esteja selecionado, criar mapa vazio com valor zero para todos os estados
    if not selected_crimes:
        all_states = pd.DataFrame({
            'State': list(state_abbr.values()),
            'Value': 0
        })
        fig = px.choropleth(
            all_states,
            locations='State',
            locationmode='USA-states',
            color='Value',
            scope='usa',
            title=f'Nenhum crime selecionado ({pd.Period(selected_month).strftime("%b %Y")})',
            color_continuous_scale='Reds',
            range_color=(0, 1),
            height=600
        )
    
    # Caso haja crimes selecionados
    else:
        # Calcular o IQR GLOBAL (todos os meses)
        df_filtered_all = df_map[df_map['series'].isin(selected_crimes)]  # Filtra os dados para os crimes selecionados
        df_sum_all = df_filtered_all.groupby(['State', 'YearMonth'])['Value'].sum().reset_index()  # Agrupa por estado e mes somando os valores

        max_value = df_sum_all['Value'].max()
        max_value_state = df_sum_all[df_sum_all['Value'] == max_value]['State']
        max_value_yearmonth = df_sum_all[df_sum_all['Value'] == max_value]['YearMonth']
        write_debug(f"Max Value: {max_value}\n\tState: {max_value_state.values[0]}\n\tYear-Month: {max_value_yearmonth.values[0]}")
        
        # Calcula quartis e IQR sobre todos os dados
        q1_global = df_sum_all['Value'].quantile(0.25)
        q3_global = df_sum_all['Value'].quantile(0.75)
        iqr_global = q3_global - q1_global
        lower_bound_1 = q1_global - 0.75 * iqr_global
        upper_bound_1 = q3_global + 0.75 * iqr_global
        lower_bound_2 = q1_global - 1.5 * iqr_global
        upper_bound_2 = q3_global + 1.5 * iqr_global
        
        # Filtra para o mes selecionado
        df_filtered = df_map[
            (df_map['series'].isin(selected_crimes)) & 
            (df_map['YearMonth'] == selected_month)
        ]

        df_aggregated = df_filtered.groupby('State')['Value'].sum().reset_index()  # Agrupa por estado somando os valores
        df_aggregated['State'] = df_aggregated['State'].map(state_abbr)  # Mapeia o nome do estado para abreviação
        df_aggregated = df_aggregated.dropna(subset=['State'])  # Remove estados sem dados
        df_aggregated['Value'] = df_aggregated['Value'].fillna(0)  # Substitui valores nulos por 0
        
        # Categoriza os valores do mes atual usando os limites GLOBAIS
        df_aggregated['Category'] = pd.cut(
            df_aggregated['Value'],
            bins=[-np.inf, 
                lower_bound_2,
                lower_bound_1,
                q1_global,
                q3_global,
                upper_bound_1,
                upper_bound_2,
                np.inf],
            labels=['Extremely Low', 'Very Low', 'Low', 'Average', 'High', 'Very High', 'Extremely High'],
            include_lowest=True
        )
        
        # Escala de cores (azul ou vermelha)
        color_discrete_map = {
            'Extremely Low': '#F7FBFF',
            'Very Low': '#CDE2FC',
            'Low': '#C0DBFC',
            'Average': '#80B5F6',
            'High': '#4586D5',
            'Very High': '#1E5598',
            'Extremely High': '#042959'
        }
        
        # Criar o mapa
        fig = px.choropleth(
            df_aggregated,
            locations='State',
            locationmode='USA-states',
            color='Category',
            scope='usa',
            title=f'Crime Index in EUA ({pd.Period(selected_month).strftime("%b %Y")})',
            color_discrete_map=color_discrete_map,
            category_orders={'Category': ['Extremely Low', 'Very Low', 'Low', 'Average', 'High', 'Very High', 'Extremely High']},
            height=600,
            hover_data={'Value': ':.0f'}
        )
        
        # Tooltip com a abreviação do estado e o valor exato do crime no mes selecionado
        fig.update_traces(
            hovertemplate='<b>%{location}</b><br>' +
            'Crime Rate: %{customdata[0]:.0f}<extra></extra>'  # Mostra o valor numérico formatado
        )
    
    # Configura o layout do grafico
    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        geo=dict(bgcolor='rgba(0, 0, 0, 0)'),
        coloraxis_showscale=bool(selected_crimes)  # Mostra a barra de cores apenas se houver crimes selecionados
    )
    
    return fig

# Modal - abrir/fechar
@app.callback(
    [Output('click-data', 'data'),
     Output('state-modal', 'style'),
     Output('modal-overlay', 'style')],
    [Input('crime-map', 'clickData'),
     Input('close-modal', 'n_clicks')],
    [State('click-data', 'data')]
)
def toggle_modal(map_click, close_click, current_data):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update, {'display': 'none'}, {'display': 'none'}
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'crime-map' and map_click:
        state = map_click['points'][0]['location']
        return {'state': state}, {'display': 'block'}, {'display': 'block'}
    else:
        return current_data, {'display': 'none'}, {'display': 'none'}

# Modal - conteudo (grafico de barras)
@app.callback(
    [Output('modal-title', 'children'),
     Output('crime-bar-chart', 'figure')],
    [Input('click-data', 'data'),
     Input('crime-selector', 'value'),
     Input('month-slider', 'value'),
     Input('select-all-crimes', 'value')],
    prevent_initial_call=True
)
def update_modal_content(click_data, selected_crimes, selected_month_index, select_all):
    if not click_data or not click_data['state']:
        return dash.no_update, dash.no_update
    
    state_abbr_rev = {v: k for k, v in state_abbr.items()}
    state_name = state_abbr_rev.get(click_data['state'], click_data['state'])
    selected_month = months_available[selected_month_index]
    
    title = f"Crimes in {state_name} - {pd.Period(selected_month).strftime('%b %Y')}"
    
    df_filtered = df_map[(df_map['State'] == state_name) & (df_map['YearMonth'] == selected_month)]
    
    if 'all' in select_all:
        df_display = df_filtered.nlargest(5, 'Value')
    else:
        df_display = df_filtered[df_filtered['series'].isin(selected_crimes)].nlargest(5, 'Value')
    
    if df_display.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Nenhum dado disponivel para os criterios selecionados",
            xaxis={'visible': False},
            yaxis={'visible': False},
            plot_bgcolor='white'
        )
    else:
        df_display = df_display.sort_values('Value', ascending=True)
        crimes_para_calculo = df_display['series'].tolist()

        df_national_avg = df_map[
            (df_map['YearMonth'] == selected_month) &
            (df_map['series'].isin(crimes_para_calculo))
        ]
        df_national_avg = df_national_avg.groupby('series')['Value'].sum().reset_index()
        df_national_avg['US_avg'] = df_national_avg['Value'] / 51

        df_display = df_display.merge(df_national_avg[['series', 'US_avg']], on='series', how='left')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_display['series'],
            x=df_display['Value'],
            orientation='h',
            text=df_display['Value'].round(2),
            textposition='auto',
            marker_color='#1f77b4',
            name='Value in the state',
        ))

        for idx, row in df_display.iterrows():
            fig.add_shape(
                type='line',
                x0=row['US_avg'],
                y0=idx-0.4,
                x1=row['US_avg'],
                y1=idx+0.4,
                line=dict(color='red', width=2, dash='dot')
            )

        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color='red', width=2, dash='dot'),
            name='National average',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f"Distribution of Crimes",
            xaxis_title="Rate per population",
            yaxis_title="Type of Crime",
            showlegend=True,
            plot_bgcolor='white',
            margin=dict(l=150, r=70, t=40, b=20),
            height=400
        )
    
    return title, fig

@app.callback(
    Output('economic-heatmap', 'figure'),
    [Input('click-data', 'data'),
     Input('economic-selector', 'value'),
     Input('month-slider', 'value'),
     Input('interval-component', 'n_intervals')],
    [State('economic-heatmap', 'relayoutData')]
)
def update_economic_heatmap(click_data, selected_metrics, selected_month_index, n_intervals, relayout_data):
    # Verificação inicial
    if not selected_metrics:
        return go.Figure(layout={
            'title': 'No Economic Indicators Selected',
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'Please select at least one economic indicator',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white'
        })
    if not click_data or not click_data.get('state') or not selected_metrics or df_economic.empty:
        return go.Figure()
    
    state_abbr_rev = {v: k for k, v in state_abbr.items()}
    state_name = state_abbr_rev.get(click_data['state'])
    
    if not state_name:
        return go.Figure()

    try:
        # 1. Obter o mes selecionado
        selected_month = months_available[selected_month_index]
        current_period = pd.Period(selected_month, freq='M')
        
        # 2. Filtrar e preparar os dados
        df_filtered = df_economic[
            (df_economic['State'] == state_name) & 
            (df_economic['Metric'].isin(selected_metrics))
        ].copy()
        
        if df_filtered.empty:
            return go.Figure()
        
        # 3. Converter para datetime e ordenar
        df_filtered['Date'] = pd.to_datetime(df_filtered['YearMonth'].astype(str))
        df_filtered = df_filtered.sort_values('Date')
        
        # 4. Normalização Z-score
        df_normalized = df_filtered.copy()
        for metric in selected_metrics:
            metric_data = df_filtered[df_filtered['Metric'] == metric]['Value']
            if len(metric_data) > 0:
                mean_val = metric_data.mean()
                std_val = metric_data.std()
                df_normalized.loc[df_filtered['Metric'] == metric, 'Value'] = (
                    (metric_data - mean_val) / std_val if std_val != 0 else 0
                )
        
        # 5. Criar pivot table
        df_pivot = df_normalized.pivot_table(
            index='Metric',
            columns='Date',
            values='Value',
            aggfunc='mean'
        ).sort_index(axis=1)
        
        # 6. Preparar eixos
        date_strings = [d.strftime('%Y-%m') for d in df_pivot.columns]
        yearly_ticks = [d for d in df_pivot.columns if d.month == 1]
        
        # 7. Determinar o range do rangeslider
        slider_range = None
        if relayout_data and 'xaxis.range[0]' in relayout_data:
            slider_range = [
                relayout_data['xaxis.range[0]'],
                relayout_data['xaxis.range[1]']]
        
        # 8. Criar heatmap
        fig = go.Figure(go.Heatmap(
            x=date_strings,
            y=df_pivot.index,
            z=df_pivot.values,
            colorscale='RdBu_r',
            zmid=0,
            hoverongaps=False,
            hoverinfo='x+y+z',
            colorbar=dict(title='Standard Deviation')
        ))
        
        # 9. Adicionar linha vermelha do periodo atual
        current_date_str = current_period.strftime('%Y-%m')
        if current_date_str in date_strings:
            x_pos = date_strings.index(current_date_str)
            fig.add_vline(
                x=x_pos,
                line=dict(color='red', width=3),
                annotation_text=current_date_str,
                annotation_position="top right",
                annotation_font=dict(color='red')
            )
        
        # 10. Configurar layout com rangeslider persistente
        fig.update_layout(
            title=f"Economic Variation in {state_name}",
            xaxis_title="Time",
            yaxis_title="Economic indicators",
            margin=dict(l=120, r=50, t=80, b=80),  # Aumentei o bottom para o slider
            height=500,
            xaxis=dict(
                tickvals=[d.strftime('%Y-%m') for d in yearly_ticks],
                ticktext=[d.strftime('%Y') for d in yearly_ticks],
                tickangle=45,
                rangeslider=dict(
                    visible=True,
                    thickness=0.1,
                    bgcolor='rgba(150,150,150,0.3)',
                    range=slider_range  # Mantem o range selecionado
                ),
                type='category',
                range=slider_range  # Tambem aplica ao eixo principal
            ),
            yaxis=dict(
                tickfont=dict(size=9),
                tickangle=-30
            )
        )
        
        return fig
    
    except Exception as e:
        write_debug(f"Erro no heatmap economico: {str(e)}")
        return go.Figure()

# =============================================
# CALLBACKS DA ABA DE COMPARAÇÃO
# =============================================

# Atualiza lista de crimes com base na pesquisa (comparação)
@app.callback(
    Output('crime-comparison-graph', 'figure'),
    [Input('state-comparison-dropdown', 'value'),
     Input('comparison-crime-selector', 'value'),
     Input('comparison-month-slider', 'value')]
)
def update_crime_comparison_graph(selected_states, selected_crimes, selected_month_index):
    import matplotlib.colors as mcolors

    def hex_to_rgba(hex_color, alpha):
        rgb = mcolors.to_rgb(hex_color)
        return f'rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, {alpha})'
    
    if not selected_states and not selected_crimes:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No states or crimes selected for comparison.<br>Please select at least one state and one crime!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white',
            'height': 200
        })

    if not selected_states:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No states selected for comparison.<br>Please select at least one state!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white',
            'height': 200
        })
    
    if not selected_crimes:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No crimes selected for comparison.<br>Please select at least one crime!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white',
            'height': 200
        })
    
    # Se o número de crimes selecionados for maior que 5, invés de mostrar o gráfico, mostrar uma mensagem
    if len(selected_crimes) > 5:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'Too many crimes selected.<br>Please select 5 or fewer crimes!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white',
            'height': 200
        })
    
    if len(selected_states) > 3:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'Too many states selected.<br>Please select 3 or fewer states!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center'
            }],
            'plot_bgcolor': 'white',
            'height': 200
        })
    
    try:
        selected_month = months_available[selected_month_index]
        current_period = pd.Period(selected_month)

        plot_height = 300
        row_heights = [plot_height] * len(selected_crimes)
        
        # Criar figura com subplots - APENAS para os crimes selecionados
        fig = make_subplots(
            rows=len(selected_crimes),  # Isso já garante 1 linha por crime
            cols=1,
            subplot_titles=[crime.split(" Reported by")[0] for crime in selected_crimes],
            row_heights=row_heights
        )
        
        colors = px.colors.qualitative.Plotly
        
        # Garantir que estamos iterando apenas sobre os crimes selecionados
        for crime_idx, crime in enumerate(selected_crimes[:len(selected_crimes)]):  # Adicionei o slice para garantir
            crime_data = []
            
            for state_idx, state in enumerate(selected_states):
                df_filtered = df_map[
                    (df_map['State'] == state) & 
                    (df_map['series'] == crime)
                ].copy()
                
                if not df_filtered.empty:
                    df_filtered['Date'] = df_filtered['YearMonth'].dt.to_timestamp()
                    df_sorted = df_filtered.sort_values('Date')
                    crime_data.append(df_sorted)
            
            if crime_data:
                df_combined = pd.concat(crime_data)
                
                for state_idx, state in enumerate(selected_states):
                    state_data = df_combined[df_combined['State'] == state]
                    if not state_data.empty:
                        color = colors[state_idx % len(colors)]
                        line_color = hex_to_rgba(color, 0.9)
                        area_color = hex_to_rgba(color, 0.2)

                        fig.add_trace(
                            go.Scatter(
                                x=state_data['Date'],
                                y=state_data['Value'],
                                mode='lines',
                                name=state,
                                line=dict(color=line_color, width=1.5),
                                showlegend=True if crime_idx == 0 else False,
                                legendgroup=state,
                                hoverinfo='skip'
                            ),
                            row=crime_idx+1,  # Usamos crime_idx+1 para começar da linha 1
                            col=1
                        )
                        
                        fig.add_trace(
                            go.Scatter(
                                x=state_data['Date'],
                                y=state_data['Value'],
                                fill='tozeroy',
                                mode='none',
                                showlegend=False,
                                fillcolor=area_color,
                                hoverinfo='skip'
                            ),
                            row=crime_idx+1,
                            col=1
                        )
                
                # Linha vertical apenas se houver dados
                current_date = current_period.to_timestamp()
                fig.add_vline(
                    x=current_date,
                    line=dict(color='red', width=1.5, dash='dot'),
                    row=crime_idx+1,
                    col=1
                )
                
                fig.update_yaxes(
                    title_text="Occurrences",
                    row=crime_idx+1,
                    col=1,
                    rangemode='tozero'
                )
        
        fig.update_layout(
            height=sum(row_heights),
            margin=dict(l=50, r=50, t=80, b=50),
            plot_bgcolor='white',
            xaxis=dict(tickformat="%b %Y"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    except Exception as e:
        write_debug(f"Erro no gráfico de comparação: {str(e)}")
        return go.Figure()

# Heatmap de comparação econômica (mantido igual)
@app.callback(
    Output('economic-comparison-heatmap', 'figure'),
    [Input('state-comparison-dropdown', 'value'),
     Input('comparison-economic-selector', 'value'),
     Input('comparison-month-slider', 'value')]
)
def update_economic_comparison_heatmap(selected_states, selected_metrics, selected_month_index):
    if not selected_states and not selected_metrics:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No states or economic indicators selected for comparison.<br>Please select at least one state and one indicator!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center',
                'xanchor': 'center',
                'yanchor': 'middle',
            }],
            'plot_bgcolor': 'white',
        })
    
    if not selected_states:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No states selected for comparison.<br>Please select at least one state!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center',
                'xanchor': 'center',
                'yanchor': 'middle',
            }],
            'plot_bgcolor': 'white',
        })
    
    if not selected_metrics:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'No economic indicators selected for comparison.<br>Please select at least one indicator!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center',
                'xanchor': 'center',
                'yanchor': 'middle',
            }],
            'plot_bgcolor': 'white',
        })
    
    if len(selected_states) > 3:
        return go.Figure(layout={
            'xaxis': {'visible': False},
            'yaxis': {'visible': False},
            'annotations': [{
                'text': 'Too many states selected.<br>Please select 3 or fewer states!',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'},
                'x': 0.5,
                'y': 0.5,
                'align': 'center',
                'xanchor': 'center',
                'yanchor': 'middle',
            }],
            'plot_bgcolor': 'white',
        })

    try:
        selected_month = months_available[selected_month_index]
        current_period = pd.Period(selected_month, freq='M')
        
        # Create subplots - one heatmap per state
        fig = make_subplots(
            rows=len(selected_states),
            cols=1,
            subplot_titles=selected_states,
            vertical_spacing=0.1,
            shared_xaxes=True
        )
        
        # Variables to maintain consistent range
        zmin, zmax = float('inf'), float('-inf')
        all_z_values = []
        
        # First pass to calculate global range
        for state in selected_states:
            df_state = df_economic[
                (df_economic['State'] == state) &
                (df_economic['Metric'].isin(selected_metrics))
            ].copy()
            
            if not df_state.empty:
                for metric in selected_metrics:
                    mask = df_state['Metric'] == metric
                    values = df_state.loc[mask, 'Value']
                    mean_val = values.mean()
                    std_val = values.std()
                    normalized = (values - mean_val) / std_val if std_val != 0 else 0
                    all_z_values.extend(normalized)
        
        if all_z_values:
            zmin, zmax = min(all_z_values), max(all_z_values)
        
        # Second pass to create heatmaps
        for i, state in enumerate(selected_states, 1):
            # Filter data for current state
            df_state = df_economic[
                (df_economic['State'] == state) &
                (df_economic['Metric'].isin(selected_metrics))
            ].copy()
            
            if df_state.empty:
                continue
                
            # Convert YearMonth to datetime and sort
            df_state['Date'] = pd.to_datetime(df_state['YearMonth'].astype(str))
            df_state = df_state.sort_values(['Metric', 'Date'])
            
            # Normalize values (Z-score per metric)
            for metric in selected_metrics:
                mask = df_state['Metric'] == metric
                values = df_state.loc[mask, 'Value']
                mean_val = values.mean()
                std_val = values.std()
                df_state.loc[mask, 'Normalized'] = (
                    (values - mean_val) / std_val if std_val != 0 else 0
                )
            
            # Create pivot table
            df_pivot = df_state.pivot_table(
                index='Date',
                columns='Metric',
                values='Normalized'
            )
            
            # Order columns according to selected_metrics
            df_pivot = df_pivot[selected_metrics]
            
            # Create heatmap for this state (without individual colorbar)
            heatmap = go.Heatmap(
                x=df_pivot.index.strftime('%Y-%m'),
                y=df_pivot.columns,
                z=df_pivot.values.T,
                colorscale='RdBu_r',
                zmin=zmin,
                zmax=zmax,
                zmid=0,
                showscale=False,  # Disable individual colorbar
                hoverongaps=False,
                hovertemplate="<b>%{y}</b><br>Date: %{x}<br>Z-Score: %{z:.2f}<extra></extra>"
            )
            
            fig.add_trace(heatmap, row=i, col=1)
            
            # Add current month line
            current_date_str = current_period.strftime('%Y-%m')
            if current_date_str in df_pivot.index.strftime('%Y-%m'):
                fig.add_vline(
                    x=current_date_str,
                    line=dict(color='red', width=2),
                    row=i, col=1
                )
            
            # Configure axes
            fig.update_yaxes(
                title_text="Indicators",
                row=i, col=1
            )
            
            if i == len(selected_states):
                fig.update_xaxes(
                    title_text="Time",
                    row=i, col=1,
                    tickangle=45,
                    tickvals=[d.strftime('%Y-%m') for d in df_pivot.index if d.month == 1],
                    ticktext=[d.strftime('%Y') for d in df_pivot.index if d.month == 1]
                )
        
        # Configure global colorbar on the last heatmap
        fig.data[-1].update(
            showscale=True,
            colorbar=dict(
                title='Standard Deviation',
                lenmode='fraction',
                len=0.8,
                y=0.5,
                yanchor='middle',
                x=1.02
            )
        )
        
        # General layout settings
        fig.update_layout(
            title_text="Economic Indicators Comparison by State",
            height=300 * len(selected_states),
            margin=dict(l=150, r=150, t=80, b=80),  # Increased right margin for colorbar
            showlegend=False
        )
        
        return fig
    
    except Exception as e:
        write_debug(f"Error in economic comparison heatmap: {str(e)}")
        return go.Figure()


# Callbacks para controles de animação na aba de comparação
@app.callback(
    Output('comparison-interval-component', 'disabled'),
    Input('comparison-play-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_comparison_play(n_clicks):
    return n_clicks % 2 == 0

# Atualiza slider e display do mes na aba de comparação
@app.callback(
    [Output('comparison-month-slider', 'value'),
     Output('comparison-current-month-display', 'children'),
     Output('comparison-play-button', 'children')],
    [Input('comparison-interval-component', 'n_intervals'),
     Input('comparison-month-slider', 'value'),
     Input('comparison-play-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_comparison_slider(n_intervals, current_value, n_clicks):
    if current_value < len(months_available) - 1:
        new_value = current_value + 1
    else:
        new_value = 0
    
    current_month = pd.Period(months_available[new_value])
    formatted_month = current_month.strftime('%b %Y')

    button_text = '❚❚ Pause' if n_clicks % 2 == 1 else '▶ Play'
    
    return new_value, f"Current Period: {formatted_month}", button_text

# Callbacks para filtros de pesquisa na aba de comparação (similares aos da página principal)
@app.callback(
    Output('comparison-crime-selector', 'options'),
    Input('comparison-crime-search', 'value')
)
def update_comparison_crime_options(search_value):
    if not search_value:
        return [{'label': crime, 'value': crime} for crime in crime_list]
    filtered = [crime for crime in crime_list if search_value.lower() in crime.lower()]
    return [{'label': crime, 'value': crime} for crime in filtered]

# Sincroniza checkboxes de crimes na aba de comparação
@app.callback(
    [Output('comparison-crime-selector', 'value'),
     Output('comparison-select-all-crimes', 'value')],
    [Input('comparison-select-all-crimes', 'value'),
     Input('comparison-crime-selector', 'value')],
    [State('comparison-crime-selector', 'options')]
)
def sync_comparison_crime_checkboxes(select_all, selected_crimes, available_options):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'comparison-select-all-crimes':
        if 'all' in select_all:
            return [option['value'] for option in available_options], ['all']
        else:
            return [], []
    else:
        if len(selected_crimes) == len(available_options):
            return selected_crimes, ['all']
        elif not selected_crimes:
            return [], []
        else:
            return selected_crimes, []

# Atualiza lista de indicadores economicos com base na pesquisa (comparação)
@app.callback(
    Output('comparison-economic-selector', 'options'),
    Input('comparison-economic-search', 'value')
)
def update_comparison_economic_options(search_value):
    if not search_value:
        return [{'label': metric, 'value': metric} for metric in economic_metrics]
    filtered = [metric for metric in economic_metrics if search_value.lower() in metric.lower()]
    return [{'label': metric, 'value': metric} for metric in filtered]

# Sincroniza checkboxes de indicadores economicos na aba de comparação
@app.callback(
    [Output('comparison-economic-selector', 'value'),
     Output('comparison-select-all-economics', 'value')],
    [Input('comparison-select-all-economics', 'value'),
     Input('comparison-economic-selector', 'value')],
    [State('comparison-economic-selector', 'options')]
)
def sync_comparison_economic_checkboxes(select_all, selected_metrics, available_options):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'comparison-select-all-economics':
        if 'all' in select_all:
            return [option['value'] for option in available_options], ['all']
        else:
            return [], []
    else:
        if len(selected_metrics) == len(available_options):
            return selected_metrics, ['all']
        elif not selected_metrics:
            return [], []
        else:
            return selected_metrics, []
        
# =============================================
# EXECUÇÃO DO APLICATIVO
# =============================================
if __name__ == '__main__':
    app.run(debug=True)