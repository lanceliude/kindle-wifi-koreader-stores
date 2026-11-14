# kindle-wifi-koreader-stores

**给已越狱、已装好 KOReader 的 Kindle 装插件商店，不需要数据线。**

> English: install KOReader plugin stores (AppStore + komarket) on a jailbroken Kindle over local Wi-Fi, no USB cable. See [README.en.md](README.en.md).

适用场景：Kindle 没有可用的数据线 / 数据线只能充电 / 想给电子书阅读器无线安装插件商店 / `;kpm add-repo` 失败 / KOReader 里找不到商店入口。

## 一句话用起来

把下面这句话，连同这个仓库链接，一起发给你的 AI Agent：

> 我的 Kindle 已经越狱、也装好 KOReader 了，但没有能用的数据线（只有充电线）。帮我按这个技能，用同一个 Wi-Fi 无线装好 KOReader 的插件商店，一步一步告诉我 Kindle 上该点什么、该输什么。

Agent 会自动在电脑上起一个本地服务，然后把 Kindle 上要点的每一步讲清楚。你不用懂技术细节。

## 装之前，先花 30 秒确认这五件事

| 检查项 | 怎么确认 |
|---|---|
| Kindle 已越狱 | 首页有 KUAL 或越狱图标 |
| KOReader 能打开 | 随便翻一本书能正常显示 |
| 电脑有 Python 3 | macOS/Linux 跑 `python3 --version`；Windows 跑 `python --version` |
| Kindle 和电脑连同一个 Wi-Fi | 同一个路由器，或同一个手机热点 |
| 电脑能上 GitHub | 脚本要从 GitHub 下载两个商店的最新版本 |

这五条有任何一条不满足，先补齐再来。这个仓库**只装这两个商店**，不负责越狱、不负责装 KOReader。

## 会装上什么

- `appstore.koplugin`：国际社区插件商店。
- `komarket.koplugin`：卡欧市场，中文插件商店。

装好之后，其他 KOReader 插件都可以在 KOReader 内部直接搜索安装，不用再折腾。

## 原理

1. 电脑上的 Python 脚本下载两个商店的最新 release。
2. 打成一个小压缩包，并在本机启动 Wi-Fi 服务。
3. Kindle 首页用 KPM 安装官方终端 kTerm。
4. 在 kTerm 里执行一条短命令。
5. 插件自动解压到 `/mnt/us/koreader/plugins/`。

## 手动跑（不想让 Agent 代劳时）

macOS / Linux：

```bash
python3 scripts/start_stores_server.py
```

Windows PowerShell：

```powershell
python scripts\start_stores_server.py
```

也可以 macOS 双击 `start.command`，Windows 用 PowerShell 运行 `start.ps1`。

脚本会打印类似下面这条命令，把它抄到 Kindle 的 kTerm 里：

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

## Kindle 上要做的四步

1. 回首页图书馆，打开搜索框，输入：

```text
;kpm install kterm
```

2. 等 KPM 装完，首页出现 kTerm，打开它。
3. 输入电脑脚本打印的那条短命令。
4. 完全退出 KOReader 再重新打开，到 `插件 → 插件管理` 勾选两个商店。

## 最容易踩的三个坑

- `-qO-` 中间是**大写字母 O**，不是数字 0。
- 冒号是 Shift + 分号；竖线是 Shift + 反斜杠。
- 如果 kTerm 里出现单独的 `>`，按 `Ctrl+C` 退出，再重输短命令。

## 已验证与限制

- 真机验证：Kindle 第 10 代入门版（J9G29R / KT4，固件 5.18.1），当时电脑是 macOS。
- 脚本只用 Python 标准库，macOS / Windows / Linux 通用，没有系统专属命令。
- Windows 侧未做真机验证；防火墙弹窗时选允许"专用网络"。
- 只建议在信任的家庭 Wi-Fi 内使用，不要把服务暴露到公网。

## 许可证

MIT
