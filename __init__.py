"""The weatherstage.com integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
# from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

import logging
# Create a logger for your integration
_LOGGER = logging.getLogger(DOMAIN)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
# PLATFORMS: list[Platform] = [Platform.LIGHT]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
type New_NameConfigEntry = ConfigEntry[MyApi]  # noqa: F821

# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Set up weatherstage.com from a config entry."""
    _LOGGER.info("Setting up %s", DOMAIN)

    api_endpoint_url = entry.data.get("api_endpoint_url")
    location_name = entry.data.get("location_name")

    _LOGGER.info("Setting up %s with endpoint %s", location_name, api_endpoint_url)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Unload a config entry."""
    # return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True
