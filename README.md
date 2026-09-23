# HA Wind Sensor

**English** · [Čeština](README.cs.md)

A public beta of a DIY wind sensor for **Seeed Studio XIAO ESP32-S3 + LaskaKit WH-SP-WS01**.
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

## Quick start: public beta

1. Open the **[public web installer](https://mathyass.github.io/ha-wind-sensor/)** in Chrome or Edge.
2. Connect the XIAO with a USB-C **data** cable, close other serial monitors and click **Connect and install**. Select its USB port. For the first clean test, select the erase option: this replaces the old firmware and removes saved Wi-Fi credentials.
3. After flashing, **Improv Serial** offers Wi-Fi setup. Enter your 2.4 GHz network credentials. If the port disappears during restart, unplug/reconnect USB and connect again; you do not need to flash again.
4. In Home Assistant, open **Settings → Devices & services** and add the discovered ESPHome device. If discovery fails, add the ESPHome integration manually using the device IP address and port `6053`. Find the IP in your router if needed. The measurement is **Wind Speed**; its entity ID may resemble `sensor.ha_wind_sensor_a1b2c3_wind_speed`, but HA determines the exact ID.
5. Spin the anemometer and check that the reading returns to zero after it stops. Continue with the checklist.
6. For offline testing, download `ha-wind-sensor-<version>-installer.zip` from [Releases](https://github.com/Mathyass/ha-wind-sensor/releases), extract it and run:

   ```sh
   python3 serve.py
   ```

   On Windows, use `py serve.py` if needed. This opens `http://localhost:8000`. Stop it with Ctrl+C.

Do not open the installer directly as `file://` or serve it over a plain LAN HTTP address. Web Serial requires a secure context: `localhost` is a local exception; public deployment requires HTTPS.

## Fallback Wi-Fi and USB recovery

When Wi-Fi cannot connect, an open fallback access point starts after about one minute. ESPHome derives its name from the device (HA Wind Sensor and a MAC suffix). Join it, prevent your phone from automatically switching networks if necessary, and open **http://192.168.4.1**. Enter the correct SSID/password. Credentials provisioned through Improv or the captive portal are saved on the device and survive power cycles.

If flashing fails, hold **BOOT**, briefly press **RESET**, release BOOT and select the serial port again. You may need to press RESET after flashing. Also check the USB data cable and external antenna.

## Measurement and limits

`pulse_meter` measures the interval between pulses and reports pulses per minute. The specified calibration is **1 Hz = 2.4 km/h**, so `60 × 0.04 = 2.4 km/h`. The configuration uses GPIO4, an internal pull-up, `internal_filter: 5ms`, `EDGE` filtering, `timeout: 5s` and one decimal place. There is no averaging or additional measurement sensor.

Five seconds without a pulse means zero. Intervals longer than 5 seconds (below approximately 0.48 km/h under this calibration) cannot produce a continuous low-speed reading with this timeout. Zero cannot distinguish still air from a disconnected wire. Real wind accuracy needs to be checked for the sensor and mounting location; balconies can significantly distort airflow.

## Updates and ESPHome Device Builder

Published firmware checks the HTTPS manifest on GitHub Pages every six hours. When a newer published version is available, Home Assistant exposes **Firmware Update** in the device’s configuration section. Read the linked release notes, then install it from HA. The manifest includes the OTA image MD5 and ESPHome validates HTTPS certificates.

ESPHome’s native OTA also listens on port **3232**. Use **`firmware/ha-wind-sensor.ota.bin`** for manual updates, never the factory image. Both update paths preserve saved Wi-Fi and the MAC-based device identity.

In a local clone, prepare the environment described below. Then upload the `.ota.bin` from the extracted release ZIP, replacing both the IP and path with your own:

```sh
esphome upload esphome/wind-sensor.yaml --device 192.168.1.123 --file /path/to/firmware/ha-wind-sensor.ota.bin
```

To build and upload a new version from source, use `esphome -s firmware_version "$(cat VERSION)" run esphome/wind-sensor.yaml --device 192.168.1.123`.

ESPHome Device Builder can discover the device and offer **Take control**. The imported local YAML references this repository as a remote package, so the owner can customize substitutions and install future builds wirelessly. The source repository must remain public for package refreshes.

## Local development and layout

```text
esphome/wind-sensor.yaml           generic firmware entry point
esphome/packages/wind-sensor.yaml  reusable device configuration
installer/                        English/Czech web UI and manifest template
scripts/build.py                  validation, compilation and packaging
scripts/package.py                factory + OTA + manifest + checksums
.github/workflows/build.yml        builds, releases and public Pages deployment
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

On Windows, activate `.venv\Scripts\activate`. ESP-IDF downloads the required toolchain on the first build. CI uses Ubuntu 24.04. `scripts/build.py` passes `VERSION` into ESPHome; the YAML default must match `VERSION` for Device Builder imports.

`dist/installer/` contains the ready-to-use website, **ESPHome’s merged factory image at offset 0**, an OTA image, build metadata and SHA-256 checksums. The same content is packaged in `dist/ha-wind-sensor-<version>-installer.zip`. Binaries, secrets and local configurations are not committed. The source `installer/manifest.json` is a template; the source installer folder has no firmware yet. The page detects a missing binary and does not offer installation.

## Builds and releases

Pushes to `main`, pull requests and manual **Run workflow** runs validate, compile and upload an artifact, retained for 30 days. A tag named **`v<contents of VERSION>`** also creates a GitHub **prerelease** with the installer ZIP attached. A mismatched tag fails validation.

```sh
# After updating VERSION, committing and verifying the build:
git tag v0.1.0-beta.4
git push origin v0.1.0-beta.4
```

While the repository is private, everything remains accessible only to collaborators and the Pages deployment is skipped. Once the repository is public and Pages is configured for GitHub Actions, each version tag publishes its release first, then deploys the English/Czech installer, manifest and firmware to the stable HTTPS address. A beta tag can therefore drive end-to-end testing of the public installer; the next stable tag replaces it for general use. The workflow never changes repository visibility. Loading ESP Web Tools from its CDN requires internet access.

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

HA discovery through mDNS works independently of source adoption. `dashboard_import` is embedded in the beta firmware, so Device Builder can fetch the public package after **Take control**.

## References and next phase

- [ESPHome pulse_meter](https://esphome.io/components/sensor/pulse_meter/)
- [ESPHome Improv Serial](https://esphome.io/components/improv_serial/) and [USB logger](https://esphome.io/components/logger/)
- [ESP Web Tools: manifest and installer](https://esphome.github.io/esp-web-tools/)
- [ESPHome OTA](https://esphome.io/components/ota/esphome/)
- [ESPHome managed HTTP updates](https://esphome.io/components/update/http_request/)
- [Seeed XIAO ESP32-S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

The public installer pipeline and managed update manifest are active. Licensing, the 3D model, photos and the MakerWorld page follow after home testing. No open-source license has been granted yet.
