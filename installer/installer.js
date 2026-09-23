const status = document.querySelector('#status');
const install = document.querySelector('#install');

async function prepareInstaller() {
  if (!window.isSecureContext || !('serial' in navigator)) {
    status.textContent = 'Otevři instalátor v Chrome nebo Edge na počítači přes HTTPS nebo http://localhost:8000.';
    return;
  }
  try {
    const response = await fetch('manifest.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Manifest chybí.');
    const manifest = await response.json();
    const part = manifest.builds.find(build => build.chipFamily === 'ESP32-S3')?.parts[0];
    if (!part || part.offset !== 0) throw new Error('Neplatný instalační manifest.');
    const firmware = await fetch(new URL(part.path, response.url), { method: 'HEAD', cache: 'no-store' });
    if (!firmware.ok) throw new Error('Firmware chybí. Stáhni a rozbal celý instalační ZIP z GitHub Actions nebo Releases.');
    await import('https://unpkg.com/esp-web-tools@10.4.0/dist/web/install-button.js?module');
    await customElements.whenDefined('esp-web-install-button');
    document.querySelector('#version').textContent = `Verze ${manifest.version}`;
    status.textContent = 'Připraveno. Připoj XIAO ESP32-S3 přes USB-C.';
    install.hidden = false;
  } catch (error) {
    status.textContent = `Instalátor není připraven: ${error.message} Zkontroluj také připojení k internetu.`;
  }
}

prepareInstaller();
