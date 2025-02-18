@echo off
chcp 65001
echo 准备打包环境...

:: 关闭可能占用文件的进程
taskkill /F /IM ffmpeg.exe 2>nul
taskkill /F /IM ffprobe.exe 2>nul

:: 清理旧文件
if exist temp_ffmpeg rmdir /s /q temp_ffmpeg
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: 检查 ffmpeg 文件夹是否存在
if not exist ffmpeg (
    echo 创建 ffmpeg 文件夹...
    mkdir ffmpeg
    
    :: 检查缓存的 ffmpeg.zip 是否存在
    if not exist ffmpeg.zip (
        echo 下载 ffmpeg...
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'"
    ) else (
        echo 使用缓存的 ffmpeg.zip...
    )
    
    echo 解压 ffmpeg...
    powershell -Command "Expand-Archive -Force ffmpeg.zip -DestinationPath temp_ffmpeg"
    
    echo 复制 ffmpeg 文件...
    copy /Y "temp_ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "ffmpeg\"
    copy /Y "temp_ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffprobe.exe" "ffmpeg\"
    
    echo 清理临时文件...
    rmdir /s /q temp_ffmpeg
)

:: 检查 spec 文件是否存在
if not exist app.spec (
    echo 创建 spec 文件...
    pyinstaller --name "语音生成器" ^
                --onefile ^
                --windowed ^
                --add-data "ffmpeg/ffmpeg.exe;ffmpeg" ^
                --add-data "ffmpeg/ffprobe.exe;ffmpeg" ^
                --hidden-import edge_tts.constants ^
                --noconsole ^
                --runtime-tmpdir "." ^
                --disable-windowed-traceback ^
                app.py
) else (
    echo 使用现有 spec 文件打包...
    pyinstaller --clean app.spec
)

echo 打包完成！
pause