# HA Wind Sensor

[English (default)](README.md) · **Čeština**

Soukromý prototyp pro **Seeed Studio XIAO ESP32-S3 + LaskaKit WH-SP-WS01**.
Výsledkem je jedna měřicí entita **Wind Speed** v **km/h** v Home Assistantu.
Bez automatizací nebo logiky žaluzií. Verze projektu je v `VERSION`.

Firmware: ESPHome **2026.9.0**, ESP-IDF. Instalátor: ESP Web Tools **10.4.0**.
Automatické kontroly nejsou potvrzením funkce na fyzickém zařízení; domácí ověření popisuje [testovací checklist](docs/test-checklist.cs.md). Instalátor se otevře anglicky; nahoře lze přepnout na češtinu. Vlastní dialogy ESP Web Tools používají jazykovou podporu této knihovny.

## Co potřebuješ

- XIAO ESP32-S3 s připojenou externí Wi-Fi anténou (8 MB flash).
- WH-SP-WS01 s reed kontaktem, dva vodiče, datový USB-C kabel a USB napájení.
- Počítač s Chrome/Edge, Pythonem 3 a internetem pro načtení knihovny instalátoru.
- 2,4GHz Wi-Fi a Home Assistant se síťovým přístupem k zařízení.

Zapoj při odpojeném napájení:

| WH-SP-WS01 | XIAO ESP32-S3 |
| --- | --- |
| Jeden vodič reed kontaktu | **D3 = GPIO4** |
| Druhý vodič | **GND** |

Kontakt nemá polaritu a nepotřebuje napájení. Firmware zapíná interní pull-up.
**D4 není GPIO4.** Deska používá 3,3V logiku. 3D model držáku a montážní dokumentace budou doplněny samostatně.

## Nejrychlejší domácí instalace

Finální veřejná adresa bude **https://mathyass.github.io/ha-wind-sensor/**. Dokud je repozitář soukromý, použij lokální instalační balíček:

