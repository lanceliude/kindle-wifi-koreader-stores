$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

try {
    python "scripts\start_stores_server.py"
} catch {
    python3 "scripts\start_stores_server.py"
}

Read-Host "Press Enter to close"
