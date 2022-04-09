# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from database import Database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from tqdm import tqdm

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_main(request: Request):
  db = Database()
  r = await db.fetchall("SELECT * FROM `dpp.shlyopa.db`.vessels")
  
  fields = ['MMSI', 'VesselName', 'CallSign', 'Length', 'Width', 'Cargo', 'VesselType']

  return templates.TemplateResponse("main.html", {
    "request": request, 
    "fields": fields,
    "data": r
  })

@app.get("/vessel/{vessel_id}", response_class=HTMLResponse)
async def get_vessel(request: Request, vessel_id: int):
  db = Database()
  r1 = await db.fetchone("SELECT * FROM `dpp.shlyopa.db`.vessels WHERE MMSI = %s", [vessel_id])
  if (r1 == None):
    raise HTTPException(404, 'Not Found')
  r2 = await db.fetchall("SELECT datetime, latitude, longitude FROM `dpp.shlyopa.db`.stamps WHERE MMSI = %s", [vessel_id])
  a = {
    'MMSI': r1[0],
    'VesselName': r1[1],
    'CallSign': r1[2],
    'Length': r1[3],
    'Width': r1[4],
    'Cargo': r1[5],
    'VesselType': r1[6],
    'Stamps': [None] * len(r2)
  }
  
  fields = ['datetime', 'latitude', 'longitude']
  
  return templates.TemplateResponse("vessel.html", {
    "request": request, 
    "fields": fields,
    "data": r2,
    "main_data": a
  }) 
  
@app.get("/api/vessels")
async def get_vessel():
  db = Database()
  r1 = await db.fetchall("SELECT MMSI FROM `dpp.shlyopa.db`.stamps")
  return r1


@app.get("/api/vessel/{vessel_id}")
async def get_vessel(vessel_id: int):
  db = Database() 
  r1 = await db.fetchone("SELECT * FROM `dpp.shlyopa.db`.vessels WHERE MMSI = %s", [vessel_id])
  if (r1 == None):
    raise HTTPException(404, 'Not found')
  r2 = await db.fetchall("SELECT MMSI, VesselName, CallSign, Length, Width, Cargo, VesselType, TranscieverClass, Stamps FROM `dpp.shlyopa.db`.stamps WHERE MMSI = %s", [vessel_id])
  a = {
    'MMSI': r1[0],
    'VesselName': r1[1],
    'CallSign': r1[2],
    'Length': r1[3],
    'Width': r1[4],
    'Cargo': r1[5],
    'VesselType': r1[6],
    'TranscieverClass': r1[7],
    'Stamps': [None] * len(r2)
  }
  for i in range(len(r2)):
    a['Stamps'][i] = {
      'datetime': r2[i][1],
      'latitude': r2[i][2],
      'longitude': r2[i][3]
    }
  return a