---
name: kindle-wifi-koreader-stores
slug: lanceliude-kindle-wifi-koreader-stores
version: 1.0.0
displayName: Kindle Wi-Fi KOReader 插件商店安装器
summary: 无数据线，通过本地 Wi-Fi 在已越狱 Kindle 上无线安装 KOReader AppStore 与卡欧市场（komarket）。
description: "Install KOReader plugin stores (AppStore + Kaou Market/komarket.koplugin) on a jailbroken Kindle over local Wi-Fi without a USB cable. Use when the user already has KOReader installed, has no usable data cable, wants to install koplugin stores wirelessly, hit ;kpm add-repo failures, cannot find KOReader built-in terminal, or wants an agent-guided kTerm + local HTTP server workflow."
tags: [kindle, koreader, wifi, kterm, appstore, plugin-store, ebook-reader, jailbroken-kindle, koreader-plugin]
license: MIT
homepage: https://github.com/lanceliude/kindle-wifi-koreader-stores
---

# Kindle Wi-Fi KOReader Stores Installer

## Goal

Install two KOReader plugin stores into `/mnt/us/koreader/plugins/` over Wi-Fi:

- `appstore.koplugin` — international community plugin store.
- `komarket.koplugin` — Kaou Market / 卡欧市场, Chinese plugin store.

After this, the user installs other KOReader plugins from inside either store.

## Operating rules

- Keep the Kindle-side command as short as possible.
- Do not ask the user to type variables, parentheses, semicolons, or fallback chains on the Kindle.
- Treat kTerm as the verified executor when KOReader's built-in terminal is missing.
- Never expose the local server to the public internet; only use the same trusted Wi-Fi network.

## Workflow

1. Confirm prerequisites: jailbroken Kindle, KOReader installed, KPM available, same Wi-Fi.
2. Start the local server:

```bash
python3 scripts/start_stores_server.py
```

On Windows, use:

```powershell
python scripts\start_stores_server.py
```

3. If Python is missing, guide the user to install Python 3 first. On macOS, `xcode-select --install` may provide `python3`. On Windows, install from python.org and enable "Add Python to PATH".
4. Let the script print the exact IP, port, and Kindle command.
5. Guide the user to install kTerm from the Kindle home search box:

```text
;kpm install kterm
```

6. Open kTerm and run the printed command.
7. If the terminal shows `>`, tell the user to press Ctrl+C and retype the shorter printed command.
8. Wait for both success lines:

```text
OK: AppStore installed to /mnt/us/koreader/plugins/appstore.koplugin
OK: Kaou Market installed to /mnt/us/koreader/plugins/komarket.koplugin
```

9. Tell the user to fully exit KOReader, reopen it, and enable both stores in `Plugins → Plugin Management`.

## References

Read these when guiding the user:

- `references/kindle-steps.md`: full verified Kindle and kTerm workflow.
- `references/keyboard-chars.md`: kTerm virtual keyboard character hints, especially colon, pipe, uppercase O, and Ctrl+C.

## Known pitfalls

- `;kpm add-repo http://...` is unreliable on the verified device; do not use it.
- The Kindle built-in browser cannot unzip directly into the plugin directory.
- `-qO-` uses capital letter O, not digit zero.
- If the user gets stuck, ask for a photo of the exact screen before changing commands.
