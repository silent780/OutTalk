# OutTalk 🎙️

A simple GUI application for text-to-speech conversion using Microsoft Edge's TTS service.

[中文文档](README_CN.md) | English

## ✨ Features

- 🗣️ Text to speech conversion using Edge TTS
- 🌎 Support for multiple voices and languages
- 🔄 MP3 to WAV format conversion
- 🖥️ Simple and intuitive interface

## 🚀 Installation

1. Make sure you have Python 3.7+ installed
2. Clone this repository:
```bash
git clone https://github.com/silent780/OutTalk.git
cd OutTalk
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## 📖 Usage

1. Run the application:
```bash
python app.py
```

2. Select output directory using "Browse" button
3. Enter or paste your text in the text area
4. Choose desired voice and speed settings
5. Click "Generate" to create MP3 file
6. Use "Convert to WAV" if needed

## 📦 Dependencies

- ⚡ edge-tts
- 🎵 pydub
- 🎨 tkinter (included with Python)
- 🎞️ ffmpeg (included in repository)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💝 Acknowledgments

- [edge-tts](https://github.com/rany2/edge-tts) - This project relies heavily on the edge-tts library, which provides access to Microsoft Edge's TTS service. Thanks to their excellent work in making this service accessible through Python.
- Thanks to all the contributors who have helped improve edge-tts.

## 🤝 Contributing

Contributions, issues and feature requests are welcome!