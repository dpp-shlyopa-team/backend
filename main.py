from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def get():
  import json
  with open('data.json') as f:
    r = json.loads(f.read())
  res = [None for _ in range(len(r))]
  
  for i in range(len(r)):
    res[i] = {
      'MMSI': r[i]['MMSI'],
      'VesselName': r[i]['VesselName'],
      'Length': r[i]['Length'],
      'Width': r[i]['Width']
    }
    
  return res