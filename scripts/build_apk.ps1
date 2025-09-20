# Build APK for the Kivy app using WSL Ubuntu-22.04
# This PowerShell wrapper calls the WSL bash script and streams logs to the console.

param(
    [string]$Distro = "Ubuntu-22.04"
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path $ProjectRoot ".." | Resolve-Path
$BashScript = Join-Path $ProjectRoot "scripts/build_apk_wsl.sh"

if (-not (Test-Path $BashScript)) {
    Write-Error "Bash script not found: $BashScript"
    exit 1
}

Write-Host "[INFO] Project root: $ProjectRoot"
Write-Host "[INFO] Using WSL distribution: $Distro"
Write-Host "[STEP] Invoking WSL build script..."

# Map Windows path to WSL path (robustly derive drive and rest)
$projPathStr = $ProjectRoot.Path
$bashPathStr = $BashScript

$projDrive = ([System.IO.Path]::GetPathRoot($projPathStr)).Substring(0,1).ToLower()
$projRest  = $projPathStr.Substring(2) -replace "\\","/"
$WSLProjectPath = "/mnt/$projDrive$projRest"

$bashDrive = ([System.IO.Path]::GetPathRoot($bashPathStr)).Substring(0,1).ToLower()
$bashRest  = $bashPathStr.Substring(2) -replace "\\","/"
$WSLBashPath = "/mnt/$bashDrive$bashRest"

wsl -d $Distro -- bash -lc "chmod +x '$WSLBashPath' && '$WSLBashPath'"

$BinDir = Join-Path $ProjectRoot "bin"
$LatestApk = Get-ChildItem -Path $BinDir -Filter "*-debug.apk" -Recurse -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($LatestApk) {
    Write-Host "[SUCCESS] APK built: $($LatestApk.FullName)"
} else {
    Write-Warning "[WARN] APK not found in bin/. Check scripts/build_apk_wsl.sh log under bin/."
}
