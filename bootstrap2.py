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
import plotly.graph_objects as go


PLOTLY_LOGO = "https://correlation1-public.s3-us-west-2.amazonaws.com/training/COLOMBIA+MAIN+SANS+TAG.svg"

###############################################################
#Load and modify the data that will be used in the app.
#################################################################
df1=stats.df5

df2 = stats.runQuery("""select * from master_table;""")
df4 = df2.groupby(['source','frame']).sum().reset_index().sort_values(['frame'],ascending=True)
#-------------------------------------------



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
                    dcc.Interval(
                        id='interval-component',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                    )
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
            'Asakusa_Kaminarimon_Gate_1_mall.mp4': 'https://youtu.be/ddT0cy2hlxw',
            'Times3_street.mp4': 'https://youtu.be/yqI0DlNUjos',
            'Times_Square-Manhattan-New_York_City_1_street.mp4': 'https://youtu.be/CJJ46OPtnws',
            'pedestrians_street.mp4': 'https://youtu.be/W6Masgc8b4U',
            'Shibuya_Scramble_Crossing_Live_Camera_2_street.mp4': 'https://youtu.be/abYr5lZr4r4'
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
    
    if selected_boxes==[]:
        selected_boxes=['Yes','No']
    else:
        selected_boxes=selected_boxes
    
    if locs==[]:
        locs=['Metro Station','Mall','Restaurant','street','Hospital']
    else:
        locs=locs
    
    filtereddf1=df1[df1['Violations'].isin(selected_boxes)][df1['Location Type'].isin(locs)][df1['Hour'].between(min(time),max(time))]
    
    df2=filtereddf1.groupby(["Hour","Violations"]).sum().reset_index().drop(columns=['Average Distance'])
    
    df2['Average Distance']=df2['total distance']/df2['Number of Observations']
    
    df3=filtereddf1.groupby(["Violations","Location Type"]).sum().reset_index()
    
            
    fig_1=px.scatter(filtereddf1, x="Average Distance", y="Number of Observations", color="Violations", size="Average Distance",
                size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    time_fig = px.scatter(df2, x="Hour", y="Number of Observations", color="Violations", size="Average Distance",
          size_max=15,width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    time_fig.update_layout(xaxis_type='category',
                  title_text='Observations per Time of the Day',
                    title_x=0.5)
    
    loc_pie = px.pie(df3.groupby('Location Type').sum().reset_index(), values='Number of Observations', names='Location Type', title='Observations per Location Type',width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
    
    loc_pie.update_layout(title_x=0.5)
    
    loc_hist=px.histogram(df3, x="Location Type", y="Number of Observations", color="Violations",width=700,height=300,color_discrete_sequence= px.colors.diverging.Picnic)
        
    return fig_1,time_fig,loc_pie,loc_hist


# Actualizacion de seleccion del video
@app.callback(Output("video_player", "url"),
              [Input('demo-dropdown', 'value')])
def select_footage(footage):
    # Find desired footage and update player video
    url = url_dict[footage]
    return url

# Actualizacion de las graficas
@app.callback(
    Output("bar-score-graph","figure"),
    [Input('demo-dropdown', 'value'),
    Input('interval-component', 'n_intervals')],
    [State('video_player', 'currentTime'),
    State('demo-dropdown', 'value')]
)
def update_barplor(value, n, currentTime, footage):
    if currentTime is None:
        return {}
    else:
        if n > 0:
            current_frame = round(currentTime * 24)
            data = df4[(df4['frame']<=current_frame) & (df4['source']==footage)]
            figure = go.Figure()
            figure.add_trace(go.Scatter(x=data['frame'], y=data['people_detected'],
                    mode='lines',
                    name='people detected'))
            figure.add_trace(go.Scatter(x=data['frame'], y=data['number_of_distance_violations'],
                    mode='lines',
                    name='Violations detected'))
            
            figure.update_layout(plot_bgcolor="white", xaxis = dict(showticklabels=False), yaxis_title="Count")

            return figure

        


if __name__ == "__main__":
    app.run_server(debug = True, host='0.0.0.0', port=8050)
