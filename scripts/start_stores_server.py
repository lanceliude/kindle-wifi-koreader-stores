#!/usr/bin/env python3
"""Start a local Wi-Fi installer server for KOReader plugin stores on a jailbroken Kindle.

The proven path is: this computer serves a plugin bundle over the LAN; kTerm on the Kindle
downloads and runs the installer. No USB cable and no `;kpm add-repo` long-URL command are needed.
"""

from __future__ import annotations

import json
import socket
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUILD = SKILL_ROOT / "build"
PREFERRED_PORTS = [8000, 8080, 8001, 9000, 9090]

PLUGINS = [
    {
        "name": "AppStore",
        "dir": "appstore.koplugin",
        "release_api": "https://api.github.com/repos/omer-faruq/appstore.koplugin/releases/latest",
        "fallback": "https://github.com/omer-faruq/appstore.koplugin/releases/download/v1.14.0/appstore.koplugin.zip",
        "asset_keyword": "appstore",
    },
    {
        "name": "Kaou Market",
        "dir": "komarket.koplugin",
        "release_api": "https://api.github.com/repos/Exhen/komarket-public/releases/latest",
        "fallback": "https://github.com/Exhen/komarket-public/releases/download/v0.5.1/komarket.koplugin-v0.5.1.zip",
        "asset_keyword": "komarket",
    },
]

BUNDLE_NAME = "stores.tar.gz"

INSTALLER = """#!/bin/sh
BASE="${1:-__BASE_URL__}"
ROOT="${INSTALLER_ROOT:-/mnt/us}"
DEST="$ROOT/koreader/plugins"
PKG="$ROOT/.stores.tar.gz"

echo "== KOReader stores Wi-Fi installer =="
echo "Server: $BASE"
echo "Stores: AppStore + Kaou Market (komarket)"

if [ ! -d "$ROOT/koreader" ]; then
  echo "ERROR: KOReader folder not found at $ROOT/koreader. Install KOReader first."
  exit 1
fi

mkdir -p "$DEST"

fetch_file() {
  url="$1"
  out="$2"
  if command -v wget >/dev/null 2>&1; then
    wget -qO "$out" "$url"
  elif command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$out" "$url"
  else
    echo "ERROR: neither wget nor curl is available in this shell."
    exit 3
  fi
}

echo "Downloading stores.tar.gz ..."
fetch_file "$BASE/stores.tar.gz" "$PKG"

if [ ! -s "$PKG" ]; then
  echo "ERROR: download failed. Check Wi-Fi and that the local computer server is still running."
  exit 4
fi

echo "Replacing old store plugins ..."
rm -rf "$DEST/appstore.koplugin" "$DEST/komarket.koplugin"

if command -v tar >/dev/null 2>&1; then
  TAR_BIN="tar"
elif [ -x "$ROOT/koreader/tar" ]; then
  TAR_BIN="$ROOT/koreader/tar"
else
  echo "ERROR: tar was not found."
  exit 5
fi

echo "Extracting into $DEST ..."
"$TAR_BIN" -xzf "$PKG" -C "$DEST"

ok=1
for d in appstore.koplugin komarket.koplugin; do
  if [ ! -f "$DEST/$d/main.lua" ]; then
    echo "ERROR: $d/main.lua is missing after extraction."
    ok=0
  fi
done

if [ "$ok" -ne 1 ]; then
  exit 6
fi

rm -f "$PKG"
echo
echo "OK: AppStore installed to $DEST/appstore.koplugin"
echo "OK: Kaou Market installed to $DEST/komarket.koplugin"
echo "Next: fully exit KOReader, reopen it, then enable both stores in"
echo "  Menu -> Plugins -> Plugin Management"
exit 0
"""


def lan_ip() -> str:
    """Return the outbound LAN IPv4 without OS-specific ifconfig/ipconfig calls."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()
    if ip.startswith("169.254."):
        return "127.0.0.1"
    return ip


def latest_release_url(plugin: dict) -> str:
    req = urllib.request.Request(
        plugin["release_api"], headers={"User-Agent": "kindle-wifi-stores-skill"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.endswith(".zip") and plugin["asset_keyword"] in name.lower():
                return asset["browser_download_url"]
    except Exception:
        pass
    return plugin["fallback"]


def build_bundle() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    out_tar = BUILD / BUNDLE_NAME

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        with tarfile.open(out_tar, "w:gz") as tar:
            for plugin in PLUGINS:
                zip_name = f"{plugin['dir']}.zip"
                zip_path = BUILD / zip_name
                url = latest_release_url(plugin)
                print(f"Downloading {plugin['name']} release: {url}")
                urllib.request.urlretrieve(url, zip_path)

                extract_root = tmp / plugin["dir"]
                extract_root.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(extract_root)

                candidates = list(extract_root.glob(f"**/{plugin['dir']}"))
                if not candidates:
                    raise SystemExit(f"{plugin['name']} zip did not contain {plugin['dir']}.")
                plugin_dir = candidates[0]
                tar.add(plugin_dir, arcname=plugin["dir"])

    print(f"Built {out_tar} ({out_tar.stat().st_size} bytes)")


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        path = path.split("?", 1)[0]
        return str(BUILD / path.lstrip("/"))

    def do_GET(self):
        route = self.path.split("?", 1)[0]
        if route in ("/g", "/g.sh"):
            host = self.headers.get("Host", "").strip()
            base = f"http://{host}" if host else f"http://{lan_ip()}"
            body = INSTALLER.replace("__BASE_URL__", base).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/x-sh; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("[stores-install] %s - %s\n" % (self.address_string(), fmt % args))


def bind() -> ThreadingHTTPServer:
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        return ThreadingHTTPServer(("0.0.0.0", port), Handler)
    for port in PREFERRED_PORTS:
        try:
            return ThreadingHTTPServer(("0.0.0.0", port), Handler)
        except OSError:
            continue
    return ThreadingHTTPServer(("0.0.0.0", 0), Handler)


if __name__ == "__main__":
    build_bundle()
    httpd = bind()
    port = httpd.server_address[1]
    ip = lan_ip()
    print("==============================")
    print(f" KOReader Stores Wi-Fi installer on port {port}")
    print("==============================")
    print("Put the Kindle and this computer on the same Wi-Fi network.")
    print("In kTerm on the Kindle, run:")
    print(f"  wget -qO- http://{ip}:{port}/g | sh")
    print("If wget is missing or fails, run:")
    print(f"  curl -fsSL http://{ip}:{port}/g | sh")
    print("\nClose this window to stop the server.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
