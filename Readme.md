# Text-to-Speech API

This project provides a simple Text-to-Speech (TTS) API using Flask.

## Installation

To set up the project, you need to install python and the required packages. Run the following command: `pip install requirements.txt`

## Local Debug mode

To start project at local. Run the following command: `py main.py` or `main_nolimit.py` (no rate limit)

## API Endpoint

### `POST /gtts`

Google Text-to-Speech (gTTS). This endpoint generates audio from the provided text.

#### Request Body

The request should be a JSON object with the following fields:

- `text` (string, required): The text to convert to speech.
- `lang` (string, optional): The language code (default is 'en').
- `locale` (string, optional): The locale code.

#### Locale When Duplicate `lang`

| Local Accent              | lang  | locale |
| ------------------------- | ----- | ------ |
| English (Australia)       | en    | com.au |
| English (United Kingdom)  | en    | co.uk  |
| English (United States)   | en    | us     |
| English (Canada)          | en    | ca     |
| English (India)           | en    | co.in  |
| English (Ireland)         | en    | ie     |
| English (South Africa)    | en    | co.za  |
| English (Nigeria)         | en    | com.ng |
| French (Canada)           | fr    | ca     |
| French (France)           | fr    | fr     |
| Mandarin (China Mainland) | zh-CN | any    |
| Mandarin (Taiwan)         | zh-TW | any    |
| Portuguese (Brazil)       | pt    | com.br |
| Portuguese (Portugal)     | pt    | pt     |
| Spanish (Mexico)          | es    | com.mx |
| Spanish (Spain)           | es    | es     |
| Spanish (United States)   | es    | us     |

### `POST /etts`

Edge Text-to-Speech (edge-TTS). This endpoint generates audio from the provided text.

#### Request Body

The request should be a JSON object with the following fields:

- `text` (string, required): The text to convert to speech.
- `voice` (string, required): The voice output.
- `volume` (string, optional): Modify volumn of audio. ex: "+30%", "-10%"
- `speed` (string, optional): Modify Speed of audio. ex: "+30%", "-10%"
- `pitch` (string, optional): Modify Pitch of audio. ex: "+5Hz", "-15.5Hz"

#### [Watch list of Voices](edge-tts-voice.md)
