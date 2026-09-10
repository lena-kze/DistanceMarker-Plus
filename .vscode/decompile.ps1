# decompile.ps1 - Holt die neueste DistanceMarker-Plus_*.wotmod aus /src/, entpackt sie nach /src/compiled/ und dekompiliert alle .pyc nach /src/decompiled/

# Uncompyle6 muss im PATH sein
$src = "${PSScriptRoot}\..\src"
$compiled = "$src\compiled"
$decompiled = "$src\decompiled"

# 1. Finde die neueste DistanceMarker-Plus_*.wotmod
$latestWotmod = Get-ChildItem -Path $src -Filter "DistanceMarker-Plus_*.wotmod" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($null -eq $latestWotmod) {
    Write-Host "[Fehler] Keine DistanceMarker-Plus_*.wotmod im src-Ordner gefunden!" -ForegroundColor Red
    exit 1
}
Write-Host "Gefundene WOTMOD: $($latestWotmod.Name)"

# 2. Leere compiled-Ordner
if (Test-Path $compiled) { Remove-Item "$compiled\*" -Recurse -Force }
else { New-Item -ItemType Directory -Path $compiled | Out-Null }

# 3. Entpacke WOTMOD nach compiled
& "C:\Program Files\WinRAR\WinRAR.exe" x -y $latestWotmod.FullName $compiled

# 4. Dekompiliere .pyc nach decompiled
uncompyle6.exe -r -o "$decompiled" "$compiled"

Write-Host ""
Write-Host "=============================="
Write-Host "Decompiling abgeschlossen!"
Write-Host "=============================="
Write-Host ""
