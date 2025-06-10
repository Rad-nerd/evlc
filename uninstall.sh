#!/bin/bash

# --- Configuration ---
INSTALL_PATH="/usr/local/bin"
EVLC_COMMAND_NAME="evlc"
EVLCWEB_INSTALL_DIR="/var/lib/evlcweb"

# --- Script Logic ---

echo "--- Uninstalling $EVLC_COMMAND_NAME Command and Web Interface ---"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script requires root privileges to uninstall system files."
  echo "Please run with sudo: sudo ./uninstall.sh"
  exit 1
fi

# 1. Stop any running web server (if it exists)
echo "Attempting to stop the EVLC web server..."
# Try to use the installed evlc command to stop the server
if command -v "$INSTALL_PATH/$EVLC_COMMAND_NAME" >/dev/null 2>&1; then
    sudo "$INSTALL_PATH/$EVLC_COMMAND_NAME" server stop
else
    echo "EVLC command not found, cannot gracefully stop server via evlc. Manual check might be needed."
    # Fallback: if evlc command is not found, try to find and kill based on PID file directly
    if [ -f "$EVLCWEB_INSTALL_DIR/evlcweb.pid" ]; then
        PID_TO_KILL=$(cat "$EVLCWEB_INSTALL_DIR/evlcweb.pid")
        if ps -p "$PID_TO_KILL" > /dev/null; then
            echo "Attempting to kill web server PID $PID_TO_KILL manually..."
            sudo kill -SIGTERM "$PID_TO_KILL" || sudo kill -SIGKILL "$PID_TO_KILL" # Try SIGTERM, then SIGKILL
        else
            echo "Stale PID file found for PID $PID_TO_KILL, process not running. Removing PID file."
        fi
        sudo rm -f "$EVLCWEB_INSTALL_DIR/evlcweb.pid" # Always remove PID file if found
    else
        echo "No web server PID file found."
    fi
fi


# 2. Stop any running VLC processes managed by evlc
echo "Attempting to stop all VLC processes..."
# Try to use the installed evlc command to stop VLC
if command -v "$INSTALL_PATH/$EVLC_COMMAND_NAME" >/dev/null 2>&1; then
    sudo "$INSTALL_PATH/$EVLC_COMMAND_NAME" stop
else
    # Fallback: if evlc command is already removed or not found, use pgrep
    echo "EVLC command not found, cannot gracefully stop VLC. Searching for 'vlc' processes with pgrep..."
    if command -v pgrep >/dev/null 2>&1; then
        PIDS_TO_KILL=$(pgrep vlc)
        if [ -n "$PIDS_TO_KILL" ]; then
            echo "Found VLC PIDs: $PIDS_TO_KILL. Attempting to kill..."
            sudo kill -SIGTERM $PIDS_TO_KILL || sudo kill -SIGKILL $PIDS_TO_KILL # Try SIGTERM, then SIGKILL
        else
            echo "No 'vlc' processes found by pgrep."
        fi
    else
        echo "pgrep not found. Cannot automatically stop VLC processes. Manual intervention might be needed."
    fi
fi

# 3. Remove the evlc command executable
echo "Removing $INSTALL_PATH/$EVLC_COMMAND_NAME..."
if [ -f "$INSTALL_PATH/$EVLC_COMMAND_NAME" ]; then
  sudo rm -f "$INSTALL_PATH/$EVLC_COMMAND_NAME"
  echo "$EVLC_COMMAND_NAME removed successfully."
else
  echo "$EVLC_COMMAND_NAME not found in $INSTALL_PATH. Already uninstalled or never installed there."
fi

# 4. Remove the web interface directory
echo "Removing web interface directory $EVLCWEB_INSTALL_DIR..."
if [ -d "$EVLCWEB_INSTALL_DIR" ]; then
  sudo rm -rf "$EVLCWEB_INSTALL_DIR"
  echo "Web interface directory removed successfully."
else
  echo "Web interface directory $EVLCWEB_INSTALL_DIR not found. Already uninstalled or never installed."
fi

echo "--- Uninstallation Complete! ---"
echo "You may need to manually remove any lingering log files (e.g., evlcweb.log) if they were created outside of $EVLCWEB_INSTALL_DIR."

exit 0
