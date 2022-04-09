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
  db = Database()
  r = await db.fetchall("SELECT * FROM `dpp.shlyopa.db`.vessels WHERE LENGTH(MMSI) >= 9 LIMIT 15 OFFSET %s", [page * 15])
  col = await db.fetchone("SELECT COUNT(*) FROM `dpp.shlyopa.db`.vessels WHERE LENGTH(MMSI) >= 9")
  
  import math
  col = math.floor(col[0] / 15)

  fields = ['MMSI', 'VesselName', 'CallSign', 'Length', 'Width', 'Cargo', 'VesselType']

  return templates.TemplateResponse("main.html", {
    "request": request, 
    "fields": fields,
    "data": r,
    "col": col,
    "page": page
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
