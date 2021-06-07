import sqlite3
import dash
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
    except sqlite3.Error as e:
        print(e)
    return conn


def update_fig_layout(fig, fig_title):
    fig.update_layout(title=fig_title,
                      font={"size": 11, "color": "White"},
                      titlefont={"size": 15, "color": "White"}, margin={"r": 0, "t": 40, "l": 0, "b": 0},
                      geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                      paper_bgcolor='rgb(41, 56, 55)', )


db_con = create_connection('f1.db')
cur = db_con.cursor()

# race year map data
df = pd.DataFrame(cur.execute('''SELECT country, race_year, round FROM circuits
                       INNER JOIN races ON circuits.circuitId = races.circuitId;'''),
                  columns=['country', 'race_year', 'round'])
df.sort_values(by=['race_year'], inplace=True)
print(df[:5])

# pit stops data
df_stop = pd.DataFrame(cur.execute('''SELECT distinct stop, lap, race_year, duration, pit_stops.milliseconds, constructorRef FROM pit_stops
                            INNER JOIN races ON pit_stops.raceId = races.aceId
                            INNER JOIN results ON results.raceId = races.aceId
                            INNER JOIN constructors ON constructors.constructorId = results.constructorId
                            where lap<50'''),
                       columns=['stop', 'lap', 'race_year', 'duration', 'ms', 'constructorRef'])
print(df_stop[:5])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/f1ddlogo.png",
                 style={'maxHeight': '5%',
                        'maxWidth': '20%'}),
    ], style={'textAlign': 'center'}),

    dcc.Dropdown(id="race_year",
                 options=[{'label': i, 'value': i} for i in df['race_year'].unique()],
                 multi=False,
                 value=2021,
                 clearable=False,
                 style={'width': "40%",
                        'white-space': 'nowrap',
                        'text-overflow': 'ellipsis',
                        'backgroundColor': 'rgb(57, 81, 85)',
                        # text color in drop down list
                        'color': 'rgb(255, 255, 255)'},
                 className='dropdown'),
    html.Br(),
    html.Div([
        dcc.Graph(id='race_map', figure={}),
        dcc.Graph(id='drivers_points', figure={})
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([
        dcc.Graph(id='constructors_points', figure={}),
        dcc.Graph(id='pit_stops', figure={})
    ], style={'width': '50%', 'display': 'inline-block'})

])


@app.callback(
    [Output(component_id='race_map', component_property='figure'),
     Output(component_id='drivers_points', component_property='figure'),
     Output(component_id='pit_stops', component_property='figure'),
     Output(component_id='constructors_points', component_property='figure')],
    [Input(component_id='race_year', component_property='value')]
)
def update_graph(option_race):
    print(option_race)
    print(type(option_race))

    dff = df.copy()
    dff = dff[dff["race_year"] == option_race]

    pit_stop = df_stop.copy()
    if option_race > 2010:
        pit_stop = pit_stop[pit_stop["race_year"] == option_race]
    else:
        pit_stop = pit_stop[pit_stop["race_year"] == 2021]

    drift = pd.DataFrame(cur.execute('''SELECT sum(points) as points, race_year, driverRef FROM results
                                        INNER JOIN races ON results.raceId = races.aceId
                                        INNER JOIN drivers ON results.driverId = drivers.driverId
                                        where race_year=? and points>0
                                        group by driverRef
                                        order by sum(points) desc;''', (int(option_race),)),
                         columns=['points', 'race_year', 'driverRef'])

    constructor = pd.DataFrame(cur.execute('''SELECT sum(points) as points, race_year, constructorRef FROM results
                                            INNER JOIN races ON results.raceId = races.aceId
                                            INNER JOIN constructors ON results.constructorId = constructors.constructorId
                                            where race_year=? and points>0
                                            group by constructorRef
                                            order by sum(points) desc;''', (int(option_race),)),
                               columns=['points', 'race_year', 'constructorRef'])

    # Plotly Express
    race_year = px.choropleth(
        data_frame=dff,
        locations=dff['country'],
        locationmode='country names',
    )
    race_year.update_layout(showlegend=False)
    update_fig_layout(race_year, 'Race this year was held in')

    driver_points = px.bar(drift, x='driverRef', y='points',
                           labels={
                               "driverRef": "Driver",
                               "points": "Number of points"
                           })
    update_fig_layout(driver_points, 'Drivers points')

    constructor_points = px.bar(constructor, x='constructorRef', y='points',
                                labels={
                                    "constructorRef": "Constructor",
                                    "points": "Number of points"
                                })
    update_fig_layout(constructor_points, 'Constructors points')

    pit_stops = px.sunburst(pit_stop, path=['stop', 'constructorRef', 'lap'], values='ms')
    update_fig_layout(pit_stops, 'Pit Stops Time')

    return race_year, driver_points, constructor_points, pit_stops


if __name__ == '__main__':
    app.run_server(debug=True)
    db_con.close()
