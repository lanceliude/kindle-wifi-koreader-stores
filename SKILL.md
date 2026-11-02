---
name: kindle-wifi-koreader-stores
slug: lanceliude-kindle-wifi-koreader-stores
version: 1.0.2
displayName: Kindle Wi-Fi KOReader 插件商店安装器
summary: 无数据线，通过本地 Wi-Fi 在已越狱 Kindle 上无线安装 KOReader AppStore 与卡欧市场（komarket）。
description: "面向已越狱、已安装 KOReader 的 Kindle 用户：无需数据线，通过同一局域网 Wi-Fi，由 Agent 启动本地服务并指导用户用 kTerm 一键无线安装 AppStore 与卡欧市场（komarket）两个插件商店。适用于用户没有可用数据线、想无线安装 KOReader 插件商店、;kpm add-repo 失败、找不到 KOReader 内置终端，或需要 Agent 引导完成 kTerm + 本地 HTTP 服务流程的场景。English: install KOReader AppStore and komarket over local Wi-Fi without USB cable using kTerm and a local agent-run HTTP server."
tags: [kindle, koreader, wifi, kterm, appstore, plugin-store, ebook-reader, jailbroken-kindle, koreader-plugin]
license: MIT
homepage: https://github.com/lanceliude/kindle-wifi-koreader-stores
---

# Kindle Wi-Fi KOReader 插件商店安装器

## 目标

通过本地 Wi-Fi，把两个 KOReader 插件商店安装到 `/mnt/us/koreader/plugins/`：

- `appstore.koplugin`：国际社区插件商店。
- `komarket.koplugin`：卡欧市场 / Kaou Market，中文插件商店。

两个商店安装完成后，用户可以直接在商店里搜索、安装其他 KOReader 插件。

## 操作原则

- Kindle 端命令必须尽量短，避免用户在虚拟键盘上输入复杂内容。
- 不要让用户在 Kindle 端输入变量、括号、分号、`|| curl` 回退链或长脚本。
- 如果 KOReader 内置终端找不到，使用已验证可用的 kTerm 作为执行终端。
- 本地 HTTP 服务只允许在同一可信家庭 Wi-Fi 下使用，不要暴露到公网。

## 执行流程

1. 先确认前置条件：Kindle 已越狱、KOReader 已安装、KPM 可用、Kindle 和电脑连接同一个 Wi-Fi。
2. 在用户电脑上启动本地服务：

```bash
python3 scripts/start_stores_server.py
```

Windows PowerShell 使用：

```powershell
python scripts\start_stores_server.py
```

3. 如果电脑缺少 Python 3，先指导用户安装 Python 3。macOS 可尝试 `xcode-select --install`；Windows 从 python.org 安装，并勾选 “Add Python to PATH”。
4. 等待脚本打印本机局域网 IP、端口，以及要在 Kindle 上执行的完整短命令。
5. 指导用户回到 Kindle 首页图书馆，打开搜索框，输入并执行：

```text
;kpm install kterm
```

6. kTerm 安装完成后打开它，输入脚本打印出来的那条短命令。
7. 如果 kTerm 下一行只出现单独的 `>`，说明命令被 shell 判断为未结束；让用户按 `Ctrl+C` 退回命令行，再重新输入脚本打印的短命令。
8. 等待出现两行成功提示：

```text
OK: AppStore installed to /mnt/us/koreader/plugins/appstore.koplugin
OK: Kaou Market installed to /mnt/us/koreader/plugins/komarket.koplugin
```

9. 指导用户完全退出 KOReader，重新打开，然后在 `插件 → 插件管理` 中启用两个商店。

## 参考文档

指导用户操作前，按需阅读：

- `references/kindle-steps.md`：已验证的 Kindle 与 kTerm 完整操作步骤。
- `references/keyboard-chars.md`：kTerm 虚拟键盘字符输入说明，重点包括冒号、竖线、大写字母 O、Shift 和 `Ctrl+C`。

## 已知坑点

- 已验证设备上 `;kpm add-repo http://...` 不可靠，不要使用这条路线。
- Kindle 原生浏览器不能直接选择插件目录，也不能自动解压安装插件。
- `-qO-` 中的 `O` 是大写字母 O，不是数字 `0`。
- 用户卡住时，先让用户拍摄当前屏幕，再根据真实报错调整命令，不要凭猜测改长命令。
