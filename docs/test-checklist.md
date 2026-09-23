# Home test — 0.1.0-beta.4

**English** · [Čeština](test-checklist.cs.md)

Record the date, version/commit from `build-info.json`, Home Assistant version, browser and outcome.
Automated builds check configuration and compilation. The steps below require physical hardware.

- [ ] External antenna attached; reed wired between **D3 / GPIO4 and GND**; USB cable supports data.
- [ ] Clean install from the ZIP in desktop Chrome/Edge succeeds on the XIAO ESP32-S3, with no reboot loop.
- [ ] The installer opens in English; the Czech link works and English can be selected again. Both use the same firmware.
- [ ] Improv offers Wi-Fi setup after reboot; valid credentials connect to a 2.4 GHz network.
- [ ] An incorrect password can be corrected; Improv credentials survive a power cycle.
- [ ] Fallback: with Wi-Fi unavailable, wait about a minute, join the open AP, visit `192.168.4.1`, enter valid credentials and check reconnection after a restart. The fallback AP should disappear once connected.
- [ ] HA discovers the device through ESPHome; manual addition using IP:6053 also works.
- [ ] One measurement entity, **Wind Speed**, with unit **km/h**, device class `wind_speed`, state class `measurement`; no blind controls.
- [ ] Smooth rotation produces intermediate readings, not only multiples of 2.4 km/h. A stationary sensor settles at zero.
- [ ] About 5 seconds after the last pulse, the reading becomes zero, with no false spikes while stationary.
- [ ] If an open-collector pulse generator is available: 1 Hz → 2.4 km/h, 10 Hz → 24.0 km/h, 20 Hz → 48.0 km/h. Allow several periods to settle. GPIO uses 3.3 V; never apply 5 V. Hand-spinning is not a precise calibration reference.
- [ ] Router outage and recovery: the device reconnects and HA readings resume.
- [ ] OTA using `.ota.bin` as described in the README succeeds, preserving Wi-Fi and entity identity. Check restart and measurement afterward.
- [ ] After publication, HA shows **Firmware Update** and a test update installs from the Pages manifest while preserving Wi-Fi and entity identity.
- [ ] After publication, ESPHome Device Builder discovers the device; **Take control** creates a valid local YAML and an OTA build from it succeeds.
- [ ] Two simultaneous sensors have different MAC-suffixed names and separate entities, if a second board is available.
- [ ] At least 24 hours of operation without unexpected reboots or false pulses when stationary.

## Before publication

- [ ] Choose the software license and a separate 3D model license; add BOM, photos and assembly instructions.
- [ ] Record physical test results, calibration limits and balcony placement effects.
- [ ] Decide the distributed firmware’s API, OTA and fallback AP security policy.
- [ ] Change repository visibility and enable public HTTPS hosting only on explicit instruction; confirm the installer, manifest, factory image and OTA image return HTTP 200.
- [ ] Confirm the published Pages manifest version, OTA MD5 and release link match the stable GitHub release.

| Date / build | Test | Result | Notes |
| --- | --- | --- | --- |
| | | | |
