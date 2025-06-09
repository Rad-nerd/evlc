# app.py (Updated: Automatic media type detection based on file extension)

from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
from werkzeug.utils import secure_filename # For secure file naming

app = Flask(__name__)

# --- Configuration ---
# Set the path to your evlc script.
# If evlc is installed in /usr/local/bin (system-wide), you can just use 'evlc'.
# Otherwise, provide the full path to your evlc executable.
EVLC_PATH = 'evlc'

# Configuration for file uploads
# IMPORTANT: This directory will be created in the same folder as app.py
UPLOAD_FOLDER = 'uploaded_media'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'gif', 'jpg', 'jpeg', 'png', 'webp'} # Ensure these match your evlc capabilities

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload folder: {UPLOAD_FOLDER}")

# Global variable to store the path of the currently playing uploaded file
current_uploaded_file = None

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if a file's extension is in the allowed list."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_media_type_from_extension(filename):
    """Determines media type (gif, photo, video) based on file extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext == 'gif':
        return 'gif'
    elif ext in {'jpg', 'jpeg', 'png', 'webp'}:
        return 'photo'
    elif ext in {'mp4', 'avi', 'mkv'}:
        return 'video'
    return 'unknown' # Should not happen if allowed_file is checked first

# --- Routes ---

@app.route('/')
def index():
    """Renders the main page with control buttons."""
    return render_template('index.html')

@app.route('/command/<action>', methods=['POST'])
def handle_command(action):
    """Handles commands sent from the web UI (only 'stop' action remains here)."""
    global current_uploaded_file # Declare global to modify the variable

    if action == 'stop':
        try:
            # First, tell evlc to stop any current playback
            result = subprocess.run([EVLC_PATH, 'stop'], check=True, capture_output=True, text=True)
            print(f"evlc stop output: {result.stdout.strip()}")
            if result.stderr:
                print(f"evlc stop error: {result.stderr.strip()}")

            # Now, attempt to delete the uploaded file if one was playing
            if current_uploaded_file and os.path.exists(current_uploaded_file):
                os.remove(current_uploaded_file)
                print(f"Deleted uploaded file: {current_uploaded_file}")
                current_uploaded_file = None # Clear the tracker
            else:
                print("No active uploaded file to delete, or file not found.")

        except subprocess.CalledProcessError as e:
            print(f"Error running evlc stop command: {e}")
            print(f"Stdout: {e.stdout.strip()}")
            print(f"Stderr: {e.stderr.strip()}")
        except FileNotFoundError:
            print(f"Error: evlc command not found at {EVLC_PATH}. Please ensure 'evlc' is in your system's PATH or provide the full path.")
        except Exception as e:
            print(f"An unexpected error occurred during stop or file deletion: {e}")

    return redirect(url_for('index')) # Always redirect back to the main page

@app.route('/upload_and_play', methods=['POST'])
def upload_and_play():
    """Handles file uploads, saves them, and initiates playback."""
    global current_uploaded_file # Declare global to modify the variable

    if 'uploaded_file' not in request.files:
        print("No file part in the request.")
        return redirect(url_for('index'))

    file = request.files['uploaded_file']
    if file.filename == '':
        print("No selected file.")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        try:
            file.save(filepath)
            print(f"File uploaded successfully to: {filepath}")
        except Exception as e:
            print(f"Error saving file: {e}")
            return redirect(url_for('index'))

        # Before playing new uploaded file, ensure old one is deleted
        if current_uploaded_file and os.path.exists(current_uploaded_file):
            try:
                os.remove(current_uploaded_file)
                print(f"Deleted previous uploaded file: {current_uploaded_file}")
            except Exception as e:
                print(f"Error deleting old uploaded file: {e}")
        
        # Set the global tracker to the newly uploaded file's path for future deletion
        current_uploaded_file = filepath

        # Automatically determine media type based on the file extension
        media_type = get_media_type_from_extension(filename)
        print(f"Automatically determined media type: {media_type}")

        # Play the file using evlc with the automatically determined media_type
        try:
            result = subprocess.run([EVLC_PATH, media_type, filepath], check=True, capture_output=True, text=True)
            print(f"Playing uploaded file (Type: {media_type}): {filepath}")
            print(f"evlc play output: {result.stdout.strip()}")
            if result.stderr:
                print(f"evlc play error: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Error playing uploaded file with evlc: {e}")
            print(f"Stdout: {e.stdout.strip()}")
            print(f"Stderr: {e.stderr.strip()}")
            # If playback fails immediately, delete the file
            if current_uploaded_file and os.path.exists(current_uploaded_file):
                try:
                    os.remove(current_uploaded_file)
                    current_uploaded_file = None
                    print(f"Deleted uploaded file due to playback error: {filepath}")
                except Exception as e_del:
                    print(f"Error deleting file after playback error: {e_del}")
        except FileNotFoundError:
            print(f"Error: evlc command not found at {EVLC_PATH}. Please ensure 'evlc' is in your system's PATH or provide the full path.")

    else:
        print(f"File type not allowed or no file selected for upload.")

    return redirect(url_for('index'))

# --- Run the App ---
if __name__ == '__main__':
    # Run in debug mode for development. Set debug=False for production.
    # host='0.0.0.0' makes it accessible from other devices on your network.
    app.run(debug=True, host='0.0.0.0')