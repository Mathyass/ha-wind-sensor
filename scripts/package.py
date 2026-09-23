"""Package a compiled build; never substitute an OTA image for the factory image."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def package():
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
        raise ValueError("VERSION must be a semantic version")
    entry_yaml = (ROOT / "esphome/wind-sensor.yaml").read_text()
    if f"firmware_version: {version}\n" not in entry_yaml:
        raise RuntimeError("The YAML default firmware_version must match VERSION")
    build = ROOT / "esphome/.esphome/build/ha-wind-sensor"
    binaries = {}
    for kind in ("factory", "ota"):
        matches = list(build.rglob(f"firmware.{kind}.bin"))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one {kind} image under {build}, found {matches}")
        data = matches[0].read_bytes()
        if len(data) < 1024 or data[0] != 0xE9:
            raise RuntimeError(f"Invalid ESP32 image: {matches[0]}")
        binaries[kind] = matches[0]
    # esphome writes this metadata after a successful compile.
    metadata = json.loads((ROOT / "esphome/.esphome/storage/wind-sensor.yaml.json").read_text())
    if metadata.get("esphome_version") != "2026.9.0":
        raise RuntimeError("Rebuild with requirements.txt before packaging")
    # Project version appears in generated C++, so a stale build is caught early.
    source = (build / "src/esphome/core/defines.h").read_text()
    if f'#define ESPHOME_PROJECT_VERSION "{version}"' not in source or '#define ESPHOME_PROJECT_NAME "mathyass.ha-wind-sensor"' not in source:
        raise RuntimeError("Build version does not match VERSION; run scripts/build.py")
    dist = ROOT / "dist"
    site = dist / "installer"
    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)
    for filename in ("index.html", "index.cs.html", "installer.js", "serve.py", "manifest.json"):
        shutil.copy2(ROOT / "installer" / filename, site / filename)
    (site / "firmware").mkdir()
    for kind, source_path in binaries.items():
        shutil.copy2(source_path, site / "firmware" / f"ha-wind-sensor.{kind}.bin")
    manifest = json.loads((site / "manifest.json").read_text())
    manifest["version"] = version
    manifest["builds"][0]["ota"]["md5"] = hashlib.md5(
        (site / "firmware/ha-wind-sensor.ota.bin").read_bytes(), usedforsecurity=False
    ).hexdigest()
    manifest["builds"][0]["ota"]["release_url"] = (
        f"https://github.com/Mathyass/ha-wind-sensor/releases/tag/v{version}"
    )
    manifest["builds"][0]["ota"]["summary"] = (
        f"HA Wind Sensor {version} — see the release notes before updating."
    )
    (site / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    shutil.copy2(ROOT / "README.md", site / "README.md")
    shutil.copy2(ROOT / "README.cs.md", site / "README.cs.md")
    shutil.copytree(ROOT / "docs", site / "docs")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    (site / "build-info.json").write_text(json.dumps({
        "version": version, "esphome": metadata["esphome_version"],
        "commit": commit, "board": "seeed_xiao_esp32s3", "chip": "ESP32-S3",
        "flash_size": "8MB", "factory_offset": 0,
    }, indent=2) + "\n")
    checksums = []
    for path in sorted(site.rglob("*")):
        if path.is_file():
            checksums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(site).as_posix()}")
    (site / "SHA256SUMS").write_text("\n".join(checksums) + "\n")
    archive = dist / f"ha-wind-sensor-{version}-installer.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(site.rglob("*")):
            if path.is_file():
                output.write(path, path.relative_to(site))
    print(f"Packaged {archive}")

if __name__ == "__main__":
    package()
