import pandas as pd
import json
from datetime import datetime
from tqdm import tqdm
from CONFIG import *

fname = 'data.csv'
print(f'Reading {fname}...')
df = pd.read_csv(fname)
print('Connecting db...')
import mysql.connector as ms
connection = ms.connect(
    host=config['database']['host'],
    port=config['database']['port'],                         
    user=config['database']['user'],
    password=config['database']['password'],
    db=config['database']['database'],
    autocommit=True
)
cursor = connection.cursor()
cursor.execute("SELECT @@VERSION;")
print(cursor.fetchone())

for index, i in tqdm(df.iterrows(), total=df.shape[0]):
  MMSI = int(i['MMSI'])
  dt = datetime.fromisoformat(i['BaseDateTime']).strftime('%Y-%m-%d %H:%M:%S')
  lat = float(i['LAT'])
  lon = float(i['LON'])
  cursor.execute('INSERT INTO `dpp.shlyopa.db`.stamps (MMSI, datetime, latitude, longitude) VALUES (%s, %s, %s, %s)', [MMSI, dt, lat, lon])