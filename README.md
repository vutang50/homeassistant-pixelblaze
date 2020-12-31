# Pixelblaze controller for Home Assistant
This is a custom component integration to allow control of [Pixelblaze](https://electromage.com/) devices in [Home Assistant](https://www.home-assistant.io/).  It incorporates the [pixelblaze-client](https://github.com/zranger1/pixelblaze-client), so many thanks to [zranger1](https://github.com/zranger1) for all the great work there. 

This component appears to home assistant as a light device which you can control the brightness, start the sequencer, set the pattern from the installed pattern list, and if the pattern supports it, a single color picker.  This works well with the [Light Entity Card](https://github.com/ljmerza/light-entity-card)

![Custom Light Entity Lovelace Card](https://github.com/vutang50/homeassistant-pixelblaze/blob/main/img/fullcard.png?raw=true)


## Known Issues
This component will not poll the pixelblaze for current state.  If a pattern is selected outside of the component, it will not be updated in HA.  There is no support to control any custom slider at the moment

## Installing

Manual steps:
1. Download or clone this project, and place the `custom_components` folder and its contents into your Home Assistant config folder.
2. Ensure `light.py` and related files are located in a folder named `pixelblaze` within the `custom_components` folder.


## Configuration
Please be sure to close any web interfaces directly to the Pixelblaze during setup, or while you are controlling it. See [Known Issues](https://github.com/zranger1/pixelblaze-client#known-issues) of the python client.  There are multiple ways this can be configured

### Integrations Page
> This is the preferred method.

1. Goto the `Configuration` -> `Integrations` page.  
2. On the bottom right of the page, click on the Orange `+` sign to add an integration.
3. Search for `Pixelblaze`. (If you don't see it, try refreshing your browser page to reload the cache.)
4. Enter the required information. 

Fields name | Type | Required | Default | Description
--- | --- | --- | --- | --- |
Host | Textbox | + | - | Hostname or IP address to access Pixelblaze device
5. No reboot is required. 

### Configuration.yaml
While this still works, it will be deprecated in the future. Please use [Integrations](#integrations-page).
Once the files are downloaded, you’ll need to **update your config** to include the following under the **`pixelblaze` domain**:

```yaml
pixelblaze:
  - host: my_pixelblaze_hostname.my.domain
    name: kitchen_lamp
  - host: 10.10.10.10
    name: living_room_tv
```

restart and it works

