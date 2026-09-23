# HA Wind Sensor

**English** · [Čeština](README.cs.md)

A private DIY prototype for **Seeed Studio XIAO ESP32-S3 + LaskaKit WH-SP-WS01**.
It provides one measurement entity, **Wind Speed**, in **km/h** in Home Assistant.
There are no blind controls or other automations. The project version is in `VERSION`.

Firmware: ESPHome **2026.9.0**, ESP-IDF. Installer: ESP Web Tools **10.4.0**.
Automated validation and compilation do not replace physical testing; use the [test checklist](docs/test-checklist.md).
The installer opens in English, with a Czech language link at the top. ESP Web Tools’ own dialogs use the library’s supported language behavior.

## What you need

- XIAO ESP32-S3 with its external Wi-Fi antenna attached (8 MB flash).
- WH-SP-WS01 reed-contact anemometer, two wires, a USB-C data cable and USB power.
- A computer with Chrome/Edge, Python 3 and internet access to load the installer library.
- A 2.4 GHz Wi-Fi network and Home Assistant with network access to the sensor.

Disconnect power before wiring:

| WH-SP-WS01 | XIAO ESP32-S3 |
| --- | --- |
| One reed-contact wire | **D3 = GPIO4** |
| Other wire | **GND** |

The contact has no polarity and needs no supply voltage. The firmware enables the internal pull-up.
**D4 is not GPIO4.** The board uses 3.3 V logic. The printed bracket and assembly guide will be added separately.

## Quick start: private home test

