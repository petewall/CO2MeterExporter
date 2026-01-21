"""
CO2 Meter Exporter

This turns CO2 and temperature measurements from a CO2 Meter into
Prometheus-style metrics.
"""

import os
import signal
from prometheus_client import Gauge, generate_latest
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse
import co2meter as co2

# Environment
BYPASS_DECRYPT = bool(os.getenv('BYPASS_DECRYPT'))
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', default='60'))

# Metrics
co2_gauge = Gauge('co2meter_co2_ppm', 'CO2 measurement, in parts per million')
temperature_gauge = Gauge('co2meter_temperature_c', 'Temperature, in degrees celcius')

# Modules
app = FastAPI()
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

# Start the monitor
monitor.start_monitoring(interval=MONITORING_INTERVAL)
def _handle_ctrl_c(_signum, _frame):
    """
    Ensure the monitoring loop is stopped before exiting.
    """
    monitor.stop_monitoring()
    raise KeyboardInterrupt

signal.signal(signal.SIGINT, _handle_ctrl_c)

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
