# Kindle-side proven steps

Verified on a jailbroken Kindle Basic 3 / J9G29R with KOReader installed.

## Prerequisites

- Kindle is jailbroken.
- KOReader is installed.
- KPM is available.
- Kindle and the user's computer are on the same Wi-Fi network.
- The computer can reach GitHub to download the AppStore and Kaou Market releases.

## Start the computer-side server

Run the bundled script. It prints the exact Kindle command.

```bash
python3 scripts/start_stores_server.py
```

On Windows PowerShell:

```powershell
python scripts\start_stores_server.py
```

If Windows Firewall asks, allow access on private networks.

## Install kTerm on Kindle

The KOReader built-in terminal may be missing from the menu on some devices. Use the official independent kTerm instead.

1. Go to the Kindle home library.
2. Open the search box.
3. Type:

```text
;kpm install kterm
```

4. Wait for KPM to finish.
5. Open kTerm from the Kindle home library.

## Run the installer in kTerm

Use the exact command printed by the computer-side script. It should look like:

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

If `wget` is missing or fails, use:

```sh
curl -fsSL http://192.168.1.50:8000/g | sh
```

Success looks like:

```text
OK: AppStore installed to /mnt/us/koreader/plugins/appstore.koplugin
OK: Kaou Market installed to /mnt/us/koreader/plugins/komarket.koplugin
```

## Enable both stores

1. Fully exit KOReader.
2. Reopen KOReader.
3. Go to:

```text
Menu → Plugins → Plugin Management
```

4. Enable AppStore and Kaou Market.
5. After this, install other KOReader plugins from inside either store.

## Do not retry these failed paths

- `;kpm add-repo http://<computer-ip>:<port>/` flashes back to home on this device.
- The Kindle built-in browser cannot choose the plugin directory or unzip the plugin.
- Long Kindle commands with variables and parentheses can trigger a `>` continuation prompt.
