from flask_cors import CORS
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from video_processing import *
from audio_processing import *
import os
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)

video_model = tf.keras.models.load_model('../models/video_model.h5')

audio_model = tf.keras.models.load_model('../models/audio_model.h5')

UPLOAD_FOLDER = '../uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/predictVideo', methods=['POST'])
def predictVideo():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(video.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    try:

        process_video(video_path)

        video_name = os.path.splitext(os.path.basename(video_path))[0]
        frames_folder = os.path.join(os.path.dirname(video_path), video_name, video_name)

        frames = extract_and_preprocess_frames(frames_folder)

        predictions = video_model.predict(frames)

        predicted_emotion = np.argmax(predictions)

        emotion_to_integer = {
            0: 'angry',
            1: 'disgust',
            2: 'fear',
            3: 'happy',
            4: 'neutral',
            5: 'sad',
            6: 'surprised'
        }

        predicted_label = emotion_to_integer.get(predicted_emotion, 'unknown')

        clear_upload_folder(UPLOAD_FOLDER)

        return jsonify({'emotion': predicted_label})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predictAudio', methods=['POST'])
def predictAudio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    if audio.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(audio.filename)
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio.save(audio_path)

    audio_features = process_audio(audio_path)

    audio_features = audio_features.reshape(1, -1)

    predictions = audio_model.predict(audio_features)

    predicted_emotion = np.argmax(predictions)

    emotion_to_integer = {
        0: 'angry',
        1: 'disgust',
        2: 'fear',
        3: 'happy',
        4: 'neutral',
        5: 'sad',
        6:'surprised'
    }

    predicted_label = emotion_to_integer.get(predicted_emotion, 'unknown')
    
    clear_upload_folder(UPLOAD_FOLDER)

    return jsonify({'emotion': predicted_label})

if __name__ == '__main__':
    app.run(debug=True, port=5000)