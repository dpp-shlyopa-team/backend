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
async def get_main(request: Request, page: int = 1):
  if (page < 1):
    page = 1
  print(page)
  db = Database()
  r = await db.fetchall("SELECT * FROM `dpp.shlyopa.db`.vessels WHERE LENGTH(MMSI) >= 9 LIMIT 15 OFFSET %s", [page * 15])
  r2 = await db.fetchall("SELECT MMSI FROM `dpp.shlyopa.db`.vessels WHERE LENGTH(MMSI) >= 9")
  
  js_data = [None] * len(r2)
  
  import math
  col = math.floor(len(r2) / 15)

  print(col)

  fields = ['MMSI', 'VesselName', 'CallSign', 'Length', 'Width', 'Cargo', 'VesselType']


  for i in range(len(r2)):
    js_data[i] = await db.fetchall("SELECT latitude, longitude FROM `dpp.shlyopa.db`.stamps WHERE MMSI = %s AND id mod 30 = 0", [r2[i][0]])

  import json

  return templates.TemplateResponse("main.html", {
    "request": request, 
    "fields": fields,
    "data": r,
    "col": col,
    "page": page,
    "js_data": json.dumps(js_data)
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
    'VesselType': r1[6]
  }
  
  fields = ['datetime', 'latitude', 'longitude']

  import json
  
  return templates.TemplateResponse("vessel.html", {
    "request": request, 
    "fields": fields,
    "data": r2,
    "main_data": a,
    "js_data": json.dumps([list(i)[1:] for i in r2])
  }) 


@app.get("/1")
async def q():
  return "1"