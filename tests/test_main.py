"""Tests for the CO2 Meter Exporter HTTP endpoints."""
# pylint: disable=redefined-outer-name
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_root_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_root_shows_co2(client):
    response = client.get("/")
    assert "850" in response.text


def test_root_shows_temperature(client):
    response = client.get("/")
    assert "22.5" in response.text


def test_root_links_to_metrics(client):
    response = client.get("/")
    assert "/metrics" in response.text


def test_metrics_ok(client):
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_content_type(client):
    response = client.get("/metrics")
    assert "text/plain" in response.headers["content-type"]


def test_metrics_contains_gauges(client):
    response = client.get("/metrics")
    assert "co2meter_co2_ppm" in response.text
    assert "co2meter_temperature_c" in response.text
    assert "co2meter_sensor_info" in response.text
