#!/bin/bash

# --- Configuration ---
# REPLACE THIS WITH THE ACTUAL RAW URL TO YOUR 'evlc' SCRIPT ON GITHUB
EVLC_RAW_URL="https://raw.githubusercontent.com/Rad-nerd/evlc/refs/heads/main/evlc"
INSTALL_PATH="/usr/local/bin"
EVLC_COMMAND_NAME="evlc" # The name of the command once installed

# --- Script Logic ---

echo "--- Installing $EVLC_COMMAND_NAME Command ---"
echo "This script will download '$EVLC_COMMAND_NAME' from GitHub and install it to '$INSTALL_PATH'."

# Check for root privileges if installing to a system directory
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script requires root privileges to install to '$INSTALL_PATH'."
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

# 5. Create the installation directory if it doesn't exist
echo "Creating installation directory '$INSTALL_PATH' if it doesn't exist..."
sudo mkdir -p "$INSTALL_PATH"

# 6. Download the evlc script
echo "Downloading $EVLC_COMMAND_NAME from $EVLC_RAW_URL..."
# -f: Fail silently (no HTML output on HTTP errors)
# -L: Follow redirects
# -o: Write to file instead of stdout
if ! sudo curl -fLo "$INSTALL_PATH/$EVLC_COMMAND_NAME" "$EVLC_RAW_URL"; then
  echo "Error: Failed to download $EVLC_COMMAND_NAME. Check URL or network connection."
  # Clean up partial download if any
  sudo rm -f "$INSTALL_PATH/$EVLC_COMMAND_NAME"
  exit 1
fi

# 7. Make the script executable
echo "Making $EVLC_COMMAND_NAME executable..."
sudo chmod +x "$INSTALL_PATH/$EVLC_COMMAND_NAME"

echo "--- Installation Complete! ---"
echo "$EVLC_COMMAND_NAME has been successfully installed to '$INSTALL_PATH'."
echo "You can now use the command directly:"
echo "  $EVLC_COMMAND_NAME status"
echo "  $EVLC_COMMAND_NAME gif /path/to/your/file.gif"

exit 0
