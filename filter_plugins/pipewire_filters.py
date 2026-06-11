# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

"""
    Jinja2 filters used by the ``ansible-pipewire`` role.
"""

from __future__ import annotations

from ansible.utils.display import Display

display = Display()


class FilterModule:
    """
        Jinja2 filters for the ansible-pipewire role.
    """

    def filters(self) -> dict[str, object]:
        """
            Return the mapping of filter names to their implementation.
        """
        return {
            "pipewire_packages": self.pipewire_packages,
            "pipewire_socket_units": self.pipewire_socket_units,
            "pipewire_normalize_users": self.pipewire_normalize_users,
        }

    def pipewire_packages(
            self,
            defaults: list[str],
            pulse_packages: list[str] | None = None,
            alsa_packages: list[str] | None = None,
            jack_packages: list[str] | None = None,
            bluetooth_packages: list[str] | None = None,
            extra_packages: list[str] | None = None,
            enable_pulse: bool = True,
            enable_alsa: bool = True,
            enable_jack: bool = False,
            enable_bluetooth: bool = True) -> list[str]:
        """
            Build the effective, deduplicated and sorted package list.

            ``defaults`` is always included; each optional component is added
            only when its matching ``enable_*`` flag is true. ``extra_packages``
            (user supplied) is always appended.
        """
        # display.v("pipewire_packages()")

        packages: list[str] = list(defaults or [])

        if enable_pulse:
            packages += pulse_packages or []
        if enable_alsa:
            packages += alsa_packages or []
        if enable_jack:
            packages += jack_packages or []
        if enable_bluetooth:
            packages += bluetooth_packages or []

        packages += extra_packages or []

        # flatten one level, then dedupe and sort
        flattened: list[str] = []
        for entry in packages:
            if isinstance(entry, (list, tuple)):
                flattened.extend(entry)
            else:
                flattened.append(entry)

        result = sorted(set(flattened))

        # display.v(f"  - packages: {result}")

        return result

    def pipewire_socket_units(
            self,
            units: list[str],
            enable_pulse: bool = True) -> list[str]:
        """
            Return the user socket units to manage.

            When pulse support is disabled the ``pipewire-pulse.socket`` unit is
            removed from the list.
        """
        # display.v("pipewire_socket_units()")

        units = list(units or [])

        if not enable_pulse:
            units = [unit for unit in units if unit != "pipewire-pulse.socket"]

        # display.v(f"  - units: {units}")

        return units

    def pipewire_normalize_users(
            self,
            users: list[str | dict[str, object]]) -> list[dict[str, object]]:
        """
            Normalize ``pipewire_users`` into a list of dictionaries.

            Plain string entries become ``{'name': <value>}``; dictionary
            entries are passed through unchanged.
        """
        # display.v("pipewire_normalize_users()")

        normalized: list[dict[str, object]] = []

        for item in users or []:
            if isinstance(item, str):
                normalized.append({"name": item})
            else:
                normalized.append(item)

        # display.v(f"  - users: {normalized}")

        return normalized
