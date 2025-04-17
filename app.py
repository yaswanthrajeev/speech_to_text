from flask import Flask, request, jsonify, send_from_directory
import os
from utils.transcriber import transcribe_and_generate_srt
app=Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/api/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    srt_filename = filename.rsplit('.', 1)[0] + '.srt'
    srt_path = os.path.join(OUTPUT_FOLDER, srt_filename)

    # Your logic here
    transcribe_and_generate_srt(file_path, srt_path)

    return jsonify({
        'message': 'Transcription complete',
        'download_url': f'/api/download/{srt_filename}'
    }), 200

@app.route('/api/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)