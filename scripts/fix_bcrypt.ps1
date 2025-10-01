# Fix bcrypt/passlib installation and enable UTF-8 output in PowerShell
# Run this in PowerShell (as your project environment):
# .\scripts\fix_bcrypt.ps1

Write-Host "1) Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host "2) Reinstalling bcrypt and passlib..."
python -m pip install --force-reinstall --no-cache-dir bcrypt passlib

Write-Host "3) Optional: set PowerShell to use UTF-8 for console output"
Write-Host "   (you can instead run: chcp 65001)"
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "Done. Try running your app again: uvicorn app.main:app --reload"