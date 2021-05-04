from bs4 import BeautifulSoup as bs
from requests.sessions import Session

from src.util import load_meter_id, save_meter_id


def get_instantaneous_demand(
    s: Session, endpoint: str, meter_id: str
) -> float:
    payload = f"""
<Command>
	<Name>device_query</Name>
	<DeviceDetails>
		<HardwareAddress>{meter_id}</HardwareAddress>
	</DeviceDetails>
	<Components>
		<Component>
			<Name>Main</Name>
			<Variables>
				<Variable>
					<Name>zigbee:InstantaneousDemand</Name>
				</Variable>
			</Variables>
		</Component>
	</Components>
</Command>
"""

    res = s.post(endpoint, data=payload)
    res.raise_for_status()
    xml = bs(res.text, "lxml")
    all_variables = xml.find_all("variable")
    return float(
        [
            variables
            for variables in all_variables
            if variables.find("name").text == "zigbee:InstantaneousDemand"
        ][0]
        .find("value")
        .text
    )


def get_smartmeter_id(s: Session, endpoint: str) -> str:
    meter_id = load_meter_id()

    if isinstance(meter_id, str):
        return meter_id

    payload = """
<Command>
	<Name>device_list</Name>
</Command>
"""

    res = s.post(endpoint, data=payload)
    res.raise_for_status()
    xml = bs(res.text, "lxml")
    meter_id = xml.find("hardwareaddress").text
    save_meter_id(meter_id)
    return get_smartmeter_id(s, endpoint)
