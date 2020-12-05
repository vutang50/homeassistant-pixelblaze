[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

<!-- [![Discord][discord-shield]][discord] -->
[![Community Forum][forum-shield]][forum]

_Component to integrate with [pixelblaze][pixelblaze]._  


**This component will set up the following platforms.**

Platform | Description
-- | --
`light` | Sets LED brightness, enables sequencer, select pattern/effects, and choose color if applicable.

![Custom Light Entity Card][exampleimg]

{% if not installed %}
## Installation

1. Click install.
2. Goto the `Configuration` -> `Integrations` page.  
3. On the bottom right of the page, click on the Orange `+` sign to add an integration.
4. Search for `Pixelblaze`. (If you don't see it, try refreshing your browser page to reload the cache.)
5. Enter the required information. 

Fields name | Type | Required | Default | Description
--- | --- | --- | --- | --- |
Host | Textbox | + | - | Hostname or IP address to access Pixelblaze device

{% endif %}


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

<!---->

***

[pixelblaze]: https://electromage.com/
[buymecoffee]: https://www.buymeacoffee.com/vutang50
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/vutang50/homeassistant-pixelblaze.svg?style=for-the-badge
[commits]: https://github.com/vutang50/homeassistant-pixelblaze/commits
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: https://github.com/vutang50/homeassistant-pixelblaze/blob/main/img/fullcard.png?raw=true
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/vutang50/homeassistant-pixelblaze/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/vutang50/homeassistant-pixelblaze.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-vutang50-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/vutang50/homeassistant-pixelblaze.svg?style=for-the-badge
[releases]: https://github.com/vutang50/homeassistant-pixelblaze/releases
[user_profile]: https://github.com/vutang50
