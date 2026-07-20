$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Virtual environment missing. Follow the setup commands in README.md."
}
Set-Location -LiteralPath $PSScriptRoot
& $python app.py
