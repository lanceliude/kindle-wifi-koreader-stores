---
name: kindle-wifi-koreader-stores
slug: lanceliude-kindle-wifi-koreader-stores
version: 1.0.3
displayName: Kindle Wi-Fi KOReader 插件商店安装器
summary: 无数据线，通过本地 Wi-Fi 在已越狱 Kindle 上无线安装 KOReader 插件商店（AppStore 应用商店 + 卡欧市场 komarket），适合给电子书阅读器装插件商店、用 kTerm 一键安装的场景。
description: "给已越狱、已装好 KOReader 的 Kindle 装插件商店，不用数据线。适用于 Kindle 没有可用数据线、数据线只能充电、想给电子书阅读器或电纸书无线安装插件商店、插件市场、KOReader 找不到商店入口、AppStore 应用商店装不上、卡欧市场（komarket）装不上、;kpm add-repo 长链接失败、KOReader 内置终端找不到、需要在 Kindle 上用 kTerm 输入命令又怕输错的场景。Agent 负责在用户电脑上启动本地 HTTP 服务，并逐步指导用户在 Kindle 首页用 KPM 装 kTerm、在 kTerm 里执行一条极短命令，插件自动解压到 /mnt/us/koreader/plugins/。触发词：Kindle 装插件、Kindle 插件商店、KOReader 插件商店、KOReader 应用商店、Kindle 无线安装、Kindle 没有数据线、kTerm 安装插件、卡欧市场、AppStore、koplugin。English: install KOReader plugin stores (AppStore + komarket) on a jailbroken Kindle over local Wi-Fi without a USB cable, using kTerm and an agent-run local HTTP server."
tags: [kindle, koreader, kterm, plugin-store, appstore, komarket, ebook-reader, jailbroken-kindle, wifi, no-usb, kindle-plugins, koreader-plugin, plugin-market]
license: MIT
homepage: https://github.com/lanceliude/kindle-wifi-koreader-stores
---

# Kindle Wi-Fi KOReader 插件商店安装器

给已越狱、已装好 KOReader 的 Kindle 装两个插件商店，**不需要数据线**。
装完之后，用户就能在 KOReader 里直接搜索、安装其他所有插件。

## 用户可以直接复制这句话给 Agent

> 我的 Kindle 已经越狱、也装好 KOReader 了，但没有能用的数据线（只有充电线）。帮我按这个技能，用同一个 Wi-Fi 无线装好 KOReader 的插件商店，一步一步告诉我 Kindle 上该点什么、该输什么。

Agent 收到后按下面的「执行流程」走即可，不需要用户自己判断技术细节。

## 开始前的 30 秒自检

用户的回答只要有一条是「否」，就先别往下走，先补齐前置条件：

| 检查项 | 怎么确认 |
|---|---|
| Kindle 已越狱吗 | Kindle 首页有 KUAL 或越狱图标；不确定就先问用户越狱时用的哪套方案 |
| KOReader 能打开吗 | 打开 KOReader 随便翻一本书，能正常显示 |
| 电脑有 Python 3 吗 | macOS / Linux 跑 `python3 --version`；Windows 跑 `python --version`，没有就去 python.org 装并勾选 Add to PATH |
| Kindle 和电脑在同一个 Wi-Fi 吗 | 两边连的是同一个路由器；手机热点也行，但两台设备要连同一个热点 |
| 电脑能上 GitHub 吗 | 脚本要从 GitHub 下载两个商店的最新版本 |

这个技能**只负责装这两个商店**，不负责越狱、不负责装 KOReader。用户如果还没越狱或没装 KOReader，先说明超出范围。

## 目标

通过本地 Wi-Fi，把两个 KOReader 插件商店安装到 `/mnt/us/koreader/plugins/`：

- `appstore.koplugin`：国际社区插件商店。
- `komarket.koplugin`：卡欧市场 / Kaou Market，中文插件商店。

## 操作原则

- Kindle 端命令必须尽量短，避免用户在虚拟键盘上输入复杂内容。
- 不要让用户在 Kindle 端输入变量、括号、分号、`|| curl` 回退链或长脚本。
- 如果 KOReader 内置终端找不到，使用已验证可用的 kTerm 作为执行终端。
- 本地 HTTP 服务只允许在同一可信家庭 Wi-Fi 下使用，不要暴露到公网。
- 用户卡住时先让他拍当前屏幕，按真实报错调整，不要凭猜测换长命令。

## 执行流程

1. 先过一遍上面的「30 秒自检」，五项全部为「是」再继续。
2. 在用户电脑上启动本地服务：

```bash
python3 scripts/start_stores_server.py
```

Windows PowerShell：

```powershell
python scripts\start_stores_server.py
```

也可以直接双击仓库里的 `start.command`（macOS）或 `start.ps1`（Windows）。

3. 脚本跑起来后会打印三样东西：本机局域网 IP、端口、以及要在 Kindle 上执行的那条短命令。把这条命令原样抄给用户。
4. 指导用户回到 Kindle 首页图书馆，打开搜索框，输入并执行：

```text
;kpm install kterm
```

5. 等 KPM 装完，Kindle 首页会出现 kTerm，打开它。
6. 让用户在 kTerm 里输入脚本打印的那条短命令，形如：

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

输入时按 `references/keyboard-chars.md` 逐个字符讲清楚：冒号是 Shift + 分号，竖线是 Shift + 反斜杠，`-qO-` 里的 `O` 是大写字母 O 不是数字 0。这是整个流程里最容易出错的地方，必须讲。
7. 如果 kTerm 下一行只出现单独的 `>`，说明 shell 认为命令没输完；让用户按 `Ctrl+C` 退回命令行，再重新输入那条短命令。
8. 等待出现两行成功提示：

```text
OK: AppStore installed to /mnt/us/koreader/plugins/appstore.koplugin
OK: Kaou Market installed to /mnt/us/koreader/plugins/komarket.koplugin
```

9. 指导用户完全退出 KOReader（不是回首页，是退出应用），重新打开，然后在 `插件 → 插件管理` 里勾选两个商店。
10. 装完就可以关掉电脑上的服务窗口。之后装其他插件都在 KOReader 里点几下完成，不再需要这个技能。

## 参考文档

指导用户操作前，按需阅读：

- `references/kindle-steps.md`：已验证的 Kindle 与 kTerm 完整操作步骤。
- `references/keyboard-chars.md`：kTerm 虚拟键盘字符输入说明，重点包括冒号、竖线、大写字母 O、Shift 和 `Ctrl+C`。

## 已知坑点

- 已验证设备上 `;kpm add-repo http://...` 不可靠，会直接闪回首页，不要用这条路线。
- Kindle 原生浏览器不能直接选择插件目录，也不能自动解压安装插件。
- `-qO-` 中的 `O` 是大写字母 O，不是数字 `0`。
- 带变量、括号、`|| curl` 的长命令在 kTerm 里会触发 `>` 续行，必须用短命令。
- 用户卡住时，先让用户拍摄当前屏幕，再根据真实报错调整命令。

## 已知适配

- 真机验证：Kindle 第 10 代入门版（J9G29R / KT4，固件 5.18.1）。
- 电脑侧脚本只用 Python 标准库，macOS / Windows / Linux 通用，未依赖任何系统专属命令。
- Windows 侧未做真机验证，遇到防火墙提示时选择允许"专用网络"。
