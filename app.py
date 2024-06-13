from flask import Flask, request, jsonify, render_template
from music import get_songs_from_playlist
from huggingface_hub import InferenceClient
from flask_cors import CORS
from PIL import Image
import os
import io
import base64
from dotenv import load_dotenv
import time
from requests.exceptions import HTTPError

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS
hf = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_songs', methods=['POST'])
def get_songs():
    try:
        data = request.json
        playlist_url = data.get('playlist_url')
        if not playlist_url:
            return jsonify({'error': 'No playlist URL provided'}), 400

        songs = get_songs_from_playlist(playlist_url)
        return jsonify({'songs': songs})
    except Exception as e:
        app.logger.error("Error occurred in /get_songs: %s", e)
        return jsonify({'error': str(e)}), 500

@app.route('/generate_image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        playlist_url = data.get('playlist_url')
        if not playlist_url:
            return jsonify({'error': 'No playlist URL provided'}), 400

        songs = get_songs_from_playlist(playlist_url)
        song_titles = ", ".join(songs)

        retries = 3
        for i in range(retries):
            try:
                # Ensure we correctly pass the prompt
                result = hf.text_to_image(model="CiroN2022/cd-md-music", prompt=f"The image is a playlist cover of objects that encapsulate the vibe and aesthetic of the following songs: {song_titles}. ")

                # Check the structure of the result
                if isinstance(result, Image.Image):
                    image = result
                else:
                    app.logger.error("Unexpected response format: %s", result)
                    return jsonify({'error': 'Unexpected response format from Hugging Face API'}), 500

                # Convert image to base64 for web display
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                return jsonify({'image': img_str})
            except HTTPError as http_err:
                if http_err.response.status_code == 500:
                    if i < retries - 1:
                        wait_time = 2 ** i
                        app.logger.warning(f"Server error, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        app.logger.error("Error occurred in /generate_image: %s", http_err)
                        return jsonify({'error': 'Server error, please try again later.'}), 500
                elif http_err.response.status_code == 429:
                    if i < retries - 1:
                        wait_time = 2 ** i
                        app.logger.warning(f"Rate limit hit, retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        app.logger.error("Rate limit exceeded: %s", http_err)
                        return jsonify({'error': 'Rate limit exceeded, please try again later.'}), 429
                else:
                    app.logger.error("Error occurred in /generate_image: %s", http_err)
                    return jsonify({'error': str(http_err)}), http_err.response.status_code
            except Exception as e:
                app.logger.error("Error occurred in /generate_image: %s", e)
                return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error("Error occurred in /generate_image: %s", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
