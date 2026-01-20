"""
CO2 Meter Exporter

This turns CO2 and temperature measurements from a CO2 Meter into
Prometheus-style metrics.
"""

import os
from prometheus_client import Gauge, Summary, generate_latest
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse
import co2meter as co2

# Environment
BYPASS_DECRYPT = bool(os.getenv('BYPASS_DECRYPT'))
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', default='60'))

# Metrics
co2_gauge = Gauge('co2meter_co2_ppm', 'CO2 measurement, in parts per million')
temperature_gauge = Gauge('co2meter_temperature_c', 'Temperature, in degrees celcius')
read_time = Summary('co2meter_request_processing_seconds', 'Time spent reading data from the meter')

# Modules
app = FastAPI()
monitor = co2.CO2monitor(bypass_decrypt=BYPASS_DECRYPT)
monitor.start_monitoring(interval=MONITORING_INTERVAL)

@read_time.time()
def read_data():
    """
    Reads the data from the CO2 Monitor
    """
    _, current_co2, current_temperature = monitor.read_data()
    co2_gauge.set(current_co2)
    temperature_gauge.set(current_temperature)

@app.get("/")
def get_root():
    """
    Redirects to the metrics endpoint
    """
    return RedirectResponse("/metrics")

@app.get("/metrics")
def get_metrics():
    """
    Returns the metrics
    """
    read_data()
    # https://fastapi.tiangolo.com/reference/responses/#fastapi.responses.PlainTextResponse
    # https://github.com/prometheus/client_python/blob/147c9d1ac01ae0c36446d1dee79aae85aaf98a6e/prometheus_client/exposition.py#L233
    return PlainTextResponse(content=generate_latest())
