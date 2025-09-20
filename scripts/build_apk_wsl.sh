#!/usr/bin/env bash
set -euo pipefail

# Build APK for Kivy app using Buildozer inside WSL Ubuntu
# This script installs prerequisites (user-local when possible) and builds a debug APK.

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/bin"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/buildozer_wsl_build.log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "[INFO] Project directory: $PROJECT_DIR"
echo "[INFO] Log file: $LOG_FILE"

# Ensure Java and system packages are present (requires sudo once)
echo "[STEP] Installing system prerequisites (git, openjdk-17, build tools)"
sudo apt-get update -y
sudo apt-get install -y git zip unzip openjdk-17-jdk python3 python3-pip python3-venv libffi-dev libssl-dev build-essential

# Ensure Python tooling and Buildozer are installed for the current user
export PATH="$HOME/.local/bin:$PATH"

echo "[STEP] Upgrading pip/setuptools/wheel and installing buildozer + cython (user install)"
python3 -m pip install --user --upgrade pip setuptools wheel
python3 -m pip install --user --upgrade cython buildozer

# Print versions for diagnostics
echo "[INFO] java version: $(java -version 2>&1 | head -n1)"
echo "[INFO] python version: $(python3 -V)"
echo "[INFO] buildozer version: $(buildozer --version || echo 'not found')"

cd "$PROJECT_DIR"

echo "[STEP] Building debug APK (this will download Android SDK/NDK on first run and can take a while)"
buildozer -v android debug

APK_PATH=$(ls -1 "$PROJECT_DIR"/bin/*-debug.apk 2>/dev/null | tail -n1 || true)
if [[ -n "${APK_PATH}" ]]; then
  echo "[SUCCESS] APK built: ${APK_PATH}"
else
  echo "[WARN] APK not found in bin/. Check the log at: $LOG_FILE"
  exit 1
fi
