"""WeatherstagePublisher class for weatherstage.com integration."""

import logging

import httpx
import json

import homeassistant.util.ssl as hass_ssl

_LOGGER = logging.getLogger(__name__)


class WeatherstagePublisher:
    """Weatherstage.com http publisher."""

    def __init__(self, api_endpoint_url: str, config_options):
        self.config_options = config_options
        self.api_endpoint_url = api_endpoint_url
        self.api_data = {
            "model": "Home Assistant Integration",
            "version": "0.0.1",
            "temperature": {"value": None, "unit": "c"},
            "humidity": {"value": None, "unit": "%"},
            "barometric_pressure_absolute": {"value": None, "unit": "hpa"},
            "barometric_pressure_relative": {"value": None, "unit": "hpa"},
        }

        self.api_data_old = {
            "model": "Home Assistant Integration",
            "version": "0.0.1",
            "temp_value": "12.1",
            "temp_unit": "c",
            "humidity_value": 80,
        }
        # map unit to api presentation
        self.unit_conversion = {"°C": "c", "°F": "f", "%": "%", "hPa": "hpa"}

    async def _send_data(self):
        """Publish sensor data to api endpoint."""
        # check if api data dict in filled with all values
        for api_item in self.api_data:
            if "value" in api_item:
                if api_item["value"] is None:
                    # skip api send if a value is still not filled
                    _LOGGER.info("API post skipped: %s", api_item)
                    return False
        ssl_context = hass_ssl.client_context()

        async with httpx.AsyncClient(verify=ssl_context) as client:
            # json_data = json.dumps(self.api_data_old)
            json_data = json.dumps(self.api_data)
            _LOGGER.info("JSON: %s", json_data)
            headers = {"content-type": "application/json"}
            response = await client.post(
                self.api_endpoint_url, data=json_data, headers=headers
            )
            if response.status_code != 204:
                _LOGGER.error(
                    "API post failed: resp: %s, request: %s", response, response.request
                )
            else:
                _LOGGER.info("API post success: %s", response)
        return True

    async def _set_event_data(self, event, api_item_name):
        """Fill api data dict."""
        _LOGGER.info("Event: %s", event)
        new_state = event.data.get("new_state")
        self.api_data[api_item_name]["value"] = round(float(new_state.state), 1)
        # convert unit of measurement to the one used by the API
        unit_of_measurement = new_state.attributes.get("unit_of_measurement")
        unit_of_measurement = self.unit_conversion.get(
            unit_of_measurement, unit_of_measurement
        )
        self.api_data[api_item_name]["unit"] = unit_of_measurement
        await self._send_data()
        return True

    async def set_temp(self, event):
        """Set temperature value."""
        await self._set_event_data(event, "temperature")
        return True

    async def set_humi(self, event):
        """Set humidity value."""
        await self._set_event_data(event, "humidity")
        return True

    async def set_pres_abs(self, event):
        """Set presure value."""
        await self._set_event_data(event, "barometric_pressure_absolute")
        await self._set_event_data(event, "barometric_pressure_relative")
        return True

    # Define the callback function to handle state changes
    async def print_event_debug(event):
        """Print event data for debuggin."""
        # _LOGGER.info("Even Data: %s", event.data)
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        # Access the friendly_name from the new state's attributes
        entity_id = new_state.entity_id
        # Access the unit of measurement from the new state's attributes
        unit_of_measurement = new_state.attributes.get("unit_of_measurement")

        if new_state is not None:
            new_value = new_state.state
            old_value = old_state.state if old_state else "unknown"
            _LOGGER.info(
                "%s, changed from %s to %s, in %s @ %s",
                entity_id,
                old_value,
                new_value,
                unit_of_measurement,
                new_state.last_changed,
            )
