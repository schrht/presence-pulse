# PresencePulse

PresencePulse is a lightweight, generic macOS-friendly utility that generates minimal periodic user activity. It is not tied to any specific application. It is intended for passive workflows such as reading, monitoring logs, or waiting for long-running tasks while keeping the machine from entering an idle state.

PresencePulse can use `pyautogui` to move the mouse by 1 pixel and immediately move it back, send a configured keyboard series, or both. At least one activity type must be enabled explicitly.

## Installation

Install dependencies with `uv`:

```bash
uv sync
```

If you do not already have `uv`, install it from the official documentation:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## How to Run

Run the utility from the project root:

```bash
uv run python main.py --enable-mouse
```

PresencePulse runs indefinitely until interrupted. Stop it with `Ctrl+C`.

You can override the defaults with command-line arguments:

```bash
uv run python main.py --min-interval 30 --max-interval 120
```

Available arguments:

- `--min-interval`: minimum seconds between activity events.
- `--max-interval`: maximum seconds between activity events.
- `--quiet`: disables timestamped logs.
- `--unsafe`: disables safe mode. Required before keyboard activity can be enabled.
- `--disable-fail-safe`: disables PyAutoGUI's screen-corner emergency stop.
- `--enable-mouse`: simulates minimal reversible mouse movement.
- `--enable-keyboard`: also simulates a configured keyboard series.
- `--keys`: comma-separated key series for keyboard simulation, such as `shift`, `shift,shift`, or `cmd+tab`.

Mouse and keyboard simulation are both disabled by default. Enable at least one activity type:

```bash
uv run python main.py --enable-mouse
```

Keyboard simulation is disabled by default. To enable it, you must disable safe mode explicitly:

```bash
uv run python main.py --unsafe --enable-keyboard --keys shift
```

To press multiple keys in sequence:

```bash
uv run python main.py --unsafe --enable-keyboard --keys shift,shift
```

To send a combined hotkey:

```bash
uv run python main.py --unsafe --enable-keyboard --keys cmd+tab
```

To send a hotkey followed by another key:

```bash
uv run python main.py --unsafe --enable-keyboard --keys cmd+tab,shift
```

Show all options:

```bash
uv run python main.py --help
```

Example log output:

```text
[2026-04-10 10:30:21] PresencePulse started (interval: 40-90s, safe_mode: True, fail_safe_enabled: True, mouse_enabled: True, keyboard_enabled: False)
[2026-04-10 10:31:14] activity triggered
[2026-04-10 10:32:30] activity triggered
[2026-04-10 10:32:42] PresencePulse stopped
```

## Configuration

Configuration lives in `presence_pulse/config.py`:

```python
DEFAULT_CONFIG = PresencePulseConfig(
    min_interval_seconds=40.0,
    max_interval_seconds=90.0,
    logging_enabled=True,
    safe_mode=True,
    fail_safe_enabled=True,
    mouse_enabled=False,
    keyboard_enabled=False,
    keyboard_keys=(),
)
```

Available options:

- `min_interval_seconds`: shortest delay between activity events.
- `max_interval_seconds`: longest delay between activity events.
- `logging_enabled`: enables timestamped console logs.
- `safe_mode`: prevents keyboard activity unless disabled explicitly.
- `fail_safe_enabled`: enables PyAutoGUI's screen-corner emergency stop.
- `mouse_enabled`: enables minimal reversible mouse movement.
- `keyboard_enabled`: enables the configured keyboard series when safe mode is disabled.
- `keyboard_keys`: keys or hotkey chords to press in order, such as `("shift",)`, `("shift", "shift")`, or `("cmd+tab",)`.

## macOS Permissions

On macOS, `pyautogui` may require Accessibility permission before it can control the mouse.

To enable it:

1. Open **System Settings**.
2. Go to **Privacy & Security**.
3. Open **Accessibility**.
4. Enable access for the terminal app you use to run PresencePulse, such as Terminal, iTerm2, or your editor.

You may need to restart the terminal after granting permission.

## Safety and Limitations

PresencePulse is designed to be subtle:

- It moves the mouse by only 1 pixel and immediately restores the original position.
- Mouse and keyboard activity are both opt-in.
- Keyboard simulation is opt-in and requires safe mode to be disabled.
- It uses randomized intervals to avoid a rigid activity pattern.
- It enables `pyautogui` fail-safe behavior, so moving the pointer to a screen corner stops PresencePulse cleanly.
- You can disable the fail-safe with `--disable-fail-safe`, but this removes PyAutoGUI's screen-corner emergency stop.

Limitations:

- The utility cannot guarantee that every application, website, or operating system idle detector will treat small mouse movement as activity.
- If the mouse is actively being used at the exact moment an event triggers, the pointer may briefly nudge by 1 pixel.
- If keyboard simulation is enabled, keys are sent to whichever app is active at that moment.
- On macOS, missing Accessibility permissions can prevent activity generation.

## Platform Notes

PresencePulse detects the current platform and prints a warning when it is not running on macOS, Windows, or Linux. The project is primarily intended for desktop environments where `pyautogui` can control the mouse.
