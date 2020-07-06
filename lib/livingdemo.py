import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import dash_player as player


###############################################################
#Creaton of the youtube video.
#################################################################
video = html.Div([
            html.Div(children=player.DashPlayer(
                    id = 'video_player',
                    url = 'https://www.youtube.com/watch?v=obtERdHvM8o',
                    controls = True,
                    playing = False,
                    width = '750px',
                    height = '500px',

                 ))
])

###############################################################
#Creaton of the first markdown video.
#################################################################

dropdownvideo =  dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Social Distancing', 'value': 'social'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC',
        clearable=False,
        style={'width': '100%'}
    )
            
