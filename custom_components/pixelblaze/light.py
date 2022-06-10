"""Light platform for Pixelblaze."""
# pylint: disable=logging-fstring-interpolation
import logging

from pixelblaze import Pixelblaze

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    SUPPORT_EFFECT,
    LightEntity,
)

from homeassistant.const import CONF_HOST, CONF_NAME

from homeassistant.util.color import color_hs_to_RGB

from .const import DOMAIN, CONFIG, PB_ATTR_HSV, PB_ATTR_RGB, EFFECT_SEQUENCER

_LOGGER = logging.getLogger(__name__)

SUPPORTED_FEATURES_BASE = SUPPORT_BRIGHTNESS | SUPPORT_EFFECT
COLOR_MODES_BASE = ()

PB_BRIGHTNESS = "brightness"
PB_ACTIVE_PROG_ID = "activeProgramId"
PB_ACTIVE_PROG = "activeProgram"
PB_SEQUENCER = "runSequencer"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the lights from config"""
    # pylint: disable=unused-argument
    ent_list = []
    dev_list = hass.data[DOMAIN][CONFIG]
    for dev in dev_list:
        ent_list.append(PixelblazeEntity(dev[CONF_HOST], dev[CONF_NAME]))

    add_entities(ent_list)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up lights for device"""
    dev = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([PixelblazeEntity(dev[CONF_HOST], dev[CONF_NAME])])


class PixelblazeEntity(LightEntity):
    """Representation of a Pixelblaze entity."""

    def __init__(self, host, unique_id):
        """Initialize the light."""
        self.id = unique_id  # pylint: disable=invalid-name
        self.host = host
        self._brightness = 0
        self._last_brightness = 64
        self._color = None
        self.color_picker_key = None
        self._supported = SUPPORTED_FEATURES_BASE
        self._effect = None
        self._effect_list = None
        self.init_pattern_list = False
        self.active_pid = None
        self.patternlist = ()

    async def async_device_update(self):
        # pylint: disable=arguments-differ, invalid-name
        _LOGGER.debug(f"Device Update for {self.id}")
        try:
            pb = Pixelblaze(self.host)
            try:
                pb_config = pb.getHardwareConfig()
                if PB_BRIGHTNESS not in pb_config:
                    _LOGGER.warning(f"Empty query hardware config for {self.id}")
                else:
                    _LOGGER.debug(pb_config)
                    if not self.init_pattern_list:
                        ## DO ONCE: Get pattern list and set patterns names as the effect list
                        self.update_pattern_list(pb)

                    self._brightness = pb_config[PB_BRIGHTNESS] * 255

                    if pb_config[PB_SEQUENCER]:
                        self._effect = EFFECT_SEQUENCER
                    else:
                        pid = pb_config[PB_ACTIVE_PROG][PB_ACTIVE_PROG_ID]
                        if pid != self.active_pid:
                            self.update_active_pattern(pb, pid)

            finally:
                pb.close()
        except Exception as e:  # pylint:disable=broad-except,invalid-name
            _LOGGER.error(
                f"Failed to update pixelblaze device {self.id}@{self.host}: Exception: {e}"
            )

    def update_pattern_list(self, pixelblaze: Pixelblaze):
        """Updates the pattern list"""
        _LOGGER.debug(f"Updating pattern list for {self.id}")
        self.patternlist = pixelblaze.getPatternList()
        p_list = list(self.patternlist.values())
        p_list.sort(key=str.lower)
        p_list.insert(0, EFFECT_SEQUENCER)
        self._effect_list = p_list
        self.init_pattern_list = True

    def update_active_pattern(self, pixelblaze: Pixelblaze, active_pid):
        """Updates the current pattern and sets the correct supported features for this effect"""
        _LOGGER.debug(f"Updating running pattern on {self.id}")
        self.active_pid = active_pid
        if self.active_pid is not None and len(self.active_pid) > 0:
            if active_pid not in self.patternlist:
                self.update_pattern_list(pixelblaze)
            self._effect = self.patternlist[active_pid]
        if pixelblaze.getColorControlName() is None:
            self._supported = SUPPORTED_FEATURES_BASE
        else:
            self._supported = SUPPORTED_FEATURES_BASE | SUPPORT_COLOR

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.id

    @property
    def should_poll(self):
        """No polling needed at this time"""
        return True

    @property
    def assumed_state(self):
        """Return True because unable to access real state of the entity."""
        return True

    @property
    def is_on(self):
        """Return true if device is on."""
        return self.brightness > 0

    @property
    def brightness(self):
        """Return the brightness property."""
        return self._brightness

    @property
    def hs_color(self):
        """Return the color property."""
        if self._color is None or self._color[1] == 0:
            return None
        return self._color

    @property
    def supported_features(self):
        """Flag supported features."""
        return self._supported

    @property
    def effect(self):
        """Return the current effect for this light."""
        return self._effect

    @property
    def effect_list(self):
        """Return the list of supported effects for this light."""
        return self._effect_list

    def turn_off(self, **kwargs):
        """Set the brightness to 0"""
        _LOGGER.debug(f"turn off for {self.id}")

        try:
            pb = Pixelblaze(self.host)  # pylint: disable=invalid-name
            try:
                pb.setBrightness(0)
                self._last_brightness = self._brightness
                self.schedule_update_ha_state()
            finally:
                pb.close()
        except Exception as e:  # pylint:disable=broad-except,invalid-name
            _LOGGER.error(
                f"Failed to turn_off pixelblaze device {self.id}@{self.host}: Exception: {e}"
            )

    def turn_on(self, **kwargs):
        """Turn on (or adjust property of) the lights."""
        _LOGGER.debug(f"turn_on for {self.id}")

        try:
            pb = Pixelblaze(self.host)  # pylint: disable=invalid-name
            try:
                if ATTR_BRIGHTNESS in kwargs:
                    self._brightness = kwargs[ATTR_BRIGHTNESS]
                    self._last_brightness = self._brightness
                else:
                    self._brightness = self._last_brightness
                pb.setBrightness(self._brightness / 255)

                if ATTR_EFFECT in kwargs:
                    self._effect = kwargs[ATTR_EFFECT]
                    if EFFECT_SEQUENCER == self._effect:
                        self._supported = SUPPORTED_FEATURES_BASE
                        pb.startSequencer()
                    else:
                        # Stop any sequencer and find the matching patternID to the name
                        pb.stopSequencer()
                        for pid, pname in self.patternlist.items():
                            if self._effect == pname:
                                pb.setActivePattern(pid)
                                self.update_active_pattern(pb, pid)
                                break

                if ATTR_HS_COLOR in kwargs:
                    # Only set the color if controls allow for it
                    color_picker_key = pb.getColorControlName()
                    if color_picker_key is not None:
                        self._color = kwargs[ATTR_HS_COLOR]
                        if color_picker_key.startswith(PB_ATTR_HSV):
                            hsv = (self._color[0] / 360, self._color[1] / 100, 1)
                            pb.setColorControl(color_picker_key, hsv)
                        elif color_picker_key.startswith(PB_ATTR_RGB):
                            rgb = color_hs_to_RGB(*tuple(self._color))
                            pb.setColorControl(
                                color_picker_key,
                                (rgb[0] / 255, rgb[1] / 255, rgb[2] / 255),
                            )
                self.schedule_update_ha_state()
            finally:
                pb.close()
        except Exception as e:  # pylint:disable=broad-except,invalid-name
            _LOGGER.error(
                f"Failed to turn_on pixelblaze device {self.id}@{self.host}: Exception: {e}"
            )
