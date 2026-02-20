#!/bin/bash

# 视频转音频 - 双击即可启动
cd "$(dirname "$0")"

echo "================================"
echo "   视频转音频工具 启动中..."
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安装 Python3，请先安装"
    echo "下载地址: https://www.python.org/downloads/"
    read -p "按回车键退出..."
    exit 1
fi

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ 未安装 ffmpeg"
    echo "Mac: brew install ffmpeg"
    echo "Windows: https://ffmpeg.org/download.html"
    read -p "按回车键退出..."
    exit 1
fi

# 安装依赖
echo "📦 检查依赖..."
pip3 install -q flask yt-dlp 2>/dev/null

# 启动服务
echo ""
echo "✅ 启动成功！"
echo ""
echo "🌐 打开浏览器访问: http://127.0.0.1:8080"
echo ""
echo "按 Ctrl+C 停止服务"
echo "================================"
echo ""

# 自动打开浏览器
sleep 2 && open "http://127.0.0.1:8080" &

# 启动 Flask
python3 app.py
