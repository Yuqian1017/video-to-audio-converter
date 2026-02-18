from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os
import uuid
import threading
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024  # 2GB max

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    while True:
        time.sleep(3600)  # Check every hour
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    filepath = os.path.join(folder, f)
                    if os.path.isfile(filepath):
                        if time.time() - os.path.getmtime(filepath) > 3600:
                            try:
                                os.remove(filepath)
                            except:
                                pass

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert/upload', methods=['POST'])
def convert_upload():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    # Generate unique filename
    unique_id = str(uuid.uuid4())
    original_ext = file.filename.rsplit('.', 1)[1].lower()
    input_filename = f"{unique_id}.{original_ext}"
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)

    # Save uploaded file
    file.save(input_path)

    # Convert to audio
    output_format = request.form.get('format', 'mp3')
    output_filename = f"{unique_id}.{output_format}"
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        result = convert_video_to_audio(input_path, output_path, output_format)
        if result['success']:
            # Clean up input file
            os.remove(input_path)
            return jsonify({
                'success': True,
                'download_id': unique_id,
                'format': output_format,
                'filename': f"audio.{output_format}"
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/convert/url', methods=['POST'])
def convert_url():
    data = request.get_json()
    url = data.get('url')
    output_format = data.get('format', 'mp3')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    unique_id = str(uuid.uuid4())
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}.%(ext)s")

    try:
        # Download video using yt-dlp
        download_cmd = [
            'yt-dlp',
            '-f', 'bestaudio/best',
            '-o', input_path,
            '--no-playlist',
            '--no-check-certificates',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--extractor-args', 'bilibili:quality=bestaudio',
            '-x',  # Extract audio directly
            url
        ]

        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            error_msg = result.stderr[-500:] if result.stderr else 'Unknown error'
            print(f"yt-dlp error: {error_msg}")
            return jsonify({'error': f'下载失败: {error_msg[:200]}'}), 400

        # Find the downloaded file
        downloaded_file = None
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            if f.startswith(unique_id):
                downloaded_file = os.path.join(app.config['UPLOAD_FOLDER'], f)
                break

        if not downloaded_file:
            return jsonify({'error': 'Download failed'}), 500

        # Convert to audio
        output_filename = f"{unique_id}.{output_format}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        convert_result = convert_video_to_audio(downloaded_file, output_path, output_format)

        # Clean up downloaded file
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)

        if convert_result['success']:
            return jsonify({
                'success': True,
                'download_id': unique_id,
                'format': output_format,
                'filename': f"audio.{output_format}"
            })
        else:
            return jsonify({'error': convert_result['error']}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Download timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def has_audio_stream(input_path):
    """Check if video has audio stream"""
    try:
        result = subprocess.run(
            ['ffprobe', '-i', input_path, '-show_streams', '-select_streams', 'a', '-loglevel', 'error'],
            capture_output=True, text=True, timeout=30
        )
        return 'codec_name' in result.stdout
    except:
        return True  # Assume has audio if check fails

def convert_video_to_audio(input_path, output_path, output_format):
    """Convert video file to audio using ffmpeg"""
    try:
        # Check if video has audio
        if not has_audio_stream(input_path):
            return {'success': False, 'error': '该视频没有音频轨道，无法转换'}

        cmd = ['ffmpeg', '-i', input_path, '-vn', '-y']

        if output_format == 'mp3':
            cmd.extend(['-acodec', 'libmp3lame', '-ab', '192k'])
        elif output_format == 'wav':
            cmd.extend(['-acodec', 'pcm_s16le'])
        elif output_format == 'aac':
            cmd.extend(['-acodec', 'aac', '-ab', '192k'])
        elif output_format == 'flac':
            cmd.extend(['-acodec', 'flac'])
        elif output_format == 'ogg':
            cmd.extend(['-acodec', 'libvorbis', '-ab', '192k'])

        cmd.append(output_path)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0 and os.path.exists(output_path):
            return {'success': True}
        else:
            return {'success': False, 'error': 'Conversion failed'}

    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Conversion timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/download/<download_id>/<format>')
def download(download_id, format):
    filename = f"{download_id}.{format}"
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)

    if os.path.exists(filepath):
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"audio.{format}"
        )
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
