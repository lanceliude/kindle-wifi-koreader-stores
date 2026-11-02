# Kindle 端已验证操作步骤

以下步骤已在已越狱、已安装 KOReader 的 Kindle Basic 3 / J9G29R 上验证通过。

## 前置条件

- Kindle 已经越狱。
- KOReader 已经安装。
- KPM 可用。
- Kindle 和用户电脑连接同一个 Wi-Fi。
- 电脑能够访问 GitHub，以下载 AppStore 和卡欧市场的发布包。

## 在电脑上启动本地服务

运行技能自带脚本，脚本会打印需要在 Kindle 上输入的准确命令。

```bash
python3 scripts/start_stores_server.py
```

Windows PowerShell 使用：

```powershell
python scripts\start_stores_server.py
```

如果 Windows 防火墙弹出提示，允许在专用网络下访问。

## 在 Kindle 上安装 kTerm

部分设备的 KOReader 菜单里找不到内置终端，因此使用官方独立终端 kTerm。

1. 回到 Kindle 首页图书馆。
2. 打开搜索框。
3. 输入：

```text
;kpm install kterm
```

4. 等待 KPM 安装完成。
5. 从 Kindle 首页图书馆打开 kTerm。

## 在 kTerm 中执行安装命令

严格使用电脑脚本打印出来的命令，格式类似：

```sh
wget -qO- http://192.168.1.50:8000/g | sh
```

如果 `wget` 不存在或执行失败，再使用：

```sh
curl -fsSL http://192.168.1.50:8000/g | sh
```

安装成功时会看到：

```text
OK: AppStore installed to /mnt/us/koreader/plugins/appstore.koplugin
OK: Kaou Market installed to /mnt/us/koreader/plugins/komarket.koplugin
```

## 启用两个商店

1. 完全退出 KOReader。
2. 重新打开 KOReader。
3. 进入：

```text
菜单 → 插件 → 插件管理
```

4. 勾选启用 AppStore 和卡欧市场。
5. 之后其他 KOReader 插件都可以在这两个商店内部搜索安装。

## 不要重试这些已验证失败的路线

- `;kpm add-repo http://<电脑IP>:<端口>/` 在这台设备上会闪回主页，不要重试。
- Kindle 原生浏览器不能直接选择插件目录，也不能自动解压插件。
- 在 Kindle 端输入带变量、括号的长命令，容易触发 `>` 续行提示。
