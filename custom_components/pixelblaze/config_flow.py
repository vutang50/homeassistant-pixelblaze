"""Config flow for Pixelblaze integration."""
# pylint: disable=logging-fstring-interpolation
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from homeassistant.const import CONF_HOST, CONF_NAME

from pixelblaze import Pixelblaze

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({CONF_HOST: str})


def pixelblaze_connect(host: str):
    """Try connecting to the local pixelblaze device"""
    # pylint: disable=invalid-name
    try:
        pb = Pixelblaze(host)
        dev_name = pb.getHardwareConfig()["name"]
        if dev_name is None:
            dev_name = host
        pb.close()
        return dev_name
    except Exception as e:  # pylint:disable=broad-except
        _LOGGER.error(f"Unable to connect to {host}: Exception: {e}")
        return None


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    dev_name = await hass.async_add_executor_job(pixelblaze_connect, data[CONF_HOST])
    if dev_name is None:
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {CONF_NAME: dev_name, CONF_HOST: data[CONF_HOST]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pixelblaze."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(info[CONF_NAME])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=info[CONF_NAME], data=info)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
