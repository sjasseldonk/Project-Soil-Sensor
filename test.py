import dash_core_components as dcc    
import dash_bootstrap_components as dbc    
import dash_html_components as html
import dash   
import plotly_express as px 

import pandas as pd

import sqlalchemy as db
from sqlalchemy import select, Table, MetaData

# For connection to db
db_user = 'newuser'
db_pwd = 'newpassword'
db_host = '192.168.2.95'
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
        showlegend=True
        )

    return fig

df = db_setup()
print(df.shape)
line_plot(df).show()