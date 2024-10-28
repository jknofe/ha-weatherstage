"""__init__.py for weatherstage.com integration."""

import logging

from homeassistant.config_entries import ConfigEntry
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
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")

        if new_state is not None:
            new_value = new_state.state
            old_value = old_state.state if old_state else "unknown"
            _LOGGER.info("Sensor value changed from %s to %s", old_value, new_value)
            # Here you can add any logic to handle the new value

    # Register the state change listener for the sensor entity

    _LOGGER.info("Create %s", config_options[CONF_TEMP_SENS])
    async_track_state_change_event(
        hass, config_options[CONF_TEMP_SENS], handle_sensor_change
    )
    # Return True to indicate successful setup
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the config data from hass.data
    hass.data[DOMAIN].pop(entry.entry_id)

    # Return True to indicate successful unload
    return True