1. Sign in to GitHub, open [Releases](https://github.com/Mathyass/ha-wind-sensor/releases) and download `ha-wind-sensor-<version>-installer.zip`. Alternatively, open a successful [Actions](https://github.com/Mathyass/ha-wind-sensor/actions) run and download the `ha-wind-sensor-installer` artifact. Extract the artifact, then extract the installer ZIP inside it.
2. Extract the **entire** installer ZIP. Open a terminal in that folder and run:

   ```sh
   python3 serve.py
   ```

   On Windows, use `py serve.py` if needed. This opens `http://localhost:8000`; open that address manually in Chrome/Edge if necessary. The server is only available on this computer. Stop it with Ctrl+C. If port 8000 is busy, run `python3 -m http.server 8001 --bind 127.0.0.1` in the same folder and open `http://localhost:8001` instead.

3. Connect the XIAO with a USB-C **data** cable, close other serial monitors and click **Connect and install**. Select its USB port. For the first clean test, select the erase option: this replaces the old firmware and removes saved Wi-Fi credentials.
4. After flashing, **Improv Serial** offers Wi-Fi setup. Enter your 2.4 GHz network credentials. If the port disappears during restart, unplug/reconnect USB and connect again; you do not need to flash again.
5. In Home Assistant, open **Settings → Devices & services** and add the discovered ESPHome device. If discovery fails, add the ESPHome integration manually using the device IP address and port `6053`. Find the IP in your router if needed. The measurement is **Wind Speed**; its entity ID may resemble `sensor.ha_wind_sensor_a1b2c3_wind_speed`, but HA determines the exact ID.
6. Spin the anemometer and check that the reading returns to zero after it stops. Continue with the checklist.

Do not open the installer directly as `file://` or serve it over a plain LAN HTTP address. Web Serial requires a secure context: `localhost` is a local exception; public deployment requires HTTPS.

## Fallback Wi-Fi and USB recovery

When Wi-Fi cannot connect, an open fallback access point starts after about one minute. ESPHome derives its name from the device (HA Wind Sensor and a MAC suffix). Join it, prevent your phone from automatically switching networks if necessary, and open **http://192.168.4.1**. Enter the correct SSID/password. Credentials provisioned through Improv or the captive portal are saved on the device and survive power cycles.

If flashing fails, hold **BOOT**, briefly press **RESET**, release BOOT and select the serial port again. You may need to press RESET after flashing. Also check the USB data cable and external antenna.

## Measurement and limits

`pulse_meter` measures the interval between pulses and reports pulses per minute. The specified calibration is **1 Hz = 2.4 km/h**, so `60 × 0.04 = 2.4 km/h`. The configuration uses GPIO4, an internal pull-up, `internal_filter: 5ms`, `EDGE` filtering, `timeout: 5s` and one decimal place. There is no averaging or additional measurement sensor.

Five seconds without a pulse means zero. Intervals longer than 5 seconds (below approximately 0.48 km/h under this calibration) cannot produce a continuous low-speed reading with this timeout. Zero cannot distinguish still air from a disconnected wire. Real wind accuracy needs to be checked for the sensor and mounting location; balconies can significantly distort airflow.

## OTA updates

ESPHome OTA listens on port **3232**. Use **`firmware/ha-wind-sensor.ota.bin`** for updates, never the factory image. OTA preserves saved Wi-Fi and the MAC-based device identity. Updates are manual; this project does not add an update entity to HA.

In a local clone, prepare the environment described below. Then upload the `.ota.bin` from the extracted release ZIP, replacing both the IP and path with your own:

```sh
esphome upload esphome/wind-sensor.yaml --device 192.168.1.123 --file /path/to/firmware/ha-wind-sensor.ota.bin
```

To build and upload a new version from source, use `esphome -s firmware_version "$(cat VERSION)" run esphome/wind-sensor.yaml --device 192.168.1.123`. Private release downloads require GitHub sign-in; the device does not fetch firmware from GitHub itself.

## Local development and layout

```text
esphome/wind-sensor.yaml           generic firmware entry point
esphome/packages/wind-sensor.yaml  reusable device configuration
installer/                        English/Czech web UI and manifest template
scripts/build.py                  validation, compilation and packaging
scripts/package.py                factory + OTA + manifest + checksums
.github/workflows/build.yml        builds on main/PR; releases on v* tags
docs/test-checklist.md             hardware tests and publication checklist
VERSION                           version for firmware and manifest
```

From the repository clone, using Python 3.13:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python dist/installer/serve.py
```

On Windows, activate `.venv\Scripts\activate`. ESP-IDF downloads the required toolchain on the first build. CI uses Ubuntu 24.04. `scripts/build.py` passes `VERSION` into ESPHome; compiling the YAML directly without that substitution labels the firmware `dev`.

`dist/installer/` contains the ready-to-use website, **ESPHome’s merged factory image at offset 0**, an OTA image, build metadata and SHA-256 checksums. The same content is packaged in `dist/ha-wind-sensor-<version>-installer.zip`. Binaries, secrets and local configurations are not committed. The source `installer/manifest.json` is a template; the source installer folder has no firmware yet. The page detects a missing binary and does not offer installation.

## Private builds and releases

Pushes to `main`, pull requests and manual **Run workflow** runs validate, compile and upload an artifact, retained for 30 days. A tag named **`v<contents of VERSION>`** also creates a GitHub **prerelease** with the installer ZIP attached. A mismatched tag fails validation.

```sh
# After updating VERSION, committing and verifying the build:
git tag v0.1.0-beta.1
git push origin v0.1.0-beta.1
```

Everything remains accessible only to people with access to the private repository. The workflow does not enable GitHub Pages, upload firmware to public hosting or change repository visibility. No GitHub token is used in the browser: it loads the manifest and firmware from the extracted package on localhost. Loading ESP Web Tools from its CDN requires internet access.

## Test firmware security

The generic image contains no Wi-Fi credentials, GitHub token or shared API encryption key. In this initial test, **the API is unencrypted, OTA has no password and the fallback AP is open**. Use a trusted network and do not forward device ports to the internet. ESPHome’s captive portal also provides web OTA while the fallback AP is active.

To secure an individual device, create ignored `esphome/wind-sensor.local.yaml`, copy the contents of `wind-sensor.yaml` into it, then add:

```yaml
api:
  encryption:
    key: !secret api_encryption_key
ota:
  - platform: esphome
    id: ota_esphome
    password: !secret ota_password
wifi:
  ap:
    password: !secret fallback_password
```

Store the values in ignored `esphome/secrets.yaml`. The API key is 32 random bytes encoded as base64; generate it with `openssl rand -base64 32`. The AP password must be 8–64 characters. Install the first secured build over USB, then supply the API key to HA and use the matching local YAML for subsequent OTA updates. Returning to the generic image removes these protections. Never include local configurations or secrets in shared builds.

HA discovery through mDNS and adding the API device work without adopting the source configuration. `dashboard_import` is intentionally omitted while the repository is private, because anonymous Device Builder imports would fail. Use the local clone/package for your own changes.

## References and next phase

- [ESPHome pulse_meter](https://esphome.io/components/sensor/pulse_meter/)
- [ESPHome Improv Serial](https://esphome.io/components/improv_serial/) and [USB logger](https://esphome.io/components/logger/)
- [ESP Web Tools: manifest and installer](https://esphome.github.io/esp-web-tools/)
- [ESPHome OTA](https://esphome.io/components/ota/esphome/)
- [Seeed XIAO ESP32-S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

Publication, licensing, public HTTPS hosting, the 3D model, photos and the MakerWorld page follow after home testing. No public open-source license has been granted yet.
