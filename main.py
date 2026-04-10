"""Command-line entry point for PresencePulse."""

from __future__ import annotations

import argparse

from presence_pulse.config import DEFAULT_CONFIG, PresencePulseConfig


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate minimal periodic user activity.",
    )
    parser.add_argument(
        "--min-interval",
        type=float,
        default=DEFAULT_CONFIG.min_interval_seconds,
        help="Minimum seconds between activity events.",
    )
    parser.add_argument(
        "--max-interval",
        type=float,
        default=DEFAULT_CONFIG.max_interval_seconds,
        help="Maximum seconds between activity events.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable timestamped activity logs.",
    )
    parser.add_argument(
        "--unsafe",
        action="store_true",
        help="Disable safe mode. Required before keyboard activity can be enabled.",
    )
    parser.add_argument(
        "--enable-keyboard",
        action="store_true",
        help="Also simulate a configured keyboard series.",
    )
    parser.add_argument(
        "--keys",
        default="",
        help=(
            "Comma-separated key series for keyboard simulation, "
            "such as 'shift', 'shift,shift', or 'cmd+tab'."
        ),
    )
    args = parser.parse_args()

    if args.enable_keyboard and not args.unsafe:
        parser.error("--enable-keyboard requires --unsafe because safe mode is mouse-only")
    if args.enable_keyboard and not parse_key_series(args.keys):
        parser.error("--enable-keyboard requires --keys with at least one key")

    return args


def parse_key_series(raw_keys: str) -> tuple[str, ...]:
    """Parse a comma-separated key series."""
    return tuple(key.strip() for key in raw_keys.split(",") if key.strip())


def config_from_args(args: argparse.Namespace) -> PresencePulseConfig:
    """Build PresencePulse configuration from parsed arguments."""
    return PresencePulseConfig(
        min_interval_seconds=args.min_interval,
        max_interval_seconds=args.max_interval,
        logging_enabled=not args.quiet,
        safe_mode=not args.unsafe,
        keyboard_enabled=args.enable_keyboard,
        keyboard_keys=parse_key_series(args.keys),
    )


def main() -> None:
    """Start PresencePulse with command-line configuration."""
    args = parse_args()

    from presence_pulse.activity import run_presence_pulse

    run_presence_pulse(config_from_args(args))


if __name__ == "__main__":
    main()
