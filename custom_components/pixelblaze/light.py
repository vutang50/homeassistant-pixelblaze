from .const import (
    DOMAIN,
    CONFIG,
    PB_ATTR_HSV,
    PB_ATTR_RGB,
    EFFECT_SEQUENCER
)

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

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    STATE_ON
)

from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util.color import color_hs_to_RGB

SUPPORTED_FEATURES_BASE = (SUPPORT_BRIGHTNESS | SUPPORT_EFFECT)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the lights from config"""
    entList = []
    devList = hass.data[DOMAIN][CONFIG]
    for dev in devList:
        entList.append( PixelblazeEntity(
            dev[CONF_HOST],
            dev[CONF_NAME]
            )
        )

    add_entities( entList )

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up lights for device"""
    dev = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities( [ PixelblazeEntity(dev[CONF_HOST], dev[CONF_NAME]) ] )

class PixelblazeEntity(LightEntity, RestoreEntity):
    """Representation of a Pixelblaze entity."""

    def __init__( self, host, unique_id ):
        """Initialize the light."""
        self.id = unique_id
        self.host = host
        self._is_on = False
        self._brightness = None
        self._color = None
        self.colorPickerKey = None
        self._supported = None
        self._effect = None

        ## TODO: ASYNC??
        pb = Pixelblaze(host)
        self.activePID = pb.getActivePattern()
        ## Get the pattern list and set the patterns names as the effect list
        self.patternlist = pb.getPatternList()
        l = list(self.patternlist.values())
        l.sort(key=str.lower)
        l.insert(0,EFFECT_SEQUENCER)
        self._effect_list = l
        self.updateActivePattern(pb, self.activePID)
        pb.close()

    async def async_added_to_hass(self):
        """Handle entity about to be added to hass event."""
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()
        if last_state:
            self._is_on = last_state.state == STATE_ON
            self._brightness = last_state.attributes.get(ATTR_BRIGHTNESS)
            self._color = last_state.attributes.get(ATTR_HS_COLOR)
            self._effect = last_state.attributes.get(ATTR_EFFECT)

    def updateActivePattern(self, pixelblaze : Pixelblaze, activePID):
        """Updates the current pattern and sets the correct supported features for this effect"""
        self.activePID = activePID
        if self.activePID is not None and len(self.activePID)>0:
            self._effect = self.patternlist[activePID]
        if pixelblaze.getColorControlName() is None:
            self._supported = ( SUPPORTED_FEATURES_BASE )
        else:
            self._supported = ( SUPPORTED_FEATURES_BASE | SUPPORT_COLOR )

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.id

    @property
    def should_poll(self):
        """No polling needed at this time"""
        return False

    @property
    def assumed_state(self):
        """Return True because unable to access real state of the entity."""
        return True

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._is_on

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
        pb = Pixelblaze(self.host)
        pb.setBrightness(0)
        pb.close()
        self._is_on = False
        self.schedule_update_ha_state()

    def turn_on(self, **kwargs):
        """Turn on (or adjust property of) the lights."""
        pb = Pixelblaze(self.host)
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            pb.setBrightness(self._brightness/255)

        if ATTR_EFFECT in kwargs:
            self._effect = kwargs[ATTR_EFFECT]
            if EFFECT_SEQUENCER == self._effect:
                self._supported = ( SUPPORTED_FEATURES_BASE )
                pb.startSequencer()
            else:
                # Stop any sequencer and find the matching patternID to the name
                pb.stopSequencer()
                for pid, pname in self.patternlist.items():
                    if self._effect == pname:
                        pb.setActivePattern(pid)
                        self.updateActivePattern(pb,pid)
                        break

        if ATTR_HS_COLOR in kwargs:
            # Only set the color if controls allow for it
            colorPickerKey = pb.getColorControlName()
            if colorPickerKey is not None:
                self._color = kwargs[ATTR_HS_COLOR]
                if colorPickerKey.startswith(PB_ATTR_HSV):
                    hsv = (self._color[0] /360 , self._color[1] /100, 1)
                    pb.setColorControl(colorPickerKey, hsv)
                elif colorPickerKey.startswith(PB_ATTR_RGB):
                    rgb = color_hs_to_RGB(*tuple(self._color))
                    pb.setColorControl(colorPickerKey, (rgb[0]/255,rgb[1]/255,rgb[2]/255))
        pb.close()

        self._is_on = True
        self.schedule_update_ha_state()