# Outputs environment info in JSON for AI consumption
# Detect Python executable (prefers Windows launcher `py`)
$python = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
  $python = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
  $python = "python"
} else {
  Write-Error "Python not found in PATH. Please install Python or add it to PATH."
  exit 1
}

# Ensure pip exists (bootstrap if necessary)
try {
  & $python -m pip -V | Out-Null
} catch {
  try { & $python -m ensurepip --upgrade | Out-Null } catch {}
}

# Collect Python version and executable path
$pythonVersion = & $python -c "import sys; print(sys.version.split()[0])"
$pythonExec = & $python -c "import sys; print(sys.executable)"

# Collect installed packages (pip freeze)
$freezeOutput = @()
try {
  $freezeOutput = & $python -m pip freeze
} catch {
  $freezeOutput = @()
}

# Parse packages into name/version pairs
$packages = @()
foreach ($line in $freezeOutput) {
  if ($line -match '^[A-Za-z0-9_.-]+==') {
    $parts = $line.Split('==', 2)
    $packages += [PSCustomObject]@{
      name    = $parts[0]
      version = $parts[1]
    }
  }
}

# Compose JSON result
$result = [PSCustomObject]@{
  python_version    = $pythonVersion
  python_executable = $pythonExec
  packages          = $packages
}

$result | ConvertTo-Json -Depth 5
