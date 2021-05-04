import datetime
import json
import logging
from os import environ
from pathlib import Path
from typing import Optional


PERSIST_FILE = environ.get(
    "PERSIST_FILE", Path.joinpath(Path.home(), "eagle200.json")
)


def build_influx_measurements(
    utc_dt: datetime.datetime,
    instantaneous_demand: float,
):
    assert isinstance(instantaneous_demand, float)
    influx_data = [
        {
            "measurement": "InstantaneousDemand",
            "time": utc_dt,
            "fields": {"kW": float(instantaneous_demand)},
        }
    ]
    return influx_data


def save_meter_id(meter_id: str):
    data = {"meter_id": meter_id}
    out = json.dumps(data, indent=2)
    with open(PERSIST_FILE, "wt") as fh:
        logging.info(f"Writing {PERSIST_FILE}")
        fh.write(out)


def load_meter_id() -> Optional[str]:
    if Path(PERSIST_FILE).exists():
        with open(PERSIST_FILE, "rt") as fh:
            logging.info(f"Loading {PERSIST_FILE}")
            return json.loads(fh.read())["meter_id"]
