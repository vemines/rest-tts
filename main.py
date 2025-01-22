
from flask import Flask, request, jsonify, make_response
import os
import hashlib
import re

from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from gtts import gTTS
import edge_tts

app = Flask(__name__)
Compress(app)

# Initialize Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"], 
    storage_uri="memory://"
)

async def gtts_audio(text, lang='en', locale=None):
    output_folder = "output/gtts"
    os.makedirs(output_folder, exist_ok=True)
    # Generate a unique filename based on the text content and other parameters
    hash_string = f"{text}{lang}{locale if locale else ''}"
    hashed_text = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    file_path = f"{output_folder}/{hashed_text}.mp3"

    try:
        if locale:
            tts = gTTS(text=text, lang=lang, tld=locale)
        else:
            tts = gTTS(text=text, lang=lang)
        tts.save(file_path)
        return file_path

    except Exception as e:
        print(f"Error generating Google TTS: {e}")
        return None

async def etts_audio(text, voice='en-US-BrianNeural', volume="+0%", rate="+0%", pitch="+0Hz"):
    output_folder = "output/etts"
    os.makedirs(output_folder, exist_ok=True)
    # Generate a unique filename based on the text content and other parameters
    hash_string = f"{text}{voice}{volume}{rate}{pitch}"
    hashed_text = hashlib.md5(hash_string.encode('utf-8')).hexdigest()
    file_path = f"{output_folder}/{hashed_text}.mp3"

    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate, volume=volume, pitch=pitch)
        with open(file_path, "wb") as f:
           # Iterate over audio data chunks from the edge-tts stream
           async for chunk in communicate.stream():
              # Check if the chunk is of type audio
              if chunk["type"] == "audio":
                # Write the audio chunk data to the output file
                f.write(chunk["data"])

        return file_path

    except Exception as e:
        print(f"Error generating Edge TTS: {type(e)} - {e}")
        return None

@app.route('/gtts', methods=['POST'])
@limiter.limit("10 per minute")
async def gtts_endpoint():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request body'}), 400

        text = data['text']
        lang = data.get('lang', 'en')  # Default to 'en' if not provided
        locale = data.get('locale')

        if not text or not isinstance(text, str) or not lang or not isinstance(lang, str) :
            return jsonify({'error': 'Invalid value type on \"text\" or \"lang\" parameter'}), 400

        if locale and not isinstance(locale, str):
             return jsonify({'error': 'Invalid value type on \"locale\" parameter'}), 400

        output_file_path = await gtts_audio(text, lang, locale)

        if output_file_path:
            return jsonify({'audio_path': output_file_path}), 200
        else:
            return jsonify({'error': 'Failed to generate TTS audio'}), 500

    except Exception as e:
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.route('/etts', methods=['POST'])
@limiter.limit("10 per minute")
async def etts_endpoint():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text in request body'}), 400

        text = data['text']
        voice = data.get('voice', 'en-US-BrianNeural')
        volume = data.get('volume', "+0%")
        speed = data.get('speed', "+0%")
        pitch = data.get('pitch', "+0Hz")

        # VALID_VOICES = ['en-US-BrianNeural', 'en-US-JennyNeural', 'en-GB-RyanNeural']
        # if voice not in VALID_VOICES:
        #     return jsonify({'error': f'Invalid voice option: {voice}. Must be one of {VALID_VOICES}'}), 400

        if not re.match(r"^[\+\-]\d{1,3}%$", volume):
            return jsonify({'error': 'Invalid volume format. Must be like "+10%" or "-5%"'}), 400
        if not re.match(r"^[\+\-]\d{1,3}%$", speed):
            return jsonify({'error': 'Invalid speed format. Must be like "+10%" or "-5%"'}), 400
        if not re.match(r"^[\+\-]?\d+(\.\d+)?Hz$", pitch):
            return jsonify({'error': 'Invalid pitch format. Must be like "+10Hz", "-5Hz", "+30Hz" or "-12.5Hz"'}), 400

        output_file_path = await etts_audio(text, voice, volume, speed, pitch)

        if output_file_path:
            return jsonify({'audio_path': output_file_path}), 200
        else:
            return jsonify({'error': 'Failed to generate TTS audio'}), 500

    except Exception as e:
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify({'error': 'Too many requests'}), 429)


if __name__ == '__main__':
    os.makedirs("output", exist_ok=True)
    app.run(debug=True, port=5000)
    print("Server in runing at port 5000")