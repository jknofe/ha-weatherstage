"""__init__.py for weatherstage.com integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_HUMI_SENS, CONF_PRES_SENS, CONF_TEMP_SENS, DOMAIN
from .weatherstage import WeatherstagePublisher as wsp

_LOGGER = logging.getLogger(__name__)

async def update_listener(hass, entry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)

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

    # Register the state change listener for the sensor entity
    WeatherstagePublisher = wsp(config_data[CONF_URL], config_options)
    if CONF_TEMP_SENS in config_options.keys():
        async_track_state_change_event(
            hass, config_options[CONF_TEMP_SENS], WeatherstagePublisher.set_temp
        )
    if CONF_HUMI_SENS in config_options.keys():
        async_track_state_change_event(
            hass, config_options[CONF_HUMI_SENS], WeatherstagePublisher.set_humi
        )
    if CONF_PRES_SENS in config_options.keys():
        async_track_state_change_event(
            hass, config_options[CONF_PRES_SENS], WeatherstagePublisher.set_pres_abs
        )

    entry.async_on_unload(entry.add_update_listener(update_listener))
    # Return True to indicate successful setup
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the config data from hass.data
    hass.data[DOMAIN].pop(entry.entry_id)

    # Return True to indicate successful unload
    return True
