"""Core activity loop for PresencePulse."""

from __future__ import annotations

import platform
import random
import time
from datetime import datetime
from typing import Any, Sequence

from presence_pulse.config import PresencePulseConfig


SUPPORTED_PLATFORMS = {"Darwin", "Windows", "Linux"}
KEY_ALIASES = {
    "cmd": "command",
    "command": "command",
    "ctrl": "ctrl",
    "control": "ctrl",
    "alt": "alt",
    "option": "option",
}


def get_pyautogui() -> Any:
    """Import pyautogui only when activity needs to be generated."""
    import pyautogui

    return pyautogui


def log(message: str, enabled: bool = True) -> None:
    """Print a timestamped log message when logging is enabled."""
    if not enabled:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def validate_config(config: PresencePulseConfig) -> None:
    """Validate interval settings before starting the activity loop."""
    if config.min_interval_seconds <= 0:
        raise ValueError("min_interval_seconds must be greater than 0")
    if config.max_interval_seconds <= 0:
        raise ValueError("max_interval_seconds must be greater than 0")
    if config.min_interval_seconds > config.max_interval_seconds:
        raise ValueError("min_interval_seconds cannot exceed max_interval_seconds")
    if config.safe_mode and config.keyboard_enabled:
        raise ValueError("keyboard activity cannot be enabled in safe mode")
    if config.keyboard_enabled and not config.keyboard_keys:
        raise ValueError("keyboard_keys must contain at least one key")


def warn_if_unsupported_platform(logging_enabled: bool = True) -> None:
    """Warn when running on a platform outside the expected desktop targets."""
    current_platform = platform.system()
    if current_platform not in SUPPORTED_PLATFORMS:
        log(
            f"warning: platform '{current_platform}' is not explicitly supported",
            logging_enabled,
        )


def trigger_mouse_activity() -> None:
    """Generate minimal reversible mouse movement."""
    pyautogui = get_pyautogui()
    pyautogui.moveRel(-1, 0, duration=0)
    pyautogui.moveRel(1, 0, duration=0)


def trigger_keyboard_activity(keys: Sequence[str]) -> None:
    """Press a configured series of keys and hotkey chords."""
    pyautogui = get_pyautogui()
    for key_spec in keys:
        key_parts = parse_key_action(key_spec)
        if len(key_parts) == 1:
            pyautogui.press(key_parts[0])
        else:
            pyautogui.hotkey(*key_parts)


def parse_key_action(key_spec: str) -> tuple[str, ...]:
    """Parse a key action such as 'shift' or 'cmd+tab'."""
    return tuple(
        KEY_ALIASES.get(key.lower(), key.lower())
        for key in key_spec.split("+")
        if key.strip()
    )


def trigger_activity(config: PresencePulseConfig) -> None:
    """Generate the configured activity event."""
    trigger_mouse_activity()

    if config.keyboard_enabled:
        trigger_keyboard_activity(config.keyboard_keys)


def random_interval(config: PresencePulseConfig) -> float:
    """Return a random wait interval using the configured bounds."""
    return random.uniform(config.min_interval_seconds, config.max_interval_seconds)


def run_presence_pulse(config: PresencePulseConfig) -> None:
    """Run the activity loop until interrupted."""
    validate_config(config)
    warn_if_unsupported_platform(config.logging_enabled)

    pyautogui = get_pyautogui()
    pyautogui.FAILSAFE = True

    if config.keyboard_enabled:
        log(
            "warning: keyboard activity is enabled and may affect the active app",
            config.logging_enabled,
        )
    elif not config.safe_mode:
        log("warning: safe mode is disabled", config.logging_enabled)

    log(
        "PresencePulse started "
        f"(interval: {config.min_interval_seconds:.0f}-"
        f"{config.max_interval_seconds:.0f}s, safe_mode: {config.safe_mode}, "
        f"keyboard_enabled: {config.keyboard_enabled})",
        config.logging_enabled,
    )

    try:
        while True:
            wait_seconds = random_interval(config)
            time.sleep(wait_seconds)
            trigger_activity(config)
            log("activity triggered", config.logging_enabled)
    except KeyboardInterrupt:
        log("PresencePulse stopped", config.logging_enabled)
