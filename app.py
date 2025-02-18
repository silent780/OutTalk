import asyncio
import edge_tts
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import platform
import sys
import warnings

# 在最开始就设置警告过滤
warnings.filterwarnings('ignore')
# 特别针对 pydub 的警告
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', message='Couldn\'t find ffmpeg or avconv')

# 设置环境变量
if getattr(sys, 'frozen', False):
    ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg')
else:
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg')
os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']

import pydub

class VoiceGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("语音生成器")
        self.root.geometry("600x400")
        self.setup_ffmpeg_path()
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # 设置工作目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            application_path = os.path.dirname(os.path.abspath(__file__))
            
        # 改变工作目录
        os.chdir(application_path)
        
        # 默认输出目录改为桌面
        default_output = os.path.join(os.path.expanduser('~'), 'Desktop', 'voice_output')
        
        # 文本输入区域
        ttk.Label(main_frame, text="需要生成的音频内容:").grid(row=0, column=0, sticky=tk.W)
        self.text_input = tk.Text(main_frame, height=5, width=50)
        self.text_input.grid(row=1, column=0, columnspan=2, pady=5)
        self.text_input.insert('1.0', "你好，我是语音助手")  # 默认文本

        # 语速选择
        ttk.Label(main_frame, text="语速:").grid(row=2, column=0, sticky=tk.W)
        self.speed = ttk.Entry(main_frame, width=20)
        self.speed.insert(0, "+0%")  # 默认语速
        self.speed.grid(row=2, column=1, sticky=tk.W, pady=5)

        # 音色选择
        ttk.Label(main_frame, text="音色:").grid(row=3, column=0, sticky=tk.W)
        self.voice = ttk.Combobox(main_frame, width=40)
        self.voice['values'] = ["en-US-AndrewMultilingualNeural",
                                "en-US-AvaMultilingualNeural",
                                "en-US-BrianMultilingualNeural",
                                "en-US-EmmaMultilingualNeural",
                                "zh-CN-XiaoxiaoNeural",
                                "zh-CN-XiaoyiNeural",
                                "zh-CN-YunjianNeural",
                                "zh-CN-YunxiNeural",
                                "zh-CN-YunxiaNeural",
                                "zh-CN-YunyangNeural",
                                "zh-CN-liaoning-XiaobeiNeural",
                                "zh-CN-shaanxi-XiaoniNeural",]  # 默认音色列表
        self.voice.set('en-US-EmmaMultilingualNeural')  # 默认音色
        self.voice.grid(row=3, column=1, sticky=tk.W, pady=5)

        # 输出目录选择
        ttk.Label(main_frame, text="保存目录:").grid(row=4, column=0, sticky=tk.W)
        self.output_dir = ttk.Entry(main_frame, width=40)
        self.output_dir.grid(row=4, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="浏览...", command=self.browse_directory).grid(row=4, column=2, pady=5)

        # 生成按钮
        self.generate_btn = ttk.Button(main_frame, text="生成语音", command=self.generate_voice)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=20)

        # 状态标签
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=6, column=0, columnspan=3)
        
        # 调整 macOS 上的界面样式
        if platform.system() == "Darwin":
            self.root.tk.call('tk', 'scaling', 2.0)  # 调整 macOS 上的界面缩放
        
                # 添加一条分割线
        ttk.Separator(main_frame, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky='ew', pady=10)
        
        # 添加 MP3 转 WAV 功能区
        ttk.Label(main_frame, text="MP3转WAV功能:").grid(row=8, column=0, sticky=tk.W)
        self.convert_btn = ttk.Button(main_frame, text="转换MP3为WAV", command=self.convert_to_wav)
        self.convert_btn.grid(row=8, column=1, pady=10)
        
        # 转换状态标签
        self.convert_status_label = ttk.Label(main_frame, text="")
        self.convert_status_label.grid(row=9, column=0, columnspan=3)
        self.output_dir.insert(0, default_output)
    
    def setup_ffmpeg_path(self):
        """设置 ffmpeg 环境"""
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                ffmpeg_path = os.path.join(base_path, 'ffmpeg')
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
                ffmpeg_path = os.path.join(base_path, 'ffmpeg')

            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
            ffprobe_exe = os.path.join(ffmpeg_path, 'ffprobe.exe')
            
            if not os.path.exists(ffmpeg_exe) or not os.path.exists(ffprobe_exe):
                self.status_label.config(text="警告: ffmpeg 文件不完整")
                return

            os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ['PATH']
        except Exception as e:
            self.status_label.config(text=f"设置 ffmpeg 失败: {str(e)}")


    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.delete(0, tk.END)
            self.output_dir.insert(0, directory)
    def mp3_to_wav(self, file_path):
        try:
            sound = pydub.AudioSegment.from_mp3(file_path)
            sound.export(file_path.replace("mp3", "wav"), format="wav")
        except Exception as e:
            if "FileNotFoundError" in str(e):
                error_msg = "错误：找不到 ffmpeg，请确保程序完整性"
            elif "decoder" in str(e):
                error_msg = f"错误：解码失败，ffmpeg路径: {os.environ['PATH']}"
            else:
                error_msg = f"错误：{str(e)}\nffmpeg路径: {os.environ['PATH']}"
            self.status_label.config(text=error_msg)
            raise Exception(error_msg)
            
    def batch_mp3_to_wav(self, folder_path):
        # 获取MP3文件夹的父目录
        parent_dir = os.path.dirname(folder_path)
        # 在父目录下创建WAV文件夹
        wav_folder = os.path.join(parent_dir, "WAV")
        os.makedirs(wav_folder, exist_ok=True)
        
        success_count = 0
        fail_count = 0
        
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                mp3_path = os.path.join(folder_path, file)
                wav_path = os.path.join(wav_folder, file.replace(".mp3", ".wav"))
                try:
                    # 使用pydub直接导出到WAV文件夹
                    sound = pydub.AudioSegment.from_mp3(mp3_path)
                    sound.export(wav_path, format="wav")
                    success_count += 1
                    self.convert_status_label.config(text=f"正在转换: {file}")
                    self.root.update()  # 更新界面显示
                except Exception as e:
                    fail_count += 1
                    error_msg = f"转换失败: {mp3_path}\n"
                    error_msg += f"错误: {str(e)}\n"
                    error_msg += f"ffmpeg路径: {os.environ['PATH']}\n"
                    error_msg += f"当前工作目录: {os.getcwd()}"
                    print(error_msg)
                    self.convert_status_label.config(text=f"转换失败，详细信息请查看控制台")
        
        return success_count, fail_count
    
    def convert_to_wav(self):
        base_folder = self.output_dir.get()
        mp3_folder = os.path.join(base_folder, "MP3")
        
        if not os.path.exists(mp3_folder):
            self.convert_status_label.config(text="错误: MP3文件夹不存在!")
            return
            
        self.convert_btn.config(state='disabled')
        self.convert_status_label.config(text="开始转换...")
        
        try:
            success_count, fail_count = self.batch_mp3_to_wav(mp3_folder)
            self.convert_status_label.config(
                text=f"转换完成! 成功: {success_count} 个文件, 失败: {fail_count} 个文件"
            )
        except Exception as e:
            self.convert_status_label.config(text=f"转换过程出错: {str(e)}")
        finally:
            self.convert_btn.config(state='normal')

    async def generate_voice_async(self):
        try:
            # 获取用户输入
            text = self.text_input.get('1.0', tk.END).strip()
            voice = self.voice.get()
            speed = self.speed.get()
            
            # 创建输出目录结构
            output_base = os.path.abspath(self.output_dir.get())  # 确保是绝对路径
            mp3_dir = os.path.join(output_base, "MP3")
            os.makedirs(mp3_dir, exist_ok=True)
            
            # 生成输出文件名
            output_file = os.path.join(mp3_dir, f"generated_voice_{len(os.listdir(mp3_dir))}.mp3")
            
            # 生成语音
            tts = edge_tts.Communicate(text=text, voice=voice, rate=speed)
            await tts.save(output_file)
            self.status_label.config(text=f"生成成功: {output_file}")
        except Exception as e:
            self.status_label.config(text=f"生成失败: {str(e)}")

    def generate_voice(self):
        self.generate_btn.config(state='disabled')
        self.status_label.config(text="正在生成...")
        asyncio.run(self.generate_voice_async())
        self.generate_btn.config(state='normal')
    


def main():
    root = tk.Tk()
    app = VoiceGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()