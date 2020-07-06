import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_player as player
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
import plotly.io as pio
import pandas as pd
from lib import livingdemo, stats


PLOTLY_LOGO = "https://correlation1-public.s3-us-west-2.amazonaws.com/training/COLOMBIA+MAIN+SANS+TAG.svg"

###############################################################
#Load and modify the data that will be used in the app.
#################################################################
df1=pd.read_csv("data/sample_db.csv")
df1['hour']=pd.to_datetime(df1['Time']).dt.hour
df1['total distance']=df1['Number of observations']*df1['Average distance']
#chart 1. Time of the day vs Number of violations and number of compliant observations
df2=df1.groupby(["hour","Violations"]).sum().reset_index().drop(columns=['Average distance','Location','Record'])
df2['Average Distance']=df2['total distance']/df2['Number of observations']


navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Social Distancing Detector", className="ml-4")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col(stats.graph1, md=6),
                    dbc.Col(stats.graph2, md=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(stats.graph3, md=6),
                    dbc.Col(stats.graph4, md=6),
                ]
            ),
        ], fluid=True
        ),
        ]
    ),
    className="mt-3",
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                livingdemo.video,
                html.Hr(),
                html.Label('Select video to Observe'),
                livingdemo.dropdownvideo,

                ], width = 6),
            ]),
           
        
        ]
    ),
    className="mt-3",
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Living Demo",tabClassName="tab-boots"),
        dbc.Tab(tab2_content, label="Stats Summary",tabClassName="tab-boots"),
    ]
)





###########################################################
#
#           APP LAYOUT:
#
###########################################################
body = html.Div([
    
    
    dbc.Container([
        
        tabs,

        
            
            
     ],
     fluid=True,
     )
    ])
app.layout = html.Div([navbar, body])


if __name__ == "__main__":
    app.run_server(debug = True)