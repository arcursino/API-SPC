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


#Create map object

app.layout = html.Div([         
    dbc.Row(
            [                
                html.Div('Hello World'),                     
                               
            ],
            style={'margin-left': '20rem',
                   'margin-top': '6rem',
                   "padding": "1rem 1rem 1rem 1rem"},
            no_gutters=True
        ),   
])

import socket
host = socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    app.run_server(debug=True, host=host, port=8080)