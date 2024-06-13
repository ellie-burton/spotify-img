from flask import Flask, request, jsonify, render_template
from music import get_songs_from_playlist
from flask_cors import CORS
import os
import io
import base64
from dotenv import load_dotenv
import time
from requests.exceptions import HTTPError
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key)

def generate_relevant_objects(song_titles):
    # Placeholder: Replace with actual logic to generate relevant objects
    return ["object1", "object2", "object3", "object4", "object5"]

def generate_emotional_descriptors(song_titles):
    # Placeholder: Replace with actual logic to generate emotional descriptors
    return ["happy", "sad", "exciting", "calm", "nostalgic"]

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
            app.logger.error('No playlist URL provided')
            return jsonify({'error': 'No playlist URL provided'}), 400

        app.logger.info('Fetching songs from playlist')
        songs = get_songs_from_playlist(playlist_url)
        song_titles = ", ".join(songs)

        app.logger.info('Generating relevant objects and emotional descriptors')
        objects = generate_relevant_objects(song_titles)
        descriptors = generate_emotional_descriptors(song_titles)

        prompt = f"The image is a playlist cover of objects that encapsulate the vibe and aesthetic of the following songs: {song_titles}. Relevant objects: {', '.join(objects)}. Emotional descriptors: {', '.join(descriptors)}."

        app.logger.info('Calling OpenAI DALL-E API with prompt')
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        if response.data:
            image_url = response.data[0].url
            return jsonify({'image_url': image_url})
        else:
            app.logger.error("Unexpected response format from OpenAI DALL-E API")
            return jsonify({'error': 'Unexpected response format from OpenAI DALL-E API'}), 500

    except HTTPError as http_err:
        app.logger.error("HTTP error occurred: %s", http_err)
        return jsonify({'error': str(http_err)}), 500
    except Exception as e:
        app.logger.error("Error occurred in /generate_image: %s", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
