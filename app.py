import dash
from dash import dcc, html
import plotly.express as px
from dash import dash_table
import pandas as pd

circuitos_df = pd.read_csv('data/circuitos.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Circuitos de Fórmula 1", style={'text-align': 'center'}),

    dcc.Dropdown(
        id='circuito-dropdown',
        options=[{'label': circuito, 'value': circuito} for circuito in circuitos_df['Circuito']],
        value=circuitos_df['Circuito'][0],
        style={'width': '50%', 'margin': 'auto'}
    ),

    html.Div(id='info-circuito', style={'text-align': 'center', 'margin-top': '20px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='mapa-circuitos')
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

        html.Div([
            html.H2("Tabla de Circuitos", style={'text-align': 'center'}),
            dash_table.DataTable(
                id='tabla-circuitos',
                columns=[{"name": i, "id": i} for i in circuitos_df.columns],
                data=circuitos_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center'},
                page_size=10,
            )
        ], style={'width': '38%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    html.H3("Ordenar por:", style={'text-align': 'center', 'margin-top': '30px'}),
    dcc.Dropdown(
        id='ordenar-por-dropdown',
        options=[
            {'label': 'Longitud', 'value': 'Longitud'},
            {'label': 'Vueltas', 'value': 'Vueltas'},
            {'label': 'Curvas', 'value': 'Curvas'}
        ],
        value='Longitud',
        style={'width': '30%', 'margin': 'auto'}
    ),
])


@app.callback(
    dash.dependencies.Output('tabla-circuitos', 'data'),
    dash.dependencies.Input('ordenar-por-dropdown', 'value')
)
def actualizar_tabla(ordenar_por):
    df_ordenado = circuitos_df.sort_values(by=ordenar_por, ascending=False)
    return df_ordenado.to_dict('records')

@app.callback(
    [dash.dependencies.Output('info-circuito', 'children'),
     dash.dependencies.Output('mapa-circuitos', 'figure')],
    [dash.dependencies.Input('circuito-dropdown', 'value')]
)
def update_info(selected_circuito):
    # Verificar si el circuito seleccionado existe en el DataFrame
    if selected_circuito not in circuitos_df['Circuito'].values:
        return "Circuito no encontrado", {}

    # Filtrar los datos para el circuito seleccionado
    circuito_info = circuitos_df[circuitos_df['Circuito'] == selected_circuito].iloc[0]
    
    info = [
        html.H3(f"{circuito_info['Circuito']} - {circuito_info['Pais']}"),
        html.P(f"Longitud: {circuito_info['Longitud']} km"),
        html.P(f"Vueltas: {circuito_info['Vueltas']}"),
        html.P(f"Curvas: {circuito_info['Curvas']}"),
        html.P(f"Récord de vuelta: {circuito_info['Récord de vuelta']}"),
        html.P(f"Último ganador: {circuito_info['Último ganador']}")
    ]
    
    # Crear el gráfico de mapa interactivo
    fig = px.scatter_geo(circuitos_df, lat='Latitud', lon='Longitud_geo',
                         text='Circuito', hover_name='Circuito', 
                         title="Ubicación de los Circuitos de F1",
                         size_max=15,  # Tamaño máximo de los puntos
                         color='Longitud',  # Color de los puntos según la longitud (puedes cambiarlo)
                         color_continuous_scale="Viridis",  # Escala de color
                         projection="natural earth")  # Proyección del mapa
    
    # Ajustar la vista del mapa
    fig.update_geos(
        visible=True,
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="whitesmoke",
        showocean=True,
        oceancolor="lightblue",
        projection_scale=5  # Controla el nivel de zoom (puedes ajustarlo)
    )

    # Mejorar los detalles de los puntos
    fig.update_traces(marker=dict(sizemode='diameter', opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))

    return info, fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
