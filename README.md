
# Ansible Role:  `pipewire`

Ansible role to install and configure pipewire on various linux systems.

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-pipewire/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-pipewire)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-pipewire)][releases]

[ci]: https://github.com/bodsch/ansible-pipewire/actions
[issues]: https://github.com/bodsch/ansible-pipewire/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-pipewire/releases

## Requirements & Dependencies


### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 12 / 13
    - Ubuntu 22.04 / 24.04

The role installs PipeWire together with the [WirePlumber](https://pipewire.pages.freedesktop.org/wireplumber/)
session manager and configures it via **drop-in files** (`*.conf.d/`), so it never
overwrites the distribution defaults.

PipeWire is designed to run as a **per-user** service. This role therefore manages
the `systemd --user` units (`pipewire.socket`, `pipewire-pulse.socket`,
`wireplumber.service`) for the configured users and enables `loginctl enable-linger`
so they start without an interactive login. A system-wide PipeWire daemon is
intentionally *not* configured, as it is discouraged upstream (per-session device
ownership / logind ACLs).

## Configuration

### Components

```yaml
pipewire_enable_pulse: true       # pipewire-pulse (PulseAudio replacement)
pipewire_enable_alsa: true        # pipewire-alsa (ALSA compatibility)
pipewire_enable_jack: false       # pipewire-jack (JACK compatibility)
pipewire_enable_bluetooth: true   # bluetooth audio support

# on debian / ubuntu mask the legacy pulseaudio user units to avoid socket conflicts
pipewire_mask_pulseaudio: true
```

### Global (system wide) configuration

Written to `/etc/pipewire/*.conf.d/` and merged into the daemon defaults.

```yaml
pipewire_global_config:
  clock_rate: 48000
  clock_allowed_rates:
    - 44100
    - 48000
    - 96000
  quantum: 1024
  min_quantum: 32
  max_quantum: 2048

# free-form extra properties (key -> value)
pipewire_context_properties: {}   # -> pipewire.conf.d/10-pipewire.conf
pipewire_pulse_properties: {}     # -> pipewire-pulse.conf.d/10-pulse.conf
pipewire_client_properties: {}    # -> client.conf.d/10-client.conf
```

### WirePlumber

The session manager config format differs by version and is detected automatically:

* **WirePlumber >= 0.5** (Arch, Debian 13, Ubuntu 24.04) uses SPA-JSON:

  ```yaml
  pipewire_wireplumber_settings:
    device.routes.default-sink-volume: 0.6
  ```

* **WirePlumber 0.4** (Debian 12, Ubuntu 22.04) uses Lua:

  ```yaml
  pipewire_wireplumber_lua:
    - 'alsa_monitor.properties["alsa.jack-device"] = false'
  ```

### Per-user configuration

```yaml
pipewire_manage_user_services: true

pipewire_users:
  - alice                       # use the global configuration
  - name: bob
    enable_services: true
    config:
      global:                   # overrides pipewire_global_config for this user
        clock_rate: 44100
      pulse_properties:
        pulse.min.req: "256/48000"
```

---
    
## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-pipewire/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
