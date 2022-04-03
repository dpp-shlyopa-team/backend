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
  return [{'MMSI': 367078130, 'LAT': 0.06667, 'LON': -122.3886, 'Length': 40, 'Width': 10}, {'MMSI': 367078130, 'LAT': 0.06667, 'LON': -122.3886, 'Length': 40, 'Width': 10}, {'MMSI': 367078130, 'LAT': 0.06667, 'LON': -122.3886, 'Length': 40, 'Width': 10}]