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
            {'label': 'Asakusa Kaminarimon Gate', 'value': 'Asakusa_Kaminarimon_Gate_1_mall.mp4'},
            {'label': 'Times Street', 'value': 'Times3_street.mp4'},
            {'label': 'Time Square', 'value': 'Times_Square-Manhattan-New_York_City_1_street.mp4'},
            {'label': 'Pedestrians Street', 'value': 'pedestrians_street.mp4'},
            {'label': 'Shibuya Scramble', 'value': 'Shibuya_Scramble_Crossing_Live_Camera_2_street.mp4'}
        ],
        value='Asakusa_Kaminarimon_Gate_1_mall.mp4',
        clearable=False,
        style={'width': '100%'}
    )

livegraph =  dcc.Graph(
                        id="bar-score-graph"
)
            
