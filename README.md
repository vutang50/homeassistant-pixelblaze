# Pixelblaze controller for Home Assistant
This is a custom component integration to allow control of [Pixelblaze](https://electromage.com/) devices in Home Assistant.  It incorporates the [pixelblaze-client](https://github.com/zranger1/pixelblaze-client), so many thanks to [zranger1](https://github.com/zranger1) for all the great work there. 

This component appears to home assistant as a light device which you can control the brightness, the pattern from the installed pattern list, and if the pattern supports it, a single color picker.  This works well with the [Light Entity Card](https://github.com/ljmerza/light-entity-card)

![Custom Light Entity Lovelace Card](https://raw.githubusercontent.com/vutang50/homeassistant-pixelblaze/master/img/fullcard.png)



## Installing

Manual steps:
1. Download or clone this project, and place the `custom_components` folder and its contents into your Home Assistant config folder.
2. Ensure `light.py`, `pixelblaze.py` and related files are located in a folder named `pixelblaze` within the `custom_components` folder.


## Configuration
To add integration use Configuration -> Integrations -> Add `Pixelblaze`.  Please be sure to close any web interfaces directly to the Pixelblaze during setup, or while you are controlling it.  


Fields name | Type | Required | Default | Description
--- | --- | --- | --- | --- |
Host | Textbox | + | - | Hostname or IP address to access Pixelblaze device


