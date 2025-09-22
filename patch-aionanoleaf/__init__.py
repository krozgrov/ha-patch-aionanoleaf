"""
Custom integration: patch_aionanoleaf

Bracket IPv6 literal hosts (and percent-encode any zone ID) used by
aionanoleaf.Nanoleaf without disturbing argument order. We accomplish this by:

1) Inspecting the original __init__ signature;
2) Binding the original (args, kwargs) to that signature to get a dict;
3) Replacing only the 'host' value with a bracketed/encoded version;
4) Calling the original __init__ **with kwargs only** (no positional args).

"""

from __future__ import annotations

import ipaddress
import inspect
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)
_LOGGER.warning("patch_aionanoleaf: module imported")


def _format_host_for_url(host: str | None) -> str | None:
    """Bracket IPv6 literal and percent-encode zone ID if present."""
    if not host:
        return host
    raw = host.strip().strip("[]")
    try:
        ip = ipaddress.ip_address(raw.split("%", 1)[0])
        if ip.version == 6:
            if "%" in raw:
                base, zone = raw.split("%", 1)
                raw = f"{base}%25{zone}"
            return f"[{raw}]"
    except ValueError:
        # Not an IP literal; leave hostnames/IPv4 unchanged
        pass
    return host


def _patch_aionanoleaf() -> None:
    try:
        import aionanoleaf.nanoleaf as nl  # type: ignore[attr-defined]

        if getattr(nl.Nanoleaf.__init__, "_ipv6_patched", False) is True:
            _LOGGER.debug("patch_aionanoleaf: already patched")
            return

        _orig_init = nl.Nanoleaf.__init__
        _sig = inspect.signature(_orig_init)

        def _patched_init(self, *args: Any, **kwargs: Any) -> None:
            # Bind args/kwargs to the original signature to get a canonical mapping
            try:
                bound = _sig.bind(self, *args, **kwargs)  # includes 'self'
            except TypeError:
                # As a fallback, try binding without 'self' then re-insert
                bound = _sig.bind_partial(self, *args, **kwargs)
            bound.apply_defaults()

            # Extract existing host; replace with bracketed IPv6 if applicable
            if "host" in _sig.parameters:
                host_val = bound.arguments.get("host")
                safe_host = _format_host_for_url(host_val)
                if safe_host is not None:
                    bound.arguments["host"] = safe_host

            # Call the original __init__ using **kwargs ONLY to avoid positional shifts
            # Remove 'self' from arguments when calling
            call_kwargs = {k: v for k, v in bound.arguments.items() if k != "self"}
            _orig_init(self, **call_kwargs)

            # DO NOT touch self._api_url; in some versions it's a read-only @property.

        # Apply patch and mark it
        nl.Nanoleaf.__init__ = _patched_init  # type: ignore[method-assign]
        nl.Nanoleaf.__init__._ipv6_patched = True  # type: ignore[attr-defined]
        _LOGGER.warning("patch_aionanoleaf: Applied aionanoleaf IPv6 URL bracket patch")

    except Exception:
        _LOGGER.exception("patch_aionanoleaf: failed to apply patch")


# Home Assistant entrypoints
async def async_setup(hass, config) -> bool:
    _LOGGER.warning("patch_aionanoleaf: async_setup running")
    _patch_aionanoleaf()
    return True


async def async_setup_entry(hass, entry) -> bool:
    _LOGGER.warning("patch_aionanoleaf: async_setup_entry running")
    _patch_aionanoleaf()
    return True
