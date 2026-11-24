"""The Pixelblaze integration."""

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONFIG

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
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
        discovery.load_platform(hass, 'light', DOMAIN, {}, config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Pixelblaze from a config entry."""
    # TODO Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = entry.data
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
