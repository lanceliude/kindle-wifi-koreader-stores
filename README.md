# kindle-wifi-koreader-stores

Install two KOReader plugin stores on a jailbroken Kindle over local Wi-Fi, without a data cable.

This installs both:

- `appstore.koplugin`: international community plugin store.
- `komarket.koplugin`: Kaou Market / 卡欧市场, Chinese plugin store.

After both stores are installed, use them inside KOReader to install other KOReader plugins.

## What this is for

Use this when:

- Your Kindle is already jailbroken.
- KOReader is already installed.
- You do not have a usable USB cable, or the cable only charges.
- You want to install `appstore.koplugin` and `komarket.koplugin` wirelessly.

This repo bootstraps only these two plugin stores. It does not jailbreak Kindle, install KOReader, or install plugins other than these stores.

## How it works

1. A local Python server on your computer downloads the latest AppStore and Kaou Market releases.
2. It bundles both plugins into one small tarball and serves it on your local Wi-Fi.
3. On the Kindle, install the official terminal `kTerm` with KPM.
4. Run one short command in kTerm.
5. The plugin is extracted into `/mnt/us/koreader/plugins/`.

## Requirements

- Jailbroken Kindle.
- KOReader installed.
- KPM available.
- Python 3 on your computer.
- Kindle and computer on the same Wi-Fi.

## Quick start

### macOS / Linux

```bash
python3 scripts/start_stores_server.py
```

### Windows PowerShell

```powershell
python scripts\start_stores_server.py
```

The script prints a command like:

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

## Kindle steps

1. Go to the Kindle home library.
2. Open search and enter:

```text
;kpm install kterm
```

3. Wait for KPM to finish.
4. Open kTerm.
5. Run the command printed by the computer script.
6. Fully exit KOReader and reopen it.
7. Enable both stores in:

```text
Plugins → Plugin Management
```

You should see both AppStore and Kaou Market after restarting KOReader.

## Notes

- `-qO-` uses the capital letter `O`, not the digit `0`.
- If kTerm shows a `>` prompt, press Ctrl+C and retype the shorter command.
- This is for trusted local Wi-Fi only. Do not expose the server to the public internet.
- Verified on Kindle Basic 3 / J9G29R. Other jailbroken devices may need device-specific adjustments.

## License

MIT
