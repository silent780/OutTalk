# OutTalk

A simple GUI application for text-to-speech conversion using Microsoft Edge's TTS service.

## Features

- Text to speech conversion using Edge TTS
- Support for multiple voices and languages
- MP3 to WAV format conversion
- Simple and intuitive interface

## Installation

1. Make sure you have Python 3.7+ installed
2. Clone this repository:
```bash
git clone https://github.com/yourusername/OutTalk.git
cd OutTalk
```

3. Install required packages:
```bash
pip install -r requirements.txt
```
## Usage

1. run app
```bash
python app.py
```

2.Select output directory using "Browse" button
3.Enter or paste your text in the text area
4.Choose desired voice and speed settings
5.Click "Generate" to create MP3 file
6.Use "Convert to WAV" if needed

## Dependencies
edge-tts
pydub
tkinter (included with Python)
ffmpeg (included in repository)

## License
This project is licensed under the MIT License - see the LICENSE file for details.