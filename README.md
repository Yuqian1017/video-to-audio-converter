---
title: Video to Audio Converter
emoji: 🎵
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8080
pinned: false
---

# 视频转音频工具 Video to Audio

将视频文件转换为音频，支持多种格式和平台。

## 快速启动

### Mac 用户
双击 `run.command` 文件即可启动

### Windows 用户
双击 `run.bat` 文件即可启动

### 命令行启动
```bash
pip install flask yt-dlp
python app.py
```

然后打开浏览器访问 http://127.0.0.1:8080

## 功能

- ✅ 上传视频文件转换为音频
- ✅ 通过 URL 下载并转换（支持 B站、抖音、YouTube 等）
- ✅ 多种输出格式：MP3、WAV、AAC、FLAC、OGG

## 支持的平台

YouTube、抖音、小红书、B站、微博、西瓜视频、快手、腾讯视频、优酷、TikTok、Instagram、Twitter/X

## 依赖

- Python 3.8+
- ffmpeg
- yt-dlp（自动安装）

### 安装 ffmpeg

**Mac:**
```bash
brew install ffmpeg
```

**Windows:**
下载 https://ffmpeg.org/download.html 并添加到 PATH

**Linux:**
```bash
sudo apt install ffmpeg
```
