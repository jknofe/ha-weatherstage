"""Config flow for weatherstage.com integration."""

from __future__ import annotations

import logging
from typing import Any

import httpx
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    FlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_HUMI_SENS,
    CONF_PRES_SENS,
    CONF_STATUS_REPORT,
    CONF_TEMP_SENS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
        vol.Required(CONF_NAME): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Validate the data can be used to set up a connection.
    if not (data[CONF_URL].startswith("https://")):
        raise UnsupportedProtocol

    import homeassistant.util.ssl as hass_ssl

    ssl_context = hass_ssl.client_context()

    async with httpx.AsyncClient(verify=ssl_context) as client:
        response = await client.get(data[CONF_URL])
        if response.status_code != 204:
            raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": data[CONF_NAME]}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for weatherstage.com."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "HTTP-connection to Endpoint failed!"
            except UnsupportedProtocol:
                errors["base"] = "URL is malformed and should start with https://"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the reconfiguration step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "HTTP-connection to Endpoint failed!"
            except UnsupportedProtocol:
                errors["base"] = "URL is malformed and should start with https://"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                entry = await self.async_set_unique_id(self.unique_id)
                self.hass.config_entries.async_update_entry(entry, data=user_input)
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="reconfigure", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    """Handle an options flow for weatherstage.com."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    # async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
    #     """Manage the options."""
    #     return await self.async_step_user()
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            # Define the schema for the options form
            data_schema=vol.Schema(
                {
                    # report status of last transmission
                    vol.Optional(
                        CONF_STATUS_REPORT,
                        default=self.config_entry.options.get(
                            CONF_STATUS_REPORT, False
                        ),
                    ): bool,
                    # sensor names
                    vol.Required(
                        CONF_TEMP_SENS,
                        default=self.config_entry.options.get(CONF_TEMP_SENS),
                    ): str,
                    vol.Required(
                        CONF_HUMI_SENS,
                        default=self.config_entry.options.get(CONF_HUMI_SENS),
                    ): str,
                    vol.Required(
                        CONF_PRES_SENS,
                        default=self.config_entry.options.get(CONF_PRES_SENS),
                    ): str,
                }
            ),
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the options form."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=OPTIONS_SCHEMA,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class UnsupportedProtocol(HomeAssistantError):
    """URL is malformed."""
