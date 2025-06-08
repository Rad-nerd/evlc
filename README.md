# evlc: VLC Commander for the Homelab

A concise command-line tool to simplify controlling VLC (via `cvlc`) for displaying media on dedicated monitors or homelab screens. Perfect for quickly showing GIFs, photos, or videos with tailored VLC settings, and managing VLC processes with ease.

---

## ✨ Features

* **Effortless Media Playback:** Play GIFs, static images (photos), and videos with optimized `cvlc` flags for seamless, distraction-free display (e.g., `--no-osd`).
* **Universal Stop Command:** Instantly find and terminate *all* running VLC (`vlc`) processes on your system, ensuring a clean slate whenever you need it.
* **Quick Status Check:** See at a glance if any `vlc` processes are currently running.
* **Quiet by Default:** Minimal output during normal operation for a clean console experience.
* **Debug Mode:** Use the `--debug` flag for verbose output, helpful for troubleshooting or understanding exactly what's happening under the hood.
* **Simplified Syntax:** Intuitive command structure (e.g., `evlc gif animation.gif` instead of lengthy `cvlc` commands).

---

## 🚀 Installation

`evlc` requires Python 3, VLC (specifically the `cvlc` command-line executable), and `pgrep` (which is usually part of the `procps` package) to be installed on your Linux system.

### Prerequisites:

Before installing `evlc`, ensure these are available:

* **Python 3:** `python3`
* **VLC Media Player:** The command-line interface `cvlc` must be installed and accessible in your system's PATH.
* **pgrep:** Typically found in the `procps` package.

**Example for Debian/Ubuntu based systems:**
```bash
sudo apt update
sudo apt install python3 vlc procps
