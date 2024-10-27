# __init__.py

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up weatherstage.com from a config entry."""
    # Retrieve the configuration data
    config_data = entry.data

    # Use the configuration data as needed
    _LOGGER.info("Setting up weatherstage.com with config: %s", config_data)

    # Example: Store the config data in hass.data for later use
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = config_data

    # Return True to indicate successful setup
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove the config data from hass.data
    hass.data[DOMAIN].pop(entry.entry_id)

    # Return True to indicate successful unload
    return True
