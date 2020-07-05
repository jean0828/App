import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_player as player

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://correlation1-public.s3-us-west-2.amazonaws.com/training/COLOMBIA+MAIN+SANS+TAG.svg"



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

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
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

        dbc.Col(html.Div(dbc.Alert("This is one column", color="primary"))),
        dbc.Row([
                 dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=6)
                 , dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=4)
                 , dbc.Col(html.Div(dbc.Alert("One of three columns", color="primary")), md=2)



        ])
            
            
     ],
     fluid=True,
     )
    ])
app.layout = html.Div([navbar, body])




if __name__ == "__main__":
    app.run_server(debug = True)