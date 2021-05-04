import datetime
import logging
from os import environ
from time import sleep

import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from src.eagle200 import get_instantaneous_demand, get_smartmeter_id
from src.util import build_influx_measurements


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

GATEWAY_IP = environ.get("GATEWAY_IP")
USERNAME = environ["CLOUDID"]
PASSWORD = environ["INSTALLATION_CODE"]

INFLUX_BUCKET = environ.get("INFLUX_BUCKET", "eagle200")

CHECK_INTERVAL = int(environ.get("CHECK_INTERVAL", "30"))
RETRY_LIMIT = int(environ.get("RETRY_LIMIT", "3"))


def do_it():
    endpoint = f"http://{GATEWAY_IP}/cgi-bin/post_manager"
    influx_client = InfluxDBClient.from_env_properties()
    influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    s = requests.Session()
    s.auth = (USERNAME, PASSWORD)
    meter_id = get_smartmeter_id(s, endpoint)

    while True:
        instantaneous_demand = get_instantaneous_demand(s, endpoint, meter_id)
        utc_dt = datetime.datetime.utcnow()
        influx_data = build_influx_measurements(
            instantaneous_demand=instantaneous_demand, utc_dt=utc_dt
        )
        logging.info("submitting stats to Influx")
        logging.info(influx_data)
        influx_write_api.write(INFLUX_BUCKET, record=influx_data)
        logging.info(f"sleeping for {CHECK_INTERVAL}")
        sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    do_it()
