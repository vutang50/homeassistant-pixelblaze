"""The Pixelblaze integration."""
import asyncio

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONFIG

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_HOST,CONF_NAME)

HOST_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [HOST_CONFIG_SCHEMA])}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["light"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Pixelblaze component."""
    hass.data[DOMAIN] = {}
    if DOMAIN in config:
        hass.data[DOMAIN][CONFIG] = config[DOMAIN]
        hass.helpers.discovery.load_platform('light', DOMAIN, {}, config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Pixelblaze from a config entry."""
    # TODO Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = entry.data
    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
