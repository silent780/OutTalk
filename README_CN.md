# OutTalk 🎙️

基于 Microsoft Edge TTS 服务的文字转语音桌面应用程序。

[English](README.md) | 中文文档

## ✨ 功能特点

- 🗣️ 使用 Edge TTS 进行文字转语音
- 🌎 支持多种语音和语言选择
- 🔄 支持 MP3 转 WAV 格式转换
- 🖥️ 简洁直观的操作界面

## 🚀 安装说明

1. 确保已安装 Python 3.7 或更高版本
2. 克隆此仓库：
```bash
git clone https://github.com/silent780/OutTalk.git
cd OutTalk
```

3. 安装必需的依赖包：
```bash
pip install -r requirements.txt
```

## 📖 使用方法

1. 运行程序：
```bash
python app.py
```

2. 点击"浏览"按钮选择输出目录
3. 在文本框中输入或粘贴需要转换的文字
4. 选择想要的语音和语速设置
5. 点击"生成"按钮生成 MP3 文件
6. 如有需要，可以点击"转换为 WAV"按钮进行格式转换

## 📦 依赖项

- ⚡ edge-tts：用于文字转语音功能
- 🎵 pydub：用于音频格式转换
- 🎨 tkinter：GUI界面框架（Python自带）
- 🎞️ ffmpeg：音频处理工具（仓库中已包含）

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 💝 致谢

- [edge-tts](https://github.com/rany2/edge-tts) - 本项目主要基于 edge-tts 库实现，该库提供了访问 Microsoft Edge TTS 服务的接口。感谢他们出色的工作使这项服务能够通过 Python 轻松使用。
- 感谢所有为 edge-tts 项目做出贡献的开发者。

## 🤝 参与贡献

欢迎提交问题反馈和功能请求！