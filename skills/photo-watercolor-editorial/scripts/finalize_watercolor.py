#!/usr/bin/env python3
"""Composite and audit a deterministic title on an immutable watercolor base."""

from pathlib import Path

from typography_engine import run_cli


if __name__ == "__main__":
    raise SystemExit(run_cli(Path(__file__).resolve().parent.parent))