1. Po přihlášení na GitHub otevři [Releases](https://github.com/Mathyass/ha-wind-sensor/releases) a stáhni `ha-wind-sensor-<verze>-installer.zip`. Alternativně v [Actions](https://github.com/Mathyass/ha-wind-sensor/actions) otevři úspěšný build a stáhni artifact `ha-wind-sensor-installer`; v něm rozbal ještě vlastní instalační ZIP.
2. Rozbal celý instalační ZIP. Otevři terminál v rozbalené složce a spusť:

   ```sh
   python3 serve.py
   ```

   Ve Windows lze použít `py serve.py`. Otevře se `http://localhost:8000`; v případě potřeby adresu otevři ručně v Chrome/Edge. Server je dostupný jen na tomto počítači, ukončíš ho Ctrl+C. Pokud je port obsazený, alternativně spusť `python3 -m http.server 8001 --bind 127.0.0.1` ve stejné složce a otevři `http://localhost:8001`.

3. Připoj XIAO datovým USB-C kabelem, zavři sériové monitory a klikni **Připojit a nainstalovat**. Vyber odpovídající USB port. První čistý test proveď s vymazáním zařízení: odstraní dosavadní firmware i uloženou Wi-Fi.
4. Po flashování průvodce přes **Improv Serial** nabídne nastavení Wi-Fi. Zadej údaje 2,4GHz sítě. Pokud port po restartu zmizí, odpoj/připoj USB a připoj se znovu; firmware nemusíš znovu nahrávat.
5. V Home Assistantu otevři **Nastavení → Zařízení a služby** a potvrď objevené ESPHome zařízení. Pokud discovery nefunguje, přidej integraci ESPHome ručně: IP zařízení a port `6053`. IP zjistíš například v routeru. Objeví se **Wind Speed**, obvykle s ID podobným `sensor.ha_wind_sensor_a1b2c3_wind_speed`; přesné ID určuje HA.
6. Roztoč anemometr a po zastavení ověř návrat k nule. Pokračuj checklistem.

Neotvírej instalátor dvojklikem jako `file://` a neservíruj ho z obyčejné LAN HTTP adresy. Web Serial potřebuje zabezpečený kontext; `localhost` funguje jako lokální výjimka, veřejné nasazení potřebuje HTTPS.

## Fallback a obnova USB

Při nepřipojené Wi-Fi se přibližně po minutě aktivuje otevřený fallback AP. ESPHome odvodí jeho název od zařízení (HA Wind Sensor a MAC suffix). Připoj se k němu, případně vypni automatický návrat telefonu k jiné síti, a otevři **http://192.168.4.1**. Nastav správné SSID/heslo. Údaje z Improv i captive portalu se ukládají v zařízení a přežijí restart.

Pokud zařízení nejde flashnout: podrž **BOOT**, krátce stiskni **RESET**, uvolni BOOT a znovu vyber sériový port. Po nahrání může být potřeba RESET. Zkontroluj také datový kabel a externí anténu.

## Měření a jeho limity

`pulse_meter` měří intervaly mezi pulzy a vrací pulzy za minutu. Zadaná kalibrace je **1 Hz = 2,4 km/h**, tedy `60 × 0,04 = 2,4 km/h`. Používáme GPIO4, interní pull-up, `internal_filter: 5ms`, režim `EDGE`, `timeout: 5s` a jednu desetinnou číslici. Nezavádíme průměrování ani další senzory.

Pět sekund bez pulzu znamená nulu. Při intervalech nad 5 s (méně než přibližně 0,48 km/h podle zadané kalibrace) nemůže toto nastavení poskytovat souvislé nízké hodnoty. Timeout nerozliší bezvětří od přerušeného vodiče. Přesnost skutečného větru je nutné ověřit pro senzor a umístění; balkon může proudění významně ovlivnit.

## Aktualizace a ESPHome Device Builder

Zveřejněný firmware kontroluje každých šest hodin HTTPS manifest na GitHub Pages. Když je dostupná novější stabilní verze, Home Assistant ukáže v konfigurační části zařízení entitu **Firmware Update**. Přečti si odkazované poznámky k vydání a aktualizaci spusť z HA. Manifest obsahuje MD5 OTA obrazu a ESPHome ověřuje HTTPS certifikát. Funkce začne pracovat po zveřejnění repozitáře a Pages webu.

Nativní ESPHome OTA je zároveň dostupná na portu **3232**. Pro ruční update použij **`firmware/ha-wind-sensor.ota.bin`**, nikdy factory image. Obě cesty zachovají uloženou Wi-Fi a MAC identitu.

V lokálním klonu repozitáře připrav prostředí podle následující sekce. Pak nahraj `.ota.bin` z rozbaleného release ZIPu (nahraď IP i cestu skutečnými hodnotami):

```sh
esphome upload esphome/wind-sensor.yaml --device 192.168.1.123 --file /cesta/k/firmware/ha-wind-sensor.ota.bin
```

Pro vlastní nově sestavený firmware lze použít `esphome -s firmware_version "$(cat VERSION)" run esphome/wind-sensor.yaml --device 192.168.1.123`. Dokud je repo private, přístup k release vyžaduje přihlášení a spravovaná kontrola aktualizací neškodně selže.

Po zveřejnění ESPHome Device Builder zařízení objeví a nabídne **Take control**. Importovaný lokální YAML odkazuje na tento repozitář jako vzdálený balíček, takže vlastník může měnit substitutions a další buildy instalovat bezdrátově. Pro aktualizaci balíčku musí repozitář zůstat veřejný.

## Lokální vývoj a struktura

```text
esphome/wind-sensor.yaml           vstup pro univerzální firmware
esphome/packages/wind-sensor.yaml  znovupoužitelná konfigurace
installer/                        web a šablona manifestu
scripts/build.py                  validace, kompilace, balení
scripts/package.py                factory + OTA + manifest + checksumy
.github/workflows/build.yml        build, release a veřejné nasazení Pages
docs/test-checklist.md             domácí testy a podmínky zveřejnění
VERSION                           verze použitá v buildu i manifestu
```

V klonu repozitáře (Python 3.13):

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python dist/installer/serve.py
```

Na Windows aktivuj `.venv\Scripts\activate`; kompilátor ESP-IDF si při prvním sestavení stáhne potřebné nástroje. CI používá Ubuntu 24.04. `scripts/build.py` dodá verzi z `VERSION`; výchozí verze v YAML musí s `VERSION` souhlasit kvůli importu do Device Builderu.

Výstup `dist/installer/` obsahuje připravený web, **factory image sloučenou ESPHome na offset 0**, OTA image, build metadata a SHA-256 kontrolní součty. Stejný obsah je v `dist/ha-wind-sensor-<verze>-installer.zip`. Binární soubory, secrets a lokální konfigurace se necommitují. Zdrojový `installer/manifest.json` je šablona; samotný zdrojový adresář ještě neobsahuje firmware. Web chybějící binární soubor pozná a instalaci nenabídne.

## Soukromé buildy a release

Push na `main`, pull request nebo ruční **Run workflow** provede kontrolu, kompilaci a vytvoří stažitelný artifact (uchování 30 dní). Tag **`v<obsah VERSION>`** navíc vytvoří GitHub **prerelease** a přiloží instalační ZIP. Neshodující se tag build odmítne.

```sh
# Po úpravě VERSION, commitu a úspěšném buildu:
git tag v0.1.0-beta.3
git push origin v0.1.0-beta.3
```

Dokud je repozitář soukromý, vše zůstává dostupné jen spolupracovníkům a nasazení Pages se přeskočí. Po zveřejnění repozitáře a nastavení Pages na GitHub Actions každý verzovací tag nejprve vytvoří release a potom nasadí anglický/český instalátor, manifest a firmware na stabilní HTTPS adresu. Beta tag tak umožňuje otestovat veřejný instalátor od začátku do konce; další stabilní tag ho později nahradí pro běžné použití. Workflow nikdy nemění viditelnost repozitáře. Načtení ESP Web Tools z CDN vyžaduje internet.

## Zabezpečení testovacího firmware

Univerzální image neobsahuje Wi-Fi credentials, GitHub token ani společný API klíč. Pro tento první test je **API bez šifrování, OTA bez hesla a fallback AP otevřený**. Používej důvěryhodnou síť; porty nepřesměrovávej do internetu. Captive portal v ESPHome také zpřístupňuje webové OTA při běhu fallback AP.

Pro zabezpečení konkrétního zařízení vytvoř ignorovaný `esphome/wind-sensor.local.yaml`, zkopíruj do něj obsah `wind-sensor.yaml` a doplň:

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

Hodnoty ulož do ignorovaného `esphome/secrets.yaml`. API klíč je base64 kódovaných 32 náhodných bytů; vygeneruješ ho `openssl rand -base64 32`. AP heslo musí mít 8–64 znaků. První zabezpečený build nahraj přes USB; potom v HA nastav nový API klíč a pro další OTA používej odpovídající lokální YAML. Návrat k univerzálnímu firmware tato zabezpečení odstraní. Lokální soubory nikdy nepřidávej do sdíleného buildu.

Home Assistant discovery přes mDNS funguje nezávisle na převzetí zdrojové konfigurace. `dashboard_import` je už v beta firmware, ale Device Builder ho dokáže stáhnout až po zveřejnění repozitáře. Do té doby používej pro změny lokální klon/package.

## Zdroje a další fáze

- [ESPHome pulse_meter](https://esphome.io/components/sensor/pulse_meter/)
- [ESPHome Improv Serial](https://esphome.io/components/improv_serial/) a [USB logger](https://esphome.io/components/logger/)
- [ESP Web Tools — manifest a instalátor](https://esphome.github.io/esp-web-tools/)
- [ESPHome OTA](https://esphome.io/components/ota/esphome/)
- [ESPHome spravované HTTP aktualizace](https://esphome.io/components/update/http_request/)
- [Seeed XIAO ESP32-S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

Veřejný instalační řetězec, spravované aktualizace a převzetí do Device Builderu jsou připravené, ale dokud je repozitář soukromý, zůstávají neaktivní. Licence, 3D model, fotografie a MakerWorld stránka přijdou po domácích testech. Zatím není udělena veřejná open-source licence.
