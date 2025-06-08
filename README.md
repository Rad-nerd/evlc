evlc: VLC Commander for the Homelab
===================================

A concise command-line tool to simplify controlling VLC (via `cvlc`) for displaying media on dedicated monitors or homelab screens. Perfect for quickly showing GIFs, photos, or videos with tailored VLC settings, and managing VLC processes with ease.

* * *

✨ Features
----------

*   **Effortless Media Playback:** Play GIFs, static images (photos), and videos with optimized `cvlc` flags for seamless, distraction-free display (e.g., `--no-osd`).
*   **Universal Stop Command:** Instantly find and terminate _all_ running VLC (`vlc`) processes on your system, ensuring a clean slate whenever you need it.
*   **Quick Status Check:** See at a glance if any `vlc` processes are currently running.
*   **Quiet by Default:** Minimal output during normal operation for a clean console experience.
*   **Debug Mode:** Use the `--debug` flag for verbose output, helpful for troubleshooting or understanding exactly what's happening under the hood.
*   **Simplified Syntax:** Intuitive command structure (e.g., `evlc gif animation.gif` instead of lengthy `cvlc` commands).

* * *

🚀 Installation
---------------

`evlc` requires Python 3, VLC (specifically the `cvlc` command-line executable), and `pgrep` (which is usually part of the `procps` package) to be installed on your Linux system.

### Prerequisites:

Before installing `evlc`, ensure these are available:

*   **Python 3:** `python3`
*   **VLC Media Player:** The command-line interface `cvlc` must be installed and accessible in your system's PATH.
*   **pgrep:** Typically found in the `procps` package.

**Example for Debian/Ubuntu based systems:**

    sudo apt update
    sudo apt install python3 vlc procps
    

### Automatic Installation (Recommended):

The easiest way to install `evlc` system-wide (to `/usr/local/bin/`) is using the provided `install.sh` script.

#### Quick Install (One-Liner)

For a super fast installation, you can directly execute the `install.sh` script from GitHub:

    sudo bash -c "$(wget -qO- [https://raw.githubusercontent.com/Rad-nerd/evlc/main/install.sh](https://raw.githubusercontent.com/Rad-nerd/evlc/main/install.sh))"
    

_This command downloads the `install.sh` script from the `main` branch of the `Rad-nerd/evlc` repository and pipes it directly to `bash` for execution, using `sudo` to allow system-wide installation. No cloning needed!_

#### Standard Git Clone

Alternatively, if you prefer to clone the repository first:

    # 1. Clone the repository
    git clone [https://github.com/Rad-nerd/evlc.git](https://github.com/Rad-nerd/evlc.git) # <--- This is your actual repo URL!
    cd evlc
    
    # 2. Make the install script executable
    chmod +x install.sh
    
    # 3. Run the installer with sudo
    sudo ./install.sh
    

The `install.sh` script will handle checking for prerequisites, downloading the `evlc` command, and setting it up in `/usr/local/bin/`.

* * *

💡 Usage
--------

Once installed, you can simply run `evlc` from any terminal.

### Play Media:

Specify the media format (`gif`, `photo`, or `video`) followed by the file path. `evlc` will automatically run `cvlc` in the background and detach it from your terminal.

*   **Play a GIF:**
    
        evlc gif /path/to/your/awesome_animation.gif
        
    
    \*(Uses `cvlc` flags like `--demux=avformat --loop --no-osd --aspect-ratio 4:3 --crop=16:9`)\*
    
*   **Display a Photo:**
    
        evlc photo /path/to/your/background_image.jpg
        
    
    \*(Uses `cvlc` flags like `--play-and-pause --no-osd`)\*
    
*   **Play a Video:**
    
        evlc video /path/to/your/looping_video.mp4
        
    
    \*(Uses `cvlc` flags like `--loop --no-osd`)\*
    

### Stop VLC:

To forcefully terminate all running `vlc` processes (any started by `evlc` or manually):

    evlc stop
    

### Check VLC Status:

To quickly see if any `vlc` processes are currently running on your system:

    evlc status
    

### Debug Mode:

For more detailed output during execution, including the exact `cvlc` command being run or verbose status messages, simply add the `--debug` flag:

    evlc video /path/to/test_video.mp4 --debug
    evlc status --debug
    

* * *

🤝 Contributing
---------------

Contributions are highly welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-awesome-feature`).
3.  Make your changes.
4.  Commit your changes with a clear message (`git commit -m 'feat: Add a new command to...'`).
5.  Push to the branch (`git push origin feature/your-awesome-feature`).
6.  Open a Pull Request.

* * *

📄 License
----------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

* * *

👨‍💻 Author
------------

*   **Lucas** - Initial development and maintenance
