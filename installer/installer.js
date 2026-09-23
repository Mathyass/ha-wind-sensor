const status = document.querySelector('#status');
const install = document.querySelector('#install');
const cs = document.documentElement.lang === 'cs';
const copy = cs ? {
  unsupported: 'Otevři instalátor v Chrome nebo Edge na počítači přes HTTPS nebo http://localhost:8000.',
  manifest: 'Manifest chybí.', invalid: 'Neplatný instalační manifest.',
  firmware: 'Firmware chybí. Stáhni a rozbal celý instalační ZIP z GitHub Actions nebo Releases.',
  version: 'Verze', ready: 'Připraveno. Připoj XIAO ESP32-S3 přes USB-C.',
  error: 'Instalátor není připraven:', internet: 'Zkontroluj také připojení k internetu.'
} : {
  unsupported: 'Open this installer in desktop Chrome or Edge using HTTPS or http://localhost:8000.',
  manifest: 'The manifest is missing.', invalid: 'Invalid installation manifest.',
  firmware: 'Firmware is missing. Download and extract the complete installer ZIP from GitHub Actions or Releases.',
  version: 'Version', ready: 'Ready. Connect your XIAO ESP32-S3 with a USB-C data cable.',
  error: 'Installer is not ready:', internet: 'Also check your internet connection.'
};

async function prepareInstaller() {
  if (!window.isSecureContext || !('serial' in navigator)) {
    status.textContent = copy.unsupported;
    return;
  }
  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(copy.manifest);
    const manifest = await response.json();
    const part = manifest.builds.find(build => build.chipFamily === 'ESP32-S3')?.parts[0];
    if (!part || part.offset !== 0) throw new Error(copy.invalid);
    const firmware = await fetch(new URL(part.path, response.url), { method: 'HEAD', cache: 'no-store' });
    if (!firmware.ok) throw new Error(copy.firmware);
    await import('https://unpkg.com/esp-web-tools@10.4.0/dist/web/install-button.js?module');
    await customElements.whenDefined('esp-web-install-button');
    document.querySelector('#version').textContent = `${copy.version} ${manifest.version}`;
    status.textContent = copy.ready;
    install.hidden = false;
  } catch (error) {
    status.textContent = `${copy.error} ${error.message} ${copy.internet}`;
  }
}

prepareInstaller();
