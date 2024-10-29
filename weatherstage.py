"""WeatherstagePublisher class for weatherstage.com integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_HUMI_SENS,
    CONF_PRES_SENS,
    CONF_STATUS_REPORT,
    CONF_TEMP_SENS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class WeatherstagePublisher:
    """Weatherstage.com http publisher."""

    def __init__(self, api_endpoint_url: str, config_options):
        self.config_options = config_options
        self.api_endpoint_url = api_endpoint_url
        self.api_data = {
            "model": "Home Assistant Integration",
            "version": "0.0.1",
            "temperature": {"value": None, "unit": "°C"},
            "humidity": {"value": None, "unit": "%"},
            "barometric_pressure_absolute": {"value": None, "unit": "hPa"},
            "barometric_pressure_relative": {"value": None, "unit": "hPa"},
        }
        _LOGGER.info("WeatherstagePublisher.__init__ %s", api_endpoint_url)

    async def _send_data(self):
        """Publish sensor data to api endpoint."""
        _LOGGER.info("Publish: %s", self.api_data)
        return True

    async def _set_event_data(self, event, api_item_name):
        """Fill api data dict."""
        _LOGGER.info("Event: %s", event)
        new_state = event.data.get("new_state")
        self.api_data[api_item_name]["value"] = new_state.state
        self.api_data[api_item_name]["unit"] = new_state.attributes.get(
            "unit_of_measurement"
        )
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
