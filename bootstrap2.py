import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_player as player
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
import plotly.io as pio
import pandas as pd

PLOTLY_LOGO = "https://correlation1-public.s3-us-west-2.amazonaws.com/training/COLOMBIA+MAIN+SANS+TAG.svg"

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
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.Col(html.Div(dbc.Alert("This is one column", color="primary"))),
            dbc.Row([
                 dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=6)
                 , dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=4)
                 , dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=2)
                 , html.Div(children=player.DashPlayer(
                    id = 'video_player',
                    url = 'https://www.youtube.com/watch?v=0lBjcaMokvo',
                    controls = True,
                    playing = False,
                    width = '600px',
                    height = '400px'

                 )),
                 



        ]),
        dbc.Row([
            dbc.Col(html.Div(
                                className='control-element',
                                children=[
                                    html.Div(children=["Footage Selection:"], style={'width': '40%'}),
                                    dcc.Dropdown(
                                        id="dropdown-footage-selection",
                                        options=[
                                            {'label': 'Drone recording of canal festival',
                                            'value': 'DroneCanalFestival'},
                                            {'label': 'Drone recording of car festival', 'value': 'car_show_drone'},
                                            {'label': 'Drone recording of car festival #2',
                                            'value': 'DroneCarFestival2'},
                                            {'label': 'Drone recording of a farm', 'value': 'FarmDrone'},
                                            {'label': 'Lion fighting Zebras', 'value': 'zebra'},
                                            {'label': 'Man caught by a CCTV', 'value': 'ManCCTV'},
                                            {'label': 'Man driving expensive car', 'value': 'car_footage'},
                                            {'label': 'Restaurant Robbery', 'value': 'RestaurantHoldup'},
                                            {'label': 'Social distancing detector', 'value': 'social_distancing'}
                                        ],
                                        value='social_distancing',
                                        clearable=False,
                                        style={'width': '60%'}
                                    )
                                ]
                ), md=12)


        ])
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