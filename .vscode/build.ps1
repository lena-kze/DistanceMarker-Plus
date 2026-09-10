# build.ps1 - Komplettes Build-Skript für DistanceMarker-Plus WOT Mod

$SchrittCount = 10

# 1. Unpack latest WOTMOD
Write-Host "`nSchritt [1/$SchrittCount]: Unpack latest WOTMOD"
# Find latest DistanceMarker-Plus*.wotmod in src folder
$srcDir = Join-Path $PSScriptRoot "..\src"
$latestSrcWotmod = Get-ChildItem -Path $srcDir -Filter "DistanceMarker-Plus*.wotmod" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($null -eq $latestSrcWotmod) {
    Write-Host "[Fehler] Keine DistanceMarker-Plus*.wotmod Datei im src-Ordner gefunden!" -ForegroundColor Red
    exit 1
}
Write-Host "Gefundene DistanceMarker WOTMOD: $($latestSrcWotmod.Name)"
& "C:\Program Files\WinRAR\WinRAR.exe" x -y $latestSrcWotmod.FullName "${PSScriptRoot}\..\interim\"


# 2. Import AS in SWF
Write-Host "`nSchritt [2/$SchrittCount]: Import AS in SWF"
& "C:\Program Files (x86)\FFDec\ffdec.bat" -importScript "${PSScriptRoot}\..\interim\res\gui\flash\DistanceMarkerFlash.swf" "${PSScriptRoot}\..\interim\res\gui\flash\DistanceMarkerFlash_modified.swf" "${PSScriptRoot}\..\modified\scripts"

# 3. Replace SWF in interim
Write-Host "`nSchritt [3/$SchrittCount]: Replace SWF in interim"
Copy-Item "${PSScriptRoot}\..\interim\res\gui\flash\DistanceMarkerFlash_modified.swf" "${PSScriptRoot}\..\interim\res\gui\flash\DistanceMarkerFlash.swf" -Force

# 4. Compile all Python files in modified/zip/res
Write-Host "`nSchritt [4/$SchrittCount]: Compile all Python files in modified/zip/res"
$compileResult = py -2.7 -m compileall "${PSScriptRoot}\..\modified\zip\res" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host $compileResult
}

# 5. Copy all files from modified/zip/res to interim/res
Write-Host "`nSchritt [5/$SchrittCount]: Copy all compiled files from modified/zip/res to interim/res"
Copy-Item "${PSScriptRoot}\..\modified\zip\res\*" "${PSScriptRoot}\..\interim\res\" -Recurse -Force

# 6. Repack latest DistanceMarker.wotmod
Write-Host "`nSchritt [6/$SchrittCount]: Repack latest DistanceMarker.wotmod"
$oldDir = Get-Location
Set-Location "${PSScriptRoot}\..\interim"
$buildDir = Join-Path $PSScriptRoot "..\build"
$newWotmodName = $latestSrcWotmod.Name
$newWotmodPath = Join-Path $buildDir $newWotmodName
& "C:\Program Files\WinRAR\WinRAR.exe" a -afzip -m0 -ibck -r $newWotmodPath "meta.xml" "res\"
Set-Location $oldDir

# 7. Copy latest DistanceMarker.wotmod to Custom_mods
Write-Host "`nSchritt [7/$SchrittCount]: Copy latest DistanceMarker.wotmod to Custom_mods"
Copy-Item $newWotmodPath "J:\Wargaming\World_of_Tanks_EU\Aslain_Modpack\Custom_mods\mods\version" -Force

# 8. Copy latest DistanceMarker.wotmod to latest mods version folder
Write-Host "`nSchritt [8/$SchrittCount]: Copy latest DistanceMarker.wotmod to latest mods version folder"
# Find latest version folder in mods directory
$modsRoot = "J:\Wargaming\World_of_Tanks_EU\mods\"
$latestVersionFolder = Get-ChildItem -Path $modsRoot -Directory | Where-Object { $_.Name -match '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' } | Sort-Object Name -Descending | Select-Object -First 1
if ($null -eq $latestVersionFolder) {
    Write-Host "[Fehler] Kein Versionsordner im mods-Verzeichnis gefunden!" -ForegroundColor Red
    exit 1
}
$modsVersionDir = $latestVersionFolder.FullName
Write-Host "Kopiere $newWotmodName nach $modsVersionDir"
Copy-Item $newWotmodPath $modsVersionDir -Force

# 9. Delete modified SWF
Write-Host "`nSchritt [9/$SchrittCount]: Delete modified SWF"
Remove-Item "${PSScriptRoot}\..\interim\res\gui\flash\DistanceMarkerFlash_modified.swf" -Force

# 10. Clear python.log
Write-Host "`nSchritt [10/$SchrittCount]: Clear python.log"
$pythonLog = "J:\Wargaming\World_of_Tanks_EU\python.log"
if (Test-Path $pythonLog) {
    Clear-Content $pythonLog
} else {
    Write-Host "python.log nicht gefunden, überspringe Clear-Content."
}

Write-Host ""
Write-Host "=============================="
Write-Host "Build abgeschlossen!"
Write-Host "=============================="
Write-Host ""
