import subprocess
import os
import argparse
import time
import signal
from flask import Flask, request, jsonify, render_template, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import glob # To find media files in folders

app = Flask(__name__)
# Replace with a strong, random secret key in a production environment
app.secret_key = 'your_super_secret_key_here' 

# Configuration for file uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'gif', 'jpg', 'jpeg', 'png', 'webp', 'mov'} # Added .mov

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables to manage VLC state and playlist
# These are re-introduced to support the playlist features in the provided HTML
vlc_status = {
    "is_playing": False,
    "current_media": None,
    "media_type": None
}
current_playlist = []
current_playlist_index = -1 # -1 means no playlist active or not started yet

# Helper function to infer media type from file extension
def infer_media_type(filepath):
    extension = filepath.rsplit('.', 1)[1].lower()
    if extension in {'mp4', 'avi', 'mkv', 'mov'}:
        return 'video'
    elif extension in {'jpg', 'jpeg', 'png', 'webp'}:
        return 'photo'
    elif extension == 'gif':
        return 'gif'
    else:
        return 'video' # Default or fallback

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _execute_evlc_command(command_parts):
    """
    Executes a command using the evlc script and returns its output.
    """
    try:
        # Assuming 'evlc' is in the system's PATH or in the same directory
        result = subprocess.run(['evlc'] + command_parts, capture_output=True, text=True, check=True)
        app.logger.info(f"evlc command: {' '.join(['evlc'] + command_parts)}")
        app.logger.info(f"evlc stdout: {result.stdout.strip()}")
        if result.stderr:
            app.logger.error(f"evlc stderr: {result.stderr.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Error executing evlc command: {e}")
        app.logger.error(f"Command stderr: {e.stderr.strip()}")
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        app.logger.error("evlc command not found. Make sure it's installed and in your system's PATH.")
        return "Error: 'evlc' command not found."


def _play_media_with_evlc(media_path, media_type):
    """
    Helper function to play media using the evlc script.
    Updates the global vlc_status.
    """
    global vlc_status

    if not os.path.exists(media_path):
        vlc_status['is_playing'] = False
        vlc_status['current_media'] = None
        vlc_status['media_type'] = None
        return f"Error: File not found at {media_path}"

    # Stop any currently playing media before starting a new one
    _execute_evlc_command(['stop'])
    time.sleep(1) # Give VLC a moment to terminate

    command_parts = [media_type, media_path]

    response = _execute_evlc_command(command_parts)

    if "Error" not in response:
        vlc_status['is_playing'] = True
        vlc_status['current_media'] = media_path
        vlc_status['media_type'] = media_type
        return f"Playing {media_type}: {os.path.basename(media_path)}"
    else:
        vlc_status['is_playing'] = False
        vlc_status['current_media'] = None
        vlc_status['media_type'] = None
        return response


@app.route('/')
def index():
    # Pass playlist status to the template for conditional rendering
    is_playlist_active = bool(current_playlist) and current_playlist_index != -1
    return render_template('index.html', is_playlist_active=is_playlist_active)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


@app.route('/play_media', methods=['POST'])
def play_media():
    global current_playlist, current_playlist_index
    
    file = request.files.get('uploaded_file')
    server_file_path = request.form.get('server_file_path')
    
    media_to_play = None
    media_type = None
    message = "No media selected."

    # Handle file upload first
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        media_to_play = filepath
        media_type = infer_media_type(filepath)
        message = f"Uploaded and attempting to play: {filename}"
        
    # If no file uploaded, check for server path
    elif server_file_path:
        media_to_play = server_file_path
        media_type = infer_media_type(server_file_path) # Infer type for server path
        message = f"Attempting to play from server path: {server_file_path}"
    
    if media_to_play:
        # Clear playlist state when a single file is played (either uploaded or server path)
        current_playlist = []
        current_playlist_index = -1
        
        playback_message = _play_media_with_evlc(media_to_play, media_type)
        if "Error" in playback_message:
            flash(f"Error: {playback_message}", 'error')
        else:
            flash(f"Success: {playback_message}", 'success')
    else:
        flash(message, 'warning')
            
    return redirect(url_for('index'))


@app.route('/play_folder_playlist', methods=['POST'])
def play_folder_playlist():
    global current_playlist, current_playlist_index
    
    folder_path = request.form.get('folder_path')

    if not folder_path:
        flash("Error: No folder path provided.", 'error')
        return redirect(url_for('index'))

    if not os.path.isdir(folder_path):
        flash(f"Error: Folder not found or is not a directory: {folder_path}", 'error')
        return redirect(url_for('index'))

    # Build playlist from files in the folder
    playlist_items = []
    for ext in ALLOWED_EXTENSIONS:
        # Use glob to find files matching extensions within the folder
        for f in glob.glob(os.path.join(folder_path, f'*.{ext}')):
            playlist_items.append({'path': f, 'type': infer_media_type(f)})
    
    # Sort for consistent playback order
    playlist_items.sort(key=lambda x: x['path'])

    if not playlist_items:
        flash(f"No supported media files found in folder: {folder_path}", 'warning')
        current_playlist = []
        current_playlist_index = -1
        return redirect(url_for('index'))

    current_playlist = playlist_items
    current_playlist_index = 0

    first_item = current_playlist[current_playlist_index]
    playback_message = _play_media_with_evlc(first_item['path'], first_item['type'])
    
    if "Error" in playback_message:
        flash(f"Error starting playlist: {playback_message}", 'error')
    else:
        flash(f"Playlist started. Now playing: {os.path.basename(first_item['path'])}", 'success')

    return redirect(url_for('index'))


@app.route('/next_playlist_item', methods=['POST'])
def next_playlist_item():
    global current_playlist, current_playlist_index

    if not current_playlist:
        flash("No active playlist to advance.", 'warning')
        return redirect(url_for('index'))

    current_playlist_index = (current_playlist_index + 1) % len(current_playlist)
    next_item = current_playlist[current_playlist_index]

    playback_message = _play_media_with_evlc(next_item['path'], next_item['type'])
    if "Error" in playback_message:
        flash(f"Error playing next item: {playback_message}", 'error')
    else:
        flash(f"Next item: {os.path.basename(next_item['path'])}", 'info')
    
    return redirect(url_for('index'))


@app.route('/command/stop', methods=['POST'])
def stop_media():
    global vlc_status, current_playlist, current_playlist_index
    response = _execute_evlc_command(['stop'])
    
    # Reset playlist state on stop
    current_playlist = []
    current_playlist_index = -1

    if "Error" not in response:
        vlc_status['is_playing'] = False
        vlc_status['current_media'] = None
        vlc_status['media_type'] = None
        flash("Media playback stopped.", 'success')
    else:
        flash(f"Failed to stop media: {response}", 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')