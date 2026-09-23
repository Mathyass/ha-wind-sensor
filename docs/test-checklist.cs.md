# Domácí test — 0.1.0-beta.2

[English](test-checklist.md) · **Čeština**

Zapiš datum, verzi/commit z `build-info.json`, verzi Home Assistantu, prohlížeč a výsledek.
Automatický build ověřuje konfiguraci a kompilaci; následující kroky vyžadují fyzický hardware.

- [ ] Anténa je připojená, reed mezi **D3 / GPIO4 a GND**, USB kabel přenáší data.
- [ ] Čistá instalace z ZIPu v Chrome/Edge: flash projde na XIAO ESP32-S3, bez restartovací smyčky.
- [ ] Instalátor se otevře anglicky; přepnutí na češtinu a zpět funguje. Obě verze používají stejný firmware.
- [ ] Improv po restartu nabídne Wi-Fi; správné údaje připojí zařízení do 2,4GHz sítě.
- [ ] Chybné heslo lze opravit; Wi-Fi zadaná přes Improv zůstane uložená po odpojení napájení.
- [ ] Fallback: při nedostupné Wi-Fi počkat přibližně minutu, najít otevřený AP, otevřít `192.168.4.1`, zadat správné údaje a ověřit připojení i po restartu. Po připojení má fallback AP zmizet.
- [ ] Home Assistant zařízení objeví přes ESPHome; alternativně funguje ruční přidání IP:6053.
- [ ] Jedna měřicí entita **Wind Speed**, jednotka **km/h**, device class `wind_speed`, state class `measurement`; žádné ovládání žaluzií.
- [ ] Plynulé roztočení ukazuje mezihodnoty, bez skoků pouze po 2,4 km/h. Po ustálení v klidu je 0.
- [ ] Po posledním pulzu přibližně do 5 s přejde hodnota na 0, bez falešných špiček při stojícím senzoru.
- [ ] Máš-li generátor impulzů s výstupem otevřený kolektor: 1 Hz → 2,4 km/h, 10 Hz → 24,0 km/h, 20 Hz → 48,0 km/h. Počkej na několik period. GPIO je 3,3 V; nepřivádět 5 V. Ruční otáčení není přesná kalibrační reference.
- [ ] Výpadek routeru a jeho návrat: zařízení se připojí a měření se v HA obnoví.
- [ ] OTA podle README s `.ota.bin` projde; Wi-Fi a identita entity zůstanou zachované. Ověřit následný restart a měření.
- [ ] Po zveřejnění HA ukáže **Firmware Update** a testovací aktualizace z Pages manifestu zachová Wi-Fi i identitu entity.
- [ ] Po zveřejnění ESPHome Device Builder zařízení objeví; **Take control** vytvoří platný lokální YAML a jeho OTA build projde.
- [ ] Dva senzory zároveň mají odlišné názvy/MAC suffixy a samostatné entity (pokud máš druhou desku).
- [ ] Alespoň 24 hodin provozu bez samovolných restartů a falešných pulzů v klidu.

## Před zveřejněním

- [ ] Vyřešit licenci k softwaru a zvlášť k 3D modelu, doplnit BOM, fotografie a montáž.
- [ ] Zaznamenat výsledky hardwarových testů a limity kalibrace / vlivu umístění na balkoně.
- [ ] Rozhodnout zabezpečení API, OTA a fallback AP pro distribuovaný firmware.
- [ ] Teprve na výslovný pokyn změnit viditelnost repozitáře a zapnout veřejný HTTPS hosting; ověřit HTTP 200 pro instalátor, manifest, factory a OTA obraz.
- [ ] Ověřit, že verze, OTA MD5 a odkaz na release ve zveřejněném Pages manifestu odpovídají stabilnímu GitHub release.

| Datum / build | Test | Výsledek | Poznámka |
| --- | --- | --- | --- |
| | | | |
