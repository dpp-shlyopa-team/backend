import pandas as pd
import json
from datetime import datetime
from tqdm import tqdm

print('Reading df...')
df = pd.read_csv("archive_5.zip")
print('Clearing df...')
df = df[df['VesselName'].notna()]
df = df[df['Length'].notna()]
df = df[df['Width'].notna()]
df = df[df['Status'].notna()]
df = df[df['Draft'].notna()]
df = df[df['IMO'].notna()]
df = df[df['CallSign'].notna()]
df = df[df['Cargo'].notna()]
df = df.loc[df['Width'] != 0]
df = df.loc[df['Length'] != 0]
print('Sorting df...')
df = df.sort_values(by=['MMSI', 'BaseDateTime'])
print('Connecting db...')
import mysql.connector as ms
connection = ms.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
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
  cursor.execute('INSERT INTO `dpp.shlyopa.db`.stamps VALUES (%s, %s, %s, %s)', [MMSI, dt, lat, lon])