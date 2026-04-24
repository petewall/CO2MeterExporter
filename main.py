"""
CO2 Meter Exporter

This turns CO2 and temperature measurements from a CO2 Meter into
Prometheus-style metrics.
"""

import os
from contextlib import asynccontextmanager
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
import co2meter as co2

# Environment
BYPASS_DECRYPT = os.getenv('BYPASS_DECRYPT', '').lower() in ('true', '1', 'yes')
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', default='60'))

# Metrics
co2_gauge = Gauge('co2meter_co2_ppm', 'CO2 measurement, in parts per million')
temperature_gauge = Gauge('co2meter_temperature_c', 'Temperature, in degrees celsius')

# Modules
monitor = co2.CO2monitor(bypass_decrypt=BYPASS_DECRYPT)

# Set up info metric
sensor_info = Gauge(
    name='co2meter_sensor_info',
    documentation='Information about the CO2 Sensor',
    labelnames=['manufacturer', 'product_name', 'serial_no']
).labels(
    manufacturer=monitor.info['manufacturer'],
    product_name=monitor.info['product_name'],
    serial_no=monitor.info['serial_no'],
).set(1)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    monitor.start_monitoring(interval=MONITORING_INTERVAL)
    yield
    monitor.stop_monitoring()

app = FastAPI(lifespan=lifespan)

def read_data():
    _, current_co2, current_temperature = monitor.read_data()
    co2_gauge.set(current_co2)
    temperature_gauge.set(current_temperature)
    return current_co2, current_temperature

@app.get("/")
def get_root():
    co2_ppm, temp_c = read_data()
    return HTMLResponse(content=f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="{MONITORING_INTERVAL}">
  <title>CO2 Meter</title>
  <style>
    body {{ font-family: sans-serif; max-width: 480px; margin: 4rem auto; padding: 0 1rem; color: #222; }}
    h1 {{ font-size: 1.4rem; margin-bottom: 2rem; }}
    .readings {{ display: flex; gap: 1.5rem; }}
    .card {{ flex: 1; border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; text-align: center; }}
    .card .value {{ font-size: 2.5rem; font-weight: bold; margin: 0.25rem 0; }}
    .card .label {{ font-size: 0.85rem; color: #666; }}
    footer {{ margin-top: 2rem; font-size: 0.85rem; }}
    a {{ color: #0066cc; }}
  </style>
</head>
<body>
  <h1>CO2 Meter</h1>
  <div class="readings">
    <div class="card">
      <div class="value">{co2_ppm}</div>
      <div class="label">CO2 (ppm)</div>
    </div>
    <div class="card">
      <div class="value">{temp_c:.1f}</div>
      <div class="label">Temperature (°C)</div>
    </div>
  </div>
  <footer>Refreshes every {MONITORING_INTERVAL}s &mdash; <a href="/metrics">Prometheus metrics</a></footer>
</body>
</html>""")

@app.get("/metrics")
def get_metrics():
    """
    Returns the metrics
    """
    read_data()
    # https://fastapi.tiangolo.com/reference/responses/#fastapi.responses.PlainTextResponse
    # https://github.com/prometheus/client_python/blob/147c9d1ac01ae0c36446d1dee79aae85aaf98a6e/prometheus_client/exposition.py#L233
    return PlainTextResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
