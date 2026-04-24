# CO2 Meter Exporter

A Prometheus metrics exporter for the [CO2 Meter](https://www.co2meter.com/) USB sensor, built on the [co2meter](https://github.com/vfilimonov/co2meter) library.

Exposes a live dashboard at `/` and Prometheus metrics at `/metrics`.

## Metrics

| Metric | Description |
| --- | --- |
| `co2meter_co2_ppm` | CO2 concentration in parts per million |
| `co2meter_temperature_c` | Temperature in degrees Celsius |
| `co2meter_sensor_info` | Labelled info metric with `manufacturer`, `product_name`, and `serial_no` |

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `MONITORING_INTERVAL` | `60` | How often (in seconds) the sensor is polled |
| `BYPASS_DECRYPT` | `false` | Set to `true` to skip USB packet decryption (useful for local dev without hardware) |

## Running locally

Install dependencies and start the server:

```sh
make run
```

This requires the CO2 meter to be plugged in. On macOS, HIDAPI talks to the device via IOKit — no extra setup needed. On Linux, you may need to add a udev rule to allow non-root access to the device.

The exporter is available at [http://localhost:9800](http://localhost:9800).

## Deploying with Docker

The container image is built for `linux/arm64` (Raspberry Pi). The CO2 meter must be passed through as a device:

```sh
docker run --device /dev/hidraw0 -p 9800:9800 ghcr.io/petewall/co2meter-exporter
```

Example `docker-compose.yml`:

```yaml
services:
  co2meter-exporter:
    image: ghcr.io/petewall/co2meter-exporter
    devices:
      - /dev/hidraw0:/dev/hidraw0
    ports:
      - "9800:9800"
    environment:
      MONITORING_INTERVAL: 60
    restart: unless-stopped
```

The `/dev/hidraw0` device node appears on Linux when the meter is plugged in. Check `ls /dev/hidraw*` or `dmesg | tail` if you are unsure of the path.

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Development

```sh
make lint   # Run pylint
make test   # Run pytest
```
