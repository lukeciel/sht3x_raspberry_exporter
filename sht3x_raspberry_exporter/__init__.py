import time
import smbus
import threading
import sht3x_raspberry_exporter.sht3x as sht3x
import pyramid.httpexceptions as httpexceptions
from pyramid.config import Configurator
from pyramid.response import Response


__version__ = "1.0.0"

index_template = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>sht3x_raspberry_exporter</h1>
        <p><a href="metrics">Metrics</a></p>
    </body>
</html>
"""

metrics_template = """
# HELP sht3x_raspberry_temperature The measured temperature in °C.
# TYPE sht3x_raspberry_temperature gauge
sht3x_raspberry_temperature {temp}

# HELP sht3x_raspberry_humidity The measured humidity in percent (0-100).
# TYPE sht3x_raspberry_humidity gauge
sht3x_raspberry_humidity {humidity}
"""

bus_lock = threading.Lock()


def index(request):
    return Response(index_template)


def metrics(request):
    lock_acquired = bus_lock.acquire(timeout=5)
    if not lock_acquired:
        raise httpexceptions.HTTPServiceUnavailable("smbus cannot be locked")
    
    bus = smbus.SMBus(1)
    time.sleep(0.2)

    try:
        temp, humidity = sht3x.read_temperature_and_humidity(bus)
    except sht3x.CRCError:
        raise httpexceptions.HTTPInternalServerError("Sensor data is corrupted")

    metrics = metrics_template.format(temp=temp, humidity=humidity).strip()
    
    bus.close()
    bus_lock.release()

    return Response(
        metrics,
        content_type="text/plain"
    )


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route("index", "/")
    config.add_route("metrics", "/metrics")
    config.add_view(index, route_name="index")
    config.add_view(metrics, route_name="metrics")
    
    return config.make_wsgi_app()
