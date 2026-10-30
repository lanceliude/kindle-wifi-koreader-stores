# kindle-wifi-koreader-stores

在已越狱 Kindle 上，通过本地 Wi-Fi 无线安装两个 KOReader 插件商店，不需要数据线。

本次会同时安装：

- `appstore.koplugin`：国际社区插件商店。
- `komarket.koplugin`：卡欧市场，中文插件商店。

两个商店装好以后，其他 KOReader 插件都可以在 KOReader 内部直接搜索安装。

## 适用场景

- Kindle 已经越狱。
- KOReader 已经安装。
- 没有可用数据线，或者数据线只能充电。
- 想通过 Wi-Fi 安装 `appstore.koplugin` 和 `komarket.koplugin`。

这个仓库只负责引导安装这两个插件商店，不负责越狱 Kindle、不负责安装 KOReader、不负责安装其他插件。

## 原理

1. 电脑上的 Python 脚本自动下载最新 AppStore 和卡欧市场 release。
2. 脚本把两个插件打包成一个 Kindle 可解压的压缩包，并在本机启动 Wi-Fi 服务。
3. Kindle 首页通过 KPM 安装官方终端 kTerm。
4. 在 kTerm 里执行一条短命令。
5. 插件自动解压到 `/mnt/us/koreader/plugins/`。

## 前置条件

- Kindle 已越狱。
- KOReader 已安装。
- KPM 可用。
- 电脑已安装 Python 3。
- Kindle 和电脑连接同一个 Wi-Fi。

## 快速开始

### macOS / Linux

```bash
python3 scripts/start_stores_server.py
```

### Windows PowerShell

```powershell
python scripts\start_stores_server.py
```

脚本会打印类似下面的命令：

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

## Kindle 操作步骤

1. 回到 Kindle 首页图书馆。
2. 打开搜索框，输入：

```text
;kpm install kterm
```

3. 等 KPM 安装完成。
4. 打开 kTerm。
5. 输入电脑脚本打印出来的那条短命令。
6. 完全退出 KOReader，再重新打开。
7. 在下面位置启用两个商店：

```text
插件 → 插件管理
```

启用后一般能看到：

- AppStore
- 卡欧市场 / Kaou Market

## 注意事项

- `-qO-` 中间是大写字母 `O`，不是数字 0。
- 如果 kTerm 里出现单独的 `>`，按 `Ctrl+C` 退回命令行，再重新输入短命令。
- 只建议在信任的家庭 Wi-Fi 里使用，不要把服务暴露到公网。
- 已验证设备：Kindle Basic 3 / J9G29R。其他越狱设备可能需要按设备型号调整。

## 许可证

MIT
