#!/bin/bash

# --- Configuration ---
# REPLACE THIS WITH THE ACTUAL RAW URL TO YOUR 'evlc' SCRIPT ON GITHUB
EVLC_RAW_URL="https://raw.githubusercontent.com/Rad-nerd/evlc/refs/heads/main/evlc"
INSTALL_PATH="/usr/local/bin"
EVLC_COMMAND_NAME="evlc" # The name of the command once installed

# NEW CONFIGURATION FOR WEB INTERFACE INSTALLATION
EVLCWEB_REPO_ZIP_URL="https://github.com/Rad-nerd/evlc/archive/refs/heads/main.zip"
EVLCWEB_INSTALL_DIR="/var/lib/evlcweb"
TEMP_DOWNLOAD_DIR="/tmp/evlc_web_install_temp" # Temporary directory for downloading/extracting

# --- Script Logic ---

echo "--- Installing $EVLC_COMMAND_NAME Command and Web Interface ---"
echo "This script will download '$EVLC_COMMAND_NAME' from GitHub and install it to '$INSTALL_PATH'."
echo "It will also install the web interface to '$EVLCWEB_INSTALL_DIR'."

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script requires root privileges to install files to system directories."
  echo "Please run with sudo: sudo ./install.sh"
  exit 1
fi

# 1. Check for curl
echo "Checking for 'curl'..."
if ! command -v curl >/dev/null 2>&1; then
  echo "Error: 'curl' is required but not installed. Please install it (e.g., sudo apt install curl)."
  exit 1
fi

# 2. Check for python3
echo "Checking for 'python3'..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: 'python3' is required but not installed. Please install it."
  exit 1
fi

# 3. Check for cvlc (VLC)
echo "Checking for 'cvlc' (VLC media player)..."
if ! command -v cvlc >/dev/null 2>&1; then
  echo "Error: 'cvlc' (VLC media player) is required but not installed. Please install it (e.g., sudo apt install vlc-bin)." # vlc-bin or vlc depending on distro
  exit 1
fi

# 4. Check for pgrep
echo "Checking for 'pgrep'..."
if ! command -v pgrep >/dev/null 2>&1; then
  echo "Error: 'pgrep' is required but not installed. Please install it (e.g., sudo apt install procps)."
  exit 1
fi

# 5. Check for unzip (new dependency for web interface installation)
echo "Checking for 'unzip'..."
if ! command -v unzip >/dev/null 2>&1; then
  echo "Error: 'unzip' is required but not installed. Please install it (e.g., sudo apt install unzip)."
  exit 1
fi

# --- Install EVLC Command (as before) ---
echo "Creating command installation directory '$INSTALL_PATH' if it doesn't exist..."
sudo mkdir -p "$INSTALL_PATH"

echo "Downloading $EVLC_COMMAND_NAME from $EVLC_RAW_URL..."
if ! sudo curl -fLo "$INSTALL_PATH/$EVLC_COMMAND_NAME" "$EVLC_RAW_URL"; then
  echo "Error: Failed to download $EVLC_COMMAND_NAME. Check URL or network connection."
  sudo rm -f "$INSTALL_PATH/$EVLC_COMMAND_NAME"
  exit 1
fi
echo "Making $EVLC_COMMAND_NAME executable..."
sudo chmod +x "$INSTALL_PATH/$EVLC_COMMAND_NAME"

# --- Install EVLC Web Interface ---
echo "Preparing web interface installation directory '$EVLCWEB_INSTALL_DIR'..."
# Remove existing directory to ensure a clean install, then create it
sudo rm -rf "$EVLCWEB_INSTALL_DIR"
sudo mkdir -p "$EVLCWEB_INSTALL_DIR"

echo "Downloading web interface repository from $EVLCWEB_REPO_ZIP_URL..."
# Create temporary directory for download and extraction
mkdir -p "$TEMP_DOWNLOAD_DIR"
if ! curl -fLo "$TEMP_DOWNLOAD_DIR/repo.zip" "$EVLCWEB_REPO_ZIP_URL"; then
  echo "Error: Failed to download web interface repository. Check URL or network connection."
  rm -rf "$TEMP_DOWNLOAD_DIR"
  exit 1
fi

echo "Extracting web interface files..."
if ! unzip -q "$TEMP_DOWNLOAD_DIR/repo.zip" -d "$TEMP_DOWNLOAD_DIR"; then
  echo "Error: Failed to extract web interface files."
  rm -rf "$TEMP_DOWNLOAD_DIR"
  exit 1
fi

# The zip file extracts to a folder named 'evlc-main' (based on the branch name)
EXTRACTED_SOURCE_DIR="$TEMP_DOWNLOAD_DIR/evlc-main/evlcweb"
if [ ! -d "$EXTRACTED_SOURCE_DIR" ]; then
  echo "Error: Expected directory '$EXTRACTED_SOURCE_DIR' not found after extraction. The repository structure might have changed."
  rm -rf "$TEMP_DOWNLOAD_DIR"
  exit 1
fi

echo "Copying web interface files to '$EVLCWEB_INSTALL_DIR'..."
# Copy contents (not the folder itself) from the extracted 'evlcweb' to the target directory
if ! sudo cp -r "$EXTRACTED_SOURCE_DIR/." "$EVLCWEB_INSTALL_DIR/"; then
  echo "Error: Failed to copy web interface files."
  rm -rf "$TEMP_DOWNLOAD_DIR"
  exit 1
fi

echo "Cleaning up temporary files..."
rm -rf "$TEMP_DOWNLOAD_DIR"

echo "--- Installation Complete! ---"
echo "$EVLC_COMMAND_NAME has been successfully installed to '$INSTALL_PATH'."
echo "The web interface has been installed to '$EVLCWEB_INSTALL_DIR'."
echo "You can now typically run the web application (e.g., using 'python3 $EVLCWEB_INSTALL_DIR/app.py')."
echo "You can also use the command line tool directly:"
echo "  $EVLC_COMMAND_NAME status"
echo "  $EVLC_COMMAND_NAME -h"

exit 0
