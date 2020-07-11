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
#Load and modify the data that will be used in the app.
#################################################################

df1=pd.read_csv("data/sample_db.csv")
df1['hour']=pd.to_datetime(df1['Time']).dt.hour
df1['total distance']=df1['Number of observations']*df1['Average distance']
#chart 1. Time of the day vs Number of violations and number of compliant observations
df2=df1.groupby(["hour","Violations"]).sum().reset_index().drop(columns=['Average distance','Location','Record'])
df2['Average Distance']=df2['total distance']/df2['Number of observations']
time_fig = px.scatter(df2, x="hour", y="Number of observations", color="Violations", size="Average Distance",
          size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
time_fig.update_layout(xaxis_type='category',
                  title_text='Observations per Time of the Day',
                    title_x=0.5)

#chart of violations per area
df3=df1.groupby(["Violations","Location type"]).sum().reset_index().drop(columns=['Average distance','Location','Record'])
df3['Average Distance']=df3['total distance']/df3['Number of observations']

loc_pie = px.pie(df3.groupby('Location type').sum().reset_index(), values='Number of observations', names='Location type', title='Observations per Location type',width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
loc_pie.update_layout(title_x=0.5)

loc_hist=px.histogram(df3, x="Location type", y="Number of observations", color="Violations",width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)

        #Average distance figure

dist_fig = px.scatter(df1, x="Average distance", y="Number of observations", color="Violations", size="Average distance",
                size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
dist_fig.update_layout(title_text='Number of Observations versus Average Distance',
                            title_x=0.5)
graph1 = dcc.Graph(figure=dist_fig,id='dist_fig')
graph2 = dcc.Graph(figure=time_fig,id='time_fig')
graph3 = dcc.Graph(figure=loc_pie,id='loc_pie')
graph4 = dcc.Graph(figure=loc_hist,id='loc_hist')

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
        {'label': 'Metro Station', 'value': 'Metro Station'},
        {'label': 'Hospital', 'value': 'Hospital'},
        {'label': 'Mall', 'value': 'Mall'},
        {'label': 'Restaurant', 'value': 'Restaurant'},
        {'label': 'Public Street', 'value': 'Public Street'}
    ],
    value=['Metro Station','Mall','Restaurant','Public Street','Hospital'],
    style={'font-size':'90%'}
)
