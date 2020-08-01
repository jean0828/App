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

from sqlalchemy import create_engine,text
engine = create_engine('postgresql+psycopg2://team_9:social_distancing@social-distancing-detector.cbnepizjacyt.us-east-2.rds.amazonaws.com/social_distancing_info')

def runQuery(sql):
    result = engine.connect().execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

df2=runQuery("""select * from master_table;""")

df2['Hour']=pd.to_datetime(df2['date_time']).dt.hour
df2['NonViolations']=df2['people_detected']-df2['number_of_distance_violations']


df2=df2.drop(columns={'date_time'
                      ,'source','people_detected'
                      ,'all_distances_avg_m','positios_with_violations'
                     ,'positions_whitout_violations'}).dropna()

df3=pd.melt(df2,id_vars=['place','frame','Hour','distances_violations_avg_m'],
            value_vars=['number_of_distance_violations']).rename(columns={'distances_violations_avg_m':'Average Distance'})
df4=pd.melt(df2,id_vars=['place','frame','Hour','good_distances_avg_m'],
            value_vars=['NonViolations']).rename(columns={'good_distances_avg_m':'Average Distance'})

df5=pd.concat([df3,df4],ignore_index=True).rename(columns={'place':'Location Type','variable':'Violations','value':'Number of Observations'}).reindex()

df5['Violations'].replace({"number_of_distance_violations": "Yes", "NonViolations": "No"}, inplace=True)

df5['total distance']=df5['Number of Observations']*df5['Average Distance']
df5['Location Type']=df5['Location Type'].str.capitalize()


yes_no_filter=dcc.Checklist(
    id='yes_no_filter',
    options=[
        {'label': 'Yes', 'value': 'Yes'},
        {'label': 'No', 'value': 'No'}
    ],
    value=['Yes','No'],
    labelStyle={'display': 'inline-block'},
    style={'font-size':'90%'}
)

hour_slicer=dcc.RangeSlider(
    id='hour_slicer',
    min=0,
    max=23,
    step=1,
    dots=True,
    value=[0,23],
    marks={0:'0:00',4:'4:00',8:'8:00',12:'12:00',16:'16:00',20:'20:00'}
)

location_filter=dcc.Checklist(
    id='location_filter',
    options=[
        {'label': 'Metro Station', 'value': 'Metro'},
        {'label': 'Beach', 'value': 'Beach'},
        {'label': 'Mall', 'value': 'Mall'},
        {'label': 'Restaurant', 'value': 'Restaurant'},
        {'label': 'Public Street', 'value': 'Street'}
    ],
    value=['Metro','Mall','Restaurant','Street','Beach'],
    style={'font-size':'90%'}
)
