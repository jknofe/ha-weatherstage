"""__init__.py for weatherstage.com integration."""

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
            "temperature": {"value": 12.1, "unit": "c"},
            "humidity": {"value": 65, "unit": "%"},
            "barometric_pressure_absolute": {"value": 995, "unit": "hpa"},
            "barometric_pressure_relative": {"value": 995, "unit": "hpa"},
        }
        _LOGGER.info("WeatherstagePublisher.__init__ %s", api_endpoint_url)

    def set_temp(self, event):
        """Publish sensor value to api endpoint."""
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        _LOGGER.info("Sensor value changed from %s to %s", old_value, new_value)
        return True

    def set_humi(self, event):
        """Publish sensor value to api endpoint."""
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        _LOGGER.info("Sensor value changed from %s to %s", old_value, new_value)
        return True

    def set_pres(self, event):
        """Publish sensor value to api endpoint."""
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        _LOGGER.info("Sensor value changed from %s to %s", old_value, new_value)
        return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up weatherstage.com from a config entry."""
    # Retrieve the configuration data
    config_data = entry.data
    config_options = entry.options

    # Use the configuration data as needed
    _LOGGER.info("Setting up weatherstage.com with config: %s", config_data)
    _LOGGER.info("Setting up weatherstage.com with options: %s", config_options)

    # Example: Store the config data in hass.data for later use
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = config_data

    # Define the callback function to handle state changes
    async def handle_sensor_change(event):
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
            # Here you can add any logic to handle the new value

    # Register the state change listener for the sensor entity
    MyWeatherstagePublisher = WeatherstagePublisher(
        config_data[CONF_URL], config_options
    )
    for conf_entry in (CONF_TEMP_SENS, CONF_HUMI_SENS, CONF_PRES_SENS):
        # _LOGGER.info("Create %s", config_options[conf_entry])
        async_track_state_change_event(
            hass, config_options[conf_entry], handle_sensor_change
        )
    # Return True to indicate successful setup
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the config data from hass.data
    hass.data[DOMAIN].pop(entry.entry_id)

    # Return True to indicate successful unload
    return True
