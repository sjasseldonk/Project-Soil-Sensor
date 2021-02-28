import dash_core_components as dcc    
import dash_bootstrap_components as dbc    
import dash_html_components as html
import dash   
import plotly_express as px 
from dash.dependencies import Input, Output

import pandas as pd
from datetime import datetime

import sqlalchemy as db
from sqlalchemy import select, Table, MetaData

# For connection to db
db_user = 'newuser'
db_pwd = 'newpassword'
db_host = '192.168.1.131'
db_port = '3306'
db_name = 'tuin_db'

def db_setup():
    # Specify connetion string
    connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
            
    # Connect to database
    engine = db.create_engine(connection_str)
    connection = engine.connect()

    # Reflect data_tuin table via engine
    metadata = MetaData(bind=engine)
    data_tuin = Table('DATA_TUIN', metadata, autoload=True, autoload_with=engine)

    # Select data from last 2 hours (last 120 rows in db) and execute
    stmt = select([data_tuin]).order_by(data_tuin.columns.ID.desc())
    results = connection.execute(stmt).fetchall()

    # Create a Dataframe from the results and set col names
    df = pd.DataFrame(results)
    df.columns = results[0].keys()

    # Convert data type to date_time and print the Dataframe
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])

    return df 


def line_plot(df):
    fig = px.line(df, x='DATE_TIME', y='SOIL_VALUE')

    fig.update_layout(
        yaxis=dict(title_text='Soil Value'),
        xaxis=dict(title_text='Date'),
        showlegend=True,
        margin=dict(l=10, r=10, t=10, b=10)
        )

    return fig

df = db_setup()
figure1 = line_plot(df)

app =  dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Dashboard Tuin")
            )
        ),

        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Sensor 1"),
                        dcc.DatePickerRange(
                            id='datepicker',
                            min_date_allowed=datetime(2020, 5, 11),
                            max_date_allowed=df['DATE_TIME'].max(),
                            initial_visible_month=df['DATE_TIME'].max(),
                            start_date=datetime(2020, 5, 11),
                            end_date=df['DATE_TIME'].max(),
                            style={
                                'margin-bottom' : 0,
                                'margin-top' : 0,
                                'padding' : 0
                            }
                        ),
                        dcc.Graph(id = 'sensor1', figure = figure1)
                    ]
                )
            )
        )

    ],
    style={'align-items': 'çenter', 'justify-content': 'center', 'textAlign' : 'center', 'font-size' : '80px', 'padding': 0, 'margin-top': '50px', 'margin-bottom': '50px', 'margin-left': '25px', 'margin-right': '25px'}

)


@app.callback(
    Output('sensor1', 'figure'),
    [Input('datepicker', 'start_date'),
    Input('datepicker', 'end_date')]
)
def update_figure(start_date, end_date):
    df = db_setup()
    df = df[(df['DATE_TIME'] >= start_date) & (df['DATE_TIME'] <= end_date)]

    fig = line_plot(df)        
    return fig


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port='8050')