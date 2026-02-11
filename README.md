# Video to Audio Converter

一个简洁的视频转音频网站，支持上传文件或通过链接转换。

## 功能

- 上传视频文件转换为音频
- 通过 URL 下载并转换（支持 YouTube、Bilibili 等）
- 多种输出格式：MP3、WAV、AAC、FLAC、OGG
- 支持拖拽上传
- 响应式设计

## 安装

1. 安装依赖：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 ffmpeg (macOS)
brew install ffmpeg

# 安装 yt-dlp (用于 URL 下载)
pip install yt-dlp
# 或
brew install yt-dlp
```

2. 运行应用：

```bash
python app.py
```

3. 打开浏览器访问 http://localhost:5000

## 使用

1. **上传文件**：点击上传区域或拖拽视频文件
2. **视频链接**：切换到"视频链接"标签，粘贴 URL
3. 选择输出格式
4. 点击"开始转换"
5. 转换完成后点击"下载音频"
