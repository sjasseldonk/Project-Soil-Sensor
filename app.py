#!/usr/bin/env python
# coding: utf-8

# In[3]:


import paho.mqtt.client as mqtt
import time
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
import sqlalchemy as db
from sqlalchemy import insert, select, Table

broker_adress = "xxx.xxx.x.xx"
broker_port = 1883

db_user = 'newuser'
db_pwd = 'newpassword'
db_host = '192.168.1.131'
db_port = '3306'
db_name = 'tuin_db'

values_to_insert = []
connected = False

def main():
    try:
        client = mqtt.Client()
        client.on_connect = on_connect #attach function to callback
        client.on_message = on_message #attach function to callback
        
        client.connect(broker_adress, broker_port)
        client.subscribe("SoilValue1")
        
        # Start the loop
        client.loop_forever()

    
    except Exception as e:
        print(e)
    
    
# Connect to MQTT broker and subscribe to a topic to receive messages
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the MQTT broker!")
        global connected
        connected = True
    else:
        print("Connection to the MQTT broker failed.")

def on_message(client, userdata, msg):
    weather, weather_temp = weather_setup()
    time_value = time.asctime()
    
    data = {
        'DATE_TIME'    : time_value,
        'WEATHER'      : weather,
        'WEATHER_TEMP' : weather_temp,
        'SENSOR'       : msg.topic,
        'SOIL_VALUE'   : msg.payload
        }
    
    global values_to_insert
    values_to_insert.append(data)
    
    if int(time_value.split(':')[1]) % 5 == 0:
        result = db_setup(values_to_insert)
        print(f'{result} sensor values are successfully added to the database!')
        values_to_insert = []


def weather_setup():
    weather_access = YahooWeather(APP_ID="1syh9H7g",
                     api_key="dj0yJmk9UjAzQTV4RDVoZFVHJmQ9WVdrOU1YTjVhRGxJTjJjbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTc3",
                     api_secret="b901246a5fd186f4bb9a8e947dacb85e85afaed9")
    
    weather_access.get_yahoo_weather_by_city("Erp", Unit.celsius)
    weather = weather_access.condition.text
    weather_temp = weather_access.condition.temperature
    
    return weather, weather_temp

def db_setup(data):
    # Specify connetion string
    connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
            
    # Connect to database
    engine = db.create_engine(connection_str)
    connection = engine.connect()

    # Pull metadata of a table
    metadata = db.MetaData(bind=engine)
    
    # Reflect 'DATA_TUIN' table via engine
    data_tuin = Table('DATA_TUIN', metadata, autoload=True, autoload_with=engine)

    # Build an insert statement for the DATA_TUIN table: stmt
    stmt = insert(data_tuin)

    # Execute stmt with the data: results
    results = connection.execute(stmt, data)
    return results.rowcount        
        

if __name__=='__main__':
        main()


