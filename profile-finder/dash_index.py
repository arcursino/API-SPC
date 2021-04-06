#imports 
import dash
import dash_table
import dash_auth
#from dash_extensions import Download
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
import pickle
import psycopg2
import numpy as np
import folium
import io
from dash.dependencies import Input, Output, State
from app import app
import geopandas
import plotly.express as px

#Create map object

#df = pd.read_csv('assets/dados.csv')
filename = 'assets/dados.json'
df = geopandas.read_file(filename, driver='GeoJSON')
geracoes = df['geracoes'].unique()
renda = df['renda'].unique()
estado = df['SIGLA_UF'].unique()
estado = sorted(estado)
colunas = df.columns

veteranos = df[df['geracoes'] == '1900 a 1940 - Veteranos']
boomers = df[df['geracoes'] == '1940 a 1959 - Baby Boomers ']
ger_x = df[df['geracoes'] == '1960 a 1979 - Geração Y']
ger_y = df[df['geracoes'] == '1980 a 1994 - Geração X']
ger_z = df[df['geracoes'] == '1994 a 2010 - Geração Z']

trace1 = go.Bar(
    x = veteranos['renda'].unique(),
    y = veteranos.groupby('renda')['geracoes'].count(),
    marker_color=px.colors.qualitative.Dark24[0],  #color
    text=veteranos.groupby('renda')['geracoes'].count(), #label/text
    textposition="outside", #text position
    name="Veteranos", #legend name
)

trace2 = go.Bar(
    x = boomers['renda'].unique(),
    y = boomers.groupby('renda')['geracoes'].count(),
    marker_color=px.colors.qualitative.Dark24[1],  #color
    text=boomers.groupby('renda')['geracoes'].count(), #label/text
    textposition="outside", #text position
    name="Baby Boomers", #legend name
)

trace3 = go.Bar(
    x = ger_x['renda'].unique(),
    y = ger_x.groupby('renda')['geracoes'].count(),
    marker_color=px.colors.qualitative.Dark24[2],  #color
    text=ger_x.groupby('renda')['geracoes'].count(), #label/text
    textposition="outside", #text position
    name="Geração X", #legend name
)

trace4 = go.Bar(
    x = ger_y['renda'].unique(),
    y = ger_y.groupby('renda')['geracoes'].count(),
    marker_color=px.colors.qualitative.Dark24[3],  #color
    text=ger_y.groupby('renda')['geracoes'].count(), #label/text
    textposition="outside", #text position
    name="Geração Y", #legend name
)

trace5 = go.Bar(
    x = ger_z['renda'].unique(),
    y = ger_z.groupby('renda')['geracoes'].count(),
    marker_color=px.colors.qualitative.Dark24[4],  #color
    text=ger_z.groupby('renda')['geracoes'].count(), #label/text
    textposition="outside", #text position
    name="Geração Z", #legend name
)

data = [trace1, trace2, trace3, trace4, trace5] #combine two charts/columns
layout = go.Layout(barmode="group", title="Faixa Salarial de acordo com as Gerações - Brasil") #define how to display the columns
fig1 = go.Figure(data=data, layout=layout)
fig1.update_layout(
    title=dict(x=0.5), #center the title
    xaxis_title="Faixa Salarial",#setup the x-axis title
    yaxis_title="Total", #setup the x-axis title
    margin=dict(l=20, r=20, t=60, b=20),#setup the margin
    paper_bgcolor="aliceblue", #setup the background color
)
fig1.update_traces(texttemplate="%{text:.2s}") #text formart

app.layout = html.Div(
    children=[
        html.Div(className="top-bar",
                 children=[
                     html.P(className="logo", children=["Profile Finder"])
                    ]
                 ),
        html.Div(className="menu-bar-left",
                 children=[
                     html.Div(style={'width' : '100%', 'height' : '45px', 'float' : 'left', 'borderLeft' : '3px solid yellow', 'marginTop' : '10px'},
                              children=[
                                      html.Img(src="/assets/imgs/stats.png", width="35px", height="35px", style={'marginTop' : '5px', 'marginLeft' : '10px'})
                                  ]),
                     
                    ]), ##menu1

        html.Div(className="menu-bar-filters", children=[
                html.Div(className="categories",
                         children=[
                             html.Div(className="filter-title-div",
                                      children=[html.Span(className="filter-title-span", children=['Escolha as opções'])
                                                ]),
                                 dcc.Dropdown(id='my_dropdown',className="filter-dropdown", style={'backgroundColor' : 'transparent', 'borderColor' : '#315475'},
                            options=[{'label': i, 'value': i} for i in estado],
                            value=[],
                            disabled=False,
                            clearable=True,
                            multi=False
                        )  
                             ]),              
                
            ]), ## menu 2

        html.Div(className="top-title"),

        html.Div(className="graph-1",
                 children=[
                     dcc.Graph(
                        id='our_graph',
                        figure = fig1,
                        #config={"displayModeBar": False},
                     ),
                    ]),
    ])


@app.callback(
    Output(component_id='our_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def groupby_estado(estado):
    filtered_data = df[df['SIGLA_UF'] == estado]
    veteranos = filtered_data[filtered_data['geracoes'] == '1900 a 1940 - Veteranos']
    boomers = filtered_data[filtered_data['geracoes'] == '1940 a 1959 - Baby Boomers ']
    ger_x = filtered_data[filtered_data['geracoes'] == '1960 a 1979 - Geração X']
    ger_y = filtered_data[filtered_data['geracoes'] == '1980 a 1994 - Geração Y']
    ger_z = filtered_data[filtered_data['geracoes'] == '1994 a 2010 - Geração Z']
    
    trace1 = go.Bar(
        x = veteranos['renda'].unique(),
        y = veteranos.groupby('renda')['geracoes'].count(),
        marker_color=px.colors.qualitative.Dark24[0],  #color
        text=veteranos.groupby('renda')['geracoes'].count(), #label/text
        textposition="outside", #text position
        name="Veteranos", #legend name
    )

    trace2 = go.Bar(
        x = boomers['renda'].unique(),
        y = boomers.groupby('renda')['geracoes'].count(),
        marker_color=px.colors.qualitative.Dark24[1],  #color
        text=boomers.groupby('renda')['geracoes'].count(), #label/text
        textposition="outside", #text position
        name="Baby Boomers", #legend name
    )

    trace3 = go.Bar(
        x = ger_x['renda'].unique(),
        y = ger_x.groupby('renda')['geracoes'].count(),
        marker_color=px.colors.qualitative.Dark24[2],  #color
        text=ger_x.groupby('renda')['geracoes'].count(), #label/text
        textposition="outside", #text position
        name="Geração X", #legend name
    )

    trace4 = go.Bar(
        x = ger_y['renda'].unique(),
        y = ger_y.groupby('renda')['geracoes'].count(),
        marker_color=px.colors.qualitative.Dark24[3],  #color
        text=ger_y.groupby('renda')['geracoes'].count(), #label/text
        textposition="outside", #text position
        name="Geração Y", #legend name
    )

    trace5 = go.Bar(
        x = ger_z['renda'].unique(),
        y = ger_z.groupby('renda')['geracoes'].count(),
        marker_color=px.colors.qualitative.Dark24[4],  #color
        text=ger_z.groupby('renda')['geracoes'].count(), #label/text
        textposition="outside", #text position
        name="Geração Z", #legend name
    )

    data = [trace1, trace2, trace3, trace4, trace5] #combine two charts/columns
    layout = go.Layout(barmode="group", title="Faixa Salarial de acordo com as Gerações - "  + estado ) #define how to display the columns
    fig1 = go.Figure(data=data, layout=layout)
    fig1.update_layout(
        title=dict(x=0.5), #center the title
        xaxis_title="Faixa Salarial",#setup the x-axis title
        yaxis_title="Total", #setup the x-axis title
        margin=dict(l=20, r=20, t=60, b=20),#setup the margin
        paper_bgcolor="aliceblue", #setup the background color
    )
    fig1.update_traces(texttemplate="%{text:.2s}") #text formart
    
    return fig1


    






import socket
host = socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    app.run_server(debug=True, host=host, port=8080)
