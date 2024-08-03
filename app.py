from flask import Flask, request, jsonify, render_template
import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)

    language = request.form.get('language', 'en-US')  # Default to English if not specified

    try:
        audio_path = extract_audio(video_path)
        transcription = transcribe_audio(audio_path, language)
    finally:
        # Ensure resources are released and files are deleted
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return jsonify({'transcription': transcription})


def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.replace('.mp4', '.wav')
    video.audio.write_audiofile(audio_path)
    video.close()  # Explicitly close the video file
    return audio_path


def transcribe_audio(audio_path, language):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            transcription = "Could not understand audio"
        except sr.RequestError:
            transcription = "Could not request results"
    return transcription


if __name__ == '__main__':
    app.run(debug=True)
