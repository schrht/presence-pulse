"""Configuration values for PresencePulse."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PresencePulseConfig:
    """Runtime configuration for periodic activity generation."""

    min_interval_seconds: float = 60.0
    max_interval_seconds: float = 90.0
    logging_enabled: bool = True
    fail_safe_enabled: bool = True
    mouse_enabled: bool = False
    keyboard_enabled: bool = False
    keyboard_keys: Tuple[str, ...] = ("shift",)


DEFAULT_CONFIG = PresencePulseConfig()
