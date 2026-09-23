"""Validate, compile and package using the ESPHome version in requirements.txt."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "VERSION").read_text().strip()
base = [sys.executable, "-m", "esphome", "-s", "firmware_version", version]
for command in ("config", "compile"):
    subprocess.run(base + [command, "esphome/wind-sensor.yaml"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "scripts/package.py"], cwd=ROOT, check=True)
