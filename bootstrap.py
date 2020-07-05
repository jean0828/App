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








body = html.Div([
    
    
    dbc.Container([
        dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Tab one',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Tab two',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),

        dbc.Col( html.Div(
                    className='video-outer-container',
                    children=html.Div(
                        style={'width': '100%', 'paddingBottom': '56.25%', 'position': 'relative'},
                        children=player.DashPlayer(
                            id='video-display',
                            style={'position': 'absolute', 'width': '100%',
                                   'height': '100%', 'top': '0', 'left': '1', 'bottom': '0', 'right': '0'},
                            url='https://www.youtube.com/watch?v=gPtn6hD7o8g',
                            controls=True,
                            playing=False,
                            volume=1,
                            width='100%',
                            height='100%'
                        )
                    )
        ),width=6,align='center'
        ),

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