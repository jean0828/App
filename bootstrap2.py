import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_player as player
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
import plotly.io as pio
import pandas as pd
import plotly.express as px
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
#-------------------------------------------
df4 = pd.read_csv("data/sample2.csv", sep=';')
df4 = df4.groupby('frame').count().reset_index()


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
        dbc.Row(
            [dbc.Col(html.Label('Violations',style={'font-weight': 'bold','font-size':'90%'}),width='0.8'),
             dbc.Col(stats.yes_no_filter,width='auto'),
             dbc.Col(html.Label('Time of the Day',style={'font-weight': 'bold','font-size':'90%'}),width='1.5'),
             dbc.Col(stats.hour_slicer,width='4'),
             dbc.Col(html.Label('Type of Location',style={'font-weight': 'bold','font-size':'90%'}),width='1.5'),
             dbc.Col(stats.location_filter)
            ]),
        html.Hr(),
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='dist_fig'), md=6),
                    dbc.Col(dcc.Graph(id='time_fig'), md=6),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='loc_pie'), md=6),
                    dbc.Col(dcc.Graph(id='loc_hist'), md=6),
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
                dbc.Col([
                    livingdemo.livegraph,
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

###########################################################
#
#          CALLBACKS:
#
###########################################################

# Data Loading
@app.server.before_first_request
def load_all_footage():
    global url_dict
    url_dict = {
            'Public Street': 'https://www.youtube.com/watch?v=obtERdHvM8o',
            'Mall': 'https://www.youtube.com/watch?v=obtERdHvM8o',
            'Hospital': 'https://www.youtube.com/watch?v=gPtn6hD7o8g'
    }



@app.callback([
    Output('dist_fig','figure'),
    Output('time_fig','figure'),
    Output('loc_pie','figure'),
    Output('loc_hist','figure')],
    [Input('yes_no_filter','value'),
    Input('location_filter','value'),
    Input('hour_slicer','value')])

def update_fig(selected_boxes,locs,time):
    df1=stats.df1
    filtereddf1=df1[df1['Violations'].isin(selected_boxes)][df1['Location type'].isin(locs)][df1['hour'].between(min(time),max(time))]
    
    df2=filtereddf1.groupby(["hour","Violations"]).sum().reset_index().drop(columns=['Average distance','Location','Record'])
    
    df2['Average Distance']=df2['total distance']/df2['Number of observations']
    
    df3=filtereddf1.groupby(["Violations","Location type"]).sum().reset_index().drop(columns=['Average distance','Location','Record'])
    
    df3['Average Distance']=df3['total distance']/df3['Number of observations']
            
    fig_1=px.scatter(filtereddf1, x="Average distance", y="Number of observations", color="Violations", size="Average distance",
                size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    time_fig = px.scatter(df2, x="hour", y="Number of observations", color="Violations", size="Average Distance",
          size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    time_fig.update_layout(xaxis_type='category',
                  title_text='Observations per Time of the Day',
                    title_x=0.5)
    
    loc_pie = px.pie(df3.groupby('Location type').sum().reset_index(), values='Number of observations', names='Location type', title='Observations per Location type',width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    loc_pie.update_layout(title_x=0.5)
    
    loc_hist=px.histogram(df3, x="Location type", y="Number of observations", color="Violations",width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
        
    return fig_1,time_fig,loc_pie,loc_hist


# Actualizacion de seleccion del video
@app.callback(Output("video_player", "url"),
              [Input('demo-dropdown', 'value')])
def select_footage(footage):
    # Find desired footage and update player video
    url = url_dict[footage]
    return url

# Actualizacion de las 
@app.callback(
    Output("bar-score-graph","figure"),
    [Input('demo-dropdown', 'value')],
    [State('video_player', 'currentTime'),
    State('demo-dropdown', 'value')]
)
def update_barplor(value, currentTime, footage):
    if currentTime is None:
        place_plot = df1[df1['Location type']==value].groupby('hour').count()
        place_figure = px.bar(place_plot, y='Violations')
        place_figure.update_layout(title_text='Number of Violation versus Time', title_x=0.5)
        return place_figure
    else:
        current_frame = round(currentTime * 5)
        figure = px.line(df4[df4['frame']<=current_frame],x='frame', y='violation')
        return figure

        


if __name__ == "__main__":
    app.run_server(debug = True)
