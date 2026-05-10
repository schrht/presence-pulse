"""Command-line entry point for PresencePulse."""

from __future__ import annotations

import argparse

from presence_pulse.config import DEFAULT_CONFIG, PresencePulseConfig


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate minimal periodic user activity.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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
        "--disable-fail-safe",
        action="store_true",
        help="Disable PyAutoGUI's screen-corner emergency stop.",
    )
    parser.add_argument(
        "--enable-mouse",
        action="store_true",
        help="Simulate minimal reversible mouse movement.",
    )
    parser.add_argument(
        "--enable-keyboard",
        action="store_true",
        help="Also simulate a configured keyboard series.",
    )
    parser.add_argument(
        "--keys",
        default=",".join(DEFAULT_CONFIG.keyboard_keys),
        help=(
            "Comma-separated key series for keyboard simulation, "
            "such as 'shift', 'shift,shift', or 'cmd+tab'."
        ),
    )
    args = parser.parse_args()

    if args.min_interval <= 0:
        parser.error(f"--min-interval must be greater than 0 (got {args.min_interval:g})")
    if args.max_interval <= 0:
        parser.error(f"--max-interval must be greater than 0 (got {args.max_interval:g})")
    if args.min_interval > args.max_interval:
        parser.error(
            "--min-interval cannot exceed --max-interval "
            f"(got --min-interval {args.min_interval:g}, --max-interval {args.max_interval:g})"
        )
    if args.enable_keyboard and not parse_key_series(args.keys):
        parser.error("--enable-keyboard requires --keys with at least one key")
    if not args.enable_mouse and not args.enable_keyboard:
        parser.error("at least one activity type must be enabled: --enable-mouse or --enable-keyboard")

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
        fail_safe_enabled=not args.disable_fail_safe,
        mouse_enabled=args.enable_mouse,
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
