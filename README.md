evlc: VLC Commander for the Homelab
===================================

![
](https://raw.githubusercontent.com/Rad-nerd/evlc/refs/heads/main/logo.png)

A concise python based command-line tool to simplify controlling VLC (via `cvlc`) for displaying media on dedicated monitors or homelab screens. Perfect for quickly showing GIFs, photos, or videos with tailored VLC settings, and managing VLC processes with ease. It also provides commands to manage a Flask web interface for remote control.

* * *

✨ Features
----------

* **Effortless Media Playback:** Play GIFs, static images (photos), and videos with optimized `cvlc` flags for seamless, distraction-free display (e.g., `--no-osd`).
* **Universal Stop Command:** Instantly find and terminate _all_ running VLC (`vlc`) processes on your system, ensuring a clean slate whenever you need it.
* **Quick Status Check:** See at a glance if any `vlc` processes are currently running.
* **Web Server Management:** Easily start, stop, and check the status of the Flask web interface for remote control of VLC, running reliably in the background via `nohup`.
* **Quiet by Default:** Minimal output during normal operation for a clean console experience.
* **Debug Mode:** Use the `--debug` flag for verbose output, helpful for troubleshooting or understanding exactly what's happening under the hood.
* **Simplified Syntax:** Intuitive command structure (e.g., `evlc gif animation.gif` instead of lengthy `cvlc` commands).

* * *

🚀 Installation
---------------

`evlc` requires Python 3, VLC (specifically the `cvlc` command-line executable), `pgrep` (usually part of the `procps` package), and `unzip` to be installed on your Linux system.

### Prerequisites:

Before installing `evlc`, ensure these are available:

* **Python 3:** `python3`
* **VLC Media Player:** The command-line interface `cvlc` must be installed and accessible in your system's PATH.
* **pgrep:** Typically found in the `procps` package.
* **unzip:** For extracting the web interface files.

**Example for Debian/Ubuntu based systems:**

    sudo apt update
    sudo apt install python3 vlc procps unzip
    

### Automatic Installation (Recommended):

The easiest way to install `evlc` system-wide (to `/usr/local/bin/`) **and its web interface** is using the provided `install.sh` script.

#### Quick Install (One-Liner)

For a super fast installation, you can directly execute the `install.sh` script from GitHub:

    sudo curl -s https://raw.githubusercontent.com/Rad-nerd/evlc/main/install.sh | bash
    

_This command downloads the `install.sh` script from the `main` branch of the `Rad-nerd/evlc` repository and pipes it directly to `bash` for execution, using `sudo` to allow system-wide installation. No cloning needed!_

#### Standard Git Clone

Alternatively, if you prefer to clone the repository first:

    # 1. Clone the repository
    git clone https://github.com/Rad-nerd/evlc.git
    cd evlc
    
    # 2. Make the install script executable
    chmod +x install.sh
    
    # 3. Run the installer with sudo
    sudo ./install.sh
    

The `install.sh` script will handle checking for prerequisites, downloading the `evlc` command, **installing the web interface**, and setting up the command in `/usr/local/bin/`.

* * *

💡 Usage
--------

Once installed, you can simply run `evlc` from any terminal.

**Important Note:** Many `evlc` commands, especially those that manage system processes (like VLC or the web server) or write to system-level log/PID files, require elevated privileges. Therefore, it's often necessary to prefix your `evlc` commands with `sudo`.

### Play Media:

Specify the media format (`gif`, `photo`, or `video`) followed by the file path. `evlc` will automatically run `cvlc` in the background and detach it from your terminal.

* **Play a GIF:**
    
        sudo evlc gif /path/to/your/awesome_animation.gif
        
    
    *(Uses `cvlc` flags like `--demux=avformat --loop --no-osd --aspect-ratio 4:3 --crop=16:9`)*
    
* **Display a Photo:**
    
        sudo evlc photo /path/to/your/background_image.jpg
        
    
    *(Uses `cvlc` flags like `--play-and-pause --no-osd`)*
    
* **Play a Video:**
    
        sudo evlc video /path/to/your/looping_video.mp4
        
    
    *(Uses `cvlc` flags like `--loop --no-osd`)*
    

### Stop VLC:

To forcefully terminate all running `vlc` processes (any started by `evlc` or manually):

    sudo evlc stop
    

### Check VLC Status:

To quickly see if any `vlc` processes are currently running on your system:

    sudo evlc status
    

### Web Server Management:

The `evlc` script can also manage the Flask web interface, allowing you to start, stop, and check its status. The web server runs in the background using `nohup`.

* **Start the Web Server:**
    ```bash
    sudo evlc server start
    ```
    *(This will start the Flask application in the background, logging output to `/var/lib/evlcweb/evlcweb.log` and storing its PID in `/var/lib/evlcweb/evlcweb.pid`.)*

* **Stop the Web Server:**
    ```bash
    sudo evlc server stop
    ```
    *(This will attempt to gracefully stop the running web server process.)*

* **Check Web Server Status:**
    ```bash
    sudo evlc server status
    ```
    *(See if the web server is currently running and its PID.)*

### Debug Mode:

For more detailed output during execution, including the exact `cvlc` command being run or verbose status messages, simply add the `--debug` flag:

    sudo evlc video /path/to/test_video.mp4 --debug
    sudo evlc status --debug
    

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

* **Lucas** - Initial development and maintenance
